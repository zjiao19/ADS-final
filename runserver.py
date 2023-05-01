#!/usr/bin/env python
from sys import argv, exit, stderr
from gameapp import app
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--port', type=int, default=8888, help='port to listen on (default: 8888)')

args = parser.parse_args()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=args.port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)
