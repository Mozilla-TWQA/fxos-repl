#!/usr/bin/env python

import readline
import sys

from marionette import Marionette

def usage():
    print "fxos-repl.py [list | connect [appname]]"

def list_iframes(m):
    iframes = m.execute_script("return document.getElementsByTagName('iframe')")
    for idx in range(0,iframes['length']):
        iframe = iframes[str(idx)]
        print iframe.get_attribute('src')

def connect_to_iframe(m, name):
    iframes = m.execute_script("return document.getElementsByTagName('iframe')")
    for idx in range(0,iframes['length']):
        iframe = iframes[str(idx)]
        if name in iframe.get_attribute('src'):
            m.switch_to_frame(iframe)
            return True
    return False

def start_repl(m):
    try:
        while True:
            s = raw_input(">>> ")
            if s == "" or s == "exit" or s == "quit":
                break
            try:
                print m.execute_script("return " + s, new_sandbox=False)
            except Exception as e:
                print "Error: " + str(e.message)
    except EOFError:
        print "\nSayonara"
        pass

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    m = Marionette('localhost', 2828)
    m.start_session()

    if sys.argv[1] == 'list':
        list_iframes(m)
    elif (sys.argv[1] == 'connect') and (len(sys.argv) == 2):
        print "Connected to System app"
        start_repl(m)
    elif (sys.argv[1] == 'connect') and (len(sys.argv) == 3):
        if connect_to_iframe(m, sys.argv[2]):
            print "Connected to " + sys.argv[2]
            start_repl(m)
        else:
            print "Wrong iframe to connect!"
    else:
        usage()
        sys.exit(1)

