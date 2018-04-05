from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

from findmyhash.algo import Algo
from findmyhash.errors import *

from .Service import Service

class PASSWORD_DECRYPT(Service):
    NAME = 		"password-decrypt"
    HOST = 		"http://password-decrypt.com/"

    ALGO_SUPPORTED	=	[Algo.JUNIPER, Algo.CISCO7]

    @classmethod
    def algo_supported(cls, algo: Algo) -> bool:
        return algo in cls.ALGO_SUPPORTED

    @classmethod
    def crack_JUNIPER(cls, hash: str) -> str:
        r = requests.post(
            urljoin(cls.HOST, "/juniper.cgi"),
            data={
                "submit": "Submit",
                "juniper_password": hash
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            found = soup.find_all(
                "input",
                attrs={
                    "name": "juniper_password",
                }
            )
            return found[0].next_sibling.next_sibling.contents[1].string
        raise HashNotFound

    @classmethod
    def crack_CISCO7(cls, hash: str) -> str:
        r = requests.post(
            urljoin(cls.HOST, "/cisco.cgi"),
            data={
                "submit": "Submit",
                "cisco_password": hash
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            found = soup.find_all(
                "input",
                attrs={
                    "name": "cisco_password",
                }
            )
            return found[0].next_sibling.next_sibling.contents[1].string
        raise HashNotFound

    @classmethod
    def crack(cls, hash: str, algo: Algo) -> str:
        res = ""
        if algo == Algo.JUNIPER:
            res = cls.crack_JUNIPER(hash)
        elif algo == Algo.CISCO7:
            res = cls.crack_CISCO7(hash)
        else:
            raise NotImplementedError
        return res