from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from findmyhash.algo import Algo
from findmyhash.errors import *

from .Service import Service

class MD5Hashing(Service):
    NAME = 		"MD5Hashing"
    HOST = 		"https://md5hashing.net/"

    ALGO_SUPPORTED	=	[
        Algo.MD2, Algo.MD4, Algo.MD5,
        Algo.SHA224, Algo.SHA256, Algo.SHA384, Algo.SHA512,
        Algo.RIPEMD128, Algo.RIPEMD160, Algo.RIPEMD256, Algo.RIPEMD320,
        Algo.WHIRLPOOL, Algo.GOST,
        Algo.SNEFRU, Algo.SNEFRU256
    ]

    @classmethod
    def algo_supported(cls, algo: Algo) -> bool:
        return algo in cls.ALGO_SUPPORTED

    @classmethod
    def crack_hash(cls, hash: str, algo: Algo) -> str:
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("headless")
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver.get(
            urljoin(cls.HOST, "hash/%s/%s" % (algo.value, hash))
        )
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "decodedValue"))
            )
            return element.text
        finally:
            driver.quit()
        raise HashNotFound

    @classmethod
    def crack(cls, hash: str, algo: Algo) -> str:
        res = ""
        if cls.algo_supported(algo) is True:
            res = cls.crack_hash(hash, algo)
        else:
            raise NotImplementedError
        return res
