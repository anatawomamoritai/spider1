import urllib.request
import os
import time
import random
#动态添加retrying模块路径，才能导入retrying模块
import sys
sys.path.append('F:\\anaconda\\lib\\site-packages')
from retrying import retry

'''
    直接找到目标图片的URL规律，进行爬取。
    retrying模块实现错误重连
    如果实在卡住，可以kill后重run,会从上次下的最后一个图片开始下载
  '''
#设置最大重复数50，可以避免下载完最后一页后一直死循环，可以去睡觉了。。。
#补充：就算重复50次后抛出异常（我只遇到了bad gatway）urlopen仍然会重复下一个50次，共n*50次
@retry(stop_max_attempt_number=50, wait_random_min=0, wait_random_max=1000)
def f(url):
    print('开始重试')
    iplist = ['117.191.11.79:8080', '47.98.237.129:80', '39.137.69.6:8080', '39.137.69.6:80', '223.111.254.83:80', '39.137.107.98:8080', '39.137.107.98:80', '120.198.230.15:8080', '120.78.174.170:8080', '117.191.11.104:8080', '117.191.11.104:80', '117.191.11.110:80', '117.191.11.111:80', '117.191.11.108:80', '117.191.11.113:8080', '117.191.11.76:80', '117.191.11.78:8080', '117.191.11.108:8080', '117.191.11.113:80', '117.191.11.74:80', '117.191.11.73:80', '117.191.11.74:8080', '117.191.11.73:8080', '117.191.11.77:8080', '117.191.11.75:80', '117.191.11.75:8080', '117.191.11.71:80', '117.191.11.103:8080']

    proxy_support = urllib.request.ProxyHandler({'http':random.choice(iplist)})

    opener = urllib.request.build_opener(proxy_support)
    opener.addhearers = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36')]

    urllib.request.install_opener(opener)

    #urlopen封装了？捕获错误然后重试n次的功能
    response = urllib.request.urlopen(url)
    #decode（‘utf-8’）不能解码jpg，后者是bytes格式
    html = response.read()#.decode('utf-8')
    print('url opened!')
    return html

    
def save_img(url):
    filename = url.split('/')[-1]
    with open (filename, 'wb') as g:
        img = f(url)
        g.write(img)

def download(i):
    while i <100:
        #HTTP Error 504: Gateway Timeout会自动重复这一帧，直到成功或退出
        #因为urllib.request.urlopen("url",timeout=?)有timeout参数
        print(i)
        url = 'http://p1.xiaoshidi.net/2014/03/26191034' + str(i) + '.jpg'
        print('downloading %s ...' %url)
               
        try:
            save_img(url)
            time.sleep(1)
            i += 1
        except urllib.error.HTTPError as e:
            print('%s: %s' %(url, e))
                
    print('all done!')

#找出上次程序中断后最后下载的页面
def find_max_num():
    last0 = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.jpg']

    last1 = []
    for num in last0:
        num = num.split('.')
        last1.append(num)
        
    last2 = []
    for num in last1:
        num = int(num[0])
        last2.append(num)
    
    last_num = max(last2) - 261910340
    if last_num > 10:
        last_num = max(last2) - 2619103400

    return last_num


if __name__ == '__main__':
    folder=r'E:\Users\ZhangMalin\Desktop\slamdunk\31'
    #判断是否已经存在folder
    if not os.path.isdir(folder):
        os.mkdir(folder)
    os.chdir(folder)
    #判断新的folder里有没有file
    if os.listdir('.'):
        last_num = find_max_num()
        download(i=last_num)
    else:
        download(i=0)
