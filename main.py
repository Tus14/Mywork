from src.masks import get_mask_account, get_mask_card_number

if __name__ == "__main__":
    card_mask = get_mask_card_number("7000792289606361")
    print(card_mask)
    account_mask = get_mask_account("73654108430135874305")
    print(account_mask)
