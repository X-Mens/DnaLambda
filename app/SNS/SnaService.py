import json
import os

import boto3

sns = boto3.client("sns")
topic = os.environ['TOPIC_ARN']


class Sns:

    @staticmethod
    def publish_result_dna_analysis(is_mutant):
        sns.publish(TopicArn=topic,
                    Message=json.dumps({"isMutant": is_mutant}))
