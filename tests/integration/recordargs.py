#!/usr/bin/env python
# coding=utf-8

import sys

# Writes command line arguments to a file so that they can be verified in a test later on.

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open('argv.txt', 'w') as file:
            for arg in sys.argv[1::]:
                file.write(arg + "\n")