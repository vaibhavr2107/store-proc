from __future__ import annotations

import json
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Set

from settings import PROJECT_SETTINGS

logger = logging.getLogger(__name__)


def build_graph(domain_services: Dict[str, Any], domain_mapped_proc: Dict[str, Any], request_id: str | None) -> Dict[str, Any]:
    req_id = request_id
    procedure_name = domain_mapped_proc.get("procedure_name", "procedure")
    table_fields = domain_mapped_proc.get("table_fields", {})
    service_items = domain_services.get("services", [])
    domain_service_map: Dict[str, List[Dict[str, Any]]] = {}
    for service in service_items:
        domain_service_map.setdefault(service["domain"], []).append(service)

    node_map: Dict[str, Dict[str, Any]] = {}
    edge_map: Dict[str, Dict[str, Any]] = {}

    def add_node(node_id: str, node_type: str, label: str, properties: Dict[str, Any]) -> None:
        if node_id not in node_map:
            node_map[node_id] = {
                "id": node_id,
                "type": node_type,
                "label": label,
                "properties": properties,
            }

    def add_edge(source: str, edge_type: str, target: str, properties: Dict[str, Any]) -> None:
        edge_id = f"{source}::{edge_type}::{target}"
        edge_map[edge_id] = {
            "id": edge_id,
            "source": source,
            "target": target,
            "type": edge_type.lower(),
            "properties": properties,
        }

    procedure_id = f"proc::{procedure_name}"
    add_node(
        procedure_id,
        "procedure",
        procedure_name,
        {"procedure": procedure_name, "request_ids": [req_id] if req_id else []},
    )

    graph_entry = {
        "procedure": {"name": procedure_name, "request_id": req_id},
        "domains": {},
    }

    for domain, services in domain_service_map.items():
        domain_id = f"domain::{domain}"
        add_node(
            domain_id,
            "domain",
            domain,
            {"domain": domain, "request_ids": [req_id] if req_id else []},
        )
        add_edge(
            procedure_id,
            "HAS_DOMAIN",
            domain_id,
            {"procedure": procedure_name, "domain": domain, "request_ids": [req_id] if req_id else []},
        )
        domain_entry = graph_entry["domains"].setdefault(domain, {"services": {}})
        for service in services:
            service_name = service["service_name"]
            service_id = f"service::{service_name}"
            service_properties = {
                "domain": domain,
                "service": service_name,
                "request_ids": [req_id] if req_id else [],
            }
            add_node(service_id, "service", service_name, service_properties)
            add_edge(
                domain_id,
                "HAS_SERVICE",
                service_id,
                {"domain": domain, "service": service_name, "request_ids": [req_id] if req_id else []},
            )
            owned_tables = service.get("owned_tables", [])
            dependencies = service.get("dependencies", [])
            dependency_services = {
                dep_domain: [s["service_name"] for s in domain_service_map.get(dep_domain, [])]
                for dep_domain in dependencies
            }
            service_entry = domain_entry["services"].setdefault(
                service_name,
                {"tables": {}, "dependencies": dependency_services},
            )
            service_entry["dependencies"] = dependency_services
            for table in owned_tables:
                table_id = f"table::{table}"
                fields = table_fields.get(table, [])
                add_node(
                    table_id,
                    "table",
                    table,
                    {"table": table, "domain": domain, "service": service_name, "fields": fields, "request_ids": [req_id] if req_id else []},
                )
                add_edge(
                    service_id,
                    "USES_TABLE",
                    table_id,
                    {"service": service_name, "table": table, "request_ids": [req_id] if req_id else []},
                )
                table_entry = service_entry["tables"].setdefault(table, {"fields": fields})
                table_entry["fields"] = fields
                for field in fields:
                    field_id = f"field::{table}::{field}"
                    add_node(
                        field_id,
                        "field",
                        field,
                        {"field": field, "table": table, "request_ids": [req_id] if req_id else []},
                    )
                    add_edge(
                        table_id,
                        "HAS_FIELD",
                        field_id,
                        {"table": table, "field": field, "request_ids": [req_id] if req_id else []},
                    )

    # service dependencies edges
    for domain, services in domain_service_map.items():
        for service in services:
            service_id = f"service::{service['service_name']}"
            for dep_domain in service.get("dependencies", []):
                for target in domain_service_map.get(dep_domain, []):
                    target_id = f"service::{target['service_name']}"
                    add_edge(
                        service_id,
                        "DEPENDS_ON",
                        target_id,
                        {
                            "source_service": service["service_name"],
                            "target_service": target["service_name"],
                            "source_domain": domain,
                            "target_domain": dep_domain,
                            "request_ids": [req_id] if req_id else [],
                        },
                    )

    return {
        "procedure": {"id": procedure_id, "name": procedure_name, "request_id": req_id},
        "domains": graph_entry["domains"],
        "nodes": list(node_map.values()),
        "edges": list(edge_map.values()),
        "graphdb_entry": graph_entry,
    }


def _build_graphml(graph: Dict[str, Any]) -> str:
    ns = {"xmlns": "http://graphml.graphdrawing.org/xmlns"}
    root = ET.Element("graphml", ns)
    ET.SubElement(root, "key", {"id": "label", "for": "node", "attr.name": "label", "attr.type": "string"})
    ET.SubElement(root, "key", {"id": "type", "for": "node", "attr.name": "type", "attr.type": "string"})
    ET.SubElement(root, "key", {"id": "edge_type", "for": "edge", "attr.name": "type", "attr.type": "string"})
    graph_element = ET.SubElement(root, "graph", {"id": "G", "edgedefault": "directed"})

    for node in graph.get("nodes", []):
        node_element = ET.SubElement(graph_element, "node", {"id": node["id"]})
        ET.SubElement(node_element, "data", {"key": "type"}).text = node.get("type", "")
        ET.SubElement(node_element, "data", {"key": "label"}).text = node.get("label", "")

    for index, edge in enumerate(graph.get("edges", [])):
        edge_id = edge.get("id") or f"e{index}"
        edge_element = ET.SubElement(
            graph_element,
            "edge",
            {"id": edge_id, "source": edge["source"], "target": edge["target"]},
        )
        ET.SubElement(edge_element, "data", {"key": "edge_type"}).text = edge.get("type", "")

    return ET.tostring(root, encoding="unicode")


def update_graphdb(graph_entry: Dict[str, Any]) -> Path:
    graphdb_dir = Path(PROJECT_SETTINGS.get("graphdb_dir", "common/graphdb"))
    graphdb_dir.mkdir(parents=True, exist_ok=True)
    graphdb_path = graphdb_dir / PROJECT_SETTINGS.get("graphdb_file", "graphdb.json")
    existing: Dict[str, Any] = {"stored_procedures": {}}
    if graphdb_path.exists():
        try:
            raw = json.loads(graphdb_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            logger.warning("Existing graph DB file is corrupted; recreating %s", graphdb_path)
            raw = {}
        stored_existing = raw.get("stored_procedures", {})
        if isinstance(stored_existing, dict):
            existing["stored_procedures"] = stored_existing

    stored = existing["stored_procedures"]
    procedure_name = graph_entry["procedure"]["name"]
    request_id = graph_entry["procedure"].get("request_id")
    proc_entry = stored.setdefault(procedure_name, {"request_ids": [], "domains": {}})
    if request_id and request_id not in proc_entry["request_ids"]:
        proc_entry["request_ids"].append(request_id)
        proc_entry["request_ids"].sort()

    for domain, domain_data in graph_entry["domains"].items():
        domain_entry = proc_entry["domains"].setdefault(domain, {"services": {}})
        for service_name, service_data in domain_data.get("services", {}).items():
            service_entry = domain_entry["services"].setdefault(
                service_name,
                {"request_ids": [], "tables": {}, "dependencies": {}, "dependents": {}},
            )
            if request_id and request_id not in service_entry["request_ids"]:
                service_entry["request_ids"].append(request_id)
                service_entry["request_ids"].sort()

            for table, table_info in service_data.get("tables", {}).items():
                table_entry = service_entry["tables"].setdefault(table, {"fields": []})
                merged_fields = set(table_entry.get("fields", []))
                merged_fields.update(table_info.get("fields", []))
                table_entry["fields"] = sorted(merged_fields)

            dependencies = service_entry.get("dependencies", {})
            for dep_domain, dep_services in service_data.get("dependencies", {}).items():
                merged_services = set(dependencies.get(dep_domain, []))
                merged_services.update(dep_services)
                if merged_services:
                    dependencies[dep_domain] = sorted(merged_services)
            service_entry["dependencies"] = dependencies

    # recompute dependents
    for domain, domain_entry in proc_entry["domains"].items():
        for service_name, service_entry in domain_entry["services"].items():
            service_entry["dependents"] = {}

    for domain, domain_entry in proc_entry["domains"].items():
        for service_name, service_entry in domain_entry["services"].items():
            for dep_domain, dep_services in service_entry.get("dependencies", {}).items():
                target_domain_entry = proc_entry["domains"].get(dep_domain, {})
                target_services = target_domain_entry.get("services", {})
                for dep_service in dep_services:
                    if dep_service in target_services:
                        dependents = target_services[dep_service].setdefault("dependents", {})
                        dependents.setdefault(domain, [])
                        if service_name not in dependents[domain]:
                            dependents[domain].append(service_name)
                            dependents[domain].sort()

    graphdb_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    logger.info("Updated shared graph database at %s", graphdb_path)
    return graphdb_path


def save_graph(graph: Dict[str, Any], request_id: str | None, output_dir: Path | None = None) -> Dict[str, Path]:
    target_dir = Path(output_dir or PROJECT_SETTINGS.get("output_dir", "output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    json_path = target_dir / PROJECT_SETTINGS.get("graph_json_filename", "storeproc_graph.json")
    graphml_path = target_dir / PROJECT_SETTINGS.get("graph_graphml_filename", "storeproc_graph.graphml")
    json_path.write_text(json.dumps(graph, indent=2), encoding="utf-8")
    graphml_path.write_text(_build_graphml(graph), encoding="utf-8")
    graphdb_path = update_graphdb(graph.get("graphdb_entry", {}))
    logger.info("Saved graph JSON to %s and GraphML to %s", json_path, graphml_path)
    return {"json": json_path, "graphml": graphml_path, "graphdb": graphdb_path}


def run_storeproc_graph(
    domain_services: Dict[str, Any],
    domain_mapped_proc: Dict[str, Any],
    output_dir: Path | None = None,
) -> Dict[str, Path]:
    request_id = PROJECT_SETTINGS.get("request_id")
    graph = build_graph(domain_services, domain_mapped_proc, request_id)
    logger.debug("Graph nodes count: %d", len(graph.get("nodes", [])))
    logger.debug("Graph edges count: %d", len(graph.get("edges", [])))
    return save_graph(graph, request_id, output_dir)
