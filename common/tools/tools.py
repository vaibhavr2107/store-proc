from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Iterable


class FileWriterTool:
    def write(self, base: Path, relative_path: str, content: str) -> Path:
        target_path = base / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")
        return target_path


def ensure_directories(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def load_workflow_module(workflow: str, module: str):
    root = Path(__file__).resolve().parents[2]
    module_path = root / workflow / f"{module}.py"
    module_name = f"{workflow}.{module}".replace("-", "_")
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module {module} from {module_path}")
    module_object = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module_object
    try:
        spec.loader.exec_module(module_object)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module_object
