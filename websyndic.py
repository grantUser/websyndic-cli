import requests

from managers.login_manager import LoginManager
from managers.point_manager import PointManager
from utils.nordvpn import nordvpn


class WebSyndic:
    def __init__(self):
        self.client = requests.Session()

    def login(self, email, password):
        login_manager = LoginManager(self.client)
        login_manager.login(email, password)

    def make_points(self):
        point_manager = PointManager(self.client)
        point_manager.make_points()

    def make_light_points(self, light_viewer=False):
        point_manager = PointManager(self.client)
        point_manager.make_light_points(light_viewer)


if __name__ == "__main__":
    websyndic = WebSyndic()
    proxies = nordvpn.get_nordvpn_proxy(
        nord_account_user="",
        nord_account_password="",
        nord_account_server="JP",
    )

    websyndic.client.proxies = proxies

    websyndic.make_light_points(
        light_viewer="https://www.websyndic.com/wv3/FR/?qs=XXXXXXXX"
    )
