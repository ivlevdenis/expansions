# coding: utf-8

import requests
import json
import random


class expansion_temp(expansion):
    def __init__(self, name):
        expansion.__init__(self, name)

    def command_boobs(self, stype, source, body, disp):
        request_temp_str = 'http://api.oboobs.ru/boobs/%d/%d/'
        count_boobs_req = 'http://api.oboobs.ru/boobs/count/'

        try:
            c = requests.get(count_boobs_req, verify=False)
            boobs_count = json.loads(c.text)[0]['count']
            c.close()
        except:
            boobs_count = 0

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

        if body.startswith('всего'):
            Answer('Сисек всего %d.' % boobs_count, stype, source, disp)
        else:
            if 5 < i < 10:
                Message(source[0], answer, disp)
                Answer('Сиськи в личке.', stype, source, disp)
            elif 10 <= i <= boobs_count:
                Answer('Зачем тебе столько?!', stype, source, disp)
            elif boobs_count == 0:
                Answer("Нет сисек :'(", stype, source, disp)
            elif i > boobs_count:
                Answer("Столько сисек нет :'(", stype, source, disp)
            else:
                Answer(answer, stype, source, disp)


    commands = ((command_boobs, "boobs", 1,),)

