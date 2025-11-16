def mask_card(card_number_str: str) -> str:
    """Маскирует номер карты, оставляя открытыми первые 6 и последние 4 цифры."""
    digits_only = "".join(filter(str.isdigit, card_number_str))

    if len(digits_only) < 10:
        return "Неверный формат номера карты"

    first_six = digits_only[:6]
    last_four = digits_only[-4:]
    masked_result = f"{first_six[:4]} {first_six[4:]}** **** {last_four}"
    return masked_result


def mask_account(account_number_str: str) -> str:
    """Маскирует номер счета, оставляя открытыми только последние 4 цифры."""
    digits_only = "".join(filter(str.isdigit, account_number_str))

    if len(digits_only) < 4:
        return "Неверный формат номера счета"

    last_four = digits_only[-4:]
    return f"**{last_four}"


def mask_account_card(data_string: str) -> str:
    """Функция принимает строку, определяет тип (карта или счет) и маскирует номер"""
    if not isinstance(data_string, str):
        return "Неверный формат: входные данные не являются строкой"
    first_digit_index = -1
    for i, char in enumerate(data_string):
        if char.isdigit():
            first_digit_index = i
            break

    if first_digit_index == -1:
        return "Неверный формат: не найден номер"
    card_type = data_string[:first_digit_index].strip()
    number_str = data_string[first_digit_index:].strip()

    if "Счет" in card_type:
        masked_number = mask_account(number_str)
        return f"{card_type} {masked_number}"
    else:
        masked_number = mask_card(number_str)
        return f"{card_type} {masked_number}"


def get_date(date_string: str) -> str:
    """Функция, которая принимает дату в виде строки с лишними элементами
    и возвращает дату в виде строки в нужном формате"""
    date_part = date_string.split("T")[0]
    year, month, day = date_part.split("-")
    return f'"{day}.{month}.{year}"'
