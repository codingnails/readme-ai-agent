from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
import os
from dotenv import load_dotenv

load_dotenv()

with open("app/prompts/review_prompt.txt", "r") as f:
    review_template = f.read()

prompt = PromptTemplate(
    input_variables=["draft_text", "refined_text"],
    template=review_template,
)

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))

review_chain = RunnableSequence(prompt | llm)

def review_readme(draft_text: str, refined_text: str) -> str:
    result = review_chain.invoke({"draft_text": draft_text, "refined_text": refined_text})
    return result.content
