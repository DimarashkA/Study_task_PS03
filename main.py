import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from deep_translator import GoogleTranslator

def get_english_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        english_word = soup.find("div", id="random_word").text.strip()
        word_definition = soup.find("div", id="random_word_definition").text.strip()
        print(f"Слово: {english_word}, Определение: {word_definition}")  # Отладочный вывод
        return {
            "english_word": english_word,
            "word_definition": word_definition
        }
    except Exception as e:
        print(f"Произошла ошибка при получении слова: {e}")
        return None

def translate_to_russian(english_word, word_definition):
    try:
        # Пробуем использовать googletrans для перевода
        translator = Translator()
        translated_word_result = translator.translate(english_word, src='en', dest='ru')
        translated_definition_result = translator.translate(word_definition, src='en', dest='ru')

        if translated_word_result and translated_definition_result:
            translated_word = translated_word_result.text
            translated_definition = translated_definition_result.text
            return translated_word, translated_definition
        else:
            return None, None

    except Exception as e:
        print(f"Ошибка при переводе с помощью googletrans: {e}")

        # Альтернативный перевод с помощью deep_translator
        try:
            translated_word = GoogleTranslator(source='en', target='ru').translate(english_word)
            translated_definition = GoogleTranslator(source='en', target='ru').translate(word_definition)
            return translated_word, translated_definition

        except Exception as alt_e:
            print(f"Ошибка при переводе с помощью deep_translator: {alt_e}")
            return None, None

def word_game():
    print("**Добро пожаловать в игру**")
    while True:
        word_dict = get_english_words()
        if not word_dict:
            print("Ошибка при получении слова. Попробуйте позже.")
            break

        english_word = word_dict.get("english_word")
        word_definition = word_dict.get("word_definition")

        # Переводим слово и определение на русский язык
        russian_word, russian_definition = translate_to_russian(english_word, word_definition)
        if not russian_word or not russian_definition:
            print("Ошибка при переводе. Попробуйте позже.")
            break

        # Начало игры
        print(f"**Значение слова - {russian_definition}**")
        user = input("Что это за слово? ")
        if user.lower().strip() == russian_word.lower().strip():
            print("**Все верно!**")
        else:
            print(f"**Ответ неверный, было загадано это слово - {russian_word}**")

        # Создаём возможность закончить игру
        play_again = input("Хотите сыграть еще раз? y/n")
        if play_again.lower() != "y":
            print("**Спасибо за игру!**")
            break

word_game()
