from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional

from settings import PROJECT_SETTINGS

from common.tools.tools import load_workflow_module

agents_module = load_workflow_module("workflow_1", "agents")
ArchitectAgent = agents_module.ArchitectAgent
bootstrap_agents = agents_module.bootstrap_agents

logger = logging.getLogger(__name__)


def define_service_architecture(
    domain_services: Dict[str, Any],
    domain_mapped_proc: Dict[str, Any],
    agent: ArchitectAgent,
) -> Dict[str, Any]:
    service_specs = []
    for service in domain_services.get("services", []):
        logger.debug("Calling ArchitectAgent for service=%s", service.get("service_name"))
        spec = agent.design_service(service["service_name"], service.get("dependencies", []))
        spec["domain"] = service["domain"]
        spec["owned_tables"] = service.get("owned_tables", [])
        _augment_service_spec(spec, service, domain_mapped_proc)
        service_specs.append(spec)
    logger.info("Prepared architecture for %d services", len(service_specs))
    return {"services": service_specs}


def run_service_architecture(domain_services: Dict[str, Any], domain_mapped_proc: Dict[str, Any]) -> Dict[str, Any]:
    agents = bootstrap_agents()
    architect: ArchitectAgent = agents["architect"]
    result = define_service_architecture(domain_services, domain_mapped_proc, architect)
    logger.debug("Service architecture output: %s", result)
    return result


def _augment_service_spec(spec: Dict[str, Any], service_data: Dict[str, Any], domain_mapped_proc: Dict[str, Any]) -> None:
    service_name = spec.get("service_name", "Service")
    entity_name = _derive_entity_name(service_name)
    service_kebab = _camel_to_kebab(service_name)
    service_slug = service_kebab.replace("-", "")
    base_pattern = PROJECT_SETTINGS.get("service_base_package_pattern", "com.barclays.uscb.{service}")
    base_package = base_pattern.format(service=service_slug)
    base_package_path = base_package.replace(".", "/")
    entity_var = entity_name[0].lower() + entity_name[1:] if entity_name else "entity"

    spec["entity_name"] = entity_name
    spec["entity_var"] = entity_var
    spec["base_package"] = base_package
    spec["base_package_path"] = base_package_path
    spec["service_kebab"] = service_kebab
    spec["service_slug"] = service_slug
    spec["modules"] = ["oasgen", "api"]
    table_fields_map = {
        table: list(domain_mapped_proc.get("table_fields", {}).get(table, []))
        for table in service_data.get("owned_tables", [])
    }
    table_field_details_map = {
        table: list(domain_mapped_proc.get("table_field_details", {}).get(table, []))
        for table in service_data.get("owned_tables", [])
    }
    table_operations_map = {
        table: dict(domain_mapped_proc.get("table_operation_columns", {}).get(table, {}))
        for table in service_data.get("owned_tables", [])
    }
    table_dependencies_map = {
        table: list(domain_mapped_proc.get("table_dependencies", {}).get(table, []))
        for table in service_data.get("owned_tables", [])
    }
    table_id_map = {
        table: _infer_id_column(table, table_fields_map.get(table, []))
        for table in service_data.get("owned_tables", [])
    }
    for table, id_column in table_id_map.items():
        if id_column and id_column not in table_fields_map.get(table, []):
            table_fields_map.setdefault(table, []).insert(0, id_column)
        if id_column:
            detail_list = table_field_details_map.setdefault(table, [])
            if all(detail.get("name") != id_column for detail in detail_list):
                detail_list.insert(0, {"name": id_column, "type": "string"})
    spec["table_fields_map"] = table_fields_map
    spec["table_field_details_map"] = table_field_details_map
    spec["table_operation_columns_map"] = table_operations_map
    spec["table_dependencies_map"] = table_dependencies_map
    spec["table_id_columns"] = table_id_map
    primary_table = service_data.get("owned_tables", [spec["service_slug"]])[0]
    primary_fields = list(table_fields_map.get(primary_table, []))
    primary_id_column = table_id_map.get(primary_table, "id")
    if primary_id_column and primary_id_column not in primary_fields:
        primary_fields.insert(0, primary_id_column)
    spec["primary_table"] = primary_table
    spec["primary_table_fields"] = primary_fields
    spec["primary_id_column"] = primary_id_column
    spec["endpoints"] = _plan_endpoints(service_data, domain_mapped_proc, spec, table_id_map)
    spec["files"] = _build_clean_architecture_files(spec)


def _plan_endpoints(
    service_data: Dict[str, Any],
    domain_mapped_proc: Dict[str, Any],
    spec: Dict[str, Any],
    id_map: Dict[str, Optional[str]],
) -> List[Dict[str, Any]]:
    endpoints: List[Dict[str, Any]] = []
    service_name = spec.get("service_name", "")
    table_operations = domain_mapped_proc.get("table_operations", {})
    table_operation_columns = domain_mapped_proc.get("table_operation_columns", {})
    table_fields = domain_mapped_proc.get("table_fields", {})

    # Common health endpoint
    endpoints.append(
        {
            "name": f"{service_name}Health",
            "method": "GET",
            "path": "/health",
            "summary": "Service health check",
            "operation_id": f"{service_name}Health",
            "table": None,
            "action": "health",
            "request_columns": [],
            "response_columns": [],
            "id_column": None,
            "tag": service_name,
        }
    )

    for table in service_data.get("owned_tables", []):
        ops = table_operations.get(table, [])
        columns_by_op = table_operation_columns.get(table, {})
        all_table_columns = table_fields.get(table, [])
        id_column = id_map.get(table) or _infer_id_column(table, all_table_columns)
        tag = _pascal_case(table)

        for action in ops:
            endpoint = _build_endpoint(
                table=table,
                action=action,
                columns=columns_by_op.get(action, []),
                id_column=id_column,
                tag=tag,
            )
            if endpoint:
                endpoints.append(endpoint)
    return endpoints


def _build_endpoint(
    table: str,
    action: str,
    columns: List[str],
    id_column: Optional[str],
    tag: str,
) -> Optional[Dict[str, Any]]:
    action = action.lower()
    base_path = f"/{table.replace('_', '-')}"
    method = None
    summary = ""
    operation_id = ""
    request_columns: List[str] = []
    response_columns: List[str] = []

    if action == "read":
        method = "GET"
        summary = f"Fetch {table}"
        operation_id = f"get{_pascal_case(table)}"
        response_columns = columns or ["*"]
    elif action == "create":
        method = "POST"
        summary = f"Create {table}"
        operation_id = f"create{_pascal_case(table)}"
        request_columns = columns
    elif action == "update":
        method = "PUT"
        summary = f"Update {table}"
        operation_id = f"update{_pascal_case(table)}"
        request_columns = columns
        if id_column:
            base_path = f"{base_path}/{{{id_column}}}"
    elif action == "delete":
        method = "DELETE"
        summary = f"Delete {table}"
        operation_id = f"delete{_pascal_case(table)}"
        if id_column:
            base_path = f"{base_path}/{{{id_column}}}"
    else:
        return None

    return {
        "name": f"{action}_{table}",
        "method": method,
        "path": base_path,
        "summary": summary,
        "operation_id": operation_id,
        "table": table,
        "action": action,
        "request_columns": request_columns,
        "response_columns": response_columns,
        "id_column": id_column if method in {"PUT", "DELETE"} else None,
        "tag": tag,
    }


def _infer_id_column(table: str, columns: List[str]) -> Optional[str]:
    if not columns:
        return "id"
    candidates = [col for col in columns if col.lower() == "id"]
    if candidates:
        return candidates[0]
    singular = _singularize(table)
    preferred = f"{singular}_id"
    for col in columns:
        if col.lower() == preferred.lower():
            return col
    ending_matches = [col for col in columns if col.lower().endswith("_id")]
    if ending_matches:
        return ending_matches[0]
    return columns[0]


def _build_clean_architecture_files(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    base_package_path = spec["base_package_path"]
    entity_name = spec["entity_name"]
    service_kebab = spec["service_kebab"]
    files = [
        {"path": "pom.xml", "template": "aggregator_pom.xml.txt"},
        {"path": "oasgen/pom.xml", "template": "oasgen_pom.xml.txt"},
        {"path": "api/pom.xml", "template": "api_pom.xml.txt"},
        {
            "path": f"api/src/main/java/{base_package_path}/Application.java",
            "template": "api_application.java.txt",
        },
        {
            "path": f"api/src/main/java/{base_package_path}/controller/{entity_name}Controller.java",
            "template": "api_controller.java.txt",
        },
        {
            "path": f"api/src/main/java/{base_package_path}/service/{entity_name}Service.java",
            "template": "api_service_interface.java.txt",
        },
        {
            "path": f"api/src/main/java/{base_package_path}/service/impl/{entity_name}ServiceImpl.java",
            "template": "api_service_impl.java.txt",
        },
        {
            "path": f"api/src/main/java/{base_package_path}/repository/{entity_name}Repository.java",
            "template": "api_repository.java.txt",
        },
        {
            "path": f"api/src/main/java/{base_package_path}/entity/{entity_name}Entity.java",
            "template": "api_entity.java.txt",
        },
        {
            "path": f"api/src/main/java/{base_package_path}/mapper/{entity_name}Mapper.java",
            "template": "api_mapper.java.txt",
        },
        {
            "path": f"api/src/main/java/{base_package_path}/exception/GlobalExceptionHandler.java",
            "template": "api_exception_handler.java.txt",
        },
        {
            "path": "api/src/main/resources/application.yml",
            "template": "api_application.yml.txt",
        },
        {
            "path": "api/src/main/resources/openapi/openapi-spec.yaml",
            "template": "api_openapi_spec.yaml.txt",
        },
        {
            "path": f"oasgen/src/main/java/{base_package_path}/api/{entity_name}Api.java",
            "template": "oasgen_api_interface.java.txt",
        },
        {
            "path": f"oasgen/src/main/java/{base_package_path}/invoker/ApiClient.java",
            "template": "oasgen_invoker.java.txt",
        },
        {
            "path": f"oasgen/src/main/java/{base_package_path}/model/{entity_name}HealthResponse.java",
            "template": "oasgen_model.java.txt",
        },
    ]
    for table in sorted(spec.get("table_fields_map", {}).keys()):
        record_name = f"{_pascal_case(table)}Record"
        files.append(
            {
                "path": f"oasgen/src/main/java/{base_package_path}/model/{record_name}.java",
                "template": "__dynamic_oasgen_record_model__",
                "table": table,
            }
        )
    return files


def _derive_entity_name(service_name: str) -> str:
    if service_name.endswith("Service") and len(service_name) > len("Service"):
        return service_name[: -len("Service")]
    return service_name or "Service"


def _camel_to_kebab(name: str) -> str:
    parts = re.findall(r"[A-Z]+(?=[A-Z][a-z]|[0-9]|$)|[A-Z]?[a-z0-9]+", name)
    return "-".join(part.lower() for part in parts if part)


def _pascal_case(name: str) -> str:
    parts = re.findall(r"[A-Z]+(?=[A-Z][a-z]|[0-9]|$)|[A-Z]?[a-z0-9]+", name)
    return "".join(part.capitalize() for part in parts)


def _singularize(name: str) -> str:
    if name.endswith("ies"):
        return name[:-3] + "y"
    if name.endswith("ses"):
        return name[:-2]
    if name.endswith("s") and len(name) > 1:
        return name[:-1]
    return name
