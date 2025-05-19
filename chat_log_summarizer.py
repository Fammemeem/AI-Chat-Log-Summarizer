import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))

def read_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as chat:
        return chat.readlines()

def parse_chat(chat_lines):
    user_message = []
    ai_message = []
    for line in chat_lines:
        line = line.strip()
        if line.startswith('User:'):
            user_message.append(line[5:].strip())  
        elif line.startswith('AI:'):
            ai_message.append(line[3:].strip())   
    return user_message, ai_message

def keyword_count(text_list):
    words = []
    for text in text_list:
        tokens = word_tokenize(text.lower())
        
        filtered = []
        for word in tokens:
            if word.isalpha() and word not in stop_words:
                filtered.append(word)
        
        words.extend(filtered)
    
    return Counter(words)


def chat_log_summarizer(file_path):
    lines = read_chat(file_path)
    user_message, ai_message = parse_chat(lines)

    total_message = len(user_message) + len(ai_message)
    user_word_counts = keyword_count(user_message)
    ai_word_counts = keyword_count(ai_message)

    total_keywords = user_word_counts + ai_word_counts
    common_keywords = total_keywords.most_common(5)

    print("Summary:")

    print("- The conversation had " + str(total_message) + " exchanges.")

    if common_keywords:
        first_keyword = common_keywords[0][0].capitalize()

        if len(common_keywords) > 1:
            second_keyword = common_keywords[1][0].lower() + 's'
            topic_sentence = "The user asked mainly about " + first_keyword + " and its " + second_keyword + "."
        else:
            topic_sentence = "The user asked mainly about " + first_keyword + "."

        print("- " + topic_sentence)

    capitalized_keywords = []
    for keyword, _ in common_keywords:
        capitalized_keywords.append(keyword.capitalize())

    keyword_string = ", ".join(capitalized_keywords)
    print("- Most common keywords: " + keyword_string + ".")


if __name__ == '__main__':
    chat_log_summarizer("chat.txt")

