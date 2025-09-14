import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts import CONSULTATION_PROMPT

class ConsultationLLM:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API key is required")
        try:
            self.llm = ChatGoogleGenerativeAI(
                google_api_key=api_key,
                model="gemini-2.5-flash",
                temperature=0.3,
                max_output_tokens=1024
            )
        except Exception:
            self.llm = ChatGoogleGenerativeAI(
                google_api_key=api_key,
                model="gemini-pro",
                temperature=0.3,
                max_output_tokens=1024
            )
        self.chain = CONSULTATION_PROMPT | self.llm

    def process_symptoms(self, symptoms):
        cleaned_symptoms = self._clean_input(symptoms)
        try:
            result = self.chain.invoke({"symptoms": cleaned_symptoms})
            response = result.content if hasattr(result, 'content') else str(result)
            print("\n[DEBUG] Raw LLM response:\n", response)
            return self._parse_response(response)
        except Exception as e:
            import traceback
            print("[DEBUG] Exception in LLM call or parsing:")
            print("Type:", type(e))
            print("Message:", e)
            print("Traceback:")
            traceback.print_exc()
            return self._fallback_recommendation(cleaned_symptoms, str(e))

    def _clean_input(self, symptoms):
        if not symptoms or len(symptoms.strip()) < 3:
            raise ValueError("Please provide more details about your symptoms")
        cleaned = re.sub(r'\s+', ' ', symptoms.strip())
        return cleaned[:1000]

    def _parse_response(self, response):
        import re
        import json
        # Remove Markdown code block if present
        code_block = re.search(r'```(?:json)?\s*([\s\S]+?)\s*```', response)
        if code_block:
            response = code_block.group(1)
        # Try to extract the largest valid JSON substring
        start = response.find('{')
        end = response.rfind('}') + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON found")
        json_str = response[start:end]
        try:
            data = json.loads(json_str)
            incomplete = False
        except json.JSONDecodeError:
            # Try to recover from truncated JSON by trimming to the last complete brace
            for i in range(len(json_str)-1, 0, -1):
                if json_str[i] == '}':
                    try:
                        data = json.loads(json_str[:i+1])
                        incomplete = True
                        break
                    except Exception:
                        continue
            else:
                raise ValueError("Failed to parse response")
        for field in ['specialist', 'reasoning', 'urgency']:
            if field not in data:
                data[field] = "Unknown"
        data.setdefault('alternative', '')
        data.setdefault('additional_notes', '')
        if incomplete:
            data['additional_notes'] += " [Warning: Output may be incomplete due to truncation.]"
        return data

    def _fallback_recommendation(self, symptoms, error):
        urgency = "High" if any(word in symptoms.lower() for word in ['chest pain', 'breathing', 'severe', 'blood']) else "Medium"
        return {
            "specialist": "General Physician",
            "reasoning": "Unable to analyze symptoms due to technical issue. A general physician can provide initial evaluation.",
            "urgency": urgency,
            "alternative": "Emergency Medicine (if severe)",
            "additional_notes": "Seek immediate care for severe symptoms."
        }