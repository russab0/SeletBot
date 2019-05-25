from constants import SITE


def list_of_links(link_name_list):
    lines = [f'🔹 [{name}]({SITE}{link})' for link, name in link_name_list]
    res = '\n'.join(lines)
    return res
