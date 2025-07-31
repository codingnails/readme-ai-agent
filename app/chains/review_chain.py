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

def calculate_quality_score(review_content: str) -> float:
    """
    Calculate a quality score based on the review content.
    Returns 1.0 if the review indicates high quality, 0.0 otherwise.
    """
    # Check for explicit quality indicators
    if any(word in review_content.lower() for word in ["excellent", "perfect", "no issues"]):
        return 1.0
    
    # Check for negative indicators
    if any(word in review_content.lower() for word in ["issues", "problems", "improvements needed"]):
        return 0.0
    
    # Default to 0.5 if no clear indicators are found
    return 0.5

def review_readme(draft_text: str, refined_text: str) -> str:
    result = review_chain.invoke({"draft_text": draft_text, "refined_text": refined_text})
    content = result.content
    quality_score = calculate_quality_score(content)
    return content, quality_score
