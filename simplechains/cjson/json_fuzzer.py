#!/usr/bin/env python3
# coding: utf-8
# import pudb
# bp = pudb.set_trace

import os
def parens(xs):
    stack = [[]]
    while True:
        x, xs = xs[0], xs[1:]
        if x == '(':
            stack[-1].append([])
            stack.append(stack[-1][-1])
        elif x == ')':
            stack.pop()
            if not stack:
                raise Exception('error: opening bracket is missing')
                #raise ValueError('error: opening bracket is missing')
        elif x in ' ':
            stack[-1].append(x)
        else:
            raise Exception('error: Only numbers')
        if xs == '':
            break
    if len(stack) > 1:
        raise Exception('incomplete: closing bracket is missing')
        #raise ValueError('error: closing bracket is missing')
    return stack.pop()

def validate_parens(input_str, log_level):
    """ return:
        rv: "complete", "incomplete" or "wrong",
        n: the index of the character -1 if not applicable
        c: the character where error happened  "" if not applicable
    """
    try:
        parens(input_str)
        return "complete",-1,""
    except Exception as e:
        msg = str(e)
        if msg.startswith("incomplete:"):
            n = len(msg)
            return "incomplete", n, ""
        elif msg.startswith("error"):
            return "wrong",len(input_str), input_str[-1]
        else:
            raise e


import json
def validate_json(input_str, log_level):
    """ return:
        rv: "complete", "incomplete" or "wrong",
        n: the index of the character -1 if not applicable
        c: the character where error happened  "" if not applicable
    """
    try:
        json.loads(input_str)
        return "complete",-1,""
    except Exception as e:
        msg = str(e)
        if msg.startswith("Expecting"):
            # Expecting value: line 1 column 4 (char 3)
            n = int(msg.rstrip(')').split()[-1])
            # If the error is "outside" the string, it can still be valid
            if n >= len(input_str):
                return "incomplete", n, ""
            else:
                return "wrong", n, input_str[n]
        elif msg.startswith("Unterminated"):
            # Unterminated string starting at: line 1 column 1 (char 0)
            n = int(msg.rstrip(')').split()[-1])
            if n >= len(input_str):
                return "incomplete", n, ""
            else:
                return "incomplete",n, input_str[n]
        elif msg.startswith("Extra data"):
            n = int(msg.rstrip(')').split()[-1])
            if n >= len(input_str):
                return "wrong", n, ""
            else:
                return "wrong",n, input_str[n]
        elif msg.startswith("Invalid "):
            idx = msg.find('(char ')
            eidx = msg.find(')')
            s = msg[idx+6:eidx]
            n = int(s)
            return "wrong",n, input_str[n]
        else:
            raise e
import string
import random

def get_next_char(log_level):
    set_of_chars = string.printable # ['[',']','{','}','(',')','<','>','1','0','a','b',':','"',',','.', '\'']
    idx = random.randrange (0,len(set_of_chars),1)
    input_char = set_of_chars[idx]
    #if (log_level):
        #print(input_char)
    return input_char

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
        #print(len(curr_str), curr_str[-1])
        rv, n, c = validate_json(curr_str, log_level)
        #rv, n, c = validate_parens(curr_str, log_level)
        if log_level:
            print("%s n=%d, c=%s. Input string is %s" % (rv,n,c,curr_str))
        if rv == "complete":
            return curr_str
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

create_valid_strings(1000000000, 0)
