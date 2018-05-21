from webscrapy import Webscrapy as ws

url = 'https://coolshell.cn/articles/1679.html'
filepath = 'test'
if __name__ =='__main__':
    ws.saveList(url,filepath)
