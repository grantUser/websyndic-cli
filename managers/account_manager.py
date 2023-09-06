import sys
from typing import Dict

import bs4
from requests import Session


class AccountManager:
    def __init__(self, client: Session, account_url: str) -> None:
        self.client: Session = client
        self.account_url: str = account_url

    def display_account_info(self) -> None:
        account_page: str = self.client.get(self.account_url).text
        if "pseudo_span" in account_page:
            account_soup: bs4.BeautifulSoup = bs4.BeautifulSoup(
                account_page, "html.parser"
            )
            username: str = account_soup.find("div", {"id": "pseudo_span"}).text
            print(f"Login successful as {username}.")
        else:
            print("Error: Unable to fetch account info.")
            sys.exit(1)
