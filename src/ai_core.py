"""
Core AI Logic and Prompt Engineering: Core AI functionality for the code refactoring agent,
including data models for AI responses and parsers for structured output.

"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI

def _load_env_with_fallbacks() -> None:
    # Try to load .env file with different encodings
    possible_encodings = [
        "utf-8",
        "utf-8-sig",
        "utf-16",
        "utf-16-le",
        "utf-16-be",
    ]

    for encoding in possible_encodings:
        try:
            if load_dotenv(encoding=encoding):
                break
        except UnicodeDecodeError:
            continue
    
    # If .env file fails, try to set the API key directly
    if not os.getenv("GOOGLE_API_KEY"):
        # Set the API key directly as a fallback
        os.environ["GOOGLE_API_KEY"] = "AIzaSyCafEqqkbhJH1N1BhFwV0vOTuzwijbsNrM"


_load_env_with_fallbacks()

def _ensure_google_api_key_from_gemini() -> None:
    if not os.getenv("GOOGLE_API_KEY") and os.getenv("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


_ensure_google_api_key_from_gemini()

class RefactoringResponse(BaseModel):
    """
    Defines the expected data structure of the LLM's JSON response.
    """
    refactored_code: str = Field(
        description="The complete, refactored Python code as a single string."
    )
    explanation: str = Field(
        description="A multi-line string explaining the key changes made and the principles behind them."
    )


def create_response_parser() -> PydanticOutputParser:
    """
    Create and configure a PydanticOutputParser for RefactoringResponse.
    
    creates a parser that can automatically validate and parse
    the LLM's JSON response into a structured RefactoringResponse object.

    Returns:
        PydanticOutputParser: A configured parser for RefactoringResponse objects
    """
    return PydanticOutputParser(pydantic_object=RefactoringResponse)


def create_refactoring_prompt_template() -> PromptTemplate:
    """
    Create and configure a PromptTemplate for code refactoring tasks.
    """
    template = """
You are an expert software architect specializing in Python code quality.
Your task is to refactor a given code snippet based on a list of identified code smells and a primary refactoring goal.

Primary Goal: {refactoring_goal}

Identified Code Smells in JSON format:
{issues_json}

Original Code Snippet:
```python
{code_snippet}
```

Instructions:
1. Analyze the original code and the provided code smells.
2. Refactor the code to address the issues and align with the primary goal. The refactored code must be syntactically correct Python.
3. Provide a clear, step-by-step explanation of the changes made, linking them to software design principles where applicable.
4. Your final output MUST be a single, valid JSON object. Do not add any text, notes, or explanations outside of the JSON structure.

The JSON object must follow this exact schema: {{ "refactored_code": "The complete, refactored Python code as a single string.", "explanation": "A multi-line string explaining the key changes made and the principles behind them." }}
"""
    
    return PromptTemplate(
        template=template,
        input_variables=["refactoring_goal", "issues_json", "code_snippet"]
    )


def configure_llm_service() -> ChatGoogleGenerativeAI:
    """
    Create and configure a ChatGoogleGenerativeAI instance for code refactoring.
    """
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please check your .env file.")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )


def create_refactoring_chain() -> Runnable:
    """
    Create and configure the complete refactoring chain using LangChain Expression Language.
    
    The chain flow: PromptTemplate -> ChatGoogleGenerativeAI -> PydanticOutputParser
    
    """
    prompt_template = create_refactoring_prompt_template()
    llm_service = configure_llm_service()
    response_parser = create_response_parser()
    
    chain = prompt_template | llm_service | response_parser
    
    return chain


def invoke_refactoring_chain(chain: Runnable, input_data: dict) -> RefactoringResponse:
    """
    Execute the refactoring chain with input data and return the parsed result.
    """
    result = chain.invoke(input_data)
    
    return result
