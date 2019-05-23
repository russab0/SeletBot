import requests
import re
from constants import SITE


class ApplicationsView:
    @staticmethod
    def list():
        r = requests.get(SITE)
        page = r.text
        app = re.findall(r'<a href="(/form/\?ID=\d{5})" class="btn" id="bx_3218110189_\d{5}">(.+)</a>', page)

        for i in range(len(app)):
            pos = app[i][1].find('style')
            app[i] = list(app[i])
            if pos >= 0:
                app[i][1] = app[i][1][:pos - 1]
        return app
