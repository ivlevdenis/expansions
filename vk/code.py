# coding: utf-8

# BlackSmith mark.2
# exp_name = "turn" # /code.py v.x3
# Id: 21~3c
# Code © (2011-2012) by WitcherGeralt [alkorgun@gmail.com]

import vk_api
from datetime import datetime

LOGIN = u''
PASSWORD = u''


def vk_login():
    login, password = LOGIN, PASSWORD
    try:
        return vk_api.VkApi(login, password)  # Авторизируемся
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return None  # и выйдем


def get_group_info(vk):
    group_id = 33241
    values = {
        'group_id': group_id,
        'fields': 'city,country,description,members_count,counters'
    }
    response = vk.method('groups.getById', values)
    ans = ''
    if response:
        for r in response:
            name = 'Имя: %s' % r['name']
            city = 'Город: %s' % r['city']['title']
            description = 'Описание: %s' % r['description']
            members_count = 'Друзья: %d' % int(r['members_count'])
            country = 'Страна: %s' % r['country']['title']
            link = 'http://vk.com/%s' % r['screen_name']
            ans = '\n'.join([ans, '\n'.join([name, description, city, country, members_count, link])])
        return ans


def get_group_stats(vk, date_from=datetime.today(), date_to=datetime.today()):
    group_id = 33241
    values = {
        'group_id': group_id,
        'date_from': date_from.strftime('%Y-%m-%d'),
        'date_to': date_to.strftime('%Y-%m-%d')
    }
    response = vk.method('stats.get', values)
    ans = ''
    if response:
        for period in response:
            visitors = 'Посетителей: %s' % period['visitors']
            views = 'Просмотров: %s' % period['views']
            subscribed = 'Подписались: %s' % period['subscribed']
            unsubscribed = 'Отписались: %s' % period['unsubscribed']
            ans = '\n'.join([ans, '\n'.join([visitors, views, subscribed, unsubscribed])])
        return ans


def get_wall_post(vk, count=1, offset=0):
    if count > 10:
        count = 10
    if count < 1:
        count = 1
    values = {
        'owner_id': -33241,
        'count': count,
        'offset': offset
    }
    response = vk.method('wall.get', values)  # Используем метод wall.get
    ans = ''
    if response:
        for item in response['items']:
            date = 'Опубликован: %s' % datetime.fromtimestamp(int(item['date'])).strftime(
                '%d.%m.%Y %H:%M:%S')
            text = 'Запись: %s' % item['text']
            comments = 'Прокомментировали: %d' % int(item['comments']['count'])
            likes = 'Понравилось: %d' % int(item['likes']['count'])
            can_publish = 'Поделились: %d' % int(item['likes']['can_publish'])
            ans = '\n'.join([ans, '\n'.join([text, date, likes, can_publish, comments])])
        return ans


class expansion_temp(expansion):
    def __init__(self, name):
        expansion.__init__(self, name)

    vk = vk_login()

    def command_vk(self, stype, source, body, disp):
        args = str(body).split()
        if len(args) > 0:
            if args[0].lower() == 'стена':
                if len(args) > 2 and str(args[1]).isdigit() and str(args[2]).isdigit():
                    Answer(get_wall_post(self.vk, int(args[1]), int(args[2])), stype, source, disp)
                elif len(args) > 1 and str(args[1]).isdigit():
                    Answer(get_wall_post(self.vk, int(args[1])), stype, source, disp)
                else:
                    Answer(get_wall_post(self.vk), stype, source, disp)
            elif args[0].lower() == 'стат':
                if len(args) > 1:
                    if args[1].lower() == 'сегодня':
                        Answer(get_group_stats(self.vk), stype, source, disp)
                    elif args[1].lower() == 'вчера':
                        yesterday = datetime.fromordinal(datetime.today().toordinal() - 1)
                        Answer(get_group_stats(self.vk, yesterday, yesterday), stype, source, disp)
                    elif args[1].lower() == 'годназад':
                        day = datetime.today().replace(year=datetime.today().year - 1)
                        Answer(get_group_stats(self.vk, day, day), stype, source, disp)
        else:
            Answer(get_group_info(self.vk), stype, source, disp)


    commands = ((command_vk, "vk", 1,),)
