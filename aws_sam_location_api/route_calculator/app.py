import json
from route import *
# import requests


def lambda_handler(event, context):
    print(f"event : {event}")
    response = dict()
    results = []
    try:
        data = json.loads(event['body'])
        source_lat = data['source_lat']
        source_lon = data['source_lon']
        dest_lat = data['dest_lat']
        dest_lon = data['dest_lon']
        results.append(json.dumps(calculate_route(
            source_lon, source_lat,
            dest_lon, dest_lat
        )))

    except Exception as e:
        print(e)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": results,
        }),
    }
