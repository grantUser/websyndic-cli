import json

import requests


class NordVPN:
    def __init__(self) -> None:
        pass

    def get_nordvpn_proxy(
        self, nord_account_user, nord_account_password, nord_account_server
    ):
        proxy = nord_account_user.replace("@", "%40").replace(":", "%3A")
        proxy += ":"
        proxy += nord_account_password.replace("@", "%40").replace(":", "%3A")
        proxy += "@"

        hostname = self.get_nordvpn_server(nord_account_server)

        proxy += hostname

        return {
            "http": f"http://{proxy}:80",
            "https": f"https://{proxy}:89",
        }

    def get_nordvpn_server(self, country):
        """
        Get the recommended NordVPN server hostname for a specified country.

        :param country: Country in alpha-2 format, e.g. 'us' for United States

        :return: Recommended NordVPN server hostname, e.g. `us123.nordvpn.com`
        """
        # Get the country's NordVPN ID
        countries = requests.get(
            url="https://nordvpn.com/wp-admin/admin-ajax.php",
            params={
                "action": "servers_countries",
            },
        ).json()

        country_id = [
            x["id"] for x in countries if x["code"].lower() == country.lower()
        ]
        if not country_id:
            return None
        country_id = country_id[0]

        # Get the recommended server for the country and return it
        recommendations = requests.get(
            url="https://nordvpn.com/wp-admin/admin-ajax.php",
            params={
                "action": "servers_recommendations",
                "filters": json.dumps({"country_id": country_id}),
            },
        ).json()
        return recommendations[0]["hostname"]


nordvpn = NordVPN()
