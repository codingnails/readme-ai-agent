from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
import os
from dotenv import load_dotenv

load_dotenv()

with open("app/prompts/overview_prompt.txt", "r") as f:
    overview_template = f.read()

prompt = PromptTemplate(
    input_variables=["repo_name", "code_entities"],
    template=overview_template,
)

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))

overview_chain = RunnableSequence(prompt | llm)

def overview_readme(repo_name: str, code_entities: str) -> str:
    result = overview_chain.invoke({"repo_name": repo_name, "code_entities": code_entities})
    return result.content
