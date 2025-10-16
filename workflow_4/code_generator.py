from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from settings import PROJECT_SETTINGS
from common.tools.tools import FileWriterTool, load_workflow_module

logger = logging.getLogger(__name__)

agents_module = load_workflow_module("workflow_1", "agents")
CodeGeneratorAgent = agents_module.CodeGeneratorAgent
bootstrap_agents = agents_module.bootstrap_agents

DEFAULT_PROMPT_DIR = Path("common") / "prompts" / "generate"
JAVA_VERSION = "21"

DYNAMIC_GENERATORS: Dict[str, str] = {
    "api_openapi_spec.yaml.txt": "_render_openapi_spec",
    "api_controller.java.txt": "_render_controller",
    "api_service_interface.java.txt": "_render_service_interface",
    "api_service_impl.java.txt": "_render_service_impl",
    "api_repository.java.txt": "_render_repository",
    "api_entity.java.txt": "_render_entity",
    "api_mapper.java.txt": "_render_mapper",
    "oasgen_api_interface.java.txt": "_render_oasgen_interface",
    "oasgen_model.java.txt": "_render_oasgen_health_model",
    "__dynamic_oasgen_record_model__": "_render_oasgen_record_model",
}


def load_prompt(template_name: str, prompts_dir: Path) -> str:
    template_path = prompts_dir / template_name
    if not template_path.exists():
        return ""
    return template_path.read_text(encoding="utf-8")


def build_template_context(service_spec: Dict[str, Any]) -> Dict[str, Any]:
    owned_tables = service_spec.get("owned_tables", [])
    dependencies = service_spec.get("dependencies", [])
    request_id = PROJECT_SETTINGS.get("request_id", "")
    context = {
        "service_name": service_spec.get("service_name", ""),
        "domain": service_spec.get("domain", ""),
        "owned_tables": ", ".join(owned_tables),
        "dependencies": ", ".join(dependencies),
        "base_package": service_spec.get("base_package", ""),
        "base_package_path": service_spec.get("base_package_path", ""),
        "entity_name": service_spec.get("entity_name", ""),
        "entity_var": service_spec.get("entity_var", ""),
        "service_kebab": service_spec.get("service_kebab", ""),
        "service_slug": service_spec.get("service_slug", ""),
        "java_version": JAVA_VERSION,
        "request_id": request_id,
    }
    context["entity_plural"] = context["entity_name"] + "s" if context["entity_name"] else "Entities"
    return context


def generate_service(service_spec: Dict[str, Any], agent: CodeGeneratorAgent, prompts_dir: Path, output_root: Path) -> List[Path]:
    payload = agent.prepare_generation_payload(service_spec)
    writer = FileWriterTool()
    service_dir = output_root / service_spec["service_name"]
    generated_paths: List[Path] = []

    context = build_template_context(service_spec)
    payload_context = payload.get("service", {})
    for key, value in payload_context.items():
        context.setdefault(key, value)

    for file_spec in service_spec.get("files", []):
        template_name = file_spec["template"]
        generator_name = DYNAMIC_GENERATORS.get(template_name)
        if generator_name:
            content = globals()[generator_name](service_spec, file_spec)
        else:
            template_content = load_prompt(template_name, prompts_dir)
            try:
                content = template_content.format(**context)
            except KeyError as exc:
                logger.warning("Missing template variable %s for template %s", exc.args[0], template_name)
                content = template_content
        generated_paths.append(writer.write(service_dir, file_spec["path"], content))
        logger.debug("Generated file %s for service %s", generated_paths[-1], service_spec["service_name"])
    logger.info("Generated %d files for service %s", len(generated_paths), service_spec["service_name"])
    return generated_paths


def run_code_generator(service_architecture: Dict[str, Any], prompts_dir: Path | None = None, output_root: Path | None = None) -> List[Path]:
    agents = bootstrap_agents()
    generator: CodeGeneratorAgent = agents["code_generator"]
    prompts_path = prompts_dir or PROJECT_SETTINGS.get("prompts_dir", DEFAULT_PROMPT_DIR)
    if isinstance(prompts_path, str):
        prompts_path = Path(prompts_path)
    output_root = output_root or PROJECT_SETTINGS.get("generated_dir", Path("generated"))
    if isinstance(output_root, str):
        output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    all_paths: List[Path] = []
    for service_spec in service_architecture.get("services", []):
        logger.debug(
            "Calling CodeGeneratorAgent for service=%s domain=%s",
            service_spec.get("service_name"),
            service_spec.get("domain"),
        )
        all_paths.extend(generate_service(service_spec, generator, Path(prompts_path), Path(output_root)))
    logger.info("Generated %d total files", len(all_paths))
    return all_paths


# ----------------------------
# Dynamic renderers
# ----------------------------


def _render_openapi_spec(service_spec: Dict[str, Any], file_spec: Optional[Dict[str, Any]] | None = None) -> str:
    service_name = service_spec.get("service_name", "Service")
    entity_name = service_spec.get("entity_name", "Entity")
    endpoints = service_spec.get("endpoints", [])
    table_fields = service_spec.get("table_fields_map", {})

    schemas: Dict[str, Dict[str, str]] = {}
    for table, columns in table_fields.items():
        schema_name = _schema_name(table)
        fields = columns or ["id"]
        schemas[schema_name] = {column: _infer_openapi_type(column) for column in fields}
    health_schema = f"{entity_name}HealthResponse"

    lines: List[str] = [
        "openapi: 3.0.3",
        "info:",
        f"  title: {service_name} API",
        "  version: 1.0.0",
        "servers:",
        "  - url: http://localhost:8080",
        "paths:",
    ]

    for endpoint in endpoints:
        method = endpoint.get("method", "GET").lower()
        path = endpoint.get("path", "/")
        summary = endpoint.get("summary", "")
        operation_id = endpoint.get("operation_id", _camel(endpoint.get("name", "operation")))
        tag = endpoint.get("tag", service_name)

        lines.append(f"  {path}:")
        lines.append(f"    {method}:")
        lines.append("      tags:")
        lines.append(f"        - {tag}")
        lines.append(f"      summary: {summary}")
        lines.append(f"      operationId: {operation_id}")

        parameters = _openapi_parameters(endpoint)
        if parameters:
            lines.append("      parameters:")
            for param in parameters:
                lines.append(f"        - name: {param['name']}")
                lines.append("          in: path")
                lines.append("          required: true")
                lines.append("          schema:")
                lines.append("            type: string")

        request_ref = _request_schema_ref(endpoint)
        if request_ref:
            lines.append("      requestBody:")
            lines.append("        required: true")
            lines.append("        content:")
            lines.append("          application/json:")
            lines.append("            schema:")
            lines.append(f"              $ref: '{request_ref}'")

        lines.append("      responses:")
        for status, schema_ref, is_array in _response_schemas(endpoint, service_spec):
            description = "Success" if status.startswith("2") else "Response"
            lines.append(f"        '{status}':")
            lines.append(f"          description: {description}")
            if schema_ref:
                lines.append("          content:")
                lines.append("            application/json:")
                lines.append("              schema:")
                if is_array:
                    lines.append("                type: array")
                    lines.append("                items:")
                    lines.append(f"                  $ref: '{schema_ref}'")
                else:
                    lines.append(f"                $ref: '{schema_ref}'")

    lines.append("components:")
    lines.append("  schemas:")
    lines.append(f"    {health_schema}:")
    lines.append("      type: object")
    lines.append("      properties:")
    lines.append("        status:")
    lines.append("          type: string")
    lines.append("        timestamp:")
    lines.append("          type: string")
    lines.append("          format: date-time")
    lines.append("    GenericResponse:")
    lines.append("      type: object")
    lines.append("      properties:")
    lines.append("        message:")
    lines.append("          type: string")
    for name, props in schemas.items():
        lines.append(f"    {name}:")
        lines.append("      type: object")
        lines.append("      properties:")
        for column, col_type in props.items():
            lines.append(f"        {column}:")
            lines.append(f"          type: {col_type}")
    return "\n".join(lines) + "\n"


def _render_controller(service_spec: Dict[str, Any], file_spec: Optional[Dict[str, Any]] | None = None) -> str:
    base_package = service_spec.get("base_package", "")
    entity_name = service_spec.get("entity_name", "Entity")
    entity_var = service_spec.get("entity_var", "entity")
    endpoints = service_spec.get("endpoints", [])

    imports = {
        "java.util.List",
        "java.util.Map",
        "org.springframework.http.ResponseEntity",
        "org.springframework.web.bind.annotation.*",
        f"{base_package}.api.{entity_name}Api",
        f"{base_package}.model.{entity_name}HealthResponse",
        f"{base_package}.service.{entity_name}Service",
    }
    if any(ep.get("method") in {"POST", "PUT"} for ep in endpoints):
        imports.add("org.springframework.http.HttpStatus")

    lines = [f"package {base_package}.controller;", ""]
    for imp in sorted(imports):
        lines.append(f"import {imp};")
    lines.append("")
    lines.append("@RestController")
    lines.append(f"public class {entity_name}Controller implements {entity_name}Api {{")
    lines.append("")
    lines.append(f"    private final {entity_name}Service {entity_var}Service;")
    lines.append("")
    lines.append(f"    public {entity_name}Controller({entity_name}Service {entity_var}Service) {{")
    lines.append(f"        this.{entity_var}Service = {entity_var}Service;")
    lines.append("    }")

    for endpoint in endpoints:
        lines.append("")
        lines.append(f"    {_mapping_annotation(endpoint)}")
        signature, body_lines = _controller_method(endpoint, entity_var, entity_name)
        lines.append(f"    {signature} {{")
        for line in body_lines:
            lines.append(f"        {line}")
        lines.append("    }")

    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def _render_service_interface(service_spec: Dict[str, Any], file_spec: Optional[Dict[str, Any]] | None = None) -> str:
    base_package = service_spec.get("base_package", "")
    entity_name = service_spec.get("entity_name", "Entity")
    endpoints = service_spec.get("endpoints", [])

    lines = [
        f"package {base_package}.service;",
        "",
        "import java.util.List;",
        "import java.util.Map;",
        "",
        f"import {base_package}.model.{entity_name}HealthResponse;",
        "",
        f"public interface {entity_name}Service {{",
        "",
        f"    {entity_name}HealthResponse health();",
    ]
    for endpoint in endpoints:
        if endpoint.get("action") == "health":
            continue
        signature = _service_signature(endpoint, include_public=False)
        lines.append("")
        lines.append(f"    {signature};")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def _render_service_impl(service_spec: Dict[str, Any], file_spec: Optional[Dict[str, Any]] | None = None) -> str:
    base_package = service_spec.get("base_package", "")
    entity_name = service_spec.get("entity_name", "Entity")
    endpoints = service_spec.get("endpoints", [])

    lines = [
        f"package {base_package}.service.impl;",
        "",
        "import java.util.Collections;",
        "import java.util.List;",
        "import java.util.Map;",
        "",
        "import org.springframework.stereotype.Service;",
        "",
        f"import {base_package}.invoker.ApiClient;",
        f"import {base_package}.model.{entity_name}HealthResponse;",
        f"import {base_package}.service.{entity_name}Service;",
        "",
        "@Service",
        f"public class {entity_name}ServiceImpl implements {entity_name}Service {{",
        "",
        "    @Override",
        f"    public {entity_name}HealthResponse health() {{",
        "        return ApiClient.healthResponse(\"UP\");",
        "    }",
    ]
    for endpoint in endpoints:
        if endpoint.get("action") == "health":
            continue
        signature = _service_signature(endpoint, include_public=True)
        body_lines = _service_body(endpoint)
        lines.append("")
        lines.append("    @Override")
        lines.append(f"    {signature} {{")
        for line in body_lines:
            lines.append(f"        {line}")
        lines.append("    }")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def _render_repository(service_spec: Dict[str, Any], file_spec: Optional[Dict[str, Any]] | None = None) -> str:
    base_package = service_spec.get("base_package", "")
    entity_name = service_spec.get("entity_name", "Entity")
    return "\n".join(
        [
            f"package {base_package}.repository;",
            "",
            "import org.springframework.data.jpa.repository.JpaRepository;",
            "",
            f"import {base_package}.entity.{entity_name}Entity;",
            "",
            f"public interface {entity_name}Repository extends JpaRepository<{entity_name}Entity, String> {{",
            "}",
            "",
        ]
    )


def _render_entity(service_spec: Dict[str, Any], file_spec: Optional[Dict[str, Any]] | None = None) -> str:
    base_package = service_spec.get("base_package", "")
    entity_name = service_spec.get("entity_name", "Entity")
    table_name = service_spec.get("primary_table", entity_name.lower())
    fields = list(service_spec.get("primary_table_fields", []) or ["status"])
    id_column = service_spec.get("primary_id_column", "id")
    if id_column not in fields:
        fields.insert(0, id_column)
    id_field = _camel(id_column or "id")
    id_pascal = _pascal(id_column or "id")

    lines = [
        f"package {base_package}.entity;",
        "",
        "import jakarta.persistence.Column;",
        "import jakarta.persistence.Entity;",
        "import jakarta.persistence.GeneratedValue;",
        "import jakarta.persistence.GenerationType;",
        "import jakarta.persistence.Id;",
        "import jakarta.persistence.Table;",
        "",
        "@Entity",
        f"@Table(name = \"{table_name}\")",
        f"public class {entity_name}Entity {{",
        "",
        "    @Id",
        "    @GeneratedValue(strategy = GenerationType.IDENTITY)",
    ]
    if id_column:
        lines.append(f"    @Column(name = \"{id_column}\")")
    lines.append(f"    private String {id_field};")
    for field in fields:
        if field == id_column:
            continue
        camel = _camel(field)
        lines.append(f"    @Column(name = \"{field}\")")
        lines.append(f"    private String {camel};")
    lines.append("")
    lines.append(f"    public String get{id_pascal}() {{")
    lines.append(f"        return {id_field};")
    lines.append("    }")
    lines.append("")
    lines.append(f"    public void set{id_pascal}(String {id_field}) {{")
    lines.append(f"        this.{id_field} = {id_field};")
    lines.append("    }")
    for field in fields:
        if field == id_column:
            continue
        camel = _camel(field)
        pascal = _pascal(field)
        lines.append("")
        lines.append(f"    public String get{pascal}() {{")
        lines.append(f"        return {camel};")
        lines.append("    }")
        lines.append("")
        lines.append(f"    public void set{pascal}(String {camel}) {{")
        lines.append(f"        this.{camel} = {camel};")
        lines.append("    }")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def _render_mapper(service_spec: Dict[str, Any], file_spec: Optional[Dict[str, Any]] | None = None) -> str:
    base_package = service_spec.get("base_package", "")
    entity_name = service_spec.get("entity_name", "Entity")
    return "\n".join(
        [
            f"package {base_package}.mapper;",
            "",
            "import java.time.OffsetDateTime;",
            "import java.util.Collections;",
            "import java.util.Map;",
            "",
            f"import {base_package}.entity.{entity_name}Entity;",
            f"import {base_package}.model.{entity_name}HealthResponse;",
            "",
            f"public final class {entity_name}Mapper {{",
            "",
            f"    private {entity_name}Mapper() {{",
            "    }",
            "",
            f"    public static {entity_name}HealthResponse toHealthResponse({entity_name}Entity entity) {{",
            f"        {entity_name}HealthResponse response = new {entity_name}HealthResponse();",
            "        response.setStatus(entity != null ? \"UP\" : \"UNKNOWN\");",
            "        response.setTimestamp(OffsetDateTime.now());",
            "        return response;",
            "    }",
            "",
            f"    public static Map<String, Object> toMap({entity_name}Entity entity) {{",
            "        return Collections.emptyMap();",
            "    }",
            "}",
            "",
        ]
    )


def _render_oasgen_interface(service_spec: Dict[str, Any], file_spec: Optional[Dict[str, Any]] | None = None) -> str:
    base_package = service_spec.get("base_package", "")
    entity_name = service_spec.get("entity_name", "Entity")
    entity_var = service_spec.get("entity_var", "entity")
    endpoints = service_spec.get("endpoints", [])

    imports = {
        "org.springframework.http.ResponseEntity",
        "org.springframework.web.bind.annotation.*",
        f"{base_package}.model.{entity_name}HealthResponse",
    }
    if any(ep.get("action") != "health" for ep in endpoints):
        imports.add("java.util.List")
        imports.add("java.util.Map")

    lines = [f"package {base_package}.api;", ""]
    for imp in sorted(imports):
        lines.append(f"import {imp};")
    lines.append("")
    lines.append(f"public interface {entity_name}Api {{")
    for endpoint in endpoints:
        lines.append("")
        lines.append(f"    {_mapping_annotation(endpoint)}")
        signature, _ = _controller_method(endpoint, entity_var, entity_name)
        interface_signature = signature.replace("public ", "", 1)
        lines.append(f"    {interface_signature};")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def _render_oasgen_health_model(service_spec: Dict[str, Any], file_spec: Optional[Dict[str, Any]] | None = None) -> str:
    base_package = service_spec.get("base_package", "")
    entity_name = service_spec.get("entity_name", "Entity")
    return "\n".join(
        [
            f"package {base_package}.model;",
            "",
            "import java.time.OffsetDateTime;",
            "",
            f"public class {entity_name}HealthResponse {{",
            "",
            "    private String status;",
            "    private OffsetDateTime timestamp = OffsetDateTime.now();",
            "",
            "    public String getStatus() {",
            "        return status;",
            "    }",
            "",
            "    public void setStatus(String status) {",
            "        this.status = status;",
            "    }",
            "",
            "    public OffsetDateTime getTimestamp() {",
            "        return timestamp;",
            "    }",
            "",
            "    public void setTimestamp(OffsetDateTime timestamp) {",
            "        this.timestamp = timestamp;",
            "    }",
            "}",
            "",
        ]
    )


def _render_oasgen_record_model(service_spec: Dict[str, Any], file_spec: Optional[Dict[str, Any]] | None = None) -> str:
    base_package = service_spec.get("base_package", "")
    table_fields_map = service_spec.get("table_fields_map", {})
    table = (file_spec or {}).get("table")
    columns = list(table_fields_map.get(table or "", []) or ["id"])
    if file_spec and "path" in file_spec:
        class_name = Path(file_spec["path"]).stem
    else:
        class_name = _schema_name(table)
    if not class_name:
        class_name = "GenericRecord"

    lines = [f"package {base_package}.model;", ""]
    lines.append(f"public class {class_name} {{")
    for column in columns:
        camel = _camel(column)
        lines.append(f"    private String {camel};")
    for column in columns:
        camel = _camel(column)
        pascal = _pascal(column)
        lines.append("")
        lines.append(f"    public String get{pascal}() {{")
        lines.append(f"        return {camel};")
        lines.append("    }")
        lines.append("")
        lines.append(f"    public void set{pascal}(String {camel}) {{")
        lines.append(f"        this.{camel} = {camel};")
        lines.append("    }")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


# ----------------------------
# Helper utilities
# ----------------------------


def _openapi_parameters(endpoint: Dict[str, Any]) -> List[Dict[str, str]]:
    return [{"name": raw} for raw in _extract_path_variables(endpoint.get("path", ""))]


def _response_schemas(endpoint: Dict[str, Any], service_spec: Dict[str, Any]) -> List[Tuple[str, Optional[str], bool]]:
    action = endpoint.get("action")
    table = endpoint.get("table")
    schema_ref = f"#/components/schemas/{_schema_name(table)}" if table else None
    entity_name = service_spec.get("entity_name", "Entity")
    if action == "health":
        return [("200", f"#/components/schemas/{entity_name}HealthResponse", False)]
    if action == "read":
        return [("200", schema_ref, True)]
    if action == "create":
        return [("201", schema_ref, False)]
    if action == "update":
        return [("200", schema_ref, False)]
    if action == "delete":
        return [("204", None, False)]
    return [("200", "#/components/schemas/GenericResponse", False)]


def _request_schema_ref(endpoint: Dict[str, Any]) -> Optional[str]:
    method = endpoint.get("method", "GET").upper()
    table = endpoint.get("table")
    if method in {"POST", "PUT"} and table:
        return f"#/components/schemas/{_schema_name(table)}"
    return None


def _service_signature(endpoint: Dict[str, Any], *, include_public: bool) -> str:
    method_name = _camel(endpoint.get("operation_id") or endpoint.get("name", "operation"))
    method = endpoint.get("method", "GET").upper()
    params, _ = _endpoint_parameters(endpoint, annotations=False)
    param_str = f"({params})" if params else "()"
    prefix = "public " if include_public else ""
    if method == "GET":
        return f"{prefix}List<Map<String, Object>> {method_name}{param_str}"
    if method == "POST":
        return f"{prefix}Map<String, Object> {method_name}{param_str}"
    if method == "PUT":
        return f"{prefix}Map<String, Object> {method_name}{param_str}"
    if method == "DELETE":
        return f"{prefix}void {method_name}{param_str}"
    return f"{prefix}String {method_name}{param_str}"


def _service_body(endpoint: Dict[str, Any]) -> List[str]:
    method = endpoint.get("method", "GET").upper()
    if method == "GET":
        return ["return Collections.emptyList();"]
    if method in {"POST", "PUT"}:
        return ["return Collections.emptyMap();"]
    if method == "DELETE":
        return ["// TODO implement delete logic"]
    return ["return \"NOT_IMPLEMENTED\";"]


def _mapping_annotation(endpoint: Dict[str, Any]) -> str:
    method = endpoint.get("method", "GET").upper()
    path = endpoint.get("path", "/")
    mapping_lookup = {
        "GET": "GetMapping",
        "POST": "PostMapping",
        "PUT": "PutMapping",
        "DELETE": "DeleteMapping",
        "PATCH": "PatchMapping",
    }
    mapping = mapping_lookup.get(method)
    normalized_path = path if path and path != "/" else ""
    if mapping:
        if normalized_path:
            return f"@{mapping}(\"{normalized_path}\")"
        return f"@{mapping}"
    method_enum = f"RequestMethod.{method}"
    if normalized_path:
        return f"@RequestMapping(value = \"{normalized_path}\", method = {method_enum})"
    return f"@RequestMapping(method = {method_enum})"


def _controller_method(endpoint: Dict[str, Any], entity_var: str, entity_name: str) -> Tuple[str, List[str]]:
    method_name = _camel(endpoint.get("operation_id") or endpoint.get("name", "operation"))
    method = endpoint.get("method", "GET").upper()
    action = endpoint.get("action")
    params, call_params = _endpoint_parameters(endpoint, annotations=True)
    call = f"{entity_var}Service.{method_name}({call_params})" if call_params else f"{entity_var}Service.{method_name}()"

    if action == "health":
        signature = f"public ResponseEntity<{entity_name}HealthResponse> {method_name}()"
        return signature, [f"return ResponseEntity.ok({entity_var}Service.health());"]

    if method == "GET":
        signature = (
            f"public ResponseEntity<List<Map<String, Object>>> {method_name}({params})"
            if params
            else f"public ResponseEntity<List<Map<String, Object>>> {method_name}()"
        )
        return signature, [f"return ResponseEntity.ok({call});"]

    if method == "POST":
        signature = (
            f"public ResponseEntity<Map<String, Object>> {method_name}({params})"
            if params
            else f"public ResponseEntity<Map<String, Object>> {method_name}()"
        )
        return signature, [f"return ResponseEntity.status(HttpStatus.CREATED).body({call});"]

    if method == "PUT":
        signature = f"public ResponseEntity<Map<String, Object>> {method_name}({params})"
        return signature, [f"return ResponseEntity.ok({call});"]

    if method == "DELETE":
        signature = f"public ResponseEntity<Void> {method_name}({params})"
        return signature, [f"{call};", "return ResponseEntity.noContent().build();"]

    signature = (
        f"public ResponseEntity<Map<String, Object>> {method_name}({params})"
        if params
        else f"public ResponseEntity<Map<String, Object>> {method_name}()"
    )
    return signature, [f"return ResponseEntity.ok({call});"]


def _endpoint_parameters(endpoint: Dict[str, Any], annotations: bool) -> Tuple[str, str]:
    path_vars = _extract_path_variables(endpoint.get("path", ""))
    method = endpoint.get("method", "GET").upper()
    params: List[str] = []
    call_params: List[str] = []
    for raw in path_vars:
        var_name = _camel(raw)
        if annotations:
            params.append(f'@PathVariable("{raw}") String {var_name}')
        else:
            params.append(f"String {var_name}")
        call_params.append(var_name)
    if method in {"POST", "PUT"}:
        body_param = "@RequestBody Map<String, Object> body" if annotations else "Map<String, Object> body"
        params.append(body_param)
        call_params.append("body")
    return ", ".join(params), ", ".join(call_params)


def _openapi_parameters(endpoint: Dict[str, Any]) -> List[Dict[str, str]]:
    return [{"name": raw} for raw in _extract_path_variables(endpoint.get("path", ""))]


def _extract_path_variables(path: str) -> List[str]:
    return [match.group(1) for match in re.finditer(r"\{([^}]+)\}", path or "")]


def _schema_name(table: Optional[str]) -> str:
    if not table:
        return "GenericResponse"
    return _pascal(table) + "Record"


def _infer_openapi_type(column: str) -> str:
    lower = column.lower()
    if lower.endswith("_id") or lower == "id":
        return "string"
    if any(token in lower for token in ("amount", "total", "cost", "price")):
        return "number"
    if "count" in lower or "quantity" in lower:
        return "integer"
    if "date" in lower or "time" in lower:
        return "string"
    return "string"


def _camel(value: str) -> str:
    parts = _split_words(value)
    if not parts:
        return value
    first, *rest = parts
    return first.lower() + "".join(part.capitalize() for part in rest)


def _pascal(value: str) -> str:
    parts = _split_words(value)
    return "".join(part.capitalize() for part in parts) if parts else value.title()


def _split_words(value: str) -> List[str]:
    if not value:
        return []
    chunks = re.split(r"[^A-Za-z0-9]+", value)
    words: List[str] = []
    pattern = re.compile(r"[A-Z]+(?=[A-Z][a-z]|[0-9])|[A-Z]?[a-z0-9]+|[0-9]+")
    for chunk in chunks:
        if not chunk:
            continue
        words.extend(pattern.findall(chunk))
    return [word for word in words if word]
