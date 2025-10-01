# 🔧 CognitCode

An intelligent assistant that acts as an expert software architect, analyzing Python code snippets and providing AI-powered refactoring suggestions with educational explanations.

## 📋 Project Description

CognitCode is a sophisticated web application that combines static code analysis with AI-powered refactoring capabilities. When a developer provides a code snippet and specifies a refactoring goal, the agent performs deep analysis to identify code smells, applies refactoring techniques, and generates clear, educational reports that explain the "why" behind each change by linking them to fundamental software design principles.

The system follows a sequential pipeline architecture using LangChain, providing both automated code improvement suggestions and educational value for developers looking to enhance their coding practices.

## ✨ Key Features

### 🎯 Core Functionality
- **Static Code Analysis**: Automated detection of code smells using Abstract Syntax Tree (AST) parsing
- **AI-Powered Refactoring**: Intelligent code improvement suggestions using Google Gemini 1.5 Flash
- **Educational Explanations**: Detailed explanations linking changes to software design principles
- **Interactive Web Interface**: User-friendly Streamlit-based interface for code input and result visualization

### 🔍 Code Smell Detection
- **Function Length Analysis**: Identifies functions with excessive statements (>20 nodes)
- **Magic Number Detection**: Flags hardcoded numerical constants that should be named
- **Extensible Rule Engine**: Modular architecture allowing easy addition of new analysis rules

### 🤖 AI Integration
- **Structured Prompt Engineering**: Carefully crafted prompts for consistent, high-quality refactoring suggestions
- **Response Validation**: Pydantic-based validation ensuring reliable AI output parsing
- **LangChain Integration**: Modern LCEL (LangChain Expression Language) for robust AI workflow orchestration

### 🎨 User Experience
- **Side-by-Side Comparison**: Original and refactored code displayed simultaneously
- **Download Functionality**: Export refactored code as Python files
- **Error Handling**: Graceful handling of syntax errors and API failures
- **Loading States**: Clear visual feedback during processing

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Streamlit**: Web framework for the user interface
- **LangChain**: AI development framework for LLM integration
- **Google Gemini 1.5 Flash**: Large Language Model for code refactoring

### Libraries and Dependencies
- **ast**: Python's built-in Abstract Syntax Trees library for code parsing
- **pydantic**: Data validation and settings management
- **langchain-google-genai**: Official Google AI integration for LangChain
- **python-dotenv**: Environment variable management
- **pytest**: Testing framework with mock support

### Development Tools
- **Git**: Version control system
- **pip**: Package management
- **Virtual Environment**: Isolated development environment

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google AI API key (for Gemini access)
- Git (for version control)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cognitcode
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file in project root
   echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   streamlit run src/app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
cognitcode/
├── .env                    # Environment variables (not tracked)
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── pytest.ini           # Pytest configuration
├── run_tests.py          # Test runner script
└── src/                  # Source code directory
    ├── app.py            # Main Streamlit application
    ├── parser.py         # AST generation service
    ├── analyzer.py       # Static analysis engine
    ├── formatter.py      # Issue data modeler
    └── ai_core.py        # Core AI logic and prompt engineering
└── tests/                # Test directory
    ├── test_ai_core.py   # AI core module tests
    ├── test_analyzer.py  # Analyzer module tests
    ├── test_formatter.py # Formatter module tests
    └── test_parser.py    # Parser module tests
```

## 🔧 System Architecture

### Phase 1: Static Analysis Engine
- **Code Ingestion Module**: Handles user input validation and preparation
- **AST Generation Service**: Parses Python code into Abstract Syntax Trees
- **Analysis Rule Engine**: Detects code smells using visitor pattern
- **Issue Data Modeler**: Formats analysis results into structured JSON

### Phase 2: Core AI Logic
- **Prompt Template Manager**: Defines structured prompts for LLM communication
- **LLM Service Connector**: Manages Google Gemini API integration
- **AI Response Parser**: Validates and parses AI responses using Pydantic
- **Refactoring Logic Orchestrator**: Coordinates the complete AI workflow

### Phase 3: User Interface
- **Application State Manager**: Manages session state using Streamlit
- **UI Layout Component**: Defines the visual structure and layout
- **Input Renderer**: Handles code input form and submission
- **Output Renderer**: Displays refactored code and explanations

### Phase 4: Integration and Testing
- **Main Application Controller**: Orchestrates end-to-end workflow
- **Configuration Management**: Handles environment variables and secrets
- **Testing Framework**: Comprehensive unit and integration tests

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python run_tests.py

# Run specific test module
pytest tests/test_analyzer.py -v

# Run with coverage
pytest --cov=src tests/
```

### Test Coverage
The project includes comprehensive test coverage for:
- AST parsing and error handling
- Code smell detection algorithms
- JSON formatting and data transformation
- AI prompt generation and response parsing
- End-to-end workflow integration

## 🌐 Deployment

### Streamlit Community Cloud
The application is designed for easy deployment on Streamlit Community Cloud:

1. **Push to GitHub**: Ensure your code is in a GitHub repository
2. **Connect to Streamlit Cloud**: Link your GitHub account
3. **Deploy**: Select the repository and configure environment variables
4. **Access**: Your app will be available at a public URL

### Environment Variables for Deployment
- `GEMINI_API_KEY`: Your Google AI API key for Gemini access

## 📚 Usage Examples

### Basic Usage
1. Open the web application
2. Paste your Python code in the left panel
3. Click "Analyze & Refactor"
4. Review the refactored code and explanation in the right panel
5. Download the improved code if desired

### Example Input
```python
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item.price * 1.15
    return total
```

### Example Output
The system would identify:
- Magic number `1.15` (tax rate)
- Potential for better variable naming
- Opportunity for more descriptive function structure

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Include comprehensive docstrings
- Write tests for all new functionality

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues
- **API Key Errors**: Ensure your Google API key is correctly set in the `.env` file as `GEMINI_API_KEY`
- **Syntax Errors**: The system will detect and report Python syntax errors
- **Import Errors**: Make sure all dependencies are installed via `pip install -r requirements.txt`

### Getting Help
- Check the troubleshooting section in the application
- Review the test files for usage examples
- Open an issue on GitHub for bugs or feature requests

## 🔮 Future Enhancements

### Planned Features
- **Multi-language Support**: Extend beyond Python to support other programming languages
- **Custom Rule Configuration**: Allow users to define their own code smell detection rules
- **Batch Processing**: Analyze multiple files simultaneously
- **Integration APIs**: REST API for programmatic access
- **Advanced Refactoring Goals**: Support for performance optimization and security enhancement

### Technical Improvements
- **Enhanced Error Recovery**: Better handling of edge cases and malformed input
- **Performance Optimization**: Caching and optimization for large codebases
- **Advanced AI Models**: Integration with additional LLM providers
- **Real-time Collaboration**: Multi-user editing and review capabilities

---

**Built with ❤️ using Python, Streamlit, and LangChain**