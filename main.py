from __future__ import annotations

import logging
from pathlib import Path

from settings import PROJECT_SETTINGS
from common.tools.tools import load_workflow_module

llm_module = load_workflow_module("workflow_1", "llm")
parse_module = load_workflow_module("workflow_2", "storeproc_parse_mapper")
graph_module = load_workflow_module("workflow_3", "storeproc_graph")
viewer_module = load_workflow_module("workflow_3", "storeproc_viewer")
domain_design_module = load_workflow_module("workflow_3", "domian_Service_Design")
architecture_module = load_workflow_module("workflow_3", "service_architecture")
generator_module = load_workflow_module("workflow_4", "code_generator")
compiler_module = load_workflow_module("workflow_4", "complier")
context_module = load_workflow_module("workflow_4", "service_context_creator")

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG if PROJECT_SETTINGS.get("debug") else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    llm_client = llm_module.create_llm_client()
    if not llm_module.check_connection(llm_client):
        raise RuntimeError("LLM connection could not be verified.")
    logger.info("Workflow 1 completed.")

    input_dir = Path(PROJECT_SETTINGS.get("input_dir", "."))
    output_root = Path(PROJECT_SETTINGS.get("output_dir", "output"))
    request_id = PROJECT_SETTINGS.get("request_id")
    request_dir = input_dir / request_id if request_id else input_dir
    request_output_dir = output_root / request_id if request_id else output_root
    artifacts_dir = request_output_dir / PROJECT_SETTINGS.get("artifacts_subdir", "artifacts")
    services_dir = request_output_dir / PROJECT_SETTINGS.get("services_subdir", "services")
    output_root.mkdir(parents=True, exist_ok=True)
    request_output_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    services_dir.mkdir(parents=True, exist_ok=True)
    proc_path = request_dir / PROJECT_SETTINGS.get("stored_procedure_filename", "storeproc.sql")
    mapping_path = request_dir / PROJECT_SETTINGS.get("domain_mapping_filename", "domain_mapper.json")

    logger.debug("Parsing stored procedure from %s with mapping %s", proc_path, mapping_path)
    domain_mapped_proc, overview_path = parse_module.run_storeproc_parse_mapper(proc_path, mapping_path, artifacts_dir)
    logger.info("Workflow 2 completed.")

    logger.debug("Designing domain services")
    domain_services = domain_design_module.run_domain_service_design(domain_mapped_proc)
    logger.debug("Domain services planned: %s", domain_services)
    graph_artifacts = graph_module.run_storeproc_graph(domain_services, domain_mapped_proc, artifacts_dir)
    mermaid_artifacts = viewer_module.run_storeproc_viewer(domain_services, domain_mapped_proc, artifacts_dir)
    logger.info("Workflow 3 graphing completed.")

    service_architecture = architecture_module.run_service_architecture(domain_services, domain_mapped_proc)
    logger.debug("Service architecture defined: %s", service_architecture)
    generated_paths = generator_module.run_code_generator(service_architecture, output_root=services_dir)
    context_paths = context_module.run_service_context_creator(
        service_architecture,
        domain_services,
        domain_mapped_proc,
        output_root=services_dir,
    )
    logger.info("Workflow 4 code generation completed.")
    compiler_summary = compiler_module.run_compiler(generated_paths + context_paths)
    logger.info("Workflow 4 compilation completed.")

    print(f"Graph stored at: {graph_artifacts['json']}")
    print(f"GraphML stored at: {graph_artifacts['graphml']}")
    if "graphdb" in graph_artifacts:
        print(f"Graph DB updated at: {graph_artifacts['graphdb']}")
    if overview_path:
        print(f"Stored procedure overview stored at: {overview_path}")
    print(f"Mermaid diagram stored at: {mermaid_artifacts['mermaid']}")
    if mermaid_artifacts.get("png"):
        print(f"Mermaid PNG stored at: {mermaid_artifacts['png']}")
    print(f"Generated artifacts: {len(generated_paths)}")
    print(f"Service context files created: {len(context_paths)}")
    print(f"Compiler summary: {compiler_summary}")


if __name__ == "__main__":
    main()
