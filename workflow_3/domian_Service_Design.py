from __future__ import annotations

import logging
from typing import Any, Dict, List, Set

from common.tools.tools import load_workflow_module

agents_module = load_workflow_module("workflow_1", "agents")
DomainDesignAgent = agents_module.DomainDesignAgent
bootstrap_agents = agents_module.bootstrap_agents

logger = logging.getLogger(__name__)


def design_domain_services(domain_mapped_proc: Dict[str, Any], agent: DomainDesignAgent) -> Dict[str, Any]:
    domains = domain_mapped_proc.get("domains", {})
    table_domains = domain_mapped_proc.get("table_domains", {})
    table_dependencies = domain_mapped_proc.get("table_dependencies", {})
    tables_in_proc = set(domain_mapped_proc.get("tables", []))

    domain_usage: Dict[str, List[str]] = {}
    for domain, configured_tables in domains.items():
        used_tables = sorted(
            {
                table
                for table in tables_in_proc
                if domain in table_domains.get(table, [])
            }
        )
        if used_tables:
            domain_usage[domain] = used_tables

    services = []
    for domain, owned_tables in domain_usage.items():
        logger.debug("Calling DomainDesignAgent for domain=%s", domain)
        plan = agent.plan_domain_services(domain, owned_tables)
        plan["dependencies"] = _derive_dependencies(domain, owned_tables, table_domains, table_dependencies)
        services.append(plan)
    logger.info("Planned %d domain services", len(services))
    return {"services": services}


def _derive_dependencies(
    domain: str,
    owned_tables: List[str],
    table_domains: Dict[str, List[str]],
    table_dependencies: Dict[str, List[str]],
) -> List[str]:
    dependencies: Set[str] = set()
    for table in owned_tables:
        for dependent_table in table_dependencies.get(table, []):
            for dependent_domain in table_domains.get(dependent_table, []):
                if dependent_domain != domain:
                    dependencies.add(dependent_domain)
    return sorted(dependencies)


def run_domain_service_design(domain_mapped_proc: Dict[str, Any]) -> Dict[str, Any]:
    agents = bootstrap_agents()
    domain_agent: DomainDesignAgent = agents["domain_design"]
    result = design_domain_services(domain_mapped_proc, domain_agent)
    logger.debug("Domain service design output: %s", result)
    return result
