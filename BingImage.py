import requests
import os
from lxml import etree


class BingImages(object):
    '''Download Bing images.'''

    def __init__(self):
        self.url = "http://bing.plmeizi.com/show/"
        self.img_dir = r"E:\BingImg"

    def getUrl(self):
        '''get the url of every image.'''
        url_list = []
        for i in range(0, 500):
            url_list.append(self.url + str(i))
        return url_list

    def getImageUrl(self):
        '''download images from url.'''
        url_list = self.getUrl()
        img = []
        for url in url_list:
            res = requests.get(url)
            html = etree.HTML(res.content)
            img_src = html.xpath('//a[@id="picurl"]/@href')
            img.append(img_src[0])
        return img

    def downloadImage(self):
        if not os.path.exists(self.img_dir):
            os.mkdir(self.img_dir)
        img = self.getImageUrl()
        for url in img:
            res = requests.get(url)
            res.encoding = "utf-8"
            img_name = (url.split('/')[-1]).split('_')[0]
            img_type = url.split('.')[-1]
            with open("{0}\{1}.{2}".format(self.img_dir, img_name, img_type), "wb") as f:
                f.write(res.content)


if __name__=="__main__":
    img = BingImages()
    img.downloadImage()
