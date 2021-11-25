import json
import logging
import os

import boto3

sns = boto3.client("sns")
topic = os.environ['TOPIC_ARN']


class Sns:

    @staticmethod
    def publish_result_dna_analysis(id_dna, is_mutant):
        """
        Send a message a Sns with the purpose the increase by one the counter of who is mutant or not
        :param id_dna: hash of dna matrix
        :param is_mutant: boolean that represent if the dna matrix was mutant or no
        """
        try:
            logging.info(f"It will send message to sns, the id {id_dna}")
            sns.publish(TopicArn=topic,
                        Message=json.dumps({"isMutant": is_mutant}))
        except Exception as e:
            logging.info(f"It was not possible send message to sns, the id {id_dna}")
