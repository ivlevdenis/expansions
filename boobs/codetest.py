# coding: utf-8

import requests
import json
import random


def command_man(body):

    request_temp_str = 'http://api.oboobs.ru/boobs/%d/%d/'
    count_boobs_req = 'http://api.oboobs.ru/boobs/count/'

    try:
        c = requests.get(count_boobs_req, verify=False)
        boobs_count = json.loads(c.text)[0]['count']
        c.close()
    except:
        boobs_count = 0

    if body.startswith('всего'):
        answer = 'Фоток с сиськами всего %d.' % boobs_count
        return answer
    i = int(body) if body.isdigit() else 1

    id_bs = random.choice(xrange(boobs_count))

    if id_bs < i:
        id_bs = i

    print(boobs_count)

    rs = request_temp_str % (id_bs,i)

    r = requests.get(rs, verify=False)
    print(r.text)
    rq_ans = json.loads(r.text)

    ans = []
    for x in rq_ans:
        id_str = '0'*(1 + len(str(boobs_count)) - len(str(x['id']))) + str(x['id'])
        ans.append('http://media.oboobs.ru/boobs/' + id_str + '.jpg')

    answer = '\n'.join(ans)

    return answer

print(command_man(''))
