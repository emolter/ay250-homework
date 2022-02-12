#!/usr/bin/env python

import argparse
import numexpr as ne
from urllib import request, parse
import numpy as np
import warnings


def response_parser(wra_string):
    
    word_list = wra_string.split(' ')
    number_list = []
    for word in word_list:
        try:
            number_list.append(float(word))
        except:
            pass
    print(number_list)
    
    if len(number_list) == 0:
        warnings.warn("Your WolframAlpha query did not return any numerical result; the result has been returned as a string. This is not really supported.")
        return wra_string
    if len(number_list) == 1:
        return number_list[0]
    if len(number_list) == 2:
        raise NotImplementedError
    if len(number_list) == 3:
        return number_list[0]*number_list[1]**number_list[2]
    else:
        raise NotImplementedError
        
    return


def calculate(input_string, use_wra = False):
    '''use_wra tells us if should web query wolframalpha or just use numexpr'''
    if not use_wra:
        return ne.evaluate(input_string)
    else:
        
        base_url = 'https://api.wolframalpha.com/v1/result?i='
        appid = '5ALVA8-2Y6E7HY96G'
        full_url = base_url + parse.quote_plus(input_string) + '&appid=' + appid
        req = request.Request(full_url)
        with request.urlopen(req) as response:
             response = response.read()
             response = response.decode('utf-8')
        
        return response_parser(response)
    
def test_1():
    assert abs(4. - calculate('2**2')) < 0.001
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='WolframAlpha enabled calculator')
    
    parser.add_argument('calc_string', help='Required. string readable by either Wolfram Alpha or numexpr.evaluate')
    group = parser.add_mutually_exclusive_group() # this way should raise if both are specified. not sure yet what happens if neither specified
    group.add_argument('-w', action='store_true', help='Use WolframAlpha mode')
    group.add_argument('-s', action='store_true', help='Use numexpr mode')
    parser.add_argument('--version', action='version', version='0.0')
    
    results = parser.parse_args()

    print(calculate(results.calc_string, use_wra = results.w))
    

    