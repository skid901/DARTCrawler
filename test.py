import math

def solution0(participant, completion):
    p, c = sorted(participant), sorted(completion)
    if len(p) == 1:
        return p[0]
    mid = math.floor( len(participant)/2 )
    p1, p2 = p[:mid], p[mid:]
    c1, c2 = c[:mid], c[mid:]
    if p1[-1] == c1[-1]:
        return solution(p2, c2)
    else :
        return solution(p1, c1)


import collections

def solution(participant, completion):
    print(collections.Counter(participant))
    print(collections.Counter(completion))
    answer = collections.Counter(participant) - collections.Counter(completion)
    print(answer)
    print(answer.keys())
    return list(answer.keys())[0]


if __name__=="__main__":
    p = ['a','b','c','d','d'] #['a', 'b', 'b', 'c']
    c = ['a','b','d','c'] #['a', 'b' ,'c']
    print('return', solution(p, c))
