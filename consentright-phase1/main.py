"""
ConsentRight Phase 1 - Main Application

Terminal-based medical consultation prototype demonstrating LangChain integration
with Google Gemini API for educational purposes.

EDUCATIONAL NOTES:
==================

This application demonstrates several important software development concepts:

1. **User Interface Design**:
   - Clear, intuitive terminal interface
   - Comprehensive input validation
   - User-friendly error messages
   - Graceful error handling and recovery

2. **LangChain Integration**:
   - Proper LLM initialization and configuration
   - Structured prompt templates for consistency
   - Chain execution with error handling
   - Response parsing and validation

3. **Production-Ready Practices**:
   - Environment variable configuration
   - Comprehensive error categorization
   - Retry logic with exponential backoff
   - Logging and debugging support
   - Input sanitization and validation

4. **User Experience (UX)**:
   - Progressive help and guidance
   - Clear feedback during processing
   - Consistent formatting and messaging
   - Accessibility considerations

Key Learning Objectives:
- How to integrate LLMs into applications
- Best practices for error handling
- User interface design principles
- Configuration management
- Input validation techniques
"""

import os
import sys
import time
import threading
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from llm_handler import ConsultationLLM
from ui import display_welcome, display_result, ask_continue, get_user_input
from error_handling import _display_error_with_guidance


def _show_processing_indicator() -> None:
    """
    Display a processing indicator with feedback.
    
    Shows progress to keep user engaged during API processing time.
    """
    print("\nProcessing your symptoms...")
    print("   Analyzing symptoms and consulting medical knowledge base...")
    
    # Simple progress indicator
    indicators = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    # Show a brief animated indicator (2 seconds)
    for i in range(20):  # 20 iterations * 0.1 seconds = 2 seconds
        print(f"\r   {indicators[i % len(indicators)]} Please wait...", end="", flush=True)
        time.sleep(0.1)
    
    print("\r   Analysis in progress...                    ")
    print("   Generating specialist recommendation...")


def _categorize_error(error: Exception) -> Dict[str, str]:
    """
    Categorize errors to provide appropriate user-friendly messages.
    
    Args:
        error (Exception): The exception to categorize
        
    Returns:
        Dict[str, str]: Error category and user-friendly message
    """
    error_str = str(error).lower()
    
    # Network and connectivity errors
    if any(keyword in error_str for keyword in ['timeout', 'connection', 'network', 'unreachable']):
        return {
            "category": "network",
            "message": "Network connection issue detected.",
            "suggestions": [
                "Check your internet connection",
                "Try again in a few moments",
                "Ensure you're not behind a restrictive firewall"
            ]
        }
    
    # API key and authentication errors
    if any(keyword in error_str for keyword in ['api key', 'authentication', 'unauthorized', 'forbidden']):
        return {
            "category": "auth",
            "message": "API authentication issue detected.",
            "suggestions": [
                "Verify your GEMINI_API_KEY in the .env file",
                "Ensure your API key is valid and active",
                "Check if your API key has the necessary permissions"
            ]
        }
    
    # Rate limiting errors
    if any(keyword in error_str for keyword in ['rate limit', 'quota', 'too many requests']):
        return {
            "category": "rate_limit",
            "message": "API rate limit exceeded.",
            "suggestions": [
                "Please wait a few minutes before trying again",
                "Consider upgrading your API plan if this happens frequently",
                "Try again with a shorter symptom description"
            ]
        }
    
    # Service availability errors
    if any(keyword in error_str for keyword in ['service unavailable', 'server error', 'internal error']):
        return {
            "category": "service",
            "message": "The AI service is temporarily unavailable.",
            "suggestions": [
                "This is likely a temporary issue with the AI service",
                "Please try again in a few minutes",
                "If the problem persists, consult a General Physician"
            ]
        }
    
    # Input validation errors
    if any(keyword in error_str for keyword in ['invalid', 'validation', 'parse', 'format']):
        return {
            "category": "input",
            "message": "There was an issue processing your symptom description.",
            "suggestions": [
                "Try rephrasing your symptoms more clearly",
                "Avoid special characters or very long descriptions",
                "Focus on the main symptoms you're experiencing"
            ]
        }
    
    # Generic/unknown errors
    return {
        "category": "unknown",
        "message": "An unexpected error occurred during processing.",
        "suggestions": [
            "Please try again with a different symptom description",
            "If the problem persists, restart the application",
            "Consider consulting a General Physician if you need immediate help"
        ]
    }


def main() -> None:
    """
    Main application function that orchestrates the entire consultation flow.
    
    Handles environment setup, LLM initialization, and manages the continuous
    consultation loop with proper error handling and user experience.
    """
    try:
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("\n❌ ERROR: GEMINI_API_KEY not found in environment variables.")
            print("\nPlease follow these steps:")
            print("1. Copy .env.example to .env")
            print("2. Add your Google Gemini API key to the .env file")
            print("3. Restart the application")
            print("\nFor API key setup instructions, see README.md")
            sys.exit(1)
        
        # EDUCATIONAL: Initialize the LLM handler
        # This demonstrates proper LangChain initialization with error handling
        print("Initializing AI consultation system...")
        try:
            # Create our ConsultationLLM instance - this sets up the LangChain components
            consultation_llm = ConsultationLLM(api_key)
            print("System ready!")
        except Exception as e:
            print(f"\n❌ ERROR: Failed to initialize consultation system.")
            print(f"   Details: {str(e)}")
            print("\nPlease check:")
            print("• Your internet connection")
            print("• Your GEMINI_API_KEY is valid")
            print("• All dependencies are installed (pip install -r requirements.txt)")
            sys.exit(1)
        
        # Display welcome message
        display_welcome()
        
        # Main consultation loop
        while True:
            try:
                # Get user input (symptoms)
                symptoms = get_user_input()
                
                # Show enhanced processing indicator with progress
                _show_processing_indicator()
                
                # EDUCATIONAL: Process symptoms through LLM with comprehensive error handling
                # This shows how to integrate LangChain processing into a user application
                try:
                    # Call our LangChain-based processing method
                    # This executes: input validation → prompt formatting → LLM call → response parsing
                    result = consultation_llm.process_symptoms(symptoms)
                    
                    # Reset error count on successful processing (for progressive help)
                    if hasattr(main, '_error_count'):
                        main._error_count = 0
                    
                    # Display the structured results to the user
                    display_result(result)
                    
                except KeyboardInterrupt:
                    print("\n\n⚠️  Processing interrupted by user (Ctrl+C)")
                    print("Returning to main menu...")
                    continue
                except Exception as e:
                    # Track consecutive errors for progressive help
                    if not hasattr(main, '_error_count'):
                        main._error_count = 0
                    main._error_count += 1
                    
                    # Display categorized error with helpful guidance
                    _display_error_with_guidance(e, main._error_count)
                    
                    # Ask if user wants to try again
                    try:
                        if not ask_continue():
                            break
                    except KeyboardInterrupt:
                        print("\n\n⚠️  Session interrupted during error recovery")
                        break
                    continue
                
                # Ask if user wants another consultation
                try:
                    if not ask_continue():
                        break
                except KeyboardInterrupt:
                    print("\n\n⚠️  Session interrupted during continuation prompt")
                    break
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Session interrupted by user (Ctrl+C)")
                print("Exiting gracefully...")
                break
            except EOFError:
                print("\n\n⚠️  Input stream ended unexpectedly")
                print("Exiting gracefully...")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error in main loop: {str(e)}")
                print("💡 This might be a system-level issue. Please:")
                print("   • Restart the application")
                print("   • Check your system resources")
                print("   • Ensure all dependencies are properly installed")
                
                try:
                    if not ask_continue():
                        break
                except:
                    print("Unable to continue safely. Exiting...")
                    break
        
        # Exit message
        print("\nThank you for using ConsentRight!")
        print("Remember: Always consult healthcare professionals for medical concerns.")
        print("Stay healthy!")
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        print("Please check your setup and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()