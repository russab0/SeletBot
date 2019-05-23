import requests
import re
from constants import SITE


class ProjectsView:
    @staticmethod
    def list():
        projects = list()
        for page_num in range(1, 5):
            r = requests.get(f'{SITE}/projects/proekty-2019/?PAGEN_1={page_num}')
            page = r.text
            projects += re.findall(r'<h3 class="news-title"><a href="(.+)">(.+)</a></h3>', page)
            page_num += 1
        print(projects)
        return projects
