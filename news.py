import requests
from bs4 import BeautifulSoup
import json

def getHTMLText(url):
    '''
    获取网页的html文档
    '''
    try:
        #添加请求头
        #不同网页的请求头不同
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36'
        }

        #获取服务器的响应内容
        res = requests.get(url, headers = headers)
        #判断返回状态码是否为200
        res.raise_for_status()
        #设置该html文档可能的编码
        res.encoding = res.apparent_encoding
        #返回网页HTML代码
        return res.text
    except:
        return '产生异常'

def main():

    # 保存爬取后的URL到列表中
    array = []
    # 保存爬取后的标题到列表中
    titleArray = []

    #目标网页————知乎
    urls = ['https://www.zhihu.com/search?q=化石收藏&utm_content=search_suggestion&type=content', 'https://www.zhihu.com/search?q=化石形成&utm_content=search_suggestion&type=content','https://www.zhihu.com/search?type=content&q=鱼化石','https://www.zhihu.com/search?type=content&q=植物化石','https://www.zhihu.com/search?q=化石复原&utm_content=search_history&type=content']
    for url in urls:
        demo = getHTMLText(url)
        # print(demo)

        #解析HTML代码
        soup = BeautifulSoup(demo, 'html.parser')

        #模糊搜索HTML代码的所有包含href属性的<a>标签
        a_labels = soup.find_all('a', attrs={'href': True})
        #查找标题
        titles = soup.find_all('span', 'Highlight')

        #获取所有<a>标签中的href对应的值，即超链接
        for a in a_labels:
            if(str(a.get('href')).startswith('/question')):
                array.append('https://www.zhihu.com' + str(a.get('href')))
        for b in titles:
            bb = str(b)
            string2 = "<em>"
            string3 = "</em>"
            string4 = "</span>"
            number2 = bb.find(string2)
            number3 = bb.find(string3)
            number4 = bb.find(string4)
            result = bb[24:number2] + bb[(number2+4):number3] + bb[number3 + 5:number4]
            while(result.find(string2) >= 0):
                index = result.find(string2)
                index2 = result.find(string3)
                result = result[0:index] + result[index+4:index2] + result[index2+5:len(result)]
            titleArray.append(result)
    index = 0
    dics = []
    for a in array:
        key = "url" + str(index)
        url = a
        topic = titleArray[index]
        index = index + 1
        newDic = {"topic" : topic, "url" : url}

        dics.append({key:newDic})

    # for a in array:
    #     print(a)
    # for b in titleArray:
    #     print(b)

    with open('data.json', 'w') as file:
        json.dump(dics, file)


main()
