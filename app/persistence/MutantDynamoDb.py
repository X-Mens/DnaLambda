import logging
from os import getenv

from boto3 import resource
from botocore.exceptions import ClientError

DYNAMO_TABLE = getenv("DYNAMO_TABLE_DNA")
dynamodb = resource('dynamodb')
dna_table = dynamodb.Table(DYNAMO_TABLE)


class MutantDynamoDb:

    @staticmethod
    def save_dna(id_dna, is_mutant):
        """
        :param id_dna: hash of dna matrix
        :param is_mutant: boolean that represent if the dna matrix was mutant or no
        """
        logging.info(f"It will persist with id {id_dna}")
        dna_table.put_item(
            Item={
                'idDna': str(id_dna),
                'isMutant': is_mutant,
            }
        )

    @staticmethod
    def get_dna_from_cache(id_dna):
        """
        :param id_dna: hash key in dynamodb
        :return: if exist document in dynamo with key equal the id_dna retrieve this id_dna
        """
        try:
            response = dna_table.get_item(Key={'idDna': str(id_dna)})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item'] if 'Item' in response else None
