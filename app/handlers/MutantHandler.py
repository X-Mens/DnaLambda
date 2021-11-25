import logging

from py27hash.hash import hash27

from app.SNS.SnsService import Sns
from app.handlers.Handler import Handler
from app.model.Dna import Dna
from app.persistence.MutantDynamoDb import MutantDynamoDb


class MutantHandler(Handler):

    def __init__(self, event):
        super().__init__(event)

    def parse_parameters(self):
        super().parse_parameters()

    def __data_retrieval(self, dna):
        status_code, message = 200, {}
        id_dna = hash27(str(dna))
        document = MutantDynamoDb.get_dna_from_cache(id_dna)
        if document:
            logging.info("Retrieve cache value " + str(document))
            if not document['isMutant']:
                status_code = 403
        else:
            dna = Dna(dna)
            is_mutant = dna.is_mutant()
            logging.info(f"Dna with idDna {id_dna} is mutant {is_mutant}")
            MutantDynamoDb.save_dna(id_dna, is_mutant)
            Sns.publish_result_dna_analysis(id_dna, is_mutant)
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
