from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import os, requests, json
from fastapi import FastAPI

app = FastAPI()

load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

class AutheniticityChecker(BaseModel):
    is_authentic: bool
    authenticity_score: float
    content: str
    source: List[str]

class UserQuery(BaseModel):
    question: str



prompt = """You are an AI-powered fact-checker specializing in verifying the authenticity of news and claims. Your task is to evaluate the credibility of the given query based on available knowledge, reasoning, and supporting evidence.  

**Output a JSON object with the following fields:** 
[IMPORTANT] Do not include `"json"` at the beginning of the response. 
- **is_authentic** (bool): Whether the claim appears to be true or misleading.  
- **authenticity_score** (float): A confidence score from 1.0 to 10.0, where 10.0 means fully verified.  
- **reasoning** (str): A concise explanation supporting the score, highlighting key evidence or inconsistencies.  
- **sources** (List[str]): A list of up to {k} credible sources that verify or refute the claim.  

**Guidelines:**  
- Base your response on logical reasoning and verifiable information.  
- If no reliable data is available, state the uncertainty in the reasoning.    

# Query: {user_query}"""


# user_query = "Did DC defeated RCB in WPL?"

def validate_news(question: str) -> str:
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {PERPLEXITY_API_KEY}"}
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": prompt.format(user_query=question, k=3)},
            {"role": "user", "content": question},
        ],
        "response_format": {
                "type": "json_schema",
            "json_schema": {"schema": AutheniticityChecker.model_json_schema()},
        }
    }
    response = requests.post(url, headers=headers, json=payload).json()
    content = response["choices"][0]["message"]["content"]
    print(content, type(content))
    # json_content = json.loads(content)
    # print(json_content)
    return content


@app.post("/news-check")
def check_authenticity(news: UserQuery):
    query=news.question
    answer=validate_news(query)
    return {"query": query, "answer": answer}


@app.get("/")
def read_root():
    return {"Hello": "World"}




