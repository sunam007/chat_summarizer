import os
import re

def read_chat_file(file_path):
    user_messages = []
    ai_messages = []
    
    """
    Regular expressions to handle various edge cases like 
    
        Normal case:       'User: Hello'
        Case variations:   'USER: Hi', 'ai: Hey'
        Whitespace:        ' User :   Hello  '
        Malformed:         'User- Hello' (skipped)
        Multi-line:        'User: Line1\n      Line2'
    """
    user_pattern = re.compile(r'^\s*user\s*:\s*(.*)$', re.IGNORECASE)
    ai_pattern = re.compile(r'^\s*ai\s*:\s*(.*)$', re.IGNORECASE)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                # Check for user message (any case)
                user_match = user_pattern.match(line)
                if user_match:
                    message = user_match.group(1).strip()
                    if message:  # Only add if there's content
                        user_messages.append(message)
                    continue
                
                # Check for AI message (any case)
                ai_match = ai_pattern.match(line)
                if ai_match:
                    message = ai_match.group(1).strip()
                    if message:
                        ai_messages.append(message)
                    continue
                
                # Handles lines that has unrecognized patterns
                print(f"Skipping unrecognized line format: {line}")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return [], []
    except UnicodeDecodeError:
        print(f"Error: Could not decode file at {file_path}")
        return [], []

    return user_messages, ai_messages

if __name__ == "__main__":
    file_path = "chatlogs/chat1.txt"
    if os.path.exists(file_path):
        user_msgs, ai_msgs = read_chat_file(file_path)

        print("User messages:")
        for msg in user_msgs:
            print("-" , msg)
        
        print("\nAI messages:")
        for msg in ai_msgs:
            print("-" , msg)
    
    else:
        print(f"{file_path} not found")