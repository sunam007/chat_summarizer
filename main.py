import os
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


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


    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return [], []
    
    except UnicodeDecodeError:
        print(f"Error: Could not decode file at {file_path}")
        return [], []

    return user_messages, ai_messages

def extract_keywords(user_msgs, ai_msgs, top_n=5):
    # combine all messages
    text = ' '.join(user_msgs + ai_msgs).lower()

    # Tokenize the text
    tokens = word_tokenize(text)

    # remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    cleaned = [
        word for word in tokens
        if word.isalnum() and word not in stop_words
    ]

    # count most common keywords
    keyword_freq = Counter(cleaned)
    return keyword_freq.most_common(top_n)

def summarize_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            user_msgs, ai_msgs = read_chat_file(file_path)

            print("=" * 50) # creates a divider for separating multiple chat summaries

            print(f"Summary for: {filename}")
            print("-" * 50)

            # Message Stats
            total_messages = len(user_msgs) + len(ai_msgs)
            print(f"Total Messages: {total_messages} (User: {len(user_msgs)} | AI: {len(ai_msgs)})\n") # prints the message counts of user and ai

            # Top Keywords
            keywords = extract_keywords(user_msgs, ai_msgs)
            keyword_list = [word for word, _ in keywords]
            print(f"The conversation mainly focused on these top keywords: {', '.join(keyword_list)}" + "\n")

            # User Messages
            print("- User Messages:")
            for msg in user_msgs:
                print("     -", msg)
            

            # AI Messages
            print("\n" +"- AI Messages:")
            for msg in ai_msgs:
                print("     -", msg)

            print("=" * 50 + "\n") # creates a divider for separating multiple chat summaries


if __name__ == "__main__":
    folder_path = "chatlogs"
    if os.path.exists(folder_path):
        summarize_folder(folder_path)
    else:
        print(f"{folder_path} folder not found.")
