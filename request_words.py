import requests
from bs4 import BeautifulSoup

def get_definition(word):
    url = f"https://dle.rae.es/{word}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_tag = soup.find("meta", property="og:description")
        if meta_tag:
            return meta_tag['content']
        else:
            return "Definición no encontrada"
    else:
        return "Definición no encontrada"

def process_word_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        words = f.read().splitlines()

    word_definitions = {}
    for word in words:
        definition = get_definition(word)
        word_definitions[word] = definition
    return word_definitions

if __name__ == "__main__":
    file_path = "rae_words.txt"
    word_definitions = process_word_list(file_path)
    file_out = "full_rae_dic.txt"
    with open(file_out, 'w', encoding='utf-8') as f:
        for word, definition in word_definitions.items():
            f.write(f"{word}: {definition}\n")
