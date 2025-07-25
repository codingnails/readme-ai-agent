# README Generator Project Plan

## Project Overview
Build a hybrid multi-agent system to automatically generate professional README files for code repositories. The system combines static code analysis with AI-powered summarization and generation to produce accurate, human-friendly documentation.

---

## Pydantic Integration
- Defines **structured models** (e.g., `FunctionInfo`, `ClassInfo`, `ModuleInfo`, `RepoSummary`) for code data.
- Ensures **type-safe communication** between agents and validates extracted JSON.
- Simplifies debugging and future API exposure (FastAPI-ready).

---

## MCP Integration (Future)
- Standardizes how agents interact with **external tools and APIs**:
  - File system access
  - Baseten-hosted inference endpoints
  - Hugging Face models
- Makes architecture **model-agnostic** and easier to expand to new agents.

---

## Agents

| Agent Name          | Type       | Function                                      |
|---------------------|------------|-----------------------------------------------|
| Repo Fetcher        | Non-AI     | Clone or download repo, gather file metadata  |
| Code Extractor      | Non-AI     | Parse source files to extract functions, classes, docstrings, and dependencies |
| Semantic Extractor  | AI-powered | Summarize extracted code data into meaningful descriptions |
| README Generator    | AI-powered | Generate formatted README markdown from semantic summaries |
| Review & Refine     | AI-powered (optional) | Review and improve README content for clarity and completeness |
| Orchestrator        | Non-AI     | Manage data flow and coordination between agents |

---

## Project Phases

### Phase 1: Repo Fetching & Static Code Extraction
- Implement Repo Fetcher and Code Extractor agents.
- Extract structured code info (functions, classes, docstrings) using Python's `ast`.
- Validate extracted data with Pydantic and output JSON summaries.

### Phase 2: Semantic Extraction with AI
- Develop Semantic Extractor to generate human-readable summaries using GPT, Claude, or Hugging Face models.
- Design effective prompts and handle API integration.

### Phase 3: README Generation
- Build README Generator agent to create complete README markdown files from summaries.
- Include sections like Overview, Installation, Usage, Contribution, License.

### Phase 4: Orchestration & Review
- Create Orchestrator agent for pipeline management and future MCP integration.
- (Optional) Add Review & Refine agent to improve README quality.
- Add error handling, logging, and usability improvements.

---

## Additional Notes
- Start with Python codebases; extend language support later.
- Use modular design with **clear input/output formats (Pydantic models + JSON)**.
- Prioritize MVP in early phases; iterate for improvements.
- Open-source the project for community feedback and contributions.

---

*End of Plan*
