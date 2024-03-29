import json
import logging
import time
from route import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.debug(event)
    try:
        response = dict()
        t1 = time.time()
        results = []
        try:
            results.append(json.dumps(calculate_route(
                90.4264914579999, 23.79809450283832, 90.30016736544847, 23.79795912830887)))
        except:
            results.append(None)
        t2 = time.time()
        logger.info("Result Count: %d Time: %.3f" % (len(results), t2 - t1))
        response['success'] = True
        response['results'] = results
    except Exception as e:
        response['success'] = False
        response['error_msg'] = str(e)
    logger.info(response)
    return json.dumps(response)
