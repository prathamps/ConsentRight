# ConsentRight Phase 1 - Medical Consultation Prototype

A terminal-based medical consultation application built with LangChain and Google Gemini API. This educational project demonstrates LLM integration for providing AI-powered medical specialist recommendations based on symptom descriptions.

## Features

- Terminal-based user interface for symptom input
- AI-powered specialist recommendations using Google Gemini 2.5 Flash
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

### Basic Consultation Flow

```text
Welcome to ConsentRight - Medical Consultation Assistant
============================================================

This AI-powered tool helps you identify which medical specialist
to consult based on your symptoms. Please note:

• This is NOT a substitute for professional medical advice
• Always consult with healthcare professionals for serious concerns
• In emergencies, call your local emergency services immediately

How to use:
• Describe your symptoms in detail
• Type 'quit' or 'exit' to end the session
• You can ask for multiple consultations in one session

------------------------------------------------------------

Please describe your symptoms:
(Be as detailed as possible for better recommendations)

> I have been experiencing severe chest pain and shortness of breath for the past 2 hours

Processing your symptoms...
   Analyzing symptoms and consulting medical knowledge base...

============================================================
CONSULTATION RESULT
============================================================

RECOMMENDED SPECIALIST: Cardiologist
URGENCY LEVEL: High

REASONING:
   Chest pain combined with shortness of breath are classic cardiovascular symptoms that require immediate cardiac evaluation to rule out heart conditions such as heart attack or other serious cardiac events.

ALTERNATIVE SPECIALIST: Emergency Medicine

ADDITIONAL NOTES:
   Given the severity and combination of symptoms, consider seeking immediate emergency care if symptoms worsen or if you experience additional symptoms like sweating, nausea, or arm pain.

------------------------------------------------------------
IMPORTANT DISCLAIMER:
   This recommendation is AI-generated and should not replace
   professional medical advice. Please consult with a healthcare
   professional for proper diagnosis and treatment.
------------------------------------------------------------

Would you like another consultation? (y/n): y
```

### Dermatology Consultation Example

```text
Please describe your symptoms:

> I have an itchy red rash on my arms and legs that appeared 2 weeks ago and seems to be spreading

Processing your symptoms...

============================================================
CONSULTATION RESULT
============================================================

RECOMMENDED SPECIALIST: Dermatologist
URGENCY LEVEL: Medium

REASONING:
   A persistent, spreading rash with itching that has lasted two weeks indicates a dermatological condition that requires specialized skin examination to determine the cause and appropriate treatment.

ALTERNATIVE SPECIALIST: General Physician

ADDITIONAL NOTES:
   Avoid scratching the affected areas to prevent secondary infection. Consider using fragrance-free moisturizers and avoiding potential allergens until you can see a specialist.

Would you like another consultation? (y/n): n

Thank you for using ConsentRight!
Remember: Always consult healthcare professionals for medical concerns.
```

### Mental Health Consultation Example

```text
Please describe your symptoms:

> I've been feeling extremely sad and hopeless for weeks, lost interest in activities I used to enjoy, and having trouble sleeping

Processing your symptoms...

============================================================
CONSULTATION RESULT
============================================================

RECOMMENDED SPECIALIST: Psychiatrist
URGENCY LEVEL: Medium

REASONING:
   Persistent feelings of sadness, hopelessness, loss of interest in activities, and sleep disturbances are classic symptoms of depression that require professional mental health evaluation and treatment.

ALTERNATIVE SPECIALIST: General Physician

ADDITIONAL NOTES:
   Mental health is just as important as physical health. Consider reaching out to trusted friends or family for support, and don't hesitate to seek professional help. If you have thoughts of self-harm, please contact a crisis helpline immediately.

Would you like another consultation? (y/n): n
```

### Emergency Scenario Example

```text
Please describe your symptoms:

> I was in a car accident an hour ago, I have a severe headache, nausea, and feel confused

Processing your symptoms...

============================================================
CONSULTATION RESULT
============================================================

RECOMMENDED SPECIALIST: Emergency Medicine
URGENCY LEVEL: High

REASONING:
   Head trauma from a car accident combined with headache, nausea, and confusion are serious symptoms that could indicate traumatic brain injury or concussion requiring immediate emergency medical evaluation.

ALTERNATIVE SPECIALIST: Neurologist

ADDITIONAL NOTES:
   These symptoms following head trauma require immediate medical attention. Do not drive yourself to the hospital. Call emergency services or have someone drive you to the nearest emergency room immediately.

Would you like another consultation? (y/n): n
```

### Testing the System

You can test the system with sample cases:

```bash
# Run comprehensive test suite
python sample_test_cases.py

# Run quick test (4 sample cases)
python sample_test_cases.py --quick

# List all available test cases
python sample_test_cases.py --list
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

### Common Setup Issues

#### 1. "ModuleNotFoundError" when running the application

**Problem:** Python can't find required modules like `langchain` or `google-generativeai`

**Solutions:**

```bash
# Ensure virtual environment is activated
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep langchain
pip list | grep google-generativeai
```

**Additional checks:**

- Ensure you're using Python 3.8 or higher: `python --version`
- Check if you're in the correct directory: `ls` should show `main.py`
- Try installing packages individually if batch install fails

#### 2. "API key not found" or Authentication Errors

**Problem:** The application can't access your Gemini API key

**Solutions:**

```bash
# Check if .env file exists
ls -la .env

# Verify .env file content (should show your key)
cat .env

# Recreate .env file if missing
cp .env.example .env
# Then edit .env and add your actual API key
```

**Common .env file issues:**

- **Extra spaces:** `GEMINI_API_KEY = your_key` ❌ → `GEMINI_API_KEY=your_key` ✅
- **Quotes:** `GEMINI_API_KEY="your_key"` ❌ → `GEMINI_API_KEY=your_key` ✅
- **Wrong variable name:** `GOOGLE_API_KEY=your_key` ❌ → `GEMINI_API_KEY=your_key` ✅

**Getting a new API key:**

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

#### 3. "Rate limit exceeded" or Quota Errors

**Problem:** You've hit API usage limits

**Solutions:**

- **Wait and retry:** The app has built-in retry logic, just wait 2-5 minutes
- **Check your quota:** Visit [Google AI Studio](https://makersuite.google.com/) to check usage
- **Upgrade plan:** Consider upgrading if you need higher limits
- **Reduce requests:** Use shorter symptom descriptions

**Rate limiting tips:**

- The app automatically waits between retries
- Avoid running multiple instances simultaneously
- Use the test suite sparingly during development

#### 4. Network and Connection Issues

**Problem:** Can't connect to Google's API servers

**Solutions:**

```bash
# Test internet connectivity
ping google.com

# Test DNS resolution
nslookup generativelanguage.googleapis.com

# Check firewall/proxy settings
# Corporate networks may block API access
```

**Network troubleshooting:**

- Try a different network (mobile hotspot)
- Check if your firewall blocks Python applications
- Verify proxy settings if in corporate environment
- Ensure your router/ISP isn't blocking Google services

#### 5. Python Version and Environment Issues

**Problem:** Compatibility issues with Python version or environment

**Solutions:**

```bash
# Check Python version (need 3.8+)
python --version

# Check pip version
pip --version

# Create fresh virtual environment
python -m venv fresh_venv
# Activate and install
fresh_venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Environment best practices:**

- Always use virtual environments
- Don't install packages globally
- Keep Python updated (3.8+ required)
- Use `python -m pip` instead of just `pip` if issues persist

### Runtime Issues

#### 6. Application Crashes or Freezes

**Problem:** App stops responding or crashes unexpectedly

**Solutions:**

- **Keyboard interrupt:** Press `Ctrl+C` to safely exit
- **Memory issues:** Restart the application
- **Long processing:** Wait up to 30 seconds for API responses

**Debugging steps:**

```bash
# Run with verbose output
python main.py 2>&1 | tee debug.log

# Check system resources
# Windows: Task Manager
# macOS/Linux: top or htop
```

#### 7. Unexpected or Poor AI Responses

**Problem:** AI gives wrong specialists or poor reasoning

**Possible causes:**

- **Vague symptoms:** Provide more detailed descriptions
- **API issues:** Temporary service problems
- **Model limitations:** AI isn't perfect

**Improvement tips:**

- Be specific about symptoms: "sharp chest pain" vs "chest discomfort"
- Include timing: "started 2 hours ago" vs "recent"
- Mention severity: "severe pain (8/10)" vs "some pain"
- Add context: "after eating" or "during exercise"

#### 8. Input Validation Errors

**Problem:** App rejects your symptom descriptions

**Common validation issues:**

- **Too short:** Need at least 5 characters
- **Too long:** Keep under 2000 characters
- **Invalid characters:** Stick to letters, numbers, basic punctuation
- **Excessive repetition:** Avoid "aaaaa" or repeated words

**Good symptom descriptions:**

```
✅ "Sharp stabbing pain in lower right abdomen for 3 hours, with nausea"
✅ "Persistent dry cough for 2 weeks, worse at night"
✅ "Sudden severe headache with sensitivity to light"

❌ "pain"
❌ "I feel bad"
❌ "aaaaahhhhh my stomach hurts so much!!!!!!"
```

### Testing and Validation

#### 9. Running Sample Test Cases

**Problem:** Want to verify the system works correctly

**Solutions:**

```bash
# Quick test (4 cases)
python sample_test_cases.py --quick

# Full test suite (20+ cases)
python sample_test_cases.py

# List available tests
python sample_test_cases.py --list
```

**Interpreting test results:**

- **80%+ success rate:** Excellent performance
- **60-80% success rate:** Good, some tuning may help
- **<60% success rate:** Check API key, network, or model issues

#### 10. Performance Optimization

**Problem:** App is slow or uses too many API calls

**Optimization tips:**

- **Shorter descriptions:** Reduce token usage
- **Batch testing:** Use test suite instead of manual testing
- **Cache results:** For development, consider caching responses
- **Rate limiting:** Built-in delays prevent API abuse

### Advanced Troubleshooting

#### 11. LangChain Integration Issues

**Problem:** Errors related to LangChain framework

**Solutions:**

```bash
# Check LangChain version
pip show langchain

# Update LangChain if needed
pip install --upgrade langchain

# Verify Google integration
python -c "from langchain.llms import GoogleGenerativeAI; print('OK')"
```

#### 12. Environment Variable Issues

**Problem:** Variables not loading correctly

**Debugging:**

```python
# Add to main.py for debugging
import os
print("Current directory:", os.getcwd())
print("Environment variables:", dict(os.environ))
print("API key found:", bool(os.getenv('GEMINI_API_KEY')))
```

#### 13. Logging and Debugging

**Enable detailed logging:**

```python
# Add to top of main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Check log files:**

- Look for error patterns
- Note API response times
- Monitor retry attempts

### Getting Additional Help

#### When to Seek Help

1. **Error persists after trying solutions above**
2. **System works but gives consistently poor results**
3. **Performance issues that affect usability**
4. **Need to modify the system for specific requirements**

#### Helpful Information to Provide

When seeking help, include:

- **Error messages:** Full text of any error messages
- **System info:** OS, Python version, pip list output
- **Steps to reproduce:** What you did before the error occurred
- **Environment:** Virtual environment status, .env file content (without API key)

#### Self-Help Resources

- **LangChain Documentation:** [python.langchain.com](https://python.langchain.com)
- **Google AI Documentation:** [ai.google.dev](https://ai.google.dev)
- **Python Virtual Environments:** [docs.python.org/3/tutorial/venv.html](https://docs.python.org/3/tutorial/venv.html)

#### Emergency Workarounds

If the system is completely broken:

1. **Use fallback:** Consult a General Physician for any symptoms
2. **Manual lookup:** Use online symptom checkers as temporary alternatives
3. **Direct consultation:** Contact healthcare providers directly
4. **Emergency services:** For urgent symptoms, call emergency services immediately

Remember: This application is educational and should never replace professional medical advice, especially in urgent situations.

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
