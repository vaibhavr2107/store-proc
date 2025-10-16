from __future__ import annotations

import json
import re
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from settings import PROJECT_SETTINGS
from common.tools.tools import load_workflow_module

logger = logging.getLogger(__name__)

TABLE_PATTERN = re.compile(r"\bfrom\s+([a-zA-Z0-9_.\[\]\"`]+)(?:\s+(?:as\s+)?([a-zA-Z0-9_]+))?", re.IGNORECASE)
JOIN_PATTERN = re.compile(r"\bjoin\s+([a-zA-Z0-9_.\[\]\"`]+)(?:\s+(?:as\s+)?([a-zA-Z0-9_]+))?", re.IGNORECASE)
SELECT_PATTERN = re.compile(r"select\s+(.*?)\s+from", re.IGNORECASE | re.DOTALL)
PROCEDURE_PATTERN = re.compile(r"create\s+procedure\s+([a-zA-Z0-9_\.]+)", re.IGNORECASE)
INSERT_PATTERN = re.compile(
    r"insert\s+into\s+([a-zA-Z0-9_.\[\]\"`]+)\s*\(([^)]+)\)",
    re.IGNORECASE | re.DOTALL,
)
UPDATE_PATTERN = re.compile(
    r"update\s+([a-zA-Z0-9_.\[\]\"`]+)\s+set\s+(.+?)(?:\bwhere\b|;|$)",
    re.IGNORECASE | re.DOTALL,
)
DELETE_PATTERN = re.compile(
    r"delete\s+from\s+([a-zA-Z0-9_.\[\]\"`]+)",
    re.IGNORECASE,
)

agents_module = load_workflow_module("workflow_1", "agents")
bootstrap_agents = agents_module.bootstrap_agents


def read_file(path: Path) -> str:
    logger.debug("Reading file: %s", path)
    return path.read_text(encoding="utf-8")


def load_domain_mapping(path: Path) -> Dict[str, List[str]]:
    content = read_file(path)
    data = json.loads(content)
    normalized = {key: [table.lower() for table in value] for key, value in data.items()}
    logger.debug("Loaded domain mapping: %s", normalized)
    return normalized


def parse_store_procedure(source: str) -> Dict[str, Any]:
    tables: Set[str] = set()
    alias_map: Dict[str, str] = {}
    for matcher in (TABLE_PATTERN, JOIN_PATTERN):
        extracted_tables, extracted_aliases = _extract_tables_and_aliases(matcher, source)
        tables.update(extracted_tables)
        alias_map.update(extracted_aliases)
    crud_details = _extract_crud_details(source, tables, alias_map)
    fields_map = crud_details["table_fields"]
    procedure_name = _extract_procedure_name(source)
    logger.debug("Parsed tables: %s", tables)
    logger.debug("Alias map: %s", alias_map)
    logger.debug("Extracted fields map: %s", fields_map)
    return {
        "tables": sorted(tables),
        "raw": source,
        "alias_map": alias_map,
        "table_fields": fields_map,
        "procedure_name": procedure_name,
        "table_operations": crud_details["table_operations"],
        "table_operation_columns": crud_details["table_operation_columns"],
    }


def _extract_tables_and_aliases(pattern: re.Pattern[str], source: str) -> Tuple[Set[str], Dict[str, str]]:
    tables: Set[str] = set()
    alias_map: Dict[str, str] = {}
    matches = pattern.findall(source)
    for match in matches:
        if isinstance(match, tuple):
            table_ref, alias = match
        else:
            table_ref, alias = match, ""
        table_name = normalize_identifier(table_ref)
        tables.add(table_name)
        if alias:
            alias_map[alias.lower()] = table_name
    return tables, alias_map


def _extract_procedure_name(source: str) -> str:
    match = PROCEDURE_PATTERN.search(source)
    if not match:
        return "procedure"
    name = match.group(1)
    segments = name.split(".")
    return segments[-1]


def _extract_table_fields(source: str, alias_map: Dict[str, str]) -> Dict[str, List[str]]:
    fields: Dict[str, Set[str]] = defaultdict(set)
    for match in SELECT_PATTERN.finditer(source):
        select_clause = match.group(1)
        for column_expr in _split_columns(select_clause):
            column_expr = column_expr.strip()
            if not column_expr:
                continue
            column_expr = column_expr.split("--")[0].strip()
            if not column_expr:
                continue
            lower_expr = column_expr.lower()
            if lower_expr.startswith("distinct "):
                column_expr = column_expr[len("distinct ") :].strip()
                lower_expr = column_expr.lower()
            as_index = lower_expr.find(" as ")
            if as_index != -1:
                column_expr = column_expr[:as_index].strip()
            if "(" in column_expr and ")" in column_expr:
                continue
            if "." in column_expr:
                alias, column = column_expr.split(".", 1)
                alias = alias.strip().lower()
                column = column.strip()
                if not column:
                    continue
                table = alias_map.get(alias, normalize_identifier(alias))
                fields[table].add(column)
            else:
                continue
    return {table: sorted(columns) for table, columns in fields.items()}


def _split_columns(select_clause: str) -> List[str]:
    columns = []
    current = []
    depth = 0
    for char in select_clause:
        if char == "," and depth == 0:
            columns.append("".join(current))
            current = []
            continue
        if char in "(":
            depth += 1
        elif char in ")":
            depth = max(0, depth - 1)
        current.append(char)
    if current:
        columns.append("".join(current))
    return columns


def _extract_crud_details(
    source: str,
    tables: Set[str],
    alias_map: Dict[str, str],
) -> Dict[str, Any]:
    operations: Dict[str, Dict[str, Set[str]]] = defaultdict(
        lambda: {"read": set(), "create": set(), "update": set(), "delete": set()}
    )

    for match in SELECT_PATTERN.finditer(source):
        select_clause = match.group(1)
        for column_expr in _split_columns(select_clause):
            column_expr = column_expr.strip()
            if not column_expr or column_expr == "*":
                continue
            lower_expr = column_expr.lower()
            if lower_expr.startswith("distinct "):
                column_expr = column_expr[len("distinct ") :].strip()
                lower_expr = column_expr.lower()
            as_index = lower_expr.find(" as ")
            if as_index != -1:
                column_expr = column_expr[:as_index].strip()
            if "." in column_expr:
                alias, column = column_expr.split(".", 1)
                alias = alias.strip().lower()
                column = column.strip()
                table = alias_map.get(alias, normalize_identifier(alias))
                operations[table]["read"].add(column or "*")
                tables.add(table)
            else:
                continue

    for match in INSERT_PATTERN.finditer(source):
        table_ref = match.group(1)
        column_list = match.group(2)
        table = normalize_identifier(table_ref)
        tables.add(table)
        columns = [col.strip().strip("`[]\"") for col in column_list.split(",") if col.strip()]
        for column in columns:
            operations[table]["create"].add(column)

    for match in UPDATE_PATTERN.finditer(source):
        table_ref = match.group(1)
        set_clause = match.group(2)
        table = normalize_identifier(table_ref)
        tables.add(table)
        assignments = _split_by_comma_outside_parentheses(set_clause)
        for assignment in assignments:
            column = assignment.split("=", 1)[0].strip().strip("`[]\"")
            if column:
                operations[table]["update"].add(column)

    for match in DELETE_PATTERN.finditer(source):
        table_ref = match.group(1)
        table = normalize_identifier(table_ref)
        tables.add(table)
        operations[table]["delete"].add("*")

    table_operations = {
        table: sorted([op for op, cols in op_map.items() if cols])
        for table, op_map in operations.items()
    }
    table_operation_columns = {
        table: {op: sorted(columns) for op, columns in op_map.items() if columns}
        for table, op_map in operations.items()
    }
    table_fields = {}
    for table in tables:
        column_sets = []
        for op in ("read", "create", "update"):
            column_sets.append(set(table_operation_columns.get(table, {}).get(op, [])))
        columns = sorted(set().union(*column_sets)) if column_sets else []
        table_fields[table] = columns
    return {
        "table_operations": table_operations,
        "table_operation_columns": table_operation_columns,
        "table_fields": table_fields,
    }


def _split_by_comma_outside_parentheses(clause: str) -> List[str]:
    parts = []
    current = []
    depth = 0
    for char in clause:
        if char == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        current.append(char)
    if current:
        parts.append("".join(current).strip())
    return [part for part in parts if part]


def normalize_identifier(identifier: str) -> str:
    cleaned = identifier.strip()
    for char in ("[", "]", "`", '"'):
        cleaned = cleaned.replace(char, "")
    parts = cleaned.split(".")
    return parts[-1].lower()


def map_domains(parsed: Dict[str, List[str]], domain_mapping: Dict[str, List[str]]) -> Dict[str, Any]:
    table_domains: Dict[str, List[str]] = {table: [] for table in parsed.get("tables", [])}
    for domain, tables in domain_mapping.items():
        for table in table_domains:
            if table in tables:
                table_domains[table].append(domain)
    logger.debug("Table to domain mapping: %s", table_domains)
    return {
        "tables": parsed.get("tables", []),
        "domains": domain_mapping,
        "table_domains": table_domains,
        "raw": parsed.get("raw", ""),
        "alias_map": parsed.get("alias_map", {}),
        "table_fields": parsed.get("table_fields", {}),
        "procedure_name": parsed.get("procedure_name", "procedure"),
        "table_operations": parsed.get("table_operations", {}),
        "table_operation_columns": parsed.get("table_operation_columns", {}),
    }


def create_storeproc_overview(domain_mapped_proc: Dict[str, Any], output_dir: Path | None = None) -> Path | None:
    agents = bootstrap_agents()
    overview_agent = agents.get("storeproc_overview")
    if overview_agent is None:
        logger.warning("StoreProcOverviewAgent unavailable; skipping overview generation.")
        return None
    target_dir = Path(output_dir or PROJECT_SETTINGS.get("output_dir", "output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    procedure_name = domain_mapped_proc.get("procedure_name", "procedure")
    sanitized_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", procedure_name)
    overview_path = target_dir / f"{sanitized_name}_overview.txt"
    overview_text = overview_agent.summarize_procedure(domain_mapped_proc)
    operations_section = _format_operations_summary(
        domain_mapped_proc.get("table_operations", {}),
        domain_mapped_proc.get("table_operation_columns", {}),
    )
    if operations_section:
        overview_text = f"{overview_text}\n\nCRUD Summary:\n{operations_section}"
    overview_path.write_text(overview_text, encoding="utf-8")
    logger.info("Stored procedure overview written to %s", overview_path)
    return overview_path


def _format_operations_summary(
    table_operations: Dict[str, List[str]],
    table_operation_columns: Dict[str, Dict[str, List[str]]],
) -> str:
    if not table_operations:
        return ""
    lines = []
    for table in sorted(table_operations.keys()):
        ops = table_operations.get(table, [])
        if not ops:
            continue
        lines.append(f"- {table}:")
        for op in ops:
            columns = table_operation_columns.get(table, {}).get(op, [])
            column_text = ", ".join(columns) if columns else "(all columns)"
            lines.append(f"  • {op.upper()}: {column_text}")
    return "\n".join(lines)


def run_storeproc_parse_mapper(
    proc_path: Path,
    mapping_path: Path,
    output_dir: Path | None = None,
) -> Tuple[Dict[str, Any], Path | None]:
    sql_text = read_file(proc_path)
    domain_mapping = load_domain_mapping(mapping_path)
    parsed = parse_store_procedure(sql_text)
    logger.info("Parsed stored procedure with %d tables", len(parsed.get("tables", [])))
    mapped = map_domains(parsed, domain_mapping)
    overview_path = create_storeproc_overview(mapped, output_dir)
    mapped["overview_path"] = overview_path
    return mapped, overview_path
