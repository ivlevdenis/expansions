# coding: utf-8

import requests
from lxml import html


class expansion_temp(expansion):
    def __init__(self, name):
        expansion.__init__(self, name)

    def command_devdb(self, stype, source, body, disp):

        request_temp_str = 'http://devdb.ru/search'
        err_ans = 'Не могу найти %s'

        def parsing_lxml_path(text, path):
            tree = html.fromstring(text)
            texts = tree.xpath(path)
            texts = [x.text for x in texts]
            # r.close()
            return texts

        def parsing_lxml_urls(text, path):
            tree = html.fromstring(text)
            texts = tree.xpath(path)
            texts = [x for x in texts]
            #r.close()
            return texts

        if len(body) < 3:
            Answer('Для поиска нужно больше 3х символов', stype, source, disp)
            return

        data = {'search': body}
        rs = request_temp_str
        r = requests.post(rs, data, verify=False)
        r.close()

        if r.status_code == requests.codes.ok and not 'Ам-м-м-м-м-м-м-м-м.' in r.text:
            # print(r.text)
            l = parsing_lxml_path(r.text, '//tr[@class="brand_model_preview_bp"]/td/a')
            t = parsing_lxml_urls(r.text, '//tr[@class="brand_model_preview_bp"]/td/a/@href')
            answer = '\n'.join(['  ==>  '.join(x) for x in map(list, zip(l, t))])
            if l and len(l) > 10:
                Message(source[0], answer, disp)
                Answer('Ответ в привате!', stype, source, disp)
                return
        elif 'хуй' in str(body).lower():
            answer = 'Забыл характеристики?!'
        elif 'пизда' in str(body):
            answer = 'Забыл характеристики?!'
        else:
            answer = err_ans % body

        Answer(answer, stype, source, disp)


    commands = ((command_devdb, "devdb", 1,),)