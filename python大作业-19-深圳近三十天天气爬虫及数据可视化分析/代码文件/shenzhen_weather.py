import requests
import json
import xlwt
from bs4 import BeautifulSoup

url = "http://d1.weather.com.cn/calendar_new/2023/101280601_202306.html?_=1685708287098"
headers = {
    "Referer":
    "http://www.weather.com.cn/",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
}
r = requests.get(url=url, headers=headers)
if r.status_code == 200:
    content = r.content.decode(encoding='utf-8')
    weathers = json.loads(content[11:])

    writebook = xlwt.Workbook()
    sheet = writebook.add_sheet('Sheet1')
    keys = ['date', 'nlyf', 'nl', 'max', 'min', 'hmax', 'hmin', 'hgl']
    for i in range(len(keys)):
        sheet.write(0, i, keys[i])
    for i in range(len(weathers)):
        for j in range(len(keys)):
            sheet.write(i + 1, j, weathers[i][keys[j]])

    writebook.save('shenzhen_weathers.xls')
