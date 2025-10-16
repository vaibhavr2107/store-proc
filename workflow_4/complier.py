from __future__ import annotations

import logging
import os
import shutil
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from settings import PROJECT_SETTINGS

logger = logging.getLogger(__name__)


def run_compiler(paths: Iterable[Path]) -> Dict[str, object]:
    materialized = list(Path(p) for p in paths)
    artifact_count = len(materialized)
    logger.debug("Compiler received %d artifact paths", artifact_count)

    service_roots = _discover_service_roots(materialized)
    if not service_roots:
        logger.info("No service projects detected for compilation")
        return {"compiled_artifacts": artifact_count, "status": "skipped", "services": {}}

    command = _build_maven_command()
    if command is None:
        message = "Maven executable not found. Ensure Maven is installed or configure 'maven_executable'."
        logger.error(message)
        return {
            "compiled_artifacts": artifact_count,
            "status": "error",
            "services": {},
            "error": message,
        }

    max_workers = min(len(service_roots), max(os.cpu_count() or 1, 2))
    logger.info("Compiling %d service projects with up to %d workers", len(service_roots), max_workers)

    results: Dict[str, Dict[str, object]] = {}
    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(_compile_service, service_dir, command): service_dir for service_dir in service_roots}
        for future in as_completed(future_map):
            service_dir = future_map[future]
            service_name = service_dir.name
            try:
                service_result = future.result()
            except Exception as exc:  # pragma: no cover - defensive
                logger.exception("Compilation failed for %s", service_name)
                service_result = {
                    "status": "error",
                    "return_code": -1,
                    "log_file": None,
                    "error": str(exc),
                }
            with lock:
                results[service_name] = service_result

    overall_status = "success" if all(r.get("status") == "success" for r in results.values()) else "failure"
    logger.info("Compiler processed %d artifacts across %d services (%s)", artifact_count, len(results), overall_status)
    return {"compiled_artifacts": artifact_count, "status": overall_status, "services": results}


def _discover_service_roots(paths: List[Path]) -> List[Path]:
    services_dir = Path(PROJECT_SETTINGS.get("output_dir", "output")) / PROJECT_SETTINGS.get("request_id", "")
    services_dir = services_dir / PROJECT_SETTINGS.get("services_subdir", "services")
    services_dir = services_dir.resolve()

    roots = set()
    for path in paths:
        for parent in path.resolve().parents:
            if parent.parent is None:
                break
            if parent == services_dir:
                # We've reached the container, stop climbing
                break
            if (parent / "pom.xml").exists() and (parent / "api").exists():
                roots.add(parent)
                break
    # If no roots were found through artifacts, fall back to scanning services directory
    if not roots and services_dir.exists():
        for maybe_service in services_dir.iterdir():
            if (maybe_service / "pom.xml").exists():
                roots.add(maybe_service)
    return sorted(roots)


def _compile_service(service_dir: Path, command: List[str]) -> Dict[str, object]:
    log_file = service_dir / "build.log"
    logger.debug("Running %s in %s", " ".join(command), service_dir)
    env = os.environ.copy()
    java_home = PROJECT_SETTINGS.get("java_home")
    if java_home:
        env["JAVA_HOME"] = str(java_home)
        env["PATH"] = str(Path(java_home) / "bin") + os.pathsep + env.get("PATH", "")

    try:
        completed = subprocess.run(
            command,
            cwd=service_dir,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        logger.error("Maven command not found while compiling %s", service_dir)
        return {
            "status": "error",
            "return_code": -1,
            "log_file": None,
            "error": f"Maven executable not found: {exc}",
        }

    _write_build_log(log_file, command, completed.stdout, completed.stderr, completed.returncode)

    status = "success" if completed.returncode == 0 else "failure"
    if status == "success":
        logger.info("Service %s compiled successfully", service_dir.name)
    else:
        logger.warning("Service %s compilation failed with code %s", service_dir.name, completed.returncode)

    return {
        "status": status,
        "return_code": completed.returncode,
        "log_file": str(log_file.relative_to(Path.cwd())) if log_file.exists() else None,
        "error": None if status == "success" else completed.stderr.strip() or "Unknown error",
    }


def _write_build_log(
    log_file: Path,
    command: Iterable[str],
    stdout: str,
    stderr: str,
    return_code: int,
) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("w", encoding="utf-8") as handle:
        handle.write("Command: ")
        handle.write(" ".join(command))
        handle.write("\nReturn code: ")
        handle.write(str(return_code))
        handle.write("\n\n--- STDOUT ---\n")
        handle.write(stdout or "")
        handle.write("\n--- STDERR ---\n")
        handle.write(stderr or "")


def _build_maven_command() -> Optional[List[str]]:
    configured = PROJECT_SETTINGS.get("maven_executable")
    candidates: List[str] = []
    if configured:
        candidates.append(str(configured))
    candidates.extend(["mvn.cmd", "mvn", "mvn.bat"])

    executable_path: Optional[str] = None
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved:
            executable_path = resolved
            break

    if not executable_path:
        return None

    additional_args = PROJECT_SETTINGS.get("maven_args") or ["-B", "-DskipTests", "clean", "package"]
    return [executable_path, *additional_args]
