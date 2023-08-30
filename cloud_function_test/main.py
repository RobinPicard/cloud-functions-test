
def main(request):
    """"""
    value = request.get_json().get("value")
    b = 1 + value
    #if code == 500:
    #    raise Exception
    return ([], 200)
