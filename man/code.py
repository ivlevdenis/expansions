# coding: utf-8

import requests


request_temp_str = 'http://www.opennet.ru/man.shtml?topic=%s'
err_ans = 'Не могу найти страницы для %s'

class expansion_temp(expansion):
    def __init__(self, name):
        expansion.__init__(self, name)

    def command_man(self, stype, source, body, disp):
        if len(str(body).replace(' ','')) < 1:
            body = 'man'

        rs = request_temp_str % body
        r = requests.get(rs, verify=False)
        r.close()

        if r.status_code == requests.codes.ok and not 'Руководство не найдено.' in r.text:
            answer = ' '.join([rs])
        elif 'хуй' in str(body).lower():
            answer = 'Забыл как пользоваться?!'
        elif 'пизда' in str(body):
            answer = 'Такая лохматая штуковина. В основном у женского пола.'
        else:
            answer = err_ans % body

        Answer(answer, stype, source, disp)


    commands = ((command_man, "man", 1,),)