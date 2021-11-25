import json
import logging
import os

from redis import Redis

HOST_REDIS = os.environ['HOST_REDIS']
PORT_REDIS = os.environ['PORT_REDIS']

redis = Redis(host=HOST_REDIS, port=PORT_REDIS)


class RedisCache:

    @staticmethod
    def get_by_hash(hash):
        """
        Retrieve the data corresponding to hash
        :param hash:
        :return:  If the connection exist, redis will retrieves the data that contains that key otherwise no
        """
        try:
            document = redis.get(str(hash))
            if document is not None:
                document_str = document.decode("UTF-8")
                document = json.loads(document_str)
            return document
        except Exception as e:
            logging.exception(e)

    @staticmethod
    def save_dna_result(hash, is_mutant):

        try:
            redis.set(hash, json.dumps({"isMutant": is_mutant}))
        except Exception as e:
            logging.exception(e)
