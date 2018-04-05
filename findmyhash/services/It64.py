from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

from findmyhash.algo import Algo
from findmyhash.errors import *

from .Service import Service

class It64(Service):
    NAME = 		"it64"
    HOST = 		"http://rainbowtables.it64.com/"

    ALGO_SUPPORTED	=	[Algo.LM]

    @classmethod
    def algo_supported(cls, algo: Algo) -> bool:
        return algo in cls.ALGO_SUPPORTED

    @classmethod
    def crack_LM(cls, hash: str) -> str:
        r = requests.post(
            urljoin(cls.HOST, "p3.php"),
            data={
                "hashe": hash,
                "ifik": " Submit ",
                "forma": "tak"
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            found = soup.find_all("table")
            return found[0].contents[1].contents[2].string.strip()
        raise HashNotFound

    @classmethod
    def crack(cls, hash: str, algo: Algo) -> str:
        res = ""
        if algo == algo.LM:
            res = cls.crack_LM(hash)
        else:
            raise NotImplementedError
        return res
