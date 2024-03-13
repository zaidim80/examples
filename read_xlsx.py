import xlrd3 as xlrd
import hashlib
import re


data = []
xlsx_path = "example.xlsx"
book = xlrd.open_workbook(xlsx_path)
sheet = book.sheet_by_index(1)
for rx in range(1, sheet.nrows):  # пропускаем заголовок в нулевой строке
    try:
        # предполагаем, что в колонках: телефон, дата отправки и текст смс с номеров карточки
        # из номера удаляем все лишние символы
        phone = re.sub("[^0-9]", "", str(sheet.cell_value(rx, 0)))
        if len(phone) != 11:
            raise Exception("Некорректный формат телефона")
        dt = xlrd.xldate.xldate_as_datetime(sheet.cell_value(rx, 1), 0)
        # из сообщения удаляем лишние символы
        msg = re.sub("[^0-9]", "", str(sheet.cell_value(rx, 2)))[:64]
        # хэшируем сообщение, формируя своеобразный ключ
        uid = hashlib.sha1(
            f"{phone}-{dt.strftime('%Y-%m-%d-%H:%M:%S')}-{msg}"
            .encode("utf-8")
        ).hexdigest()
        data.append({
            "uid": uid,
            "dt": dt,
            "phone": phone,
            "text": msg,
        })
    except Exception as e:
        print(f"Ошибка обработки сообщения ({xlsx_path}/{rx}) : {e}")
