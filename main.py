import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

# Создание функции для получения случайных английских слов
def get_english_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешного запроса
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

    try:
        # Создание объекта Soup
        soup = BeautifulSoup(response.content, "html.parser")
        # Получение слова и его объяснения
        english_word = soup.find("div", id="random_word").text.strip()
        word_definition = soup.find("div", id="random_word_definition").text.strip()
        # Возврат словаря с результатами
        return {
            "english_word": english_word,
            "word_definition": word_definition
        }
    except Exception as e:
        print(f"Произошла ошибка при парсинге HTML: {e}")
        return None

# Создание функции для перевода слова и его определения на русский язык
def translate_to_russian(english_word, word_definition):
    try:
        translator = GoogleTranslator(source='en', target='ru')
        translated_word = translator.translate(english_word)
        translated_definition = translator.translate(word_definition)
        return translated_word, translated_definition
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        return None, None

# Создание функции для игры
def word_game():
    print("Добро пожаловать в игру")

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
        print(f"Значение слова - {russian_definition}")
        user_guess = input("Что это за слово? ")

        if user_guess.lower() == russian_word.lower():
            print("Все верно!")
        else:
            print(f"Ответ неверный, правильное слово - {russian_word}")

        # Предложение сыграть еще раз
        play_again = input("Хотите сыграть еще раз? y/n: ")
        if play_again.lower() != "y":
            print("Спасибо за игру!")
            break

# Запуск игры
if __name__ == "__main__":
    word_game()

