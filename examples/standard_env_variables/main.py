import os


def main(request):
    assert os.environ["ENV"] == "dev"
    assert os.environ["LOCATION_ID"] == "europe-west1"
    assert os.environ["NAME"] == "test_dev"
    return ("OK", 200)
