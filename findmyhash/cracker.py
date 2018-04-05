import base64
import hashlib
import random


from findmyhash import services
from findmyhash.algo import Algo
from findmyhash.errors import *

class Cracker(object):
    def __init__(self, iterable):
        self.iterable = iterable

    @staticmethod
    def crack_hash(hash: str, algo: Algo, service) -> str:
        result = None
        try:
            result = service.crack(hash, algo)
        except NotImplementedError:
            print("Algorithm: '%s' not implemented for '%s' service" % (algo, service.NAME))
        except HashNotFound:
            print("Hash not found by '%s' service" % (service.NAME,))
        return result

    @classmethod
    def loop_services_crack_hashes(cls, hash: str, algo: Algo) -> str:
        s = services.Service.by_algo(algo)
        random.shuffle(s)
        for service in s:
            result = cls.crack_hash(hash, algo, service)
            if result is not None:
                return result
        return None

    @staticmethod
    def validate_hash(hash: str, cracked: str, algo: Algo) -> bool:
        # NOTE: I'm all for trusting the third parties added here and not double checking
        # Hence removing the cross-check with multiple services

        res = False
        if algo.name in hashlib.algorithms_available:
            h = hashlib.new(algo.name)
            h.update(cracked.encode("utf-8"))

            if h.hexdigest().lower() == hash:
                res = True
        elif algo in [Algo.LDAP_MD5, Algo.LDAP_SHA1]:
            # NOTE: this is fucking ugly, almost tempted to leave the user do the pre-work
            # leaving for now for compatibility purposes
            alg = algo.name.split('_')[1]
            ahash = base64.decodestring(hash.split('}')[1])

            h = hashlib.new(alg)
            h.update(cracked.encode("utf-8"))

            if h.digest() == ahash:
                res =  True
        elif algo == Algo.NTLM or (algo == Algo.LM and ':' in hash):
            candidate = hashlib.new('md4', cracked.split()[-1].encode('utf-16le')).hexdigest()

            # It's a LM:NTLM combination or a single NTLM hash
            if (':' in hash and candidate == hash.split(':')[1]) or (':' not in hash and candidate == hash):
                res = True
        else:
            # Can't and won't validate the hash, assuming it's correct
            res = True

        return res


    def crack(self, algo: Algo):
        print(services.Service.get_supported_algos())
        for activehash in self.iterable:
            activehash = activehash.strip()
            if algo not in [Algo.JUNIPER, Algo.LDAP_MD5, Algo.LDAP_SHA1]:
                activehash = activehash.lower()

            result = self.__class__.loop_services_crack_hashes(activehash, algo)
            if result is None:
                continue

            if self.__class__.validate_hash(activehash, result, algo) is True:
                print(("'%s': '%s'\n" % (activehash, result)))