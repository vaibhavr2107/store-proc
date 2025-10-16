from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from settings import PROJECT_SETTINGS
from common.tools.tools import FileWriterTool, load_workflow_module

logger = logging.getLogger(__name__)

agents_module = load_workflow_module("workflow_1", "agents")
bootstrap_agents = agents_module.bootstrap_agents

READ_ME_TEMPLATE = "service_readme.txt"
CONTEXT_TEMPLATE = "service_context.json.txt"


def _format_owned_tables(service_spec: Dict[str, Any]) -> str:
    return ", ".join(service_spec.get("owned_tables", [])) or "None"


def _format_dependencies(service_spec: Dict[str, Any]) -> str:
    return ", ".join(service_spec.get("dependencies", [])) or "None"


def _collect_directory_structure(service_dir: Path) -> List[Dict[str, str]]:
    if not service_dir.exists():
        return [{"path": "", "description": "(service directory missing)"}]
    entries: List[Dict[str, str]] = []
    for path in sorted(service_dir.rglob("*")):
        if path.is_dir():
            continue
        rel_path = path.relative_to(service_dir).as_posix()
        entries.append({"path": rel_path, "description": _describe_file(rel_path)})
    return entries or [{"path": "", "description": "(empty service directory)"}]


def _describe_file(rel_path: str) -> str:
    lower = rel_path.lower()
    if "pom.xml" in lower:
        return "Maven project configuration."
    if "application" in lower and lower.endswith(".yml"):
        return "Spring Boot application settings."
    if "openapi" in lower and lower.endswith((".yml", ".yaml")):
        return "OpenAPI specification."
    if lower.endswith(".java"):
        return "Java source file."
    if lower.endswith(".json"):
        return "JSON resource file."
    if lower.endswith(".md"):
        return "Documentation file."
    return "Service resource file."


def _extract_api_endpoints(service_spec: Dict[str, Any], service_dir: Path) -> List[Dict[str, str]]:
    plan = service_spec.get("endpoints")
    if plan:
        return [
            {
                "method": endpoint.get("method", "").upper(),
                "path": endpoint.get("path", ""),
                "summary": endpoint.get("summary", ""),
            }
            for endpoint in plan
        ]
    return []


def _load_template(prompts_dir: Path, template_name: str) -> str:
    template_path = prompts_dir / template_name
    if not template_path.exists():
        return ""
    return template_path.read_text(encoding="utf-8")


def _render_template(template: str, context: Dict[str, Any]) -> str:
    try:
        return template.format(**context)
    except KeyError as exc:
        logger.warning("Missing template variable %s in context, returning raw template", exc.args[0])
        return template


def _write_service_artifacts(service_dir: Path, readme: str, context_json: str) -> List[Path]:
    writer = FileWriterTool()
    readme_path = writer.write(service_dir, "README.md", readme)
    json_path = writer.write(service_dir, "service_context.json", context_json)
    return [readme_path, json_path]


def run_service_context_creator(
    service_architecture: Dict[str, Any],
    domain_services: Dict[str, Any],
    domain_mapped_proc: Dict[str, Any],
    prompts_dir: Path | None = None,
    output_root: Path | None = None,
) -> List[Path]:
    agents = bootstrap_agents()
    context_agent = agents.get("service_context")
    if context_agent is None:
        logger.warning("ServiceContextAgent not available; skipping README/context generation.")
        return []

    prompts_path = Path(prompts_dir or PROJECT_SETTINGS.get("prompts_dir", Path("common") / "prompts" / "generate"))
    output_root = Path(output_root or PROJECT_SETTINGS.get("generated_dir", "generated"))
    output_root.mkdir(parents=True, exist_ok=True)

    table_fields = domain_mapped_proc.get("table_fields", {})
    request_id = PROJECT_SETTINGS.get("request_id")
    request_ids = [request_id] if request_id else []

    readme_template = _load_template(prompts_path, READ_ME_TEMPLATE)
    context_template = _load_template(prompts_path, CONTEXT_TEMPLATE)

    generated_paths: List[Path] = []
    for service_spec in service_architecture.get("services", []):
        service_dir = output_root / service_spec.get("service_name", "service")
        table_details = "\n".join(
            f"- {table}: {', '.join(table_fields.get(table, [])) or 'all columns'}"
            for table in service_spec.get("owned_tables", [])
        ) or "No tables assigned"
        service_description = context_agent.describe_service(service_spec)
        service_description.setdefault("table_details", table_details)
        service_description.setdefault("dependency_summary", _format_dependencies(service_spec))
        service_description.setdefault("one_liner", service_spec.get("service_name", ""))

        structure_entries = _collect_directory_structure(service_dir)
        api_endpoints = _extract_api_endpoints(service_spec, service_dir)
        api_endpoints_lines = (
            "\n".join(
                f"- {ep['method']} {ep['path']}: {ep.get('summary', '')}" for ep in api_endpoints
            )
            or "No API endpoints documented."
        )

        readme_context = {
            "service_name": service_spec.get("service_name", ""),
            "domain": service_spec.get("domain", ""),
            "owned_tables": _format_owned_tables(service_spec),
            "dependencies": _format_dependencies(service_spec),
            "service_description": service_description.get("service_description", ""),
            "table_details": service_description.get("table_details", table_details),
            "one_liner": service_description.get("one_liner", ""),
            "directory_structure": "\n".join(
                f"- {entry['path']}: {entry['description']}" for entry in structure_entries
            ),
            "api_endpoints": api_endpoints_lines,
        }
        readme_content = _render_template(readme_template, readme_context) if readme_template else ""

        context_context = {
            "service_name_json": json.dumps(service_spec.get("service_name", "")),
            "domain_json": json.dumps(service_spec.get("domain", "")),
            "request_ids_json": ", ".join(json.dumps(rid) for rid in request_ids),
            "owned_tables_json": ", ".join(json.dumps(table) for table in service_spec.get("owned_tables", [])),
            "dependencies_json": ", ".join(json.dumps(dep) for dep in service_spec.get("dependencies", [])),
            "service_description_json": json.dumps(service_description.get("service_description", "")),
            "dependency_summary_json": json.dumps(service_description.get("dependency_summary", "")),
            "directory_structure_json": json.dumps(structure_entries),
            "api_endpoints_json": json.dumps(api_endpoints),
        }
        context_content = _render_template(context_template, context_context) if context_template else "{}"

        generated_paths.extend(_write_service_artifacts(service_dir, readme_content, context_content))
        logger.info("Created service context files for %s", service_spec.get("service_name"))

    return generated_paths
