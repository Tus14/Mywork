from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card
from src.generators import filter_by_currency, transaction_descriptions,card_number_generator

if __name__ == "__main__":
    card_mask = get_mask_card_number("7000792289606361")
    print(card_mask)
    account_mask = get_mask_account("73654108430135874305")
    print(account_mask)


if __name__ == "__main__":
    masked_number_add = mask_account_card("Счет 73654108430135874305")
    print(masked_number_add)


if __name__ == "__main__":
    new_date = get_date("2024-03-11T02:26:18.671407")
    print(new_date)


if __name__ == "__main__":
    new_list = filter_by_state(
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ]
    )
    print(new_list)


if __name__ == "__main__":
    new_dict = sort_by_date(
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ]
    )
    print(new_dict)


if __name__ == "__main__":
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 414288290,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {"name": "RUB", "code": "RUB"},
            },
            "description": "Перевод на карту Visa Classic",
            "from": "Счет 91446864726574786720",
            "to": "Счет 71408169819385550293",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 441945815,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "41096.36",
                "currency": {"name": "RUB", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 48284242693570777058",
            "to": "Счет 44168058198471844548",
        },
    ]
    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))


if __name__ == "__main__":
    transactions = [
        {
            "id": 939719570,
            "description": "Перевод организации",
            "state": "EXECUTED",
            # ... другие поля ...
        },
        {
            "id": 142264268,
            "description": "Перевод со счета на счет",
            "state": "EXECUTED",
            # ... другие поля ...
        },
        {
            "id": 414288290,
            "description": "Перевод со счета на счет",
            "state": "EXECUTED",
            # ... другие поля ...
        },
        {
            "id": 441945815,
            "description": "Перевод с карты на карту",
            "state": "EXECUTED",
            # ... другие поля ...
        },
        {
            "id": 441945816,
            "description": "Перевод организации",
            "state": "EXECUTED",
            # ... другие поля ...
        },
    ]

    descriptions = transaction_descriptions(transactions)
    for _ in range(5):
        print(next(descriptions))


if __name__ == "__main__":
    descriptions = card_number_generator(1, 5)
    for card_number in descriptions:
        print(card_number)