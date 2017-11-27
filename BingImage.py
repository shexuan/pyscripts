import requests
import os
from lxml import etree


class BingImages(object):
    '''Download Bing images.'''

    def __init__(self):
        self.url = "http://bing.plmeizi.com/show/"
        self.img_dir = r"E:\BingImg"

    def getUrl(self):
        '''get the url of every image html.'''
        for i in range(100, 500):
            yield self.url + str(i)

    def getImageUrl(self):
        '''get the source url of images.'''
        url_list = self.getUrl()
        for url in url_list:
            res = requests.get(url)
            html = etree.HTML(res.content)
            img_src = html.xpath('//a[@id="picurl"]/@href')
            yield img_src[0]

    def downloadImage(self):
        '''Download image.'''
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
        print('over')


if __name__ == "__main__":
    img = BingImages()
    img.downloadImage()
