import json
import logging


class Handler:

    def __init__(self, event):
        self.event = event
        self.resource = event['resource'].lstrip('/').lower()
        self.http_method = event['httpMethod'].lstrip('/').lower()
        if isinstance(event['body'], str):
            self.body = json.loads(event['body'])
        else:
            self.body = event['body']
        self.malformed_request = False
        self.logger = logging.getLogger(__name__)

    def parse_parameters(self):

        if 'dna' not in self.body:
            self.malformed_request = True
            return
        self.dna = list(self.body["dna"])

    def process(self):
        pass
