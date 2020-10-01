#!/usr/bin/env python3
# coding: utf-8
# import pudb
# bp = pudb.set_trace

import csv
import subprocess
import os
def validate_csv(input_str, log_level):
    """ return:
        rv: "complete", "incomplete" or "wrong",
        n: the index of the character -1 if not applicable
        c: the character where error happened  "" if not applicable
    """
    try:
        reader = csv.reader(input_str.split('\n'), delimiter=',')
        cmd = "echo '"+ input_str + "' | ./csv"

        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr = p.communicate()
        output = stderr
        output = output.decode('utf-8')
        if output != "":
            return "wrong", len(input_str), "input_str[-1]"
        if output.find("Syntax error") != -1:
            return "wrong", len(input_str), "input_str[-1]"
        else:
            return "complete",-1,""
    except Exception as e:
        msg = str(e)
        print("Can't parse: " + msg)
        n = len(msg)
        return "wrong", n, ""


import string
import random

def get_next_char(log_level):
    set_of_chars = string.printable # ['[',']','{','}','(',')','<','>','1','0','a','b',':','"',',','.', '\'']
    set_of_chars = set_of_chars.replace("'", '')
    idx = random.randrange (0,len(set_of_chars),1)
    input_char = set_of_chars[idx]
    return input_char
import random
def generate(log_level):
    """
    Feed it one character at a time, and see if the parser rejects it.
    If it does not, then append one more character and continue.
    If it rejects, replace with another character in the set.
    :returns completed string
    """
    prev_str = ""
    while True:
        char = get_next_char(log_level)
        curr_str = prev_str + str(char)
        rv, n, c = validate_csv(curr_str, log_level)

        if log_level:
            print("%s n=%d, c=%s. Input string is %s" % (rv,n,c,curr_str))
        if rv == "complete":
            if random.randrange(5) == 0:
                return curr_str
            else:
                prev_str = curr_str
                continue
        elif rv == "incomplete": # go ahead...
            prev_str = curr_str
            continue
        elif rv == "wrong": # try again with a new random character do not save current character
            continue
        else:
            print("ERROR What is this I dont know !!!")
            break
    return None
import time
def create_valid_strings(n, log_level):
    os.remove("valid_inputs.txt")
    tic = time.time()
    while True:
        created_string = generate(log_level)
        toc = time.time()
        if created_string is not None:
            with open("valid_inputs.txt", "a") as myfile:
                var = f"Time used until input was generated: {toc - tic:f}\n" + repr(created_string) + "\n\n"
                myfile.write(var)
                myfile.close()

create_valid_strings(10, 0)
