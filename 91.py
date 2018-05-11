
from multiprocessing import Pool
import time
import re
import multiprocessing
from bs4 import BeautifulSoup
import  requests
from xlrd import open_workbook
from xlutils.copy import copy
#print("程序开始执行 by cl monkey13180\")
try:
    f = open('config.txt', 'r')
    config = str(f.read()).split('\n')
    start = config[0]
    end = config[1]
    url = config[2]
except Exception as e:
    print("请在当前目录下创建config.txt, 请按顺序填写页码,fid,域名并敲回车!")

class Pool_91(object):
    def __init__(self,range,res):
        self.range=range
        self.res=res
    def run(self):
        # print(self.res)
        AllData = []
        for x in range(self.range[0], self.range[1]):
            proxy_list = []
            true_url = self.getTrueUrl(x)
            proxy_list.append(true_url)
            proxy_list.append(self.res[x][1])
            AllData.append(proxy_list)
        # print(AllData)
        return AllData
    def getTrueUrl(self,num):

        print('正在保存：{}{}'.format(self.res[num][1],self.res[num][0]))
        try:
            data = {
                'url': self.res[num][0]
            }
            aaa = requests.post('http://cj.9530.net/index.php', data=data, allow_redirects=False)
            soup = BeautifulSoup(aaa.content, 'lxml')
            aa = (soup.find_all(attrs={'download': 'a'}))
            true_url =(aa[0].get('href'))
        except:
            pass
        return true_url
    def mycallback(self,x):


        rexcel = open_workbook("list.xls")
        rows = rexcel.sheets()[0].nrows
        excel = copy(rexcel)
        table = excel.get_sheet(0)
        #
        row = rows
        for value in x:
            table.write(row, 0, time.strftime("%Y-%m-%d %H:%M:%S"))
            table.write(row, 1, value[1])
            table.write(row, 2, value[0])
            row += 1
        excel.save("list.xls")



if __name__ == '__main__':
    multiprocessing.freeze_support()
    AllUrl = []
    for i in range(int(start), int(end)+1):  # 1-6
        time.sleep(2)
        data={
            'session_language':'cn_CN'
        }
        page = requests.post('{}&page={}'.format(url,i),data)
        soup = BeautifulSoup(page.content, 'html.parser')
        TempUrlList = soup.find_all(href=re.compile('view_video'),title='')
        TempUrlList1 = soup.find_all(class_='listchannel')
        for i in TempUrlList:
            UrlList = []
            UrlList.append(i['href'])
            UrlList.append(i.findAll('img')[0]['title'])
            AllUrl.append((UrlList))

    all_num = len(AllUrl)
    num = 4  # number of cpu cores
    per_num, left = divmod(all_num, num)
    s = range(0, all_num, per_num)
    res = []
    for i in range(len(s) - 1):
        res.append((s[i], s[i + 1]))
    res.append((s[len(s) - 1], all_num))
    pool = Pool()
    for i in res:
        _91pron = Pool_91(i,AllUrl)

        pool.apply_async(_91pron.run, (), callback=_91pron.mycallback)

    pool.close()
    pool.join()
