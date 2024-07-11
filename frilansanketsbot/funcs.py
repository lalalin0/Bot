import datetime
from config import database


def read_file(file):
    """Читает содержимое файла и возвращает его как строку."""
    try:
        with open(file, mode='r', encoding='utf-8') as f:
            contents = f.read()
        return contents
    except FileNotFoundError:
        print(f"File {file} not found.")
        return ""
    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return ""


def write_file(file, contents):
    """Записывает строку contents в файл file."""
    try:
        with open(file, mode='w', encoding='utf-8') as f:
            f.write(contents)
    except Exception as e:
        print(f"Error writing to file {file}: {e}")


def checker(text):
    """Проверяет, содержит ли текст какие-либо ключевые слова из базы данных."""
    keywords = database.get_all_keywords()
    print(keywords)
    for category, keyword in keywords:
        if keyword.lower() in text.lower():
            print(keyword)
            return True
    return False


def read_file_s(filename):
    """Читает содержимое файла и возвращает список строк."""
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            contents = file.read()
        return contents.split()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return []


def timee(user_id):
    """Проверяет, находится ли текущее время в пределах заданного интервала."""
    try:
        current_hour = datetime.datetime.now().hour
        time_range = database.select_ints(user_id, "time")
        start_hour, end_hour = map(int, time_range.split("-"))
        return start_hour <= current_hour < end_hour
    except Exception as e:
        print(f"Error checking time for user {user_id}: {e}")
        return False
