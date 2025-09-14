"""
ConsentRight Phase 1 - Main Application

Terminal-based medical consultation prototype using LangChain and Google Gemini API.
This application helps users get specialist recommendations based on symptom descriptions.
"""

import os
import sys
import time
import threading
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from llm_handler import ConsultationLLM


def display_welcome() -> None:
    """
    Display welcome message and application introduction.
    
    Shows clear instructions for using the application and explains
    what users can expect from the consultation process.
    """
    print("\n" + "="*60)
    print("🏥 Welcome to ConsentRight - Medical Consultation Assistant")
    print("="*60)
    print("\nThis AI-powered tool helps you identify which medical specialist")
    print("to consult based on your symptoms. Please note:")
    print("\n• This is NOT a substitute for professional medical advice")
    print("• Always consult with healthcare professionals for serious concerns")
    print("• In emergencies, call your local emergency services immediately")
    print("\nHow to use:")
    print("• Describe your symptoms in detail")
    print("• Type 'quit' or 'exit' to end the session")
    print("• You can ask for multiple consultations in one session")
    print("\n" + "-"*60)


def get_user_input() -> str:
    """
    Get symptom input from user with comprehensive validation and quit command handling.
    
    Returns:
        str: Validated symptom description from user
        
    Raises:
        KeyboardInterrupt: If user interrupts with Ctrl+C
        SystemExit: If user enters quit command
    """
    max_attempts = 3
    attempt_count = 0
    
    while True:
        try:
            print("\nPlease describe your symptoms:")
            print("(Be as detailed as possible for better recommendations)")
            print("💡 Tip: Include when symptoms started, severity, and any triggers")
            
            # Get user input
            user_input = input("\n> ").strip()
            
            # Handle quit commands
            if user_input.lower() in ['quit', 'exit', 'q', 'stop']:
                print("\nThank you for using ConsentRight. Take care of your health!")
                sys.exit(0)
            
            # Reset attempt count on any input (even invalid)
            if user_input:
                attempt_count = 0
            
            # Comprehensive input validation
            validation_result = _validate_symptom_input(user_input)
            
            if validation_result["valid"]:
                return validation_result["cleaned_input"]
            else:
                # Display specific error message
                print(f"\n❌ {validation_result['error_message']}")
                
                # Provide helpful suggestions based on error type
                if validation_result["error_type"] == "empty":
                    print("   💡 Please describe what you're experiencing (pain, discomfort, changes, etc.)")
                    print("   💡 If you want to exit, type 'quit'")
                elif validation_result["error_type"] == "too_short":
                    print("   💡 Try to include more details like:")
                    print("      • Where do you feel the symptoms?")
                    print("      • How long have you had them?")
                    print("      • How severe are they (1-10 scale)?")
                elif validation_result["error_type"] == "too_long":
                    print("   💡 Please try to be more concise while keeping important details")
                elif validation_result["error_type"] == "invalid_characters":
                    print("   💡 Please use only letters, numbers, and basic punctuation")
                elif validation_result["error_type"] == "repeated_characters":
                    print("   💡 Please avoid excessive repetition of characters")
                
                # Track consecutive failed attempts
                attempt_count += 1
                if attempt_count >= max_attempts:
                    print(f"\n⚠️  Having trouble? Here are some example symptom descriptions:")
                    print("   • 'I have a severe headache that started this morning'")
                    print("   • 'Sharp chest pain when breathing, started 2 hours ago'")
                    print("   • 'Persistent cough with fever for 3 days'")
                    print("   • 'Stomach pain and nausea after eating'")
                    attempt_count = 0  # Reset after showing examples
                
                continue
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Session interrupted by user (Ctrl+C)")
            print("Thank you for using ConsentRight. Stay healthy! 🌟")
            sys.exit(0)
        except EOFError:
            print("\n\n⚠️  Input stream ended unexpectedly")
            print("Thank you for using ConsentRight. Stay healthy! 🌟")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error while getting input: {str(e)}")
            print("   Please try again or type 'quit' to exit")
            continue


def _validate_symptom_input(user_input: str) -> Dict[str, Any]:
    """
    Comprehensive validation of user symptom input.
    
    Args:
        user_input (str): Raw user input to validate
        
    Returns:
        Dict[str, Any]: Validation result with status, cleaned input, and error details
    """
    # Initialize result structure
    result = {
        "valid": False,
        "cleaned_input": "",
        "error_message": "",
        "error_type": ""
    }
    
    # Check for empty input
    if not user_input or len(user_input.strip()) == 0:
        result["error_message"] = "Please enter a description of your symptoms."
        result["error_type"] = "empty"
        return result
    
    # Clean and normalize input
    cleaned = user_input.strip()
    
    # Check minimum length (more comprehensive than before)
    if len(cleaned) < 5:
        result["error_message"] = "Please provide a more detailed description of your symptoms (at least 5 characters)."
        result["error_type"] = "too_short"
        return result
    
    # Check maximum length to prevent API abuse and improve processing
    if len(cleaned) > 2000:
        result["error_message"] = "Symptom description is too long. Please keep it under 2000 characters."
        result["error_type"] = "too_long"
        return result
    
    # Check for excessive repetition of characters (spam detection)
    if _has_excessive_repetition(cleaned):
        result["error_message"] = "Please avoid excessive repetition of characters."
        result["error_type"] = "repeated_characters"
        return result
    
    # Check for valid characters (allow letters, numbers, spaces, basic punctuation)
    import re
    if not re.match(r'^[a-zA-Z0-9\s\.,;:!?\-\'\"()\[\]\/\+\*&%$#@]+$', cleaned):
        result["error_message"] = "Please use only standard characters (letters, numbers, and basic punctuation)."
        result["error_type"] = "invalid_characters"
        return result
    
    # Additional cleaning: normalize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Check for meaningful content (not just punctuation or numbers)
    if not re.search(r'[a-zA-Z]', cleaned):
        result["error_message"] = "Please include descriptive text about your symptoms."
        result["error_type"] = "no_meaningful_content"
        return result
    
    # Input is valid
    result["valid"] = True
    result["cleaned_input"] = cleaned
    return result


def _has_excessive_repetition(text: str) -> bool:
    """
    Check if text has excessive character repetition that might indicate spam or invalid input.
    
    Args:
        text (str): Text to check for repetition
        
    Returns:
        bool: True if excessive repetition is detected
    """
    import re
    
    # Check for more than 4 consecutive identical characters
    if re.search(r'(.)\1{4,}', text):
        return True
    
    # Check for more than 10 repetitions of the same word
    words = text.lower().split()
    if len(words) > 0:
        word_counts = {}
        for word in words:
            if len(word) > 2:  # Only check words longer than 2 characters
                word_counts[word] = word_counts.get(word, 0) + 1
                if word_counts[word] > 10:
                    return True
    
    return False


def display_result(result: Dict[str, Any]) -> None:
    """
    Format and display consultation results in a user-friendly way.
    
    Args:
        result (Dict[str, Any]): Consultation result from LLM handler containing
                                specialist, reasoning, urgency, and optional fields
    """
    print("\n" + "="*60)
    print("📋 CONSULTATION RESULT")
    print("="*60)
    
    # Display primary recommendation
    specialist = result.get('specialist', 'Unknown')
    print(f"\n🏥 RECOMMENDED SPECIALIST: {specialist}")
    
    # Display urgency with appropriate emoji
    urgency = result.get('urgency', 'Medium')
    urgency_emoji = {
        'High': '🚨',
        'Medium': '⚠️',
        'Low': '💡'
    }
    print(f"{urgency_emoji.get(urgency, '⚠️')} URGENCY LEVEL: {urgency}")
    
    # Display reasoning
    reasoning = result.get('reasoning', 'No reasoning provided')
    print(f"\n📝 REASONING:")
    print(f"   {reasoning}")
    
    # Display alternative specialist if provided
    alternative = result.get('alternative', '')
    if alternative and alternative.strip():
        print(f"\n🔄 ALTERNATIVE SPECIALIST: {alternative}")
    
    # Display additional notes if provided
    additional_notes = result.get('additional_notes', '')
    if additional_notes and additional_notes.strip():
        print(f"\n💡 ADDITIONAL NOTES:")
        print(f"   {additional_notes}")
    
    # Display important disclaimer
    print(f"\n" + "-"*60)
    print("⚠️  IMPORTANT DISCLAIMER:")
    print("   This recommendation is AI-generated and should not replace")
    print("   professional medical advice. Please consult with a healthcare")
    print("   professional for proper diagnosis and treatment.")
    print("-"*60)


def _show_processing_indicator() -> None:
    """
    Display an enhanced processing indicator with animated feedback.
    
    Shows progress to keep user engaged during API processing time.
    """
    print("\n🔄 Processing your symptoms...")
    print("   Analyzing symptoms and consulting medical knowledge base...")
    
    # Simple progress indicator
    indicators = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    # Show a brief animated indicator (2 seconds)
    for i in range(20):  # 20 iterations * 0.1 seconds = 2 seconds
        print(f"\r   {indicators[i % len(indicators)]} Please wait...", end="", flush=True)
        time.sleep(0.1)
    
    print("\r   ✅ Analysis in progress...                    ")
    print("   📊 Generating specialist recommendation...")


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


def _display_error_with_guidance(error: Exception, attempt_number: int = 1) -> None:
    """
    Display user-friendly error messages with helpful guidance.
    
    Args:
        error (Exception): The error that occurred
        attempt_number (int): Which attempt this is (for progressive help)
    """
    error_info = _categorize_error(error)
    
    print(f"\n❌ {error_info['message']}")
    
    # Show suggestions based on error category
    print("\n💡 Suggestions:")
    for suggestion in error_info['suggestions']:
        print(f"   • {suggestion}")
    
    # Progressive help - show more detailed guidance on repeated failures
    if attempt_number >= 2:
        print(f"\n⚠️  This is attempt #{attempt_number}. Additional help:")
        
        if error_info['category'] == 'network':
            print("   • Try using a different network connection")
            print("   • Check if your firewall is blocking the application")
        elif error_info['category'] == 'auth':
            print("   • Verify the .env file exists and contains GEMINI_API_KEY=your_key_here")
            print("   • Make sure there are no extra spaces around the API key")
        elif error_info['category'] == 'rate_limit':
            print("   • Consider waiting 5-10 minutes before trying again")
            print("   • Try describing fewer symptoms at once")
        
        print("   • Type 'quit' if you want to exit and try again later")
    
    # Show fallback option for persistent errors
    if attempt_number >= 3:
        print(f"\n🏥 Immediate help: If you have urgent symptoms, please:")
        print("   • Contact your doctor directly")
        print("   • Visit an urgent care center")
        print("   • Call emergency services if symptoms are severe")


def ask_continue() -> bool:
    """
    Ask user if they want to continue with another consultation.
    
    Returns:
        bool: True if user wants to continue, False if they want to exit
    """
    while True:
        try:
            print("\nWould you like another consultation? (y/n): ", end="")
            response = input().strip().lower()
            
            if response in ['y', 'yes', 'yeah', 'yep']:
                return True
            elif response in ['n', 'no', 'nope', 'quit', 'exit']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
                continue
                
        except KeyboardInterrupt:
            print("\n")
            return False
        except EOFError:
            print("\n")
            return False


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
        
        # Initialize the LLM handler
        print("🔄 Initializing AI consultation system...")
        try:
            consultation_llm = ConsultationLLM(api_key)
            print("✅ System ready!")
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
                
                # Process symptoms through LLM with timeout handling
                try:
                    result = consultation_llm.process_symptoms(symptoms)
                    
                    # Reset error count on successful processing
                    if hasattr(main, '_error_count'):
                        main._error_count = 0
                    
                    # Display the results
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
        print("\n👋 Thank you for using ConsentRight!")
        print("Remember: Always consult healthcare professionals for medical concerns.")
        print("Stay healthy! 🌟")
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        print("Please check your setup and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()