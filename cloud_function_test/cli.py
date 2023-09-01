import argparse
import sys
from .main import main as entrypoint_main


def main():
    parser = argparse.ArgumentParser(description='cloud-function-test CLI')
    
    parser.add_argument('--type', '-t', type=str, help='Type of test used: "http" (default) or "event"')
    parser.add_argument('--module', '-m', type=str, help='Name of the module in which test classes are defined')
    parser.add_argument('--port', '-p', type=int, help='Number of the port on which functions-framework should run the local server')
    parser.add_argument('--env', '-v', type=str, help='Path to the file in which are defined environment variables')
    parser.add_argument('--entrypoint', '-e', type=str, help='Name of the entrypoint function of the Cloud Function')

    args = parser.parse_args()

    type = args.type
    module = args.module
    port = args.port
    env = args.env
    entrypoint = args.entrypoint

    entrypoint_main(type, module, port, env, entrypoint)

if __name__ == '__main__':
    main()
