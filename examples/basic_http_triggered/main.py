import logging


def main(request):
    value = request.get_json()
    logging.info(value)
    if "a" not in value:
        return ("Error", 400)
    return ({**value, "b": 2}, 200)
