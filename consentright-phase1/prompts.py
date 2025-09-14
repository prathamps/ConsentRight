"""
Prompt templates and configuration for ConsentRight medical consultation system.

This module contains structured prompt templates for LangChain integration,
specialist definitions, and output formatting templates for consistent LLM responses.
"""

from langchain.prompts import PromptTemplate

# List of all 12 medical specialties as defined in requirements
SPECIALIST_LIST = [
    "Cardiologist",
    "Neurologist", 
    "Dermatologist",
    "Gastroenterologist",
    "Orthopedist",
    "Psychiatrist",
    "ENT",
    "Ophthalmologist",
    "Gynecologist",
    "General Physician",
    "Emergency Medicine",
    "Rheumatologist"
]

# Expected output format template for consistent LLM responses
OUTPUT_FORMAT = """
Please respond in the following JSON format:
{
    "specialist": "Primary recommended specialist from the list",
    "reasoning": "Clear explanation for why this specialist is recommended",
    "urgency": "High/Medium/Low - urgency level based on symptoms",
    "alternative": "Alternative specialist if applicable (optional)",
    "additional_notes": "Any extra guidance or recommendations (optional)"
}
"""

# Main consultation prompt template with few-shot examples
CONSULTATION_PROMPT = PromptTemplate(
    input_variables=["symptoms"],
    template="""You are a medical consultation AI assistant that helps users identify which medical specialist they should consult based on their symptoms. 

Available specialists: {specialist_list}

Your task is to analyze the provided symptoms and recommend the most appropriate specialist, along with reasoning and urgency level.

{output_format}

Here are some examples of good responses:

Example 1:
Symptoms: "I have been experiencing chest pain and shortness of breath for the past few days"
Response:
{{
    "specialist": "Cardiologist",
    "reasoning": "Chest pain and shortness of breath are classic cardiovascular symptoms that require cardiac evaluation to rule out heart conditions",
    "urgency": "High",
    "alternative": "Emergency Medicine",
    "additional_notes": "If symptoms are severe or worsening, seek immediate emergency care"
}}

Example 2:
Symptoms: "I have a persistent rash on my arms that's been itchy for two weeks"
Response:
{{
    "specialist": "Dermatologist",
    "reasoning": "Persistent skin rash with itching indicates a dermatological condition that requires specialized skin examination",
    "urgency": "Low",
    "alternative": "General Physician",
    "additional_notes": "Avoid scratching and consider over-the-counter antihistamines for temporary relief"
}}

Example 3:
Symptoms: "I've been having severe headaches with nausea and sensitivity to light"
Response:
{{
    "specialist": "Neurologist",
    "reasoning": "Severe headaches combined with nausea and photophobia suggest possible neurological conditions like migraines or other brain-related issues",
    "urgency": "Medium",
    "alternative": "General Physician",
    "additional_notes": "Keep a headache diary noting triggers, duration, and severity"
}}

Now analyze these symptoms and provide your recommendation:

Symptoms: {symptoms}

Response:""".format(
        specialist_list=", ".join(SPECIALIST_LIST),
        output_format=OUTPUT_FORMAT
    )
)