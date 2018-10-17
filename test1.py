#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__':
    input = '11 128 15 111 59 31 70 102 50 172 88 56 40 41 12'
    split = input.split(' ')
    totalCharge = 0
    for token in split:
        distance = int(token)
        if distance < 4 or distance > 178:
            break
        else:
            charge = 720
            distance -= 40
            if distance > 0:
                temp = divmod(distance, 8)
                charge += 80 * (temp[0] + 0 if temp[1] == 0 else 1)
            if totalCharge + charge > 20000:
                break
            else:
                totalCharge += charge
    print(20000 - totalCharge)
