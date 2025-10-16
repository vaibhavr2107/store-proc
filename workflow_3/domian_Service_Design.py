from __future__ import annotations

import logging
from typing import Any, Dict, List, Sequence, Set

from common.tools.tools import load_workflow_module

agents_module = load_workflow_module("workflow_1", "agents")
DomainDesignAgent = agents_module.DomainDesignAgent
bootstrap_agents = agents_module.bootstrap_agents

logger = logging.getLogger(__name__)


def design_domain_services(domain_mapped_proc: Dict[str, Any], agent: DomainDesignAgent) -> Dict[str, Any]:
    services = []
    domains = domain_mapped_proc.get("domains", {})
    table_domains = domain_mapped_proc.get("table_domains", {})
    for domain, tables in domains.items():
        logger.debug("Calling DomainDesignAgent for domain=%s", domain)
        plan = agent.plan_domain_services(domain, tables)
        plan["dependencies"] = _derive_dependencies(domain, tables, table_domains)
        services.append(plan)
    logger.info("Planned %d domain services", len(services))
    return {"services": services}


def _derive_dependencies(domain: str, tables: Sequence[str], table_domains: Dict[str, List[str]]) -> List[str]:
    dependencies: Set[str] = set()
    for table in tables:
        peers = table_domains.get(table, [])
        for peer in peers:
            if peer != domain:
                dependencies.add(peer)
    return sorted(dependencies)


def run_domain_service_design(domain_mapped_proc: Dict[str, Any]) -> Dict[str, Any]:
    agents = bootstrap_agents()
    domain_agent: DomainDesignAgent = agents["domain_design"]
    result = design_domain_services(domain_mapped_proc, domain_agent)
    logger.debug("Domain service design output: %s", result)
    return result
