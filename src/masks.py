from typing import Union


def get_mask_card_number(card_number: Union[int, str]) -> Union[int, str]:
    """Принимает номер карты и возвращает его маскированную версию."""
    card_number = str(card_number)
    card_number = card_number.replace(" ", "")
    first_digit = card_number[:6]
    last_digit = card_number[-4:]
    masked_cod = "*" * (len(card_number) - 10)
    card_mask = f"{first_digit[:4]} {first_digit[4:]}{masked_cod[:2]} {masked_cod[2:]} {last_digit}"
    return card_mask


def get_mask_account(account_number: Union[int, str]) -> Union[int, str]:
    """Принимает номер счёта и возвращает его маскированную версию."""
    account_number = str(account_number)
    last_digit = account_number[-4:]
    account_mask = f"**{last_digit}"

    return account_mask
