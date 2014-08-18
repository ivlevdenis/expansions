# coding: utf-8

# BlackSmith mark.2
# exp_name = "vk" # /code.py v.x3
# Id: 21~3c
# Code © (2011-2014) by den4ik [ivlevdenis.ru@gmail.com]

import os
import vk_api
import json
from datetime import datetime


def vk_login(login, password):
    try:
        return vk_api.VkApi(login, password)  # Авторизируемся
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return None  # и выйдем


def get_group_info(vk, group_id):
    values = {
        'group_id': group_id,
        'fields': 'city,country,description,members_count,counters'
    }
    response = vk.method('groups.getById', values)
    ans = ''
    if response:
        for r in response:
            name = 'Имя: {}'.format(r['name'])
            city = 'Город: {}'.format(r['city']['title'])
            description = 'Описание: {}'.format(r['description'])
            members_count = 'Друзья: {}'.format(int(r['members_count']))
            country = 'Страна: {}'.format(r['country']['title'])
            link = 'http://vk.com/{}'.format(r['screen_name'])
            ans = '\n'.join([ans, '\n'.join([name, description, city, country, members_count, link])])
        return ans


def get_group_stats(vk, group_id, date_from=datetime.today(), date_to=datetime.today()):
    values = {
        'group_id': group_id,
        'date_from': date_from.strftime('%Y-%m-%d'),
        'date_to': date_to.strftime('%Y-%m-%d')
    }
    response = vk.method('stats.get', values)
    ans = ''
    if response:
        visitors = 'Посетителей: {}'.format(sum([int(x['visitors']) for x in response if x['visitors']]))
        views = 'Просмотров: {}'.format(sum([int(x['views']) for x in response if x['views']]))
        subscribed = 'Подписались: {}'.format(sum([int(x['subscribed']) for x in response if x['subscribed']]))
        unsubscribed = 'Отписались: {}'.format(sum(
            [int(x['unsubscribed']) for x in response if x['unsubscribed']]))
        sex_male = 0
        sex_female = 0
        for r in response:
            sex_male += sum([int(x['visitors']) for x in r['sex'] if x['value'] == 'm'])
            sex_female += sum([int(x['visitors']) for x in r['sex'] if x['value'] == 'f'])
        sex_male = '♂ - {}'.format(sex_male)
        sex_female = '♀ - {}'.format(sex_female)
        ans = '\n'.join([visitors, views, subscribed, unsubscribed, sex_male + ' ' + sex_female])
        return ans


def get_wall_post(vk, group_id, count=1, offset=0):
    if count > 10:
        count = 10
    if count < 1:
        count = 1
    values = {
        'owner_id': -1 * group_id,
        'count': count,
        'offset': offset
    }
    response = vk.method('wall.get', values)  # Используем метод wall.get
    ans = ''
    if response:
        for item in response['items']:
            date = 'Опубликован: {}'.format(datetime.fromtimestamp(int(item['date'])).strftime(
                '%d.%m.%Y %H:%M:%S'))
            text = 'Запись: {}'.format(item['text'])
            comments = 'Комментариев: {}'.format(int(item['comments']['count']))
            likes = '♥ - {}'.format(int(item['likes']['count']))
            can_publish = '♲ - {}'.format(int(item['likes']['can_publish']))
            ans = '\n'.join([ans, '\n'.join([text, date, can_publish + ' ' + likes, comments])])
        return ans


def get_topics(vk, group_id, count=1, offset=0):
    if count < 1:
        count = 1
    if count > 10:
        count = 10
    values = {
        'group_id': group_id,
        'count': count,
        'offset': offset,
        'order': 2
    }
    response = vk.method('board.getTopics', values)
    ans = ''
    if response:
        items_count = response['count']
        if count > items_count:
            count = items_count
        for item in response['items']:
            date = 'Опубликован: {}'.format(datetime.fromtimestamp(int(item['created'])).strftime(
                '%d.%m.%Y %H:%M:%S'))
            title = 'Название: {}'.format(item['title'])
            comments = 'Комментариев: {}'.format(int(item['comments']))
            id = 'id: {}'.format(int(item['id']))
            ans = '\n\n'.join([ans, '\n'.join([title, comments, date, id])])
        return ans


def comment_topic(vk, group_id, topic_id, comment):
    values = {
        'group_id': group_id,
        'topic_id': topic_id,
        'text': comment,
    }
    return vk.method('board.addComment', values)


def get_topic_comments(vk, group_id, topic_id, count=1, offset=0, order=0):
    if count < 1:
        count = 1
    if count > 10:
        count = 10
    sort = 'asc' if order else 'desc'
    values = {
        'group_id': group_id,
        'topic_id': topic_id,
        'count': count,
        'offset': offset,
        'sort': sort
    }
    response = vk.method('board.getComments', values)
    ans = ''
    if response:
        items_count = response['count']
        if count > items_count:
            count = items_count
        if len(response['items']) > 0:
            for item in response['items']:
                date = 'Опубликован: {}'.format(datetime.fromtimestamp(int(item['date'])).strftime(
                    '%d.%m.%Y %H:%M:%S'))
                text = 'Сообщение: {}'.format(item['text'])
                id = 'id: {}'.format(int(item['id']))
                ans = '\n\n'.join([ans, '\n'.join([text, date, id])])
        return ans


class expansion_temp(expansion):
    def __init__(self, name):
        expansion.__init__(self, name)
        self.confn = os.path.join(os.getcwd(), 'expansions', 'vk', 'vk.cfg')
        self.vk_config = json.load(open(self.confn))
        self.vk = vk_login(self.vk_config['login'], self.vk_config['password'])
        self.group_id = int(self.vk_config['group'])
        self.watch_topics = self.vk_config['watch_topics']


    def command_vk(self, stype, source, body, disp):
        args = str(body).split()
        post_temp = 'https://vk.com/topic-{0}_{1}?post={2}'
        if len(args) > 0:
            if args[0].lower() == 'стена':
                if len(args) > 2 and str(args[1]).isdigit() and str(args[2]).isdigit():
                    Answer(get_wall_post(self.vk, self.group_id, int(args[1]), int(args[2])), stype, source, disp)
                elif len(args) > 1 and str(args[1]).isdigit():
                    Answer(get_wall_post(self.vk, self.group_id, int(args[1])), stype, source, disp)
                else:
                    Answer(get_wall_post(self.vk), stype, source, disp)
            elif args[0].lower() == 'стат':
                if len(args) > 1:
                    if args[1].lower() == 'сегодня':
                        Answer(get_group_stats(self.vk, self.group_id, ), stype, source, disp)
                    elif args[1].lower() == 'вчера':
                        yesterday = datetime.fromordinal(datetime.today().toordinal() - 1)
                        Answer(get_group_stats(self.vk, self.group_id, yesterday, yesterday), stype, source, disp)
                    elif args[1].lower() == 'год':
                        day = datetime(datetime.today().year, 1, 1)
                        Answer(get_group_stats(self.vk, self.group_id, day), stype, source, disp)
                    elif args[1].lower() == 'месяц':
                        day = datetime(datetime.today().year, datetime.today().month, 1)
                        Answer(get_group_stats(self.vk, self.group_id, day), stype, source, disp)
                    elif args[1].lower() == 'годназад':
                        day = datetime.today().replace(year=datetime.today().year - 1)
                        Answer(get_group_stats(self.vk, self.group_id, day, day), stype, source, disp)
                    elif args[1].lower() == 'дата' and len(args) > 2:
                        try:
                            day = datetime.strptime(str(args[2]), '%d-%m-%Y')
                            Answer(get_group_stats(self.vk, self.group_id, day, day), stype, source, disp)
                        except ValueError as e:
                            Answer('Неправильный формат даты, пример: 14-08-2014.', stype, source, disp)
                    elif args[1].lower() == 'период' and len(args) > 3:
                        try:
                            day1 = datetime.strptime(str(args[2]), '%d-%m-%Y')
                            day2 = datetime.strptime(str(args[3]), '%d-%m-%Y')
                        except ValueError as e:
                            Answer('Неправильный формат даты, пример: 14-08-2014.', stype, source, disp)
                        if day2.toordinal() > day1.toordinal():
                            if day2.year - day1.year < 4:
                                Answer(get_group_stats(self.vk, self.group_id, day1, day2), stype, source, disp)
                            else:
                                Answer('Слишком большой период для запроса статистики.', stype, source, disp)
                        else:
                            Answer('Начальная дата не может быть больше конечной.', stype, source, disp)
            elif args[0].lower() == 'топик':
                if len(args) > 2 and str(args[1]).isdigit():
                    if args[2].lower() == 'коммент':
                        try:
                            link = post_temp.format(self.group_id, args[1],
                                                    comment_topic(self.vk, self.group_id, int(args[1]),
                                                                  ' '.join(args[3:])))
                            Answer('Комментарий успешно добавлен.\n' + link, stype, source, disp)
                        except vk_api.ApiError as e:
                            Answer('Ошибка комментирования.', stype, source, disp)
                    elif args[2].lower() == 'читать':
                        if len(args) > 4 and str(args[3]).isdigit() and str(args[3]).isdigit():
                            Answer(get_topic_comments(self.vk, self.group_id, int(args[1]), int(args[3]),
                                                      int(args[4])), stype, source, disp)
                        elif len(args) > 3 and str(args[3]).isdigit():
                            Answer(get_topic_comments(self.vk, self.group_id, int(args[1]), int(args[3])),
                                   stype, source, disp)
                        else:
                            Answer(get_topic_comments(self.vk, self.group_id, int(args[1])), stype, source,
                                   disp)
                else:
                    Answer('Неправильный формат запроса.', stype, source, disp)
            elif args[0].lower() == 'топики':
                if len(args) > 1 and str(args[1]).isdigit():
                    Answer(get_topics(self.vk, self.group_id, int(args[1])), stype, source, disp)
                else:
                    Answer(get_topics(self.vk, self.group_id), stype, source, disp)

        else:
            Answer(get_group_info(self.vk, self.group_id), stype, source, disp)


    commands = ((command_vk, "vk", 1,),)
