def main(request):
    value = request.get_json()
    if "a" not in value:
        return ("Error", 400)
    return ({**value, "b": 2}, 200)
