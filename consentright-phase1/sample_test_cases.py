"""
Sample Test Cases for ConsentRight Medical Consultation System

This module contains various symptom scenarios and their expected outputs for testing
and demonstration purposes. These cases help validate the LLM's performance and
provide examples for educational use.

Usage:
    python sample_test_cases.py

This will run through all test cases and display the results, allowing you to
verify that the system is working correctly and producing reasonable recommendations.
"""

import os
import sys
from typing import Dict, List, Any
from dotenv import load_dotenv

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_handler import ConsultationLLM


class TestCase:
    """
    Represents a single test case with symptoms and expected outcomes.
    """
    
    def __init__(self, name: str, symptoms: str, expected_specialist: str, 
                 expected_urgency: str, description: str = ""):
        self.name = name
        self.symptoms = symptoms
        self.expected_specialist = expected_specialist
        self.expected_urgency = expected_urgency
        self.description = description


# Comprehensive test cases covering different medical specialties and scenarios
SAMPLE_TEST_CASES = [
    
    # Cardiology Cases
    TestCase(
        name="Acute Chest Pain",
        symptoms="I have severe chest pain that started suddenly, along with shortness of breath and sweating",
        expected_specialist="Cardiologist",
        expected_urgency="High",
        description="Classic cardiac emergency symptoms requiring immediate attention"
    ),
    
    TestCase(
        name="Heart Palpitations",
        symptoms="I've been experiencing irregular heartbeat and palpitations for the past week",
        expected_specialist="Cardiologist", 
        expected_urgency="Medium",
        description="Cardiac rhythm issues that need evaluation but not immediately life-threatening"
    ),
    
    # Neurology Cases
    TestCase(
        name="Severe Migraine",
        symptoms="I have intense headaches with nausea, vomiting, and sensitivity to light for 3 days",
        expected_specialist="Neurologist",
        expected_urgency="Medium",
        description="Classic migraine presentation requiring neurological evaluation"
    ),
    
    TestCase(
        name="Stroke Symptoms",
        symptoms="Sudden weakness on my left side, difficulty speaking, and facial drooping",
        expected_specialist="Neurologist",
        expected_urgency="High", 
        description="Potential stroke symptoms requiring emergency neurological care"
    ),
    
    # Dermatology Cases
    TestCase(
        name="Persistent Rash",
        symptoms="I have an itchy red rash on my arms and legs that's been there for 2 weeks",
        expected_specialist="Dermatologist",
        expected_urgency="Low",
        description="Chronic skin condition requiring dermatological examination"
    ),
    
    TestCase(
        name="Suspicious Mole",
        symptoms="I noticed a mole on my back that has changed color and size recently",
        expected_specialist="Dermatologist",
        expected_urgency="Medium",
        description="Potential skin cancer concern requiring prompt dermatological evaluation"
    ),
    
    # Gastroenterology Cases
    TestCase(
        name="Severe Abdominal Pain",
        symptoms="Sharp abdominal pain in the lower right side with nausea and fever",
        expected_specialist="Gastroenterologist",
        expected_urgency="High",
        description="Possible appendicitis or other serious abdominal condition"
    ),
    
    TestCase(
        name="Chronic Digestive Issues",
        symptoms="I've had persistent bloating, diarrhea, and stomach cramps for several months",
        expected_specialist="Gastroenterologist",
        expected_urgency="Medium",
        description="Chronic gastrointestinal symptoms requiring specialized evaluation"
    ),
    
    # Orthopedic Cases
    TestCase(
        name="Sports Injury",
        symptoms="I injured my knee playing basketball, it's swollen and I can't put weight on it",
        expected_specialist="Orthopedist",
        expected_urgency="Medium",
        description="Acute musculoskeletal injury requiring orthopedic assessment"
    ),
    
    TestCase(
        name="Chronic Back Pain",
        symptoms="I've had lower back pain for months that gets worse with sitting",
        expected_specialist="Orthopedist",
        expected_urgency="Low",
        description="Chronic musculoskeletal condition requiring orthopedic evaluation"
    ),
    
    # Psychiatry Cases
    TestCase(
        name="Depression Symptoms",
        symptoms="I've been feeling extremely sad, hopeless, and have lost interest in activities for weeks",
        expected_specialist="Psychiatrist",
        expected_urgency="Medium",
        description="Mental health symptoms requiring psychiatric evaluation"
    ),
    
    TestCase(
        name="Anxiety and Panic",
        symptoms="I have frequent panic attacks with racing heart, sweating, and fear of dying",
        expected_specialist="Psychiatrist",
        expected_urgency="Medium",
        description="Anxiety disorder symptoms requiring mental health treatment"
    ),
    
    # ENT Cases
    TestCase(
        name="Hearing Loss",
        symptoms="I've noticed gradual hearing loss in my right ear over the past month",
        expected_specialist="ENT",
        expected_urgency="Medium",
        description="Hearing impairment requiring ENT specialist evaluation"
    ),
    
    TestCase(
        name="Chronic Sinus Issues",
        symptoms="I have persistent nasal congestion, facial pressure, and thick discharge for weeks",
        expected_specialist="ENT",
        expected_urgency="Low",
        description="Chronic sinusitis requiring ENT evaluation"
    ),
    
    # Ophthalmology Cases
    TestCase(
        name="Vision Changes",
        symptoms="I'm experiencing blurred vision and seeing flashing lights in my peripheral vision",
        expected_specialist="Ophthalmologist",
        expected_urgency="High",
        description="Potential retinal detachment requiring urgent eye care"
    ),
    
    TestCase(
        name="Eye Infection",
        symptoms="My eye is red, painful, and producing yellow discharge",
        expected_specialist="Ophthalmologist",
        expected_urgency="Medium",
        description="Eye infection requiring ophthalmological treatment"
    ),
    
    # Gynecology Cases
    TestCase(
        name="Irregular Periods",
        symptoms="I've been having irregular menstrual cycles and heavy bleeding for several months",
        expected_specialist="Gynecologist",
        expected_urgency="Medium",
        description="Gynecological symptoms requiring specialized women's health evaluation"
    ),
    
    # General Medicine Cases
    TestCase(
        name="General Flu Symptoms",
        symptoms="I have fever, body aches, fatigue, and a mild cough for 3 days",
        expected_specialist="General Physician",
        expected_urgency="Low",
        description="Common viral illness symptoms suitable for general medical care"
    ),
    
    # Emergency Medicine Cases
    TestCase(
        name="Multiple Trauma",
        symptoms="I was in a car accident and have multiple injuries including head trauma",
        expected_specialist="Emergency Medicine",
        expected_urgency="High",
        description="Multiple trauma requiring immediate emergency medical care"
    ),
    
    # Rheumatology Cases
    TestCase(
        name="Joint Pain and Stiffness",
        symptoms="I have morning stiffness and pain in multiple joints, especially hands and knees",
        expected_specialist="Rheumatologist",
        expected_urgency="Medium",
        description="Possible autoimmune or inflammatory joint condition"
    ),
    
    # Edge Cases and Complex Scenarios
    TestCase(
        name="Vague Symptoms",
        symptoms="I just don't feel well, tired all the time",
        expected_specialist="General Physician",
        expected_urgency="Low",
        description="Non-specific symptoms best evaluated by general medicine first"
    ),
    
    TestCase(
        name="Multiple System Symptoms",
        symptoms="I have chest pain, dizziness, nausea, and shortness of breath",
        expected_specialist="Cardiologist",  # Most likely given the combination
        expected_urgency="High",
        description="Multi-system symptoms that could indicate serious cardiac condition"
    )
]


def run_test_case(consultation_llm: ConsultationLLM, test_case: TestCase) -> Dict[str, Any]:
    """
    Run a single test case and return the results.
    
    Args:
        consultation_llm (ConsultationLLM): Initialized LLM handler
        test_case (TestCase): Test case to run
        
    Returns:
        Dict[str, Any]: Test results including actual vs expected outcomes
    """
    try:
        print(f"\n{'='*60}")
        print(f"🧪 TEST CASE: {test_case.name}")
        print(f"{'='*60}")
        print(f"📝 Description: {test_case.description}")
        print(f"🔍 Symptoms: {test_case.symptoms}")
        print(f"🎯 Expected Specialist: {test_case.expected_specialist}")
        print(f"⚡ Expected Urgency: {test_case.expected_urgency}")
        
        print(f"\n🔄 Processing...")
        
        # Process the symptoms
        result = consultation_llm.process_symptoms(test_case.symptoms)
        
        # Extract results
        actual_specialist = result.get('specialist', 'Unknown')
        actual_urgency = result.get('urgency', 'Unknown')
        reasoning = result.get('reasoning', 'No reasoning provided')
        alternative = result.get('alternative', '')
        
        # Check if results match expectations
        specialist_match = actual_specialist == test_case.expected_specialist
        urgency_match = actual_urgency == test_case.expected_urgency
        
        # Display results
        print(f"\n📊 RESULTS:")
        print(f"   🏥 Actual Specialist: {actual_specialist} {'✅' if specialist_match else '❌'}")
        print(f"   ⚡ Actual Urgency: {actual_urgency} {'✅' if urgency_match else '❌'}")
        print(f"   💭 Reasoning: {reasoning}")
        if alternative:
            print(f"   🔄 Alternative: {alternative}")
        
        # Overall assessment
        overall_success = specialist_match and urgency_match
        print(f"\n🎯 OVERALL: {'✅ PASS' if overall_success else '❌ FAIL'}")
        
        return {
            'test_case': test_case.name,
            'success': overall_success,
            'specialist_match': specialist_match,
            'urgency_match': urgency_match,
            'actual_specialist': actual_specialist,
            'actual_urgency': actual_urgency,
            'reasoning': reasoning,
            'alternative': alternative
        }
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return {
            'test_case': test_case.name,
            'success': False,
            'error': str(e),
            'specialist_match': False,
            'urgency_match': False
        }


def run_all_test_cases(api_key: str, selected_cases: List[str] = None) -> Dict[str, Any]:
    """
    Run all test cases or a selected subset.
    
    Args:
        api_key (str): Google Gemini API key
        selected_cases (List[str], optional): List of test case names to run
        
    Returns:
        Dict[str, Any]: Summary of all test results
    """
    try:
        # Initialize the LLM handler
        print("🚀 Initializing ConsentRight consultation system...")
        consultation_llm = ConsultationLLM(api_key)
        print("✅ System initialized successfully!")
        
        # Filter test cases if specific ones are selected
        cases_to_run = SAMPLE_TEST_CASES
        if selected_cases:
            cases_to_run = [case for case in SAMPLE_TEST_CASES if case.name in selected_cases]
            print(f"\n🎯 Running {len(cases_to_run)} selected test cases...")
        else:
            print(f"\n🎯 Running all {len(cases_to_run)} test cases...")
        
        results = []
        successful_tests = 0
        
        # Run each test case
        for i, test_case in enumerate(cases_to_run, 1):
            print(f"\n📍 Progress: {i}/{len(cases_to_run)}")
            result = run_test_case(consultation_llm, test_case)
            results.append(result)
            
            if result.get('success', False):
                successful_tests += 1
            
            # Add a small delay between tests to avoid rate limiting
            if i < len(cases_to_run):
                import time
                time.sleep(1)
        
        # Generate summary
        total_tests = len(cases_to_run)
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n{'='*60}")
        print(f"📈 TEST SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Successful Tests: {successful_tests}/{total_tests}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        # Show failed tests if any
        failed_tests = [r for r in results if not r.get('success', False)]
        if failed_tests:
            print(f"\n❌ Failed Tests:")
            for failed in failed_tests:
                print(f"   • {failed['test_case']}")
                if 'error' in failed:
                    print(f"     Error: {failed['error']}")
        
        return {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': success_rate,
            'results': results,
            'failed_tests': failed_tests
        }
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        return {
            'total_tests': 0,
            'successful_tests': 0,
            'success_rate': 0,
            'error': str(e)
        }


def main():
    """
    Main function to run sample test cases.
    """
    print("🏥 ConsentRight Sample Test Cases")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in environment variables.")
        print("\nPlease ensure you have:")
        print("1. Created a .env file with your API key")
        print("2. Set GEMINI_API_KEY=your_actual_api_key")
        return
    
    # Check if user wants to run specific test cases
    if len(sys.argv) > 1:
        if sys.argv[1] == '--list':
            print("\n📋 Available Test Cases:")
            for i, case in enumerate(SAMPLE_TEST_CASES, 1):
                print(f"{i:2d}. {case.name}")
                print(f"    {case.description}")
            return
        elif sys.argv[1] == '--quick':
            # Run a quick subset of tests
            quick_cases = [
                "General Flu Symptoms",
                "Acute Chest Pain", 
                "Persistent Rash",
                "Severe Migraine"
            ]
            print("\n🚀 Running quick test suite...")
            run_all_test_cases(api_key, quick_cases)
            return
    
    # Run all test cases
    print("\n🚀 Running comprehensive test suite...")
    print("This may take several minutes due to API rate limiting...")
    
    try:
        summary = run_all_test_cases(api_key)
        
        if summary['success_rate'] >= 80:
            print(f"\n🎉 Excellent! The system is performing well.")
        elif summary['success_rate'] >= 60:
            print(f"\n👍 Good performance, but there's room for improvement.")
        else:
            print(f"\n⚠️  The system may need tuning or there could be API issues.")
            
        print(f"\n💡 Tips for improving results:")
        print(f"   • Ensure stable internet connection")
        print(f"   • Check API key permissions")
        print(f"   • Review failed cases for pattern analysis")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed: {str(e)}")


if __name__ == "__main__":
    main()