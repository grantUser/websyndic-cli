import re
import sys
from typing import Dict

from requests import Session

from managers.account_manager import AccountManager


class LoginManager:
    def __init__(self, client: Session) -> None:
        self.client: Session = client
        self.urls: Dict[str, str] = {
            "home": "https://www.websyndic.com/wv3/EN/?p=home",
            "login": "https://www.websyndic.com/wv3/cc.php",
            "account": "https://www.websyndic.com/wv3/EN/?p=account",
        }

    def extract_data(self, url: str) -> Dict[str, str]:
        page_content: str = self.client.get(url).text
        key_match = re.search(r"var key=(.*?);", page_content)
        rdi_match = re.search(r'var rdi="(.*?)";', page_content)

        if key_match and rdi_match:
            key: str = key_match[1]
            rdi: str = rdi_match[1]
        else:
            print(
                "Error: Unable to extract data. Check your internet connection and try again."
            )
            sys.exit(1)

        return {
            "key": key,
            "rdi": rdi,
            "sx": "1",
            "sh": "2",
        }

    def login(self, email: str, password: str) -> None:
        home_data: Dict[str, str] = self.extract_data(self.urls["home"])
        login_data: Dict[str, str] = {
            "key": home_data["key"],
            "target": "login",
            "rdi": "rdi",
            "login": email,
            "pass": password,
            "ol": "",
            "op": "",
            "sh": home_data["sh"],
            "sx": home_data["sx"],
        }

        print("Attempting to log in...")
        login_response: str = self.client.post(self.urls["login"], data=login_data).text

        if login_response == "login o":
            account_manager: AccountManager = AccountManager(
                self.client, self.urls["account"]
            )
            account_manager.display_account_info()
        else:
            print("Error: Login failed. Check your credentials and try again.")
            sys.exit(1)
