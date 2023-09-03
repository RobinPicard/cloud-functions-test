import argparse
import sys

from .main import main as entrypoint_main


def main():
    parser = argparse.ArgumentParser(description='cloud-functions-test CLI')
    
    parser.add_argument('--module', '-m', type=str, help='Name of the module in which test classes are defined')
    parser.add_argument('--source', '-s', type=str, help='Path to the file in which your Cloud Function is defined')
    parser.add_argument('--entrypoint', '-e', type=str, help='Name of the entrypoint function of the Cloud Function')
    parser.add_argument('--env', '-v', type=str, help='Path to the file in which are defined environment variables')
    parser.add_argument('--port', '-p', type=int, help='Number of the port on which functions-framework should run the local server')

    args = parser.parse_args()

    module = args.module
    source = args.source
    entrypoint = args.entrypoint
    env = args.env
    port = args.port

    entrypoint_main(module, source, entrypoint, env, port)

if __name__ == '__main__':
    main()
