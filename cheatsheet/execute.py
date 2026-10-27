"""Runs one code example in a fresh Jupyter kernel and captures what it prints and plots (ADR 0002, ADR 0003)."""

import asyncio
import json
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from jupyter_client import AsyncKernelClient, AsyncKernelManager
from jupyter_client.kernelspec import KernelSpecManager

TIMEOUT_SECONDS = 60  # per example, and for the kernel to start
_KERNEL_NAME = "cheatsheet-python"
# A kernel is given free ports before it starts, and when several start at once another process can
# take one first; the kernel then dies with "Address already in use". A new kernel gets new ports.
_START_ATTEMPTS = 3

# Matplotlib draws with the non-interactive inline backend, which sends every figure open at
# plt.show() or at the end of the example as SVG. The fixed hash salt and missing date keep the
# SVG the same from build to build.
_KERNEL_CONFIG = """c.InlineBackend.figure_formats = {"svg"}
c.InlineBackend.rc = {"svg.hashsalt": "cheatsheet"}
c.InlineBackend.print_figure_kwargs = {"bbox_inches": "tight", "metadata": {"Date": None}}
"""


# ipywidgets: the part of a display_data message that names a displayed widget, the containers whose
# children are drawn in their place, and the controls the site can draw, by model name.
_WIDGET_VIEW = "application/vnd.jupyter.widget-view+json"
_CONTAINERS = {"VBoxModel", "HBoxModel", "BoxModel"}
_CONTROLS = {
    "IntSliderModel": "slider",
    "FloatSliderModel": "slider",
    "DropdownModel": "dropdown",
    "CheckboxModel": "checkbox",
    "TextModel": "text",
}


@dataclass(frozen=True)
class Run:
    stdout: str
    error_type: str | None = None
    error: str | None = None  # the final traceback line, e.g. "KeyError: 'sd'"
    figures: tuple[str, ...] = ()  # SVG documents, in the order they were shown
    widgets: tuple[dict, ...] = ()  # the controls displayed, in display order (see _controls)
    unsupported_widget: str | None = None  # the model name of the first displayed control not in _CONTROLS
    timed_out: bool = False  # still running after the timeout, so it was stopped


def run_example(code: str, timeout: float = TIMEOUT_SECONDS) -> Run:
    """Run `code` in a new kernel of this environment's Python, then shut the kernel down.

    The kernel starts in an empty working directory with a private IPython profile, so an
    example sees neither other examples' variables nor the repository or user startup files.
    It is safe to call from several threads at once; each call gets its own kernel. Code still
    running after `timeout` seconds is stopped with the kernel and returns a timed-out Run.
    """
    # The kernel is driven from a worker thread with its own short-lived event loop, so this works
    # even when the caller already runs one (e.g. Playwright in the browser tests). A selector loop
    # is what pyzmq needs; the kernel itself is started with subprocess.Popen, not by the loop.
    with ThreadPoolExecutor(max_workers=1) as worker:
        return worker.submit(asyncio.run, _run(code, timeout), loop_factory=asyncio.SelectorEventLoop).result()


async def _run(code: str, timeout: float) -> Run:
    with tempfile.TemporaryDirectory(prefix="cheatsheet-kernel-") as scratch:
        root = Path(scratch)
        (root / "cwd").mkdir()
        (root / "ipython" / "profile_default").mkdir(parents=True)
        (root / "ipython" / "profile_default" / "ipython_kernel_config.py").write_text(_KERNEL_CONFIG, encoding="utf-8")
        manager, client = await _start_kernel(root)
        try:
            stdout: list[str] = []
            errors: list[dict] = []
            figures: list[str] = []
            # A widget's model is sent when it is made, then changed by updates (interact sets each
            # control's description and starting value afterwards), so the state is read at the end.
            models: dict[str, dict] = {}  # each widget model's state, by its comm id
            shown: list[str] = []  # the model ids of the widgets displayed, in order

            def collect(message: dict) -> None:
                content = message["content"]
                if message["msg_type"] == "stream" and content["name"] == "stdout":
                    stdout.append(content["text"])
                elif message["msg_type"] == "error":
                    errors.append(content)
                elif message["msg_type"] == "display_data" and "image/svg+xml" in content["data"]:
                    svg = content["data"]["image/svg+xml"]
                    figures.append(svg[svg.index("<svg") :])  # without the XML prolog, so it can sit inline in HTML
                elif message["msg_type"] == "display_data" and _WIDGET_VIEW in content["data"]:
                    shown.append(content["data"][_WIDGET_VIEW]["model_id"])
                elif message["msg_type"] == "comm_open" and content["target_name"] == "jupyter.widget":
                    models[content["comm_id"]] = dict(content["data"]["state"])
                elif message["msg_type"] == "comm_msg" and content["data"].get("method") == "update":
                    models.setdefault(content["comm_id"], {}).update(content["data"]["state"])

            try:
                await client.execute_interactive(
                    code, store_history=False, allow_stdin=False, timeout=timeout, output_hook=collect
                )
            except TimeoutError:
                timed_out = True
            else:
                timed_out = False
        finally:
            client.stop_channels()
            await manager.shutdown_kernel(now=True)

    text = "".join(stdout).rstrip("\n")
    if timed_out:
        return Run(stdout=text, timed_out=True)
    controls = [control for model_id in shown for control in _controls(models, model_id)]
    captured = {
        "figures": tuple(figures),
        "widgets": tuple(control for control in controls if "kind" in control),
        "unsupported_widget": next((control["model"] for control in controls if "kind" not in control), None),
    }
    if not errors:
        return Run(stdout=text, **captured)
    name, value = errors[0]["ename"], errors[0]["evalue"]
    return Run(stdout=text, error_type=name, error=f"{name}: {value}" if value else name, **captured)


def _controls(models: dict[str, dict], model_id: str) -> list[dict]:
    """The controls in a displayed widget, depth first and in order: containers are walked and Output widgets
    left out. Each is a supported control's data for the site, or {"model": <name>} for one it can't draw."""
    state = models.get(model_id, {})
    name = state.get("_model_name", "")
    if name in _CONTAINERS:
        return [c for child in state["children"] for c in _controls(models, child.removeprefix("IPY_MODEL_"))]
    if name == "OutputModel":
        return []
    if name not in _CONTROLS:
        return [{"model": name}]
    control = {"kind": _CONTROLS[name], "description": state["description"]}
    if control["kind"] == "slider":
        control |= {key: state[key] for key in ("min", "max", "step", "value")}
        control |= {
            "readout": _readout(state["value"], state["readout_format"]),
            "minReadout": _readout(state["min"], state["readout_format"]),
            "maxReadout": _readout(state["max"], state["readout_format"]),
        }
    elif control["kind"] == "dropdown":
        options, index = state["_options_labels"], state["index"]
        control |= {"options": list(options), "value": None if index is None else options[index]}
    else:
        control["value"] = state["value"]
    return [control]


def _readout(number: float, readout_format: str) -> str:
    """The number as a slider's readout shows it. Jupyter formats it with d3-format, whose usual formats
    (".2f" for floats, "d" for ints) mean the same to Python's format(); any other gives the plain number."""
    try:
        return format(number, readout_format)
    except ValueError:
        return str(number)


async def _start_kernel(root: Path) -> tuple[AsyncKernelManager, AsyncKernelClient]:
    """Start a kernel and wait until it answers, starting a new one if it dies first (see _START_ATTEMPTS)."""
    for _ in range(_START_ATTEMPTS - 1):
        try:
            return await _start_kernel_once(root)
        except RuntimeError:  # "Kernel died before replying to kernel_info"
            pass
    return await _start_kernel_once(root)


async def _start_kernel_once(root: Path) -> tuple[AsyncKernelManager, AsyncKernelClient]:
    manager = AsyncKernelManager(kernel_name=_KERNEL_NAME, kernel_spec_manager=_kernel_specs(root))
    await manager.start_kernel(cwd=str(root / "cwd"), env=_kernel_env(root))
    client = manager.client()
    client.start_channels()
    try:
        await client.wait_for_ready(timeout=TIMEOUT_SECONDS)
    except BaseException:
        client.stop_channels()
        await manager.shutdown_kernel(now=True)
        raise
    return manager, client


def _kernel_specs(root: Path) -> KernelSpecManager:
    """A kernel spec pointing at this interpreter, so no globally installed kernel can be picked up."""
    spec_dir = root / "kernels" / _KERNEL_NAME
    spec_dir.mkdir(parents=True, exist_ok=True)
    spec = {
        "argv": _kernel_argv(),
        "display_name": "Cheat sheet examples",
        "language": "python",
    }
    (spec_dir / "kernel.json").write_text(json.dumps(spec), encoding="utf-8")
    return KernelSpecManager(kernel_dirs=[str(root / "kernels")], ensure_native_kernel=False)


def _kernel_argv() -> list[str]:
    # Errors only: the kernel listens on 127.0.0.1 with signed messages, so its notice about
    # unencrypted TCP would just repeat for every example.
    return [
        sys.executable, "-X", "utf8", "-m", "ipykernel_launcher",
        "-f", "{connection_file}", "--IPKernelApp.log_level=ERROR",
    ]


def _kernel_env(root: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith(("PYTHON", "IPYTHON", "JUPYTER", "MPL"))}
    env["IPYTHONDIR"] = str(root / "ipython")
    env["MPLBACKEND"] = "module://matplotlib_inline.backend_inline"
    env["PYTHONIOENCODING"] = "utf-8"
    return env
