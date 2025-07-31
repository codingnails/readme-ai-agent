from langgraph.graph import StateGraph
from app.agents.tools import overview_tool, refine_tool, review_tool

class ReadmeState(dict):
    repo_name: str
    code_entities: str
    draft: str
    refined: str
    review: str
    iteration: int

def generate_draft(state):
    print("Calling overview_tool")
    # overview_tool expects a dict with repo_summary keys
    repo_summary_dict = {
        "repo_summary": {
            "repo_name": state["repo_name"],
            "code_entities": state["code_entities"],
        }
    }
    state["draft"] = overview_tool.invoke(repo_summary_dict)
    return state

def refine_draft(state):
    print("Calling refine_tool")
    tool_input = {
        "draft_text": state["draft"],
        "previous_readme": state.get("refined", ""),
        "review_report": state.get("review", "")
    }
    state["refined"] = refine_tool.invoke(tool_input)
    return state

def review_draft(state):
    state["iteration"] += 1
    print("Calling review_tool")
    tool_input = {
        "draft_text": state["draft"],
        "refined_text": state["refined"]
    }
    review_output = review_tool.invoke(tool_input)
    if isinstance(review_output, tuple) and len(review_output) > 0:
        state["review"] = review_output[0]
        state["quality_score"] = review_output[1]
    else:
        state["review"] = str(review_output)
        state["quality_score"] = 0
    return state

def check_quality(state):
    print(f"\n--- check_quality called ---")
    print(f"Current iteration at start of check: {state['iteration']}")
    print(f"Content of state['review'] (first 100 chars): {state['review'][:100]}...")

    review_condition_met = "No issues found" in state["review"]
    iteration_limit_met = state["iteration"] >= 3

    if review_condition_met or iteration_limit_met:
        return "done"
    
    state["draft"] = state["refined"]
    return "refine"


builder = StateGraph(ReadmeState)
builder.add_node("draft", generate_draft)
builder.add_node("refine", refine_draft)
builder.add_node("review", review_draft)
builder.set_entry_point("draft")
builder.add_edge("draft", "refine")
builder.add_edge("refine", "review")
builder.add_conditional_edges("review", check_quality, {"done": "__end__", "refine": "refine"})

graph = builder.compile()

def run_readme_agent(repo_summary):
    initial_state = ReadmeState(
        repo_name=repo_summary.repo_name,
        code_entities="\n".join([f"{fn.name}" for fn in repo_summary.functions]),
        draft="",
        refined="",
        review="",
        iteration=0
    )
    final_state = graph.invoke(initial_state)
    return final_state["refined"], final_state["review"]
