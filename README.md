# Store Procedure Microservice Designer

## Overview
This project orchestrates multiple workflows to analyse stored procedures, map database tables to domains, generate knowledge graphs, design Spring Boot microservices, and scaffold service code artefacts. The design emphasises modular workflows backed by configurable LLM-powered agents.

## Project Structure
- `workflow_1/`: LLM connectivity and agent bootstrap code.
- `workflow_2/`: Stored procedure parsing, domain mapping, graph generation, and Mermaid rendering.
- `workflow_3/`: Domain-driven service design, architecture planning, and artefact generation.
- `workflow_4/`: Code generation, service context artifacts, and placeholder compiler pipeline.
- `common/tools/`: Shared utility helpers.
- `common/prompts/`: Prompt templates used by the code generator.
- `common/graphdb/`: Aggregated knowledge graph store shared across requests.
- `input/<request_id>/`: Stored procedure and domain mapping inputs.
- `output/<request_id>/`: Generated artefacts, knowledge-graph exports, and service scaffolds.
- `settings.py`: Global configuration.
- `main.py`: Sequential workflow runner.

## Prerequisites
- Python 3.11 or later.
- Optional: Java 21 and Maven (required once code generation is extended to real builds).

## Installation
```bash
python -m venv .venv
. .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -U pip
```
Install any additional dependencies required by future extensions (none are required for the current scaffolding).

## Configuration
Edit `settings.py` to point to the desired stored procedure file, domain mapping JSON, prompt directory, and output locations. Configure the active `request_id` to switch between subfolders inside `input/`. LLM connection details are also stored here for convenience.

## Usage
```bash
python main.py
```
The runner will:
1. Verify the LLM configuration.
2. Parse the stored procedure and apply domain mappings.
3. Persist JSON, GraphML, and Mermaid graph representations inside `output/<request_id>/artifacts/`.
4. Produce service design JSON, generate placeholder Spring skeleton files, and emit per-service README/context metadata under `output/<request_id>/services/`.
5. Update the shared graph database snapshot inside `common/graphdb/`.
6. Execute a stub compiler workflow and report generated artefact counts.

## Next Steps
- Implement real LLM chat calls inside `workflow_1/llm.py`.
- Replace placeholder parsing with a SQL-aware parser.
- Extend the code generator to create full Spring Boot projects per service definition.
- Wire the compiler stage to invoke Maven or Gradle builds for each generated service.
