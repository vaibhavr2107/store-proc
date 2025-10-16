from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Set

from common.tools.tools import load_workflow_module

logger = logging.getLogger(__name__)

llm_module = load_workflow_module("workflow_1", "llm")
LLMClient = llm_module.LLMClient
create_llm_client = llm_module.create_llm_client


@dataclass
class AgentContext:
    llm: LLMClient


class DomainDesignAgent:
    def __init__(self, context: AgentContext):
        self.context = context

    def plan_domain_services(self, domain_name: str, tables: List[str]) -> Dict[str, Any]:
        logger.debug("DomainDesignAgent LLM request: domain=%s tables=%s", domain_name, tables)
        return {
            "domain": domain_name,
            "service_name": f"{domain_name.title().replace(' ', '')}Service",
            "owned_tables": tables,
        }


class ArchitectAgent:
    def __init__(self, context: AgentContext):
        self.context = context

    def design_service(self, service_name: str, dependencies: List[str]) -> Dict[str, Any]:
        logger.debug(
            "ArchitectAgent LLM request: service=%s dependencies=%s",
            service_name,
            dependencies,
        )
        modules = ["api", "application", "domain", "infrastructure"]
        files = [
            {"path": "pom.xml", "template": "pom.xml.txt"},
            {"path": "src/main/resources/application.yaml", "template": "application.yaml.txt"},
            {"path": "src/main/resources/openapi/openapi-spec.yml", "template": "openapi_spec.yml.txt"},
        ]
        return {
            "service_name": service_name,
            "dependencies": dependencies,
            "modules": modules,
            "files": files,
        }


class CodeGeneratorAgent:
    def __init__(self, context: AgentContext):
        self.context = context

    def prepare_generation_payload(self, service_spec: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug("CodeGeneratorAgent LLM request: service=%s", service_spec.get("service_name"))
        return {"service": service_spec}


class ServiceContextAgent:
    def __init__(self, context: AgentContext):
        self.context = context

    def describe_service(self, service_spec: Dict[str, Any]) -> Dict[str, str]:
        owned_tables = ", ".join(service_spec.get("owned_tables", []))
        dependencies = ", ".join(service_spec.get("dependencies", []))
        service_name = service_spec.get("service_name", "")
        domain_name = service_spec.get("domain", "")
        one_liner = (
            f"{service_name} coordinates {domain_name} domain responsibilities "
            f"across tables {owned_tables or 'none'}."
        )
        table_details = "\n".join(f"- {table}" for table in service_spec.get("owned_tables", [])) or "No tables assigned"
        return {
            "service_description": one_liner,
            "table_details": table_details,
            "dependency_summary": dependencies or "No dependencies",
            "one_liner": one_liner,
        }


class StoreProcOverviewAgent:
    def __init__(self, context: AgentContext):
        self.context = context

    def summarize_procedure(self, domain_mapped_proc: Dict[str, Any]) -> str:
        procedure_name = domain_mapped_proc.get("procedure_name", "procedure")
        tables = ", ".join(domain_mapped_proc.get("tables", []))
        domain_lines = []
        for domain, table_list in domain_mapped_proc.get("domains", {}).items():
            domain_lines.append(f"- {domain}: {', '.join(table_list)}")
        domain_section = "\n".join(domain_lines) or "No domain mappings found."

        flow_lines = []
        for step in domain_mapped_proc.get("procedure_steps", []):
            descriptions = step.get("description", [])
            if not descriptions:
                continue
            flow_lines.append(f"- {' '.join(descriptions)}")
        flow_section = "\n".join(flow_lines) or "No explicit join flow detected."

        dependencies = _derive_domain_dependencies(
            domain_mapped_proc.get("table_domains", {}),
            domain_mapped_proc.get("table_dependencies", {}),
        )
        dependency_lines = []
        for domain, dep_map in dependencies.items():
            if not dep_map:
                continue
            for dep_domain, table_pairs in dep_map.items():
                tables_text = ", ".join(sorted(table_pairs))
                dependency_lines.append(f"- {domain} depends on {dep_domain} via {tables_text}")
        dependency_section = "\n".join(dependency_lines) or "No inter-domain dependencies identified."

        alias_map = domain_mapped_proc.get("alias_map", {})
        alias_lines = [f"- {alias} -> {table}" for alias, table in alias_map.items()]
        alias_section = "\n".join(alias_lines) or "No table aliases detected."

        overview = [
            f"Procedure: {procedure_name}",
            "",
            "Summary:",
            f"The stored procedure orchestrates data retrieval across tables: {tables or 'none'}.",
            "",
            "Domain Mapping:",
            domain_section,
            "",
            "Procedure Flow:",
            flow_section,
            "",
            "Inter-Domain Dependencies:",
            dependency_section,
            "",
            "Table Aliases:",
            alias_section,
        ]
        return "\n".join(overview)


def _derive_domain_dependencies(
    table_domains: Dict[str, List[str]],
    table_dependencies: Dict[str, List[str]],
) -> Dict[str, Dict[str, Set[str]]]:
    domain_dependencies: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))
    for source_table, dependent_tables in table_dependencies.items():
        source_domains = table_domains.get(source_table, [])
        if not source_domains:
            continue
        for dependent_table in dependent_tables:
            target_domains = table_domains.get(dependent_table, [])
            if not target_domains:
                continue
            for source_domain in source_domains:
                for target_domain in target_domains:
                    if source_domain == target_domain:
                        continue
                    domain_dependencies[source_domain][target_domain].add(f"{source_table}->{dependent_table}")
    # convert to plain dicts
    converted: Dict[str, Dict[str, Set[str]]] = {}
    for domain, dep_map in domain_dependencies.items():
        converted[domain] = {other: set(values) for other, values in dep_map.items()}
    return converted


def bootstrap_agents() -> Dict[str, Any]:
    client = create_llm_client()
    context = AgentContext(llm=client)
    logger.info("Bootstrapping agents with shared LLM context (model=%s)", client.config.model)
    return {
        "domain_design": DomainDesignAgent(context),
        "architect": ArchitectAgent(context),
        "code_generator": CodeGeneratorAgent(context),
        "service_context": ServiceContextAgent(context),
        "storeproc_overview": StoreProcOverviewAgent(context),
    }
