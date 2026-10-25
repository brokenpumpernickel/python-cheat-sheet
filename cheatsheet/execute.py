"""Runs one code example in a fresh Jupyter kernel and captures what it prints (ADR 0002, ADR 0003)."""

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


@dataclass(frozen=True)
class Run:
    stdout: str
    error_type: str | None = None
    error: str | None = None  # the final traceback line, e.g. "KeyError: 'sd'"


def run_example(code: str) -> Run:
    """Run `code` in a new kernel of this environment's Python, then shut the kernel down.

    The kernel starts in an empty working directory with a private IPython profile, so an
    example sees neither other examples' variables nor the repository or user startup files.
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
        (root / "ipython").mkdir()
        manager = AsyncKernelManager(kernel_name=_KERNEL_NAME, kernel_spec_manager=_kernel_specs(root))
        await manager.start_kernel(cwd=str(root / "cwd"), env=_kernel_env(root))
        client = manager.client()
        try:
            client.start_channels()
            await client.wait_for_ready(timeout=TIMEOUT_SECONDS)
            stdout: list[str] = []
            errors: list[dict] = []

            def collect(message: dict) -> None:
                content = message["content"]
                if message["msg_type"] == "stream" and content["name"] == "stdout":
                    stdout.append(content["text"])
                elif message["msg_type"] == "error":
                    errors.append(content)

            await client.execute_interactive(
                code, store_history=False, allow_stdin=False, timeout=TIMEOUT_SECONDS, output_hook=collect
            )
        finally:
            client.stop_channels()
            await manager.shutdown_kernel(now=True)

    text = "".join(stdout).rstrip("\n")
    if not errors:
        return Run(stdout=text)
    name, value = errors[0]["ename"], errors[0]["evalue"]
    return Run(stdout=text, error_type=name, error=f"{name}: {value}" if value else name)


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
    env["PYTHONIOENCODING"] = "utf-8"
    return env
