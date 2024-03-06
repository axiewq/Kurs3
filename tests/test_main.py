import json
from main import load_operations, sorted_by_type, FILE_PATH, formatted_date, masked_account, results
import pytest
from datetime import datetime

# Путь к тестовым данным
TEST_DATA_PATH = FILE_PATH


# Фикстура для загрузки тестовых данных
@pytest.fixture
def test_data():
    with open(TEST_DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


# Тесты для функции load_operations()
def test_load_operations(test_data):
    operations = load_operations()
    assert isinstance(operations, list)
    assert len(operations) == len(test_data)


# Тест для функции sorted_by_type()
def test_sorted_by_type(test_data):
    executed_operations = sorted_by_type(test_data)
    assert len(executed_operations) <= 5
    for operation in executed_operations:
        assert operation['state'] == 'EXECUTED'


# Тест для функции formatted_date()
def test_formatted_date(test_data):
    date_string = test_data[0]['date']
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')
    formatted_dates = formatted_date([{'date': date_string}])
    assert formatted_dates == [date_object.strftime('%d.%m.%Y')]


# Тесты для функции masked_account()
def test_masked_account_empty():
    assert masked_account('') == ''


def test_masked_account_card():
    card_number = '1234567812345678'
    masked = masked_account(card_number).strip()
    assert masked == '1234 56** **** 5678'


def test_masked_account_account():
    account = 'Счет 19708645243227258542 '
    assert masked_account(account) == 'Счет **8542'


# Тест для функции results()
from main import formatted_date, masked_account, results

def test_results(capsys):
    operation = {
        'date': '2023-12-31T23:59:59.999',
        'description': 'Test operation',
        'from': '1234567812345678',
        'to': 'Счет 1234567890',
        'operationAmount': {'amount': 100, 'currency': {'name': 'RUB'}}
    }
    formatted_dates = formatted_date([operation])
    results([operation])
    captured = capsys.readouterr()
    expected_output = f"{formatted_dates[0]} {operation['description']}\n{masked_account(operation['from'])} -> {masked_account(operation['to'])}\n{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}\n\n"
    assert captured.out == expected_output
