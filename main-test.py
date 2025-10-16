from __future__ import annotations

import sys
from pathlib import Path

from settings import PROJECT_SETTINGS
from common.tools.tools import load_workflow_module


def main() -> None:
    llm_module = load_workflow_module("workflow_1", "llm")
    parse_module = load_workflow_module("workflow_2", "storeproc_parse_mapper")
    domain_design_module = load_workflow_module("workflow_3", "domian_Service_Design")
    graph_module = load_workflow_module("workflow_3", "storeproc_graph")
    viewer_module = load_workflow_module("workflow_3", "storeproc_viewer")
    architecture_module = load_workflow_module("workflow_3", "service_architecture")
    generator_module = load_workflow_module("workflow_4", "code_generator")
    context_module = load_workflow_module("workflow_4", "service_context_creator")
    compiler_module = load_workflow_module("workflow_4", "complier")

    client = llm_module.create_llm_client()
    input_dir = Path(PROJECT_SETTINGS.get("input_dir", "input"))
    request_id = PROJECT_SETTINGS.get("request_id")
    request_dir = input_dir / request_id if request_id else input_dir
    output_root = Path(PROJECT_SETTINGS.get("output_dir", "output"))
    request_output_dir = output_root / request_id if request_id else output_root
    artifacts_dir = request_output_dir / PROJECT_SETTINGS.get("artifacts_subdir", "artifacts")
    services_dir = request_output_dir / PROJECT_SETTINGS.get("services_subdir", "services")
    output_root.mkdir(parents=True, exist_ok=True)
    request_output_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    services_dir.mkdir(parents=True, exist_ok=True)
    proc_path = request_dir / PROJECT_SETTINGS.get("stored_procedure_filename", "storeproc.sql")
    mapping_path = request_dir / PROJECT_SETTINGS.get("domain_mapping_filename", "domain_mapper.json")

    stored_proc_text = proc_path.read_text(encoding="utf-8")
    try:
        llm_response = client.chat(
            [
                {"role": "system", "content": "You are a helpful architect who summarises stored procedures."},
                {"role": "user", "content": f"Summarise this stored procedure:\n{stored_proc_text}"},
            ],
            max_tokens=200,
            purpose="stored-proc-summary",
        )
    except RuntimeError as exc:
        print(f"LLM summary call failed: {exc}")
        llm_response = {"error": str(exc)}
        summary = ""
    else:
        summary = ""
        choices = llm_response.get("choices")
        if choices:
            summary = choices[0].get("message", {}).get("content", "") or ""
    print("LLM summary:")
    printable_summary = summary.strip()
    if printable_summary:
        encoding = sys.stdout.encoding or "utf-8"
        safe_summary = printable_summary.encode(encoding, errors="ignore").decode(encoding, errors="ignore")
        print(safe_summary)
    else:
        print(llm_response)

    domain_mapped_proc, overview_path = parse_module.run_storeproc_parse_mapper(proc_path, mapping_path, artifacts_dir)
    domain_services = domain_design_module.run_domain_service_design(domain_mapped_proc)
    graph_artifacts = graph_module.run_storeproc_graph(domain_services, domain_mapped_proc, artifacts_dir)
    mermaid_artifacts = viewer_module.run_storeproc_viewer(domain_services, domain_mapped_proc, artifacts_dir)
    service_architecture = architecture_module.run_service_architecture(domain_services, domain_mapped_proc)
    generated_paths = generator_module.run_code_generator(service_architecture, output_root=services_dir)
    context_paths = context_module.run_service_context_creator(
        service_architecture,
        domain_services,
        domain_mapped_proc,
        output_root=services_dir,
    )
    compiler_summary = compiler_module.run_compiler(generated_paths + context_paths)

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
