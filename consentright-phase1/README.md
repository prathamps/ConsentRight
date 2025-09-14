# ConsentRight Phase 1 - Medical Consultation Prototype

A simple terminal-based medical consultation application built with LangChain and Google Gemini API. This educational project demonstrates LLM integration for providing AI-powered medical specialist recommendations based on symptom descriptions.

## Features

- Terminal-based user interface for symptom input
- AI-powered specialist recommendations using Google Gemini
- LangChain integration for prompt engineering and LLM orchestration
- Robust error handling and retry logic
- Continuous consultation sessions
- Educational code structure with clear comments

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Internet connection for API calls

## Setup Instructions

### 1. Clone and Navigate to Project

```bash
cd consentright-phase1
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

1. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file and add your Google Gemini API key:

   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. To get a Gemini API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key
   - Copy the key to your `.env` file

### 5. Run the Application

```bash
python main.py
```

## Usage Examples

### Basic Consultation

```
Welcome to ConsentRight - Medical Consultation Assistant
========================================================

Please describe your symptoms (or type 'quit' to exit):
> I have been experiencing chest pain and shortness of breath

Processing your symptoms...

Consultation Result:
-------------------
Recommended Specialist: Cardiologist
Reasoning: Chest pain combined with shortness of breath are classic symptoms that require cardiac evaluation to rule out heart conditions.
Urgency Level: High
Alternative Specialist: Emergency Medicine

Would you like another consultation? (y/n): n

Thank you for using ConsentRight. Take care!
```

### Multiple Consultations

```
Please describe your symptoms (or type 'quit' to exit):
> headache and dizziness for 3 days

Processing your symptoms...

Consultation Result:
-------------------
Recommended Specialist: Neurologist
Reasoning: Persistent headache with dizziness lasting multiple days warrants neurological evaluation.
Urgency Level: Medium
Alternative Specialist: General Physician

Would you like another consultation? (y/n): y

Please describe your symptoms (or type 'quit' to exit):
> quit

Thank you for using ConsentRight. Take care!
```

## Project Structure

```
consentright-phase1/
├── main.py              # Main application entry point
├── llm_handler.py       # LangChain and LLM integration
├── prompts.py           # Prompt templates and configurations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .env                 # Your actual environment variables (create this)
├── README.md           # This file
└── tests/              # Unit tests (to be created)
    ├── test_llm_handler.py
    ├── test_main.py
    ├── conftest.py
    └── mock_responses.py
```

## Available Specialists

The application can recommend the following medical specialists:

- Cardiologist (Heart conditions)
- Neurologist (Brain and nervous system)
- Dermatologist (Skin conditions)
- Gastroenterologist (Digestive system)
- Orthopedist (Bones and joints)
- Psychiatrist (Mental health)
- ENT (Ear, Nose, Throat)
- Ophthalmologist (Eye conditions)
- Gynecologist (Women's health)
- General Physician (General medical care)
- Emergency Medicine (Urgent care)
- Rheumatologist (Autoimmune and joint diseases)

## Troubleshooting

### Common Issues

**"ModuleNotFoundError" when running the application:**

- Ensure you've activated your virtual environment
- Run `pip install -r requirements.txt` to install dependencies

**"API key not found" error:**

- Check that your `.env` file exists and contains `GEMINI_API_KEY`
- Verify your API key is valid and active
- Ensure there are no extra spaces around the API key

**"Rate limit exceeded" error:**

- Wait a few minutes before trying again
- The application has built-in retry logic with exponential backoff

**Network connection errors:**

- Check your internet connection
- Verify you can access Google services
- Try again in a few minutes

### Getting Help

If you encounter issues:

1. Check the error message carefully - they're designed to be helpful
2. Verify your API key configuration
3. Ensure all dependencies are installed correctly
4. Check that you're using Python 3.8 or higher

## Educational Notes

This project demonstrates several important concepts:

- **LangChain Integration**: See how `LLMChain` orchestrates prompts and responses
- **Prompt Engineering**: Structured prompts in `prompts.py` for consistent outputs
- **Error Handling**: Robust retry logic and graceful degradation
- **Environment Configuration**: Secure API key management
- **User Experience**: Clear terminal interface with helpful feedback

## Next Steps (Phase 2)

Future enhancements may include:

- Web interface
- Conversation history
- Multiple language support
- Enhanced medical knowledge base
- Integration with medical databases

## License

This is an educational project. Please use responsibly and remember that this application provides educational information only and should not replace professional medical advice.
