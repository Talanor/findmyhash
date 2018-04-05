from bs4 import BeautifulSoup
import requests

from findmyhash.algo import Algo
from findmyhash.errors import *

from .Service import Service

class MD5DECRYPTION(Service):
	NAME = 		"md5decryption"
	HOST = 		"http://md5decryption.com"

	ALGO_SUPPORTED	=	[Algo.MD5]

	@classmethod
	def algo_supported(cls, algo: Algo) -> bool:
		return algo in cls.ALGO_SUPPORTED

	@classmethod
	def crack_MD5(cls, hash: str) -> str:
		r = requests.post(
			cls.HOST,
			data={
				"hash": hash,
				"submit": "Decrypt+It!"
			},
			headers={
				"Content-Type": "application/x-www-form-urlencoded"
			}
		)
		if r.status_code == 200:
			soup = BeautifulSoup(r.text, 'html.parser')
			found = soup.find_all("font")
			return found[5].parent.parent.contents[1]
		raise HashNotFound

	@classmethod
	def crack(cls, hash: str, algo: Algo) -> str:
		res = ""
		if algo == Algo.MD5:
			res = cls.crack_MD5(hash)
		else:
			raise NotImplementedError
		return res