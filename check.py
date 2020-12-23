import requests

def pretty_print(text,content):
    content = content.decode('utf8')
    print(text.format(content))

#GET-запрос, возвращающий время в заданной временной зоне
print('Тест №1:GET-запрос, возвращающий время в заданной временной зоне')
res = requests.get('http://localhost:8051/America/New_York/')
pretty_print('Время в Нью-Йорке: {}',res.content)

res = requests.get('http://localhost:8051/Europe/London/')
pretty_print('Время в Лондоне: {}',res.content)

res = requests.get('http://localhost:8051/')
pretty_print('Время по Гринвичу: {}',res.content)
print('-'*40)

#POST-запрос, возвращающий время в заданной временной зоне на основе времени из другой временной зоны
print('Тест №2:POST-запрос, возвращающий время в заданной временной зоне на основе времени из другой временной зоны')
data = {
    'date': '10.22.2020 03:51:05',
    'tz': 'America/New_York',
    'target_tz':'Europe/London'
}
res = requests.post('http://localhost:8051/api/v1/convert',data=data)
pretty_print('Время в Лондоне, при заданном времени в Нью-Йорке: {}', res.content)

data = {
    'date': '07.10.2020 03:33:05',
    'tz': 'Europe/Moscow',
    'target_tz':'Europe/Amsterdam'
}
res = requests.post('http://localhost:8051/api/v1/convert',data=data)
pretty_print('Время в Амстердаме, при заданном времени в Москве: {}', res.content)
print('-'*40)

#POST-запрос, возвращающий кол-во секунд между заданным временем
print('Тест №3:POST-запрос, возвращающий кол-во секунд между заданным временем')
data = {
    'first_date':'12.20.2021 22:21:05',
    'first_tz': 'EST',
    'second_date':'12:30pm 2020-12-01',
    'second_tz': 'Europe/Moscow'
}
res = requests.post('http://localhost:8051/api/v1/datediff',data=data)
pretty_print('Разница в секундах между заданными моментами времени: {}', res.content)

data = {
    'first_date':'10.20.2020 17:22:04',
    'first_tz': 'America/New_York',
    'second_date':'04:30am 2020-08-03',
    'second_tz': 'Europe/Amsterdam'
}
res = requests.post('http://localhost:8051/api/v1/datediff',data=data)
pretty_print('Разница в секундах между заданными моментами времени: {}', res.content)