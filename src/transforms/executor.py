from __future__ import annotations

import asyncio
import logging
import os
import shlex
import tempfile
import time
from typing import Any

from src.transforms.registry import TransformDef
from src.orchestrator.executor import ExecutionResult, ExecutionManager

logger = logging.getLogger("transforms")


class TransformExecutor:
    def __init__(self, execution_manager: ExecutionManager | None = None) -> None:
        self.executor = execution_manager or ExecutionManager(container_first=False)

    async def execute(
        self,
        transform: TransformDef,
        input_text: str = "",
        input_path: str = "",
        timeout: int = 30,
    ) -> ExecutionResult:
        method = transform.method

        if method == "passthrough":
            return ExecutionResult(stdout=input_text, return_code=0, sandbox="none")

        if method == "redirect":
            return await self._exec_redirect(transform, input_text, input_path, timeout)

        if method == "pipe":
            return await self._exec_pipe(transform, input_text, timeout)

        if method == "convert":
            return await self._exec_convert(transform, input_text, input_path, timeout)

        if method == "copy":
            return await self._exec_copy(transform, input_text, input_path, timeout)

        return ExecutionResult(stderr=f"Unknown transform method: {method}", return_code=-1)

    async def _exec_redirect(
        self,
        transform: TransformDef,
        input_text: str,
        input_path: str,
        timeout: int,
    ) -> ExecutionResult:
        if input_path:
            return ExecutionResult(
                stdout=f"File available at: {input_path}",
                return_code=0,
                sandbox="redirect",
            )
        if transform.command_template:
            out_path = tempfile.mktemp(prefix="transform-")
            command = transform.command_template.format(input=shlex.quote(input_text[:256]), output=shlex.quote(out_path))
            return await self.executor.execute(command, timeout=timeout)
        return ExecutionResult(stdout=input_text, return_code=0, sandbox="redirect")

    async def _exec_pipe(
        self,
        transform: TransformDef,
        input_text: str,
        timeout: int,
    ) -> ExecutionResult:
        if transform.command_template:
            command = transform.command_template.format(input=shlex.quote(input_text[:256]))
            return await self.executor.execute(command, timeout=timeout)
        return ExecutionResult(stdout=input_text, return_code=0, sandbox="pipe")

    async def _exec_convert(
        self,
        transform: TransformDef,
        input_text: str,
        input_path: str,
        timeout: int,
    ) -> ExecutionResult:
        if transform.command_template:
            tmp_in = input_path or self._write_temp(input_text)
            tmp_out = tempfile.mktemp(prefix="convert-")
            command = transform.command_template.format(
                input=shlex.quote(tmp_in),
                output=shlex.quote(tmp_out),
            )
            result = await self.executor.execute(command, timeout=timeout)
            if result.success and os.path.exists(tmp_out):
                with open(tmp_out) as f:
                    result.stdout = f.read()
            if not input_path:
                try:
                    os.unlink(tmp_in)
                except OSError:
                    pass
            try:
                os.unlink(tmp_out)
            except OSError:
                pass
            return result
        if transform.converter_tool:
            return ExecutionResult(
                stdout=f"Converter tool {transform.converter_tool} would process input",
                return_code=0,
                sandbox="convert",
            )
        return ExecutionResult(stdout=input_text, return_code=0, sandbox="convert")

    async def _exec_copy(
        self,
        transform: TransformDef,
        input_text: str,
        input_path: str,
        timeout: int,
    ) -> ExecutionResult:
        if input_path:
            dest = tempfile.mktemp(prefix="copy-")
            import shutil
            shutil.copy2(input_path, dest)
            return ExecutionResult(stdout=f"Copied to {dest}", return_code=0, sandbox="copy")
        return ExecutionResult(stdout=input_text, return_code=0, sandbox="copy")

    def _write_temp(self, content: str) -> str:
        path = tempfile.mktemp(prefix="transform-input-")
        with open(path, "w") as f:
            f.write(content)
        return path


async def execute_transform_pipeline(
    transforms: list[TransformDef],
    input_text: str = "",
    timeout: int = 30,
) -> ExecutionResult:
    executor = TransformExecutor()
    current_input = input_text
    for transform in transforms:
        result = await executor.execute(transform, input_text=current_input, timeout=timeout)
        if not result.success:
            return result
        current_input = result.stdout
    return ExecutionResult(stdout=current_input, return_code=0, sandbox="pipeline")
