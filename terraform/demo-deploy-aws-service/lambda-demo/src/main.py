import logging


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def handler(event, context):
    
    logger.info(f"Hello from Lambda! - Event: {event} | Context: {context}")
    logger.info("Event:", event)
    return {"result": "200 OK!"}
