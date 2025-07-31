from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
import os
from dotenv import load_dotenv

load_dotenv()

with open("app/prompts/refine_prompt.txt", "r") as f:
    refine_template = f.read()

refine_prompt = PromptTemplate(
    input_variables=["draft_text", "previous_readme", "review_report"],
    template=refine_template,
)

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))

refine_chain = RunnableSequence(refine_prompt | llm)

def refine_readme(draft_text: str, previous_readme: str, review_report: str) -> str:
    result = refine_chain.invoke({"draft_text": draft_text, "previous_readme": previous_readme, "review_report": review_report})
    return result.content
