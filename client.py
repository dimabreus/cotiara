import requests
import json

# URL вашего API
url = 'https://cotiara.onrender.com/run'

# Код JavaScript, который вы хотите выполнить
code = """
var a = 1 + 1

echo %a%
"""

# Формирование тела запроса
payload = json.dumps({
    'code': code
})

# Заголовки запроса
headers = {
    'Content-Type': 'application/json'
}

# Отправка POST-запроса
response = requests.post(url, headers=headers, data=payload)

# Вывод ответа от сервера
print(response.json())
