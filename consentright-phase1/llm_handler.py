"""
ConsentRight Phase 1 - LLM Handler

LangChain integration with Google Generative AI for medical consultation recommendations.
Uses Gemini 2.5 Flash model for optimal performance and accuracy.
"""

import os
import time
import json
import logging
from typing import Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from prompts import SPECIALIST_LIST, CONSULTATION_PROMPT

# Configure logging for error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConsultationLLM:
    """
    LangChain-based LLM handler for medical consultation recommendations.
    
    This class integrates with Google Gemini API through LangChain to process
    symptom descriptions and provide specialist recommendations with reasoning.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the ConsultationLLM with LangChain and Google Gemini API.
        
        Args:
            api_key (str): Google Gemini API key for authentication
            
        Raises:
            ValueError: If API key is invalid or missing
            Exception: If LangChain initialization fails
        """
        if not api_key or not isinstance(api_key, str) or len(api_key.strip()) == 0:
            raise ValueError("Invalid API key provided. Please check your GEMINI_API_KEY environment variable.")
        
        try:
            # Initialize LangChain LLM with Gemini 2.5 Flash
            # Try different model names in case 2.5 flash isn't available
            try:
                self.llm = ChatGoogleGenerativeAI(
                    google_api_key=api_key,
                    model="gemini-2.5-flash",
                    temperature=0.3,
                    max_output_tokens=2048
                )
                logger.info("Using Gemini 2.5 Flash model")
            except Exception as e:
                logger.warning(f"Gemini 2.5 Flash not available: {e}")
                try:
                    self.llm = ChatGoogleGenerativeAI(
                        google_api_key=api_key,
                        model="gemini-1.5-flash",
                        temperature=0.3,
                        max_output_tokens=2048
                    )
                    logger.info("Fallback to Gemini 1.5 Flash model")
                except Exception as e2:
                    logger.warning(f"Gemini 1.5 Flash not available: {e2}")
                    self.llm = ChatGoogleGenerativeAI(
                        google_api_key=api_key,
                        model="gemini-pro",
                        temperature=0.3,
                        max_output_tokens=2048
                    )
                    logger.info("Fallback to Gemini Pro model")
            
            # Create modern LangChain runnable sequence
            self.chain = CONSULTATION_PROMPT | self.llm
            
            logger.info("ConsultationLLM initialized successfully with LangChain and Gemini 2.5 Flash")
            
        except Exception as e:
            logger.error(f"Failed to initialize ConsultationLLM: {str(e)}")
            raise Exception(f"LangChain initialization failed: {str(e)}")
    
    def process_symptoms(self, symptoms: str) -> Dict[str, Any]:
        """
        Process symptom description and return specialist recommendation.
        
        Args:
            symptoms (str): User's symptom description
            
        Returns:
            Dict[str, Any]: Structured recommendation with specialist, reasoning, urgency, etc.
            
        Raises:
            ValueError: If symptoms input is invalid
            Exception: If processing fails after retries
        """
        # Validate and sanitize input
        cleaned_symptoms = self._validate_and_sanitize_input(symptoms)
        
        try:
            logger.info(f"Processing symptoms: {cleaned_symptoms[:50]}...")
            
            # Execute LangChain with retry logic
            def _execute_chain():
                result = self.chain.invoke({"symptoms": cleaned_symptoms})
                return result.content if hasattr(result, 'content') else str(result)
            
            # Implement retry logic for production robustness
            response = self._retry_with_backoff(_execute_chain, max_retries=3, base_delay=1.0)
            
            # Parse and validate the response
            parsed_result = self._parse_response(response)
            
            logger.info("Symptoms processed successfully")
            return parsed_result
            
        except KeyboardInterrupt:
            logger.info("Processing interrupted by user")
            raise KeyboardInterrupt("Processing was interrupted by user")
        except Exception as e:
            logger.error(f"Failed to process symptoms after retries: {str(e)}")
            
            # Provide more specific error information
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                raise Exception("Request timed out. The AI service may be experiencing high load. Please try again.")
            elif "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
                raise Exception("API rate limit exceeded. Please wait a few minutes before trying again.")
            elif "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                raise Exception("API authentication failed. Please check your GEMINI_API_KEY in the .env file.")
            elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                raise Exception("Network connection error. Please check your internet connection and try again.")
            
            # Provide fallback recommendation for other errors
            logger.info("Attempting to provide fallback recommendation")
            try:
                return self.fallback_recommendation(cleaned_symptoms)
            except Exception as fallback_error:
                logger.error(f"Fallback recommendation also failed: {str(fallback_error)}")
                raise Exception(f"Unable to process symptoms due to technical issues: {str(e)}")
    

    
    def _validate_and_sanitize_input(self, symptoms: str) -> str:
        """
        Validate and sanitize user input for symptom processing with comprehensive checks.
        
        Args:
            symptoms (str): Raw symptom input from user
            
        Returns:
            str: Cleaned and validated symptom text
            
        Raises:
            ValueError: If input is invalid with specific error message
        """
        if not symptoms or not isinstance(symptoms, str):
            raise ValueError("Symptoms must be provided as a non-empty string")
        
        # Strip whitespace and check for empty input
        cleaned = symptoms.strip()
        if len(cleaned) == 0:
            raise ValueError("Symptoms description cannot be empty")
        
        # Check minimum meaningful length
        if len(cleaned) < 5:
            raise ValueError("Please provide a more detailed description of your symptoms")
        
        # Check for reasonable length limits (prevent API abuse and improve processing)
        if len(cleaned) > 2000:
            logger.warning("Symptom input truncated due to length")
            cleaned = cleaned[:1997] + "..."
        
        # Check for excessive repetition that might indicate spam or invalid input
        import re
        if re.search(r'(.)\1{5,}', cleaned):
            raise ValueError("Please avoid excessive repetition of characters in your symptom description")
        
        # Check for meaningful content (must contain letters)
        if not re.search(r'[a-zA-Z]', cleaned):
            raise ValueError("Please include descriptive text about your symptoms")
        
        # Basic sanitization - normalize whitespace and remove potential problematic characters
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove or replace potentially problematic characters that might interfere with processing
        # Keep basic punctuation but remove unusual characters
        cleaned = re.sub(r'[^\w\s\.,;:!?\-\'\"()\[\]\/]', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Final validation after cleaning
        if len(cleaned) < 3:
            raise ValueError("After cleaning, your symptom description is too short. Please provide more details.")
        
        logger.info(f"Input validated and sanitized successfully (length: {len(cleaned)})")
        return cleaned
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse and validate LLM response into structured format.
        
        Args:
            response (str): Raw response from LLM
            
        Returns:
            Dict[str, Any]: Parsed and validated response data
            
        Raises:
            Exception: If response parsing fails
        """
        try:
            # Try to extract JSON from response
            # The response might contain extra text, so we need to find the JSON part
            response_clean = response.strip()
            
            # Look for JSON-like structure in the response
            start_idx = response_clean.find('{')
            end_idx = response_clean.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON structure found in response")
            
            json_str = response_clean[start_idx:end_idx]
            parsed_data = json.loads(json_str)
            
            # Validate required fields
            required_fields = ['specialist', 'reasoning', 'urgency']
            for field in required_fields:
                if field not in parsed_data or not parsed_data[field]:
                    raise ValueError(f"Missing or empty required field: {field}")
            
            # Validate specialist is from our predefined list
            if parsed_data['specialist'] not in SPECIALIST_LIST:
                logger.warning(f"Unexpected specialist: {parsed_data['specialist']}")
                # Don't fail, but log the warning
            
            # Validate urgency level
            valid_urgency = ['High', 'Medium', 'Low']
            if parsed_data['urgency'] not in valid_urgency:
                logger.warning(f"Invalid urgency level: {parsed_data['urgency']}, defaulting to Medium")
                parsed_data['urgency'] = 'Medium'
            
            # Ensure optional fields exist (set to empty string if missing)
            optional_fields = ['alternative', 'additional_notes']
            for field in optional_fields:
                if field not in parsed_data:
                    parsed_data[field] = ""
            
            logger.info("Response parsed and validated successfully")
            return parsed_data
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            raise Exception(f"Failed to parse LLM response as JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Response validation failed: {str(e)}")
            raise Exception(f"Response validation failed: {str(e)}")
    
    def _retry_with_backoff(self, func, *args, max_retries: int = 3, base_delay: float = 1.0, **kwargs) -> Any:
        """
        Execute function with exponential backoff retry strategy and user feedback.
        
        Args:
            func: Function to execute with retry logic
            *args: Positional arguments for the function
            max_retries (int): Maximum number of retry attempts
            base_delay (float): Base delay in seconds for exponential backoff
            **kwargs: Keyword arguments for the function
            
        Returns:
            Any: Result from successful function execution
            
        Raises:
            Exception: If all retry attempts fail
            KeyboardInterrupt: If user interrupts during retry
        """
        last_exception = None
        
        for attempt in range(max_retries + 1):  # +1 for initial attempt
            try:
                if attempt > 0:
                    # Calculate exponential backoff delay
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.info(f"Retrying in {delay} seconds (attempt {attempt}/{max_retries})")
                    
                    # Provide user feedback during retry delay
                    print(f"\r   ⏳ Retrying... (attempt {attempt}/{max_retries}) - waiting {delay:.1f}s", end="", flush=True)
                    
                    # Sleep with interrupt handling
                    try:
                        time.sleep(delay)
                    except KeyboardInterrupt:
                        print("\n   ⚠️  Retry interrupted by user")
                        raise KeyboardInterrupt("Retry process interrupted by user")
                    
                    print(f"\r   🔄 Retrying API call... (attempt {attempt}/{max_retries})                    ", flush=True)
                
                # Execute the function
                result = func(*args, **kwargs)
                
                if attempt > 0:
                    logger.info(f"Function succeeded on retry attempt {attempt}")
                    print(f"\r   ✅ Success on retry attempt {attempt}!                                        ")
                
                return result
                
            except KeyboardInterrupt:
                logger.info("Retry process interrupted by user")
                raise KeyboardInterrupt("Processing interrupted by user during retry")
            except Exception as e:
                last_exception = e
                
                # Categorize the error to determine if retry is appropriate
                if self._should_retry_error(e):
                    if attempt < max_retries:
                        logger.warning(f"Attempt {attempt + 1} failed with retryable error: {str(e)}")
                        print(f"\r   ⚠️  Attempt {attempt + 1} failed, will retry...                              ", flush=True)
                        continue
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed. Last error: {str(e)}")
                        print(f"\r   ❌ All retry attempts failed                                                  ")
                else:
                    logger.error(f"Non-retryable error encountered: {str(e)}")
                    print(f"\r   ❌ Non-retryable error occurred                                               ")
                    break
        
        # If we get here, all retries failed
        raise Exception(f"Processing failed after {max_retries + 1} attempts. Last error: {str(last_exception)}")
    
    def _should_retry_error(self, error: Exception) -> bool:
        """
        Determine if an error should trigger a retry attempt.
        
        Args:
            error (Exception): The exception to evaluate
            
        Returns:
            bool: True if the error is retryable, False otherwise
        """
        error_str = str(error).lower()
        
        # Network-related errors that should be retried
        retryable_errors = [
            'timeout',
            'connection',
            'network',
            'rate limit',
            'quota exceeded',
            'service unavailable',
            'internal server error',
            'bad gateway',
            'gateway timeout'
        ]
        
        # Check if error message contains retryable error indicators
        for retryable in retryable_errors:
            if retryable in error_str:
                return True
        
        # Authentication errors should not be retried
        non_retryable_errors = [
            'authentication',
            'unauthorized',
            'invalid api key',
            'forbidden',
            'access denied'
        ]
        
        for non_retryable in non_retryable_errors:
            if non_retryable in error_str:
                return False
        
        # Default to retry for unknown errors (conservative approach)
        return True
    
    def fallback_recommendation(self, symptoms: str) -> Dict[str, Any]:
        """
        Provide fallback recommendation when LLM processing fails.
        
        Args:
            symptoms (str): Original symptom description
            
        Returns:
            Dict[str, Any]: Fallback recommendation structure
        """
        logger.info("Providing fallback recommendation due to processing failure")
        
        # Analyze symptoms for basic urgency indicators
        urgency = self._assess_basic_urgency(symptoms)
        
        fallback_response = {
            "specialist": "General Physician",
            "reasoning": "Unable to process symptoms due to technical issues. A general physician can provide initial evaluation and refer you to the appropriate specialist if needed.",
            "urgency": urgency,
            "alternative": "Emergency Medicine (if symptoms are severe or life-threatening)",
            "additional_notes": "Please seek immediate medical attention if you experience severe symptoms such as chest pain, difficulty breathing, severe bleeding, or loss of consciousness."
        }
        
        return fallback_response
    
    def _assess_basic_urgency(self, symptoms: str) -> str:
        """
        Perform basic urgency assessment based on keyword analysis.
        
        Args:
            symptoms (str): Symptom description
            
        Returns:
            str: Urgency level (High, Medium, Low)
        """
        if not symptoms:
            return "Medium"
        
        symptoms_lower = symptoms.lower()
        
        # High urgency keywords
        high_urgency_keywords = [
            'chest pain', 'difficulty breathing', 'shortness of breath',
            'severe pain', 'bleeding', 'unconscious', 'seizure',
            'stroke', 'heart attack', 'emergency', 'severe headache',
            'high fever', 'vomiting blood', 'severe abdominal pain'
        ]
        
        # Low urgency keywords
        low_urgency_keywords = [
            'mild', 'occasional', 'minor', 'slight', 'small rash',
            'dry skin', 'minor headache', 'light cough'
        ]
        
        # Check for high urgency indicators
        for keyword in high_urgency_keywords:
            if keyword in symptoms_lower:
                return "High"
        
        # Check for low urgency indicators
        for keyword in low_urgency_keywords:
            if keyword in symptoms_lower:
                return "Low"
        
        # Default to medium urgency
        return "Medium"