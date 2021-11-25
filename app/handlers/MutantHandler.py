import logging
from py27hash.hash import hash27
from app.SNS.SnaService import Sns
from app.handlers.Handler import Handler
from app.model.Dna import Dna
from app.persistence.MutantDynamoDb import MutantDynamoDb
from app.persistence.RedisCache import RedisCache


class MutantHandler(Handler):

    def __init__(self, event):
        super().__init__(event)

    def parse_parameters(self):
        super().parse_parameters()

    def __data_retrieval(self, dna):
        status_code, message = 200, {}
        id_dna = hash27(str(dna))
        info_cache = RedisCache.get_by_hash(id_dna)
        if info_cache:
           logging.info("Retrieve cache value " + str(info_cache))
           if not info_cache['isMutant']:
               status_code = 403
        else:
            dna = Dna(dna)
            is_mutant = dna.is_mutant()
            logging.info(f"Dna with idDna {id_dna} is mutant {is_mutant}")
            MutantDynamoDb.save_dna(id_dna, is_mutant)
            Sns.publish_result_dna_analysis(is_mutant)
            RedisCache.save_dna_result(id_dna, is_mutant)
            if not is_mutant:
               status_code = 403
        return status_code, message

    def process(self):
        self.parse_parameters()
        if self.malformed_request:
            status_code, message = 400, {"message": "Malformed request."}
        else:
            status_code, message = self.__data_retrieval(self.body['dna'])
        return status_code, message
