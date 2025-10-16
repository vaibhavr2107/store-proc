from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Iterable

logger = logging.getLogger(__name__)


def run_compiler(paths: Iterable[Path]) -> Dict[str, int]:
    materialized = list(paths)
    count = len(materialized)
    logger.info("Compiler processed %d artifacts", count)
    return {"compiled_artifacts": count, "status": "pending"}
