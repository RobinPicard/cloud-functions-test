import os
import logging 


def main(event, context):
    logging.error(event)
    logging.info(event)
    assert event == context
