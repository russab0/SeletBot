import requests
import re
from constants import SITE


class CampsView:
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


#for camp in CampsView().list():
#    print('===========' + camp[1] + '==========')
#    CampsView().retrieve(camp[1])
CampsView().retrieve('Санак')
