"""
Core AI Logic and Prompt Engineering

This module provides the core AI functionality for the code refactoring agent,
including data models for AI responses and parsers for structured output.

Author: CognitCode
"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI

def _load_env_with_fallbacks() -> None:
    """
    Attempt to load environment variables from a .env file using several
    possible encodings to avoid UnicodeDecodeError when the file is saved
    with a BOM or UTF-16.

    This function is intentionally silent on failure, since the application
    can also rely on process-level environment variables.
    """
    possible_encodings = [
        "utf-8",
        "utf-8-sig",
        "utf-16",
        "utf-16-le",
        "utf-16-be",
    ]

    for encoding in possible_encodings:
        try:
            # Returns True if a .env file was found and loaded
            if load_dotenv(encoding=encoding):
                break
        except UnicodeDecodeError:
            # Try the next encoding
            continue


# Load environment variables at import time with safe fallbacks.
_load_env_with_fallbacks()

def _ensure_google_api_key_from_gemini() -> None:
    """
    Ensure `GOOGLE_API_KEY` is available by falling back to `GEMINI_API_KEY`.

    Some environments or docs use `GEMINI_API_KEY` while the Google SDKs expect
    `GOOGLE_API_KEY`. This helper bridges that gap to prevent runtime failures
    when configuring the LLM client.
    """
    # If GOOGLE_API_KEY is not set but GEMINI_API_KEY is, mirror the value
    if not os.getenv("GOOGLE_API_KEY") and os.getenv("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


# Apply env key fallback after attempting to load .env
_ensure_google_api_key_from_gemini()

class RefactoringResponse(BaseModel):
    """
    Defines the expected data structure of the LLM's JSON response.
    
    This model represents the structured output that the AI will generate
    when refactoring code, containing both the refactored code and an
    explanation of the changes made.
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
    
    This function creates a parser that can automatically validate and parse
    the LLM's JSON response into a structured RefactoringResponse object.
    The parser ensures that the AI's output conforms to the expected schema
    and provides type safety for the rest of the application.
    
    Returns:
        PydanticOutputParser: A configured parser for RefactoringResponse objects
        
    Example:
        >>> parser = create_response_parser()
        >>> # The parser can be used in LangChain chains to automatically
        >>> # parse and validate LLM responses
    """
    return PydanticOutputParser(pydantic_object=RefactoringResponse)


def create_refactoring_prompt_template() -> PromptTemplate:
    """
    Create and configure a PromptTemplate for code refactoring tasks.
    
    This function creates a structured prompt template that will be sent to the
    language model for code refactoring. The template includes placeholders for
    the refactoring goal, identified code smells, and the original code snippet.
    
    Returns:
        PromptTemplate: A configured prompt template for refactoring tasks
        
    Example:
        >>> template = create_refactoring_prompt_template()
        >>> # The template can be used with LangChain chains to format prompts
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
    
    This function creates a configured instance of the Google Gemini model
    specifically optimized for code refactoring tasks. The configuration uses
    the gemini-1.5-flash model with deterministic output (temperature=0) to ensure
    consistent and reliable refactoring suggestions.
    
    The function relies on the GOOGLE_API_KEY environment variable for authentication.
    
    Returns:
        ChatGoogleGenerativeAI: A configured instance ready for use in LangChain.
        
    Raises:
        ValueError: If the GOOGLE_API_KEY environment variable is not set.
    
    Example:
        >>> # Ensure your .env file has GOOGLE_API_KEY="your-api-key"
        >>> llm = configure_llm_service()
        >>> # The LLM can now be used in LangChain chains.
    """
    # The ChatGoogleGenerativeAI class automatically looks for this env variable.
    # This check provides a more user-friendly error message.
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please check your .env file.")
    
    # The API key is passed implicitly from the environment.
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )


def create_refactoring_chain() -> Runnable:
    """
    Create and configure the complete refactoring chain using LangChain Expression Language.
    
    This function orchestrates all the AI components into a single, executable chain.
    It creates instances of the prompt template, LLM service, and response parser,
    then connects them using the LCEL pipe operator to form a complete workflow.
    
    The chain flow: PromptTemplate -> ChatGoogleGenerativeAI -> PydanticOutputParser
    
    Returns:
        Runnable: A complete, executable chain ready for processing refactoring requests
        
    Example:
        >>> chain = create_refactoring_chain()
        >>> # The chain can be invoked with input data to get refactoring results
    """
    # Create instances of all components
    prompt_template = create_refactoring_prompt_template()
    llm_service = configure_llm_service()
    response_parser = create_response_parser()
    
    # Construct the complete chain using LCEL pipe operator
    chain = prompt_template | llm_service | response_parser
    
    return chain


def invoke_refactoring_chain(chain: Runnable, input_data: dict) -> RefactoringResponse:
    """
    Execute the refactoring chain with input data and return the parsed result.
    
    This function takes a configured chain and input data dictionary, invokes
    the chain to process the refactoring request, and returns the final
    structured RefactoringResponse object.
    
    Args:
        chain (Runnable): The configured refactoring chain
        input_data (dict): Dictionary containing:
            - "refactoring_goal": The primary refactoring objective
            - "issues_json": JSON string of identified code smells
            - "code_snippet": The original Python code to refactor
    
    Returns:
        RefactoringResponse: The parsed and validated refactoring result
        
    Example:
        >>> chain = create_refactoring_chain()
        >>> input_data = {
        ...     "refactoring_goal": "Improve Readability",
        ...     "issues_json": "[{\"line_number\": 5, \"issue_code\": \"FUNC_TOO_LONG\"}]",
        ...     "code_snippet": "def long_function(): pass"
        ... }
        >>> result = invoke_refactoring_chain(chain, input_data)
        >>> print(result.refactored_code)
    """
    # Invoke the chain with the input data
    result = chain.invoke(input_data)
    
    return result
