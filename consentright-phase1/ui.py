import sys

def display_welcome():
    print("\n" + "="*60)
    print("Welcome to ConsentRight - Medical Consultation Assistant")
    print("="*60)
    print("\nDescribe your symptoms in detail. Type 'quit' or 'exit' to end.")
    print("-"*60)

def display_result(result):
    print("\n" + "="*60)
    print("CONSULTATION RESULT")
    print("="*60)
    print(f"\nRECOMMENDED SPECIALIST: {result.get('specialist', 'Unknown')}")
    print(f"URGENCY LEVEL: {result.get('urgency', 'Medium')}")
    print(f"\nREASONING:\n   {result.get('reasoning', 'No reasoning provided')}")
    alt = result.get('alternative', '')
    if alt and alt.strip():
        print(f"\nALTERNATIVE SPECIALIST: {alt}")
    notes = result.get('additional_notes', '')
    if notes and notes.strip():
        print(f"\nADDITIONAL NOTES:\n   {notes}")
    print("\n" + "-"*60)
    print("IMPORTANT: This is AI-generated. Consult a healthcare professional.")
    print("-"*60)

def ask_continue():
    while True:
        try:
            response = input("\nWould you like another consultation? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no', 'quit', 'exit']:
                return False
        except KeyboardInterrupt:
            print()
            return False
        except EOFError:
            print()
            return False

def get_user_input():
    while True:
        try:
            user_input = input("\nPlease describe your symptoms:\n> ").strip()
            if user_input.lower() in ['quit', 'exit', 'q', 'stop']:
                print("\nThank you for using ConsentRight. Take care of your health!")
                sys.exit(0)
            from validation import validate_symptom_input
            validation_result = validate_symptom_input(user_input)
            if validation_result["valid"]:
                return validation_result["cleaned_input"]
            else:
                print(f"\n❌ {validation_result['error_message']}")
        except KeyboardInterrupt:
            print("\nSession interrupted by user.")
            sys.exit(0)
        except EOFError:
            print("\nInput stream ended unexpectedly.")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")

