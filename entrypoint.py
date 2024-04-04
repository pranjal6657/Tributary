import json

import redis as redis
from flask import Flask, request
from loguru import logger

HISTORY_LENGTH = 10
DATA_KEY = "engine_temperature"

app = Flask(__name__)


@app.route('/record', methods=['POST'])
def record_engine_temperature():
    payload = request.get_json(force=True)
    logger.info(f"(*) record request --- {json.dumps(payload)} (*)")

    engine_temperature = payload.get("engine_temperature")
    logger.info(f"engine temperature to record is: {engine_temperature}")

    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    database.lpush(DATA_KEY, engine_temperature)
    logger.info(f"stashed engine temperature in redis: {engine_temperature}")

    while database.llen(DATA_KEY) > HISTORY_LENGTH:
        database.rpop(DATA_KEY)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    logger.info(f"engine temperature list now contains these values: {engine_temperature_values}")

    logger.info(f"record request successful")
    return {"success": True}, 200


@app.route('/collect', methods=['POST'])
def collect_engine_temperature():
    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    logger.info(f"pulled engine temperature values from redis: {engine_temperature_values}")

    datapoint_sum = 0
    for data_point in engine_temperature_values:
        datapoint_sum += float(data_point)
    average_engine_temperature = datapoint_sum / len(engine_temperature_values)
    logger.info(f"calculated average engine temperature: {average_engine_temperature}")
    logger.info(f"returning current engine temperature: {engine_temperature_values[0]}")

    result = {
        "current_engine_temperature": engine_temperature_values[0],
        "average_engine_temperature": average_engine_temperature
    }
    logger.info(f"collect request successful")
    return result, 200
