def categorize_error(error):
    error_str = str(error).lower()
    if any(k in error_str for k in ['timeout', 'connection', 'network', 'unreachable']):
        return {"category": "network", "message": "Network connection issue.", "suggestions": ["Check your internet connection", "Try again later"]}
    if any(k in error_str for k in ['api key', 'authentication', 'unauthorized', 'forbidden']):
        return {"category": "auth", "message": "API authentication issue.", "suggestions": ["Verify your GEMINI_API_KEY", "Check API permissions"]}
    if any(k in error_str for k in ['rate limit', 'quota', 'too many requests']):
        return {"category": "rate_limit", "message": "API rate limit exceeded.", "suggestions": ["Wait before trying again"]}
    if any(k in error_str for k in ['service unavailable', 'server error', 'internal error']):
        return {"category": "service", "message": "AI service unavailable.", "suggestions": ["Try again later"]}
    if any(k in error_str for k in ['invalid', 'validation', 'parse', 'format']):
        return {"category": "input", "message": "Input processing issue.", "suggestions": ["Rephrase your symptoms"]}
    return {"category": "unknown", "message": "Unexpected error.", "suggestions": ["Try again", "Restart the app"]}

def _display_error_with_guidance(error, attempt_number=1):
    info = categorize_error(error)
    print(f"\n❌ {info['message']}")
    print("\nSuggestions:")
    for s in info['suggestions']:
        print(f"   • {s}")
    if attempt_number >= 3:
        print("\nIf urgent, contact a doctor or emergency services.")

