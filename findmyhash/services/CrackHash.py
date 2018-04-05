from bs4 import BeautifulSoup
import requests

from findmyhash.algo import Algo
from findmyhash.errors import *

from .Service import Service

class CrackHash(Service):
	NAME = 		"Crackhash"
	HOST = 		"http://www.crackhash.com/"

	ALGO_SUPPORTED	=	[Algo.MD5, Algo.SHA1]

	@classmethod
	def algo_supported(cls, algo: Algo) -> bool:
		return algo in cls.ALGO_SUPPORTED

	@classmethod
	def crack_hash(cls, hash: str) -> str:
		r = requests.post(
			cls.HOST,
			data={
				"hash": hash,
				"crack": "crack"
			},
			headers={
				"Content-Type": "application/x-www-form-urlencoded"
			}
		)
		if r.status_code == 200:
			soup = BeautifulSoup(r.text, 'html.parser')
			found = soup.find_all(
				"tr",
				attrs={
					"class": "success"
				}
			)
			found = found[0].find("center")
			return found.string.split("==>")[-1][1:]
		raise HashNotFound

	@classmethod
	def crack(cls, hash: str, algo: Algo) -> str:
		res = ""
		if algo == Algo.MD5 or algo == Algo.SHA1:
			res = cls.crack_hash(hash)
		else:
			raise NotImplementedError
		return res
