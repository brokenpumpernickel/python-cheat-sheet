"""Runs one code example in a fresh Jupyter kernel and captures what it prints and plots (ADR 0002, ADR 0003)."""

import asyncio
import json
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from jupyter_client import AsyncKernelManager
from jupyter_client.kernelspec import KernelSpecManager

TIMEOUT_SECONDS = 60
_KERNEL_NAME = "cheatsheet-python"

# Matplotlib draws with the non-interactive inline backend, which sends every figure open at
# plt.show() or at the end of the example as SVG. The fixed hash salt and missing date keep the
# SVG the same from build to build.
_KERNEL_CONFIG = """c.InlineBackend.figure_formats = {"svg"}
c.InlineBackend.rc = {"svg.hashsalt": "cheatsheet"}
c.InlineBackend.print_figure_kwargs = {"bbox_inches": "tight", "metadata": {"Date": None}}
"""


@dataclass(frozen=True)
class Run:
    stdout: str
    error_type: str | None = None
    error: str | None = None  # the final traceback line, e.g. "KeyError: 'sd'"
    figures: tuple[str, ...] = ()  # SVG documents, in the order they were shown


def run_example(code: str) -> Run:
    """Run `code` in a new kernel of this environment's Python, then shut the kernel down.

    The kernel starts in an empty working directory with a private IPython profile, so an
    example sees neither other examples' variables nor the repository or user startup files.
    It is safe to call from several threads at once; each call gets its own kernel.
    """
    # The kernel is driven from a worker thread with its own short-lived event loop, so this works
    # even when the caller already runs one (e.g. Playwright in the browser tests). A selector loop
    # is what pyzmq needs; the kernel itself is started with subprocess.Popen, not by the loop.
    with ThreadPoolExecutor(max_workers=1) as worker:
        return worker.submit(asyncio.run, _run(code), loop_factory=asyncio.SelectorEventLoop).result()


async def _run(code: str) -> Run:
    with tempfile.TemporaryDirectory(prefix="cheatsheet-kernel-") as scratch:
        root = Path(scratch)
        (root / "cwd").mkdir()
        (root / "ipython" / "profile_default").mkdir(parents=True)
        (root / "ipython" / "profile_default" / "ipython_kernel_config.py").write_text(_KERNEL_CONFIG, encoding="utf-8")
        manager = AsyncKernelManager(kernel_name=_KERNEL_NAME, kernel_spec_manager=_kernel_specs(root))
        await manager.start_kernel(cwd=str(root / "cwd"), env=_kernel_env(root))
        client = manager.client()
        try:
            client.start_channels()
            await client.wait_for_ready(timeout=TIMEOUT_SECONDS)
            stdout: list[str] = []
            errors: list[dict] = []
            figures: list[str] = []

            def collect(message: dict) -> None:
                content = message["content"]
                if message["msg_type"] == "stream" and content["name"] == "stdout":
                    stdout.append(content["text"])
                elif message["msg_type"] == "error":
                    errors.append(content)
                elif message["msg_type"] == "display_data" and "image/svg+xml" in content["data"]:
                    svg = content["data"]["image/svg+xml"]
                    figures.append(svg[svg.index("<svg") :])  # without the XML prolog, so it can sit inline in HTML

            await client.execute_interactive(
                code, store_history=False, allow_stdin=False, timeout=TIMEOUT_SECONDS, output_hook=collect
            )
        finally:
            client.stop_channels()
            await manager.shutdown_kernel(now=True)

    text = "".join(stdout).rstrip("\n")
    if not errors:
        return Run(stdout=text, figures=tuple(figures))
    name, value = errors[0]["ename"], errors[0]["evalue"]
    return Run(stdout=text, error_type=name, error=f"{name}: {value}" if value else name, figures=tuple(figures))


def _kernel_specs(root: Path) -> KernelSpecManager:
    """A kernel spec pointing at this interpreter, so no globally installed kernel can be picked up."""
    spec_dir = root / "kernels" / _KERNEL_NAME
    spec_dir.mkdir(parents=True)
    spec = {
        # Errors only: the kernel listens on 127.0.0.1 with signed messages, so its notice about
        # unencrypted TCP would just repeat for every example.
        "argv": [
            sys.executable, "-X", "utf8", "-m", "ipykernel_launcher",
            "-f", "{connection_file}", "--IPKernelApp.log_level=ERROR",
        ],
        "display_name": "Cheat sheet examples",
        "language": "python",
    }
    (spec_dir / "kernel.json").write_text(json.dumps(spec), encoding="utf-8")
    return KernelSpecManager(kernel_dirs=[str(root / "kernels")], ensure_native_kernel=False)


def _kernel_env(root: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith(("PYTHON", "IPYTHON", "JUPYTER", "MPL"))}
    env["IPYTHONDIR"] = str(root / "ipython")
    env["MPLBACKEND"] = "module://matplotlib_inline.backend_inline"
    env["PYTHONIOENCODING"] = "utf-8"
    return env
