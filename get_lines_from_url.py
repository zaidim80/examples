import requests


# в данном примере все строки фиксированного размера,
# но несложно заменить на проверку минимального размера
STR_SIZE = 7

# источник с текстовым файлом большого размера
SRC_URL = "http://localhost:9000/storage/cards.txt"

# в реальном окружении понадобится добавить обработку исключений
counter = 0
errors = 0
with requests.get(SRC_URL, stream=True) as r:
    r.raise_for_status()
    last = ""
    for chunk in r.iter_content(chunk_size=8192):
        chunk_lines = chunk.splitlines()
        chunk_lines[0] = last.encode() + chunk_lines[0]
        chunk_len = len(chunk_lines)
        # в случае нефиксированного размера строк данная логика потребует доработки
        if chunk_len > 1 and len(chunk_lines[-1].decode()) < STR_SIZE:
            # в случае наличия в конце списка короткой строки сохраняем её
            last = chunk_lines[-1].decode()
            chunk_len -= 1
        else:
            last = ""
        for i in range(0, chunk_len):
            # преобразование байт-массива в строку и удаление переводов строки
            # при необходимости можно расширить список "лишних" символов
            # .strip("\n\r \t\ufeff") - удаление также табуляций и неразрывных пробелов
            s = chunk_lines[i].decode().strip()
            if len(s) == STR_SIZE:
                # считаем строку и при необходимости производим с ней некоторые действия
                counter += 1
                # todo: обработка строки
            elif len(s) > 0:
                # считаем пропущенные строки
                errors += 1
print(f"Прочитано строк: {counter}, ошибок чтения: {errors}")
