import json
import logging
import logging.config
import sys
import traceback

from app.handlers.DefaultHandler import DefaultHandler
from app.handlers.MutantHandler import MutantHandler
from app.utils.Logger import LOGGING_CONFIG
from app.utils.Response import build_response

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()

Handlers = {
    "post_mutant": MutantHandler,
    "default": DefaultHandler
}


def lambda_handler(event, context):
    logging.info('Received event: ' + json.dumps(event))
    try:
        resource = event['resource'].lstrip('/').lower()
        http_method = event['httpMethod'].lstrip('/').lower()
        handler_type = Handlers["default"]
        handler_path = f"{http_method}_{resource}"
        if handler_path in Handlers:
            handler_type = Handlers[handler_path]
        handler = handler_type(event)
        status, response = handler.process()
        response = build_response(status, response)
        logging.info(f'Response [{response}]')
    except Exception as e:
        logging.error(e)
        tb = sys.exc_info()[2]
        tb_info = traceback.format_tb(tb)[0]
        py_msg = "PYTHON ERRORS:\nTraceback info:\n" + tb_info + "\nError Info:\n" + str(sys.exc_info()[1])
        logging.error(py_msg)
        response = build_response(500, e.args[0])
    return response


