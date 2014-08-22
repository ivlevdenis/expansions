# coding: utf-8

# BlackSmith mark.2
# exp_name = "url" # /code.py v.x3
# Id: 24~3c
# Code © (2014) by den4ik [ivlevdenis.ru@gmail.com]

import re
import os
import requests
from lxml import html


def parsing(txt):
    title = re.search('<title[^>]*>([^<]+)</title>', txt, re.IGNORECASE)
    if title:
        title = title.group(1)
        title = re.sub('\s+', ' ', title)
        return html.fromstring(title).text
    else:
        return u'Не могу стащить заголовок :('


headers = {
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Connection': 'keep-alive',
}

mime_answers = {
    'image': u'Изображение',
    'video': u'Видео'
}


def str_fsize(sz):
    """
    Formats file size as string (i.e., 1.25 Mb)
    """
    if sz < 1024:
        return u'%.2f байт' % sz
    sz /= 1024.0
    if sz < 1024:
        return u'%.2f КБ' % sz
    sz /= 1024.0
    if sz < 1024:
        return u'%.2f МБ' % sz
    sz /= 1024.0
    if sz < 1024:
        return u'%.2f ГБ' % sz
    sz /= 1024.0
    return u'%.2f ТБ' % sz


def get_headers(url):
    r = requests.head(url, verify=False)
    if r.status_code != requests.codes.ok:
        r = requests.get(url, verify=False)
    return r.headers


class expansion_temp(expansion):
    def __init__(self, name):
        expansion.__init__(self, name)


    def urlParser(self, body):
        url_list = re.findall(
            r'http[s]?://(?:[а-яА-ЯёЁa-zA-Z0-9]|[$-_@.&+]|[!*\(\),]|(?:%[а-яА-ЯёЁa-zA-Z0-9][а-яА-ЯёЁa-zA-Z0-9]))+',
            body,
            re.IGNORECASE)
        ans = ""
        if url_list:
            for x in url_list:
                try:
                    head = get_headers(x)
                    if head:
                        ct = head.get('content-type')
                        if 'text/html' in ct:
                            cont = requests.get(x, verify=False, headers=headers)
                            if not cont.text:
                                cont = requests.post(x, verify=False, headers=headers)
                            enc = requests.utils.get_encoding_from_headers(head)
                            enc_cont = requests.utils.get_encodings_from_content(cont.text)
                            if len(enc_cont) > 0:
                                enc = enc_cont[0] if isinstance(enc_cont, list) else enc_cont
                            cont.encoding = enc
                            title = parsing(cont.text)
                            ans = u"\n".join([ans, u"Заголовок: %s" % title])
                        else:
                            ans_prefix = ''
                            if str(ct).split('/')[0] in mime_answers.keys():
                                ans_prefix = mime_answers[str(ct).split('/')[0]] + ':'
                            size = head.get('content-length') if head.get('content-length') else '0'
                            ans = u"\n".join([ans, ans_prefix + ' ' + u" — ".join(
                                [os.path.basename(x), ct, str_fsize(float(size))])])
                    else:
                        ans = u"1/ Нет такого адреса :'("
                except RuntimeError:
                    ans = u"2/ Нет такого адреса :'("
        return ans

    def urlWatcher(self, stanza, isConf, stype, source, body, isToBs, disp):
        if len(body) < 500:
            answer = self.urlParser(body)
            if answer:
                if isConf and not isToBs:
                    Message(source[1], answer, disp)
                else:
                    Answer(answer, stype, source, disp)

    handlers = ((urlWatcher, "01eh"),)


