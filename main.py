import json
import os
from datetime import datetime
from pprint import pprint

ROOT = os.path.dirname(__file__)
FILE_PATH = os.path.join(ROOT, 'source/operations.json')


def load_operations():
    with open(FILE_PATH, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


def sorted_by_type(operations):
    executed_operations = []
    for operation in operations:
        if operation.get('state') == 'EXECUTED':
            executed_operations.append(operation)
    sorted_executed_operations = sorted(executed_operations, reverse=True, key=lambda x: x['date'])
    return sorted_executed_operations[:5]


def formatted_date(last_5_executed_operations):
    formatted_dates = []
    for operation in last_5_executed_operations:
        date_string = operation['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')
        formatted_date = date_object.strftime('%d.%m.%Y')
        formatted_dates.append(formatted_date)
    return formatted_dates


def masked_account(account):
    if account == '':
        return ''

    elif 'счет' in account.lower():
        masked = account[:5] + '**' + account[-5:-1]
        return masked


    else:
        card_name = ''
        card_numb = ''
        for symb in account:
            if symb.isalpha() or symb == ' ':
                card_name += symb
            if symb.isdigit() or symb == ' ':
                card_numb += symb
        else:
            card_numb = card_numb.strip()
            card_numb = card_numb[:4] + ' ' + card_numb[4:6] + '** **** ' + card_numb[-4:]
            masked = card_name.strip() + ' ' + card_numb
            return masked


def results(last_5_executed_operations):
    for operation in last_5_executed_operations:
        formatted_dates = formatted_date([operation])
        description = operation['description']
        from_account = masked_account(operation.get('from', ''))
        to_account = masked_account(operation.get('to', ''))
        amount = operation['operationAmount']['amount']
        currency = operation['operationAmount']['currency']['name']
        print(f"{formatted_dates[0]} {description}")
        print(f"{from_account} -> {to_account}")
        print(f"{amount} {currency}\n")


# Загрузка операций
data = load_operations()

# Получение отсортированных данных и форматированных дат
last_5_executed_operations = sorted_by_type(data)
formatted_dates = formatted_date(last_5_executed_operations)

# Вывод результатов
results(last_5_executed_operations)