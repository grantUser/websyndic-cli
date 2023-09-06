import contextlib
import sys
import time
from typing import Dict

import bs4
from lxml import etree
from requests import Session


class PointManager:
    def __init__(self, client: Session) -> None:
        self.client: Session = client
        self.urls: Dict[str, str] = {
            "visio01": "https://www.websyndic.com/wv3/EN/?p=visio01",
            "target": "https://www.websyndic.com/wv3/target.php",
            "valid_surf": "https://www.websyndic.com/wv3/valid_surf.php",
            "valid_surf_light": "https://www.websyndic.com/wv3/valid_surf_light.php",
        }

    def valid_surf(self, endpoint, payload):
        try:
            response = self.client.post(
                self.urls[endpoint],
                data=payload,
                headers={
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
                },
            )

            remove_spacer = response.text.split("[Spacer]")
            remove_empty = list(filter(None, remove_spacer))

            account_infos = remove_empty[-17:]

            s = remove_spacer[4]
            c = account_infos[6]
            lid = account_infos[-1]

            wait_time = int(remove_empty[-3])
            current_credits = account_infos[-17]

            self.target(s, c, lid, current_credits, wait_time, endpoint, payload)
        except Exception:
            print("Error when attempting to generate points.")
            self.valid_surf(endpoint, payload)

    def target(self, s, c, lid, current_credits, wait_time, endpoint, payload):
        target = f"https://www.websyndic.com/wv3/target.php?s={s}&c={c}&lid={lid}"

        target_response = self.client.get(target).text
        soup = bs4.BeautifulSoup(target_response, "html.parser")
        meta_refresh_tag = soup.find("meta", {"http-equiv": "refresh"})
        refresh_content = meta_refresh_tag.get("content").split("url=")[1]

        self.client.get(refresh_content).text
        print(f"Next gain in {wait_time} seconds. ({current_credits})")
        time.sleep(wait_time)
        self.valid_surf(endpoint, payload)

    def get_light_viewer(self, light_viewer):
        redirect = self.client.get(light_viewer, allow_redirects=True)
        return redirect.url

    def make_light_points(self, light_viewer_link) -> None:
        visio_page = self.client.get(light_viewer_link).text

        visio_soup = bs4.BeautifulSoup(visio_page, "html.parser")
        dom = etree.HTML(str(visio_soup))
        target_url = (
            "https://www.websyndic.com/wv3/EN/"
            + dom.xpath('//*[@id="main_page_offline"]/div/div[3]/div/div/a')[0].attrib[
                "href"
            ]
        )
        self.client.get(self.urls["target"]).text
        target_page = self.client.get(target_url).text
        self.client.get(self.urls["target"]).text

        key = target_page.split("var key=")[1].split(";")[0]
        rv = target_page.split('["')[1].split('",')[0]
        v = target_page.split('["')[1].split('",')[1].split('"')[1].split('"]')[0]

        payload = f"key={key}&w=1.1&rv={rv}&v={v}"
        self.valid_surf("valid_surf_light", payload)

    def make_points(self) -> None:
        visio_page = self.client.get(self.urls["visio01"]).text

        visio_soup = bs4.BeautifulSoup(visio_page, "html.parser")
        dom = etree.HTML(str(visio_soup))
        target_url = (
            "https://www.websyndic.com/wv3/EN/"
            + dom.xpath('//*[@id="main_page"]/div[1]/div[3]/div/div/a')[0].attrib[
                "href"
            ]
        )
        self.client.get(self.urls["target"]).text
        target_page = self.client.get(target_url).text
        self.client.get(self.urls["target"]).text

        key = target_page.split("var key=")[1].split(";")[0]
        rv = target_page.split('["')[1].split('",')[0]
        v = target_page.split('["')[1].split('",')[1].split('"')[1].split('"]')[0]

        payload = f"key={key}&w=1.1&rv={rv}&v={v}"
        self.valid_surf("valid_surf", payload)
