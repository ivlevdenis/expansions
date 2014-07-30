# coding: utf-8

# BlackSmith mark.2
# exp_name = "url" # /code.py v.x3
# Id: 24~3c
# Code © (2014) by den4ik [ivlevdenis.ru@gmail.com]

import re
import os
import requests
from lxml.html import parse, etree, HTMLParser

def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (("'", '&#39;'), ('"', '&quot;'), ('>', '&gt;'), ('<', '&lt;'), ('&', '&amp;'))
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

def str_fsize(sz):
    """
    Formats file size as string (i.e., 1.2 Mb)
    """
    if sz < 1024:
        return '%.2f байт' % sz
    sz /= 1024.0
    if sz < 1024:
        return '%.2f КБ' % sz
    sz /= 1024.0
    if sz < 1024:
        return '%.2f МБ' % sz
    sz /= 1024.0
    if sz < 1024:
        return '%.2f ГБ' % sz
    sz /= 1024.0
    return '%.2f ТБ' % sz


image_str = 'Изображение'
video_str = 'Видеозапись'
audio_str = 'Аудиозапись'
mime_answers = {
    'image': image_str,
    'video': video_str,
    'audio': audio_str
}

def parsing_lxml_fs(string):
    parser = HTMLParser()
    tree = etree.HTML(string, parser)
    texts = tree.xpath("string(//head//title)")
    return texts

def parsing(txt):
    title = re.search(r'<title[^>]*>([^<]+)</title>', txt, re.IGNORECASE)
    if title:
        return html_decode(re.sub(r'\s+', ' ', title.group(1), re.IGNORECASE))
    else:
        return 'Не могу стащить заголовок :('

class expansion_temp(expansion):
    def __init__(self, name):
        expansion.__init__(self, name)


    def urlParser(self, body, begin_string):
        url_list = re.findall(
            u'http[s]?://(?:[а-яА-ЯёЁa-zA-Z0-9]|[$-_@.&+]|[!*\(\),]|(?:%[а-яА-ЯёЁa-zA-Z0-9][а-яА-ЯёЁa-zA-Z0-9]))+',
            body,
            re.IGNORECASE)
        # url_list = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body,
        #                      re.IGNORECASE)
        ans = ""
        if url_list:
            for x in url_list:
                try:
                    r = requests.head(x, verify=False)
                    r.close()
                    if r.status_code == 501:
                        r = requests.get(x, verify=False)
                    if r.status_code == requests.codes.ok:
                        ct = r.headers.get('content-type')
                        if 'text/html' in ct:
                            t = requests.get(x, verify=False)
                            if requests.utils.get_encodings_from_content(t.text):
                                t.encoding = ''.join(requests.utils.get_encodings_from_content(t.text)[0])
                            title = parsing_lxml_fs(t.text)
                            ans = "\n".join([ans, title])
                            t.close()
                        else:
                            if str(ct).split('/')[0] in mime_answers.keys():
                                ans_prefix = mime_answers[str(ct).split('/')[0]] + ':'
                            else:
                                ans_prefix = 'Файл:'
                            ans = "\n".join(
                                [ans, " -- ".join([ans_prefix, os.path.basename(x), ct,
                                                   str_fsize(float(r.headers.get('content-length')))])])
                    else:
                        ans = "1/ Нет такого адреса :'("
                except:
                    ans = "2/ Нет такого адреса :'("

        return ans

    def urlWatcher(self, stanza, isConf, stype, source, body, isToBs, disp):
        if len(body) < 500:
            answer = self.urlParser(body, "Заголовок: %s")
            if answer:
                Message(source[1], answer, disp)

    handlers = ((urlWatcher, "01eh"),)


