from findmyhash.algo import Algo
from functools import reduce
import operator

class Service(object):
    @classmethod
    def get_services(cls):
        return cls.__subclasses__()

    @classmethod
    def get_supported_algos(cls):
        return list(set(
            reduce(
                operator.add,
                map(lambda s: s.ALGO_SUPPORTED, cls.get_services())
            )
        ))

    @classmethod
    def by_algo(cls, algo: Algo):
        return [c for c in cls.get_services() if c.algo_supported(algo) is True]