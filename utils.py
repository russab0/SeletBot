from constants import SITE
from queries.camps import CampsView


def list_of_links(link_name_list):
    lines = [f'🔹 [{name}]({SITE}{link})' for link, name in link_name_list]
    res = '\n'.join(lines)
    return res


def camp_detail(name):
    fields = CampsView.retrieve(name)
    name = fields.pop('name')
    link = fields.pop('link')
    res = f'*{name}*\n'
    for key, value in fields.items():
        if value:
            res += f'*{key}*: {value[0]}\n'
    res += f'[{SITE + link}](Подробнее) '
    print(res)
    return res
