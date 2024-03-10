import time
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

def process_word_list(file_path, file):
    with open(file_path, 'r', encoding='utf-8') as f:
        words = f.read().splitlines()
    i = 0
    total_words = len(words)
    for word in words:
        retries = 3
        while retries > 0:
            try:
                definition = get_definition(word)
                break
            except Exception as e:
                print(f"oopsie doopsie retry")
                retries -= 1
                if retries == 0:
                    definition = "Definición no encontrada"
                else:
                    time.sleep(5)
        file.write(f"{word}: {definition}\n")
        i += 1
        if (i % 100 == 0):
            print(f"Hechas {i} definiciones de {total_words} palabras")

if __name__ == "__main__":
    file_path = "rae_words.txt"
    file_out = "rae_words_with_def.txt"
    with open(file_out, 'w', encoding='utf-8') as f:
        process_word_list(file_path, f)

