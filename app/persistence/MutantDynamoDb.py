from os import getenv

from boto3 import resource

DYNAMO_TABLE = getenv("DYNAMO_TABLE_DNA")
dynamodb = resource('dynamodb')
dna_table = dynamodb.Table(DYNAMO_TABLE)


class MutantDynamoDb:

    @staticmethod
    def save_dna(id_dna, is_mutant):
        dna_table.put_item(
            Item={
                'idDna': str(id_dna),
                'isMutant': is_mutant,
            }
        )
