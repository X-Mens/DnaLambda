import json

import boto3

sns = boto3.client("sns")
topic = "arn:aws:sns:us-east-1:142347585731:test"  # os.environ['TOPIC_ANR']


class Sns:

    @staticmethod
    def publish_result_dna_analysis(is_mutant):
        sns.publish(TopicArn=topic,
                    Message=json.dumps({"isMutant": is_mutant}))
