"""
Main Application Controller

This module provides the complete Streamlit web application for the code refactoring agent.
It integrates all backend modules (parser, analyzer, formatter, ai_core) into a functional
web interface that allows users to input code, analyze it for issues, and receive
AI-powered refactoring suggestions.

"""

import streamlit as st
from typing import Tuple


import os
import sys
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, os.pardir))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from src.parser import generate_ast_from_code
from src.analyzer import run_analysis
from src.formatter import format_issues_to_json
from src.ai_core import create_refactoring_chain, invoke_refactoring_chain, RefactoringResponse


def initialize_state():
    """
    Initialize the application's session state with default values.
    
    This function ensures that all required session state variables are properly
    initialized with their default values if they don't already exist.
    """
    if 'loading' not in st.session_state:
        st.session_state['loading'] = False
    
    if 'error' not in st.session_state:
        st.session_state['error'] = None
    
    if 'result' not in st.session_state:
        st.session_state['result'] = None




def render_main_layout() -> Tuple:
    """
    Render the main application layout and return column objects. 
 
    """
    # Display main title and description
    st.title("🔧 CognitCode - AI-Powered Code Refactoring")
    st.markdown("""
    **An intelligent assistant that analyzes your Python code and provides AI-powered refactoring suggestions.**
    
    Simply paste your code below, and our agent will identify code smells and suggest improvements.
    """)
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    return col1, col2


def render_input_form() -> Tuple[str, bool]:
    """
    Render the input form for code submission.
    """
    with st.form(key='code_form'):
        st.subheader("📝 Original Code")
        st.markdown("Paste your Python code below:")
        
        code_snippet = st.text_area(
            "Code Input",
            height=400,
            placeholder="def example_function():\n    # Your code here\n    pass",
            help="Enter the Python code you want to refactor"
        )

        submitted = st.form_submit_button(
            "🚀 Analyze & Refactor",
            type="primary",
            use_container_width=True
        )
    
    return code_snippet, submitted


def render_output_display():
    """
    Render the output display based on application state.
    
    """

    if st.session_state['loading']:
        with st.spinner("🤖 AI is analyzing your code and generating refactoring suggestions..."):
            st.empty()  
    

    elif st.session_state['error']:
        st.error(f"❌ **Error:** {st.session_state['error']}")
        st.markdown("""
        **Troubleshooting Tips:**
        - Make sure your code is valid Python syntax
        - Check that you have a valid Google API key configured
        - Try with a simpler code snippet first
        """)
    
    elif st.session_state['result']:
        result: RefactoringResponse = st.session_state['result']
        
        st.subheader("✨ Refactored Code")
        st.code(result.refactored_code, language='python')
        
        st.subheader("📖 Explanation")
        st.markdown(result.explanation)
        
        st.download_button(
            label="💾 Download Refactored Code",
            data=result.refactored_code,
            file_name="refactored_code.py",
            mime="text/python"
        )
    

    else:
        st.info("👈 Enter your Python code in the left panel and click 'Analyze & Refactor' to get started!")


# Main Application Controller Logic
def main():
    """
    Main application controller that orchestrates the entire workflow.

    """
    st.set_page_config(
        page_title="CognitCode",
        page_icon="🔧",
        layout="wide"
    )
    
    initialize_state()

    col1, col2 = render_main_layout()
    
    with col1:
        code_snippet, submitted = render_input_form()
    
    with col2:
        render_output_display()
    
    if submitted:
        if not code_snippet.strip():
            st.session_state['error'] = "Please enter some code to analyze."
            st.session_state['loading'] = False
            st.rerun()
            return
        
        st.session_state['loading'] = True
        st.session_state['result'] = None
        st.session_state['error'] = None
        
        try:
            # -- Begin Backend Pipeline --
            
            # Step A: AST Generation
            ast_tree, error = generate_ast_from_code(code_snippet)
            if error:
                raise ValueError(error)
            
            # Step B: Static Analysis
            issues = run_analysis(ast_tree)
            
            # Step C: Data Formatting
            issues_json = format_issues_to_json(issues)
            
            # Step D: AI Refactoring
            ai_chain = create_refactoring_chain()
            input_data = {
                "code_snippet": code_snippet,
                "issues_json": issues_json,
                "refactoring_goal": "Improve Readability"
            }
            result = invoke_refactoring_chain(ai_chain, input_data)
            
            # -- End Backend Pipeline --
            
            #successful result
            st.session_state['result'] = result
            
        except Exception as e:
            st.session_state['error'] = str(e)
        
        finally:
            st.session_state['loading'] = False
            st.rerun()


if __name__ == "__main__":
    main()
