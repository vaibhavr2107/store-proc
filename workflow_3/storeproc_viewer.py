from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List
from urllib import error, request

from settings import PROJECT_SETTINGS

logger = logging.getLogger(__name__)
MERMAID_PNG_ENDPOINT = "https://kroki.io/mermaid/png"


def build_mermaid(domain_services: Dict[str, Any], domain_mapped_proc: Dict[str, Any]) -> List[str]:
    lines = ["graph TD"]
    table_fields = domain_mapped_proc.get("table_fields", {})
    services = domain_services.get("services", [])
    domain_service_map: Dict[str, List[Dict[str, Any]]] = {}
    for service in services:
        domain_service_map.setdefault(service["domain"], []).append(service)

    for domain, service_list in domain_service_map.items():
        domain_id = _safe_id(f"domain_{domain}")
        lines.append(f"    {domain_id}[Domain: {domain}]")
        for service in service_list:
            service_id = _safe_id(f"service_{service['service_name']}")
            lines.append(f"    {domain_id} --> {service_id}[Service: {service['service_name']}]")
            for table in service.get("owned_tables", []):
                table_id = _safe_id(f"table_{table}")
                lines.append(f"    {service_id} --> {table_id}[Table: {table}]")
                fields = table_fields.get(table, [])
                for field in fields:
                    field_id = _safe_id(f"field_{table}_{field}")
                    lines.append(f"    {table_id} --> {field_id}[Field: {field}]")

    for service in services:
        source_id = _safe_id(f"service_{service['service_name']}")
        for dep_domain in service.get("dependencies", []):
            for target in domain_service_map.get(dep_domain, []):
                target_id = _safe_id(f"service_{target['service_name']}")
                lines.append(f"    {source_id} -->|depends on| {target_id}")

    return lines


def save_mermaid(lines: List[str], output_dir: Path | None = None) -> Dict[str, Path]:
    target_dir = Path(output_dir or PROJECT_SETTINGS.get("output_dir", "output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    mermaid_path = target_dir / PROJECT_SETTINGS.get("graph_mermaid_filename", "storeproc_graph.mmd")
    png_path = target_dir / PROJECT_SETTINGS.get("graph_mermaid_png_filename", "storeproc_graph.png")
    mermaid_text = "\n".join(lines)
    mermaid_path.write_text(mermaid_text, encoding="utf-8")
    logger.info("Saved Mermaid diagram to %s", mermaid_path)
    try:
        png_bytes = _render_mermaid_png(mermaid_text)
    except RuntimeError as exc:
        logger.warning("Failed to render Mermaid PNG: %s", exc)
        png_path.write_bytes(b"")
    else:
        png_path.write_bytes(png_bytes)
        logger.info("Saved Mermaid PNG to %s", png_path)
    return {"mermaid": mermaid_path, "png": png_path}


def _render_mermaid_png(mermaid_text: str) -> bytes:
    payload = mermaid_text.encode("utf-8")
    req = request.Request(
        MERMAID_PNG_ENDPOINT,
        data=payload,
        headers={"Content-Type": "text/plain; charset=utf-8"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            return response.read()
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc
    except TimeoutError as exc:
        raise RuntimeError(f"Rendering timeout: {exc}") from exc


def _safe_id(raw: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in raw)


def run_storeproc_viewer(
    domain_services: Dict[str, Any],
    domain_mapped_proc: Dict[str, Any],
    output_dir: Path | None = None,
) -> Dict[str, Path]:
    lines = build_mermaid(domain_services, domain_mapped_proc)
    return save_mermaid(lines, output_dir)
