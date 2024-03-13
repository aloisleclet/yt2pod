#!/bin/python3

import sys
from Core import Core

core = Core()

args = sys.argv[1:]

def menu(args):
    # @todo check args
    
    if (len(args) == 0):
        print("Invalid syntax: ./yt2pod help")
        return () 

    if (args[0] == 'add'):
        core.addChannel(args[1])
    elif (args[0] == 'remove'):
        core.removeChannel(args[1])
    elif  (args[0] == 'list'):
        core.listChannel()
    elif (args[0] == 'update'):
        core.update()
    elif (args[0] == 'help'):
            print('./yt2pod add https://www.youtube.com/@mychannel')
            print('./yt2pod remove @mychannel')
            print('./yt2pod list')
            print('./yt2pod update')
    else:
        print("Invalid syntax: ./yt2pod help")


# main

menu(args)
