#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


def function(arg):
    '''the function you want to accomplish.'''
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="the function of this module.")
    parser.add_argument("--arg", "-a", type="", help="")
    args = vars(parser.parse_args())

    arg = args["arg"]
    function(arg)
