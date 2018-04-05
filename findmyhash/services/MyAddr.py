from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

from findmyhash.algo import Algo
from findmyhash.errors import *

from .Service import Service

class MY_ADDR(Service):
	NAME = 		"my-addr"
	HOST = 		"http://md5.my-addr.com"

	ALGO_SUPPORTED	=	[Algo.MD5]

	@classmethod
	def algo_supported(cls, algo: Algo) -> bool:
		return algo in cls.ALGO_SUPPORTED

	@classmethod
	def crack_MD5(cls, hash: str) -> str:
		r = requests.post(
			urljoin(cls.HOST, "/md5_decrypt-md5_cracker_online/md5_decoder_tool.php"),
			data={
				"md5": hash,
			},
			headers={
				"Content-Type": "application/x-www-form-urlencoded"
			}
		)
		if r.status_code == 200:
			soup = BeautifulSoup(r.text, 'html.parser')
			found = soup.find_all(
				attrs={
					"class": "middle_title",
				}
			)
			return found[1].parent.contents[1][2:]
		raise HashNotFound

	@classmethod
	def crack(cls, hash: str, algo: Algo) -> str:
		res = ""
		if algo == Algo.MD5:
			res = cls.crack_MD5(hash)
		else:
			raise NotImplementedError
		return res