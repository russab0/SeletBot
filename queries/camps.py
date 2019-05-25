import requests
import re
from constants import SITE, CAMPS_NAMES_KEYWORDS


class CampsView:
    cur = None

    @staticmethod
    def list():
        r = requests.get(SITE + '/projects/camp/')
        page = r.text
        camps = re.findall(r'<a href="(/projects/camp/.+/)">(.+)</a>\n', page)[:19]
        return camps

    @staticmethod
    def retrieve(camp_name):
        camps = {name: link for link, name in CampsView.list()}
        info_site = SITE + camps[camp_name]

        r = requests.get(info_site)
        page = r.text
        track = re.findall(r'<div class="title">\s*Направление:\s*</div>\s*([^<]+)<', page)
        dates = re.findall(r'<div class="title">\s*Время проведения:\s*</div>\s*([^<]+)', page)
        place = re.findall(r'<div class="title">\s*Место проведения:\s*</div>\s*([^<]+)', page)
        reg = r'<b>Участники( смены)?: ?</b>\s*(ученики)?(&nbsp;</span>)?([^</\r/,]+)'
        part = re.findall(reg, page)
        if part:
            part = [part[0][1] + part[0][3]]
        fields = {'name': camp_name,
                  'link': camps[camp_name],
                  'Направление': track,
                  'Даты': dates,
                  'Место': place,
                  'Участники': part}
        return fields

    def camp_detail(name):
        fields = CampsView.retrieve(name)
        name = fields.pop('name')
        link = fields.pop('link')
        res = f'*{name}*\n'
        for key, value in fields.items():
            if value:
                res += f'*{key}*: {value[0]}\n'
        res += f'[{SITE + link}](Подробнее) '
        return res

    @staticmethod
    def next():
        if CampsView.cur is None:
            CampsView.cur = 0
        else:
            CampsView.cur += 1
        if CampsView.cur >= len(CAMPS_NAMES_KEYWORDS):
            CampsView.cur = 0
        name = list(CAMPS_NAMES_KEYWORDS.keys())[CampsView.cur]
        return CampsView.camp_detail(name)

    @staticmethod
    def prev():
        if CampsView.cur is None:
            CampsView.cur = 0
        else:
            CampsView.cur -= 1
        if CampsView.cur < 0:
            CampsView.cur = len(CAMPS_NAMES_KEYWORDS) - 1
        name = list(CAMPS_NAMES_KEYWORDS.keys())[CampsView.cur]
        return CampsView.camp_detail(name)
