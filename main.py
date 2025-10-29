from src.masks import get_mask_account, get_mask_card_number

if __name__ == "__main__":
    card_mask = get_mask_card_number("7000792289606361")
    print(card_mask)
    account_mask = get_mask_account("73654108430135874305")
    print(account_mask)


from src.widget import mask_account_card

if __name__ == "__main__":
    masked_number_add = mask_account_card("Счет 73654108430135874305")
    print(masked_number_add)
