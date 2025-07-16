import json
import sys

def verify_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"SUCCESS: '{file_path}' is a valid JSON file.")
        return True
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in '{file_path}'.")
        print(f"Details: {e}")
        return False
    except FileNotFoundError:
        print(f"ERROR: File not found at '{file_path}'.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_json.py <file_path>")
        sys.exit(1)
    
    file_to_check = sys.argv[1]
    if not verify_json(file_to_check):
        sys.exit(1)
