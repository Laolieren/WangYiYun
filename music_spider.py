import requests
from lxml import etree
import json
# shi
class WangYiYun(object):
    def __init__(self):
        """
        初始化操作
        """
        self.headers = {
            "Connection": "close",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
        }
        self.type_url = "https://music.163.com/discover/playlist/"

    def get_response(self, url):
        """
        请求地址返回响应
        """
        response = requests.get(url, headers=self.headers)

        return response.content.decode()

    def collect_tpye_info(self, html_str):
        """
        获取歌曲分类信息
        """
        html = etree.HTML(html_str)
        groups = html.xpath("//dl[@class='f-cb']/dd/a")
        type_url_list = []
        for group in groups:
            item = {}
            # 种类名称
            item['name'] = group.xpath("@data-cat")[0] if len(group.xpath("@data-cat")) > 0 else None
            # 种类对应的url地址
            item['href'] = "https://music.163.com" + group.xpath("@href")[0] if len(group.xpath("@href")) > 0 else None
            type_url_list.append(item)
        return type_url_list

    def get_music_form(self, type_url):
        """
        每个种类对应的歌单信息
        """
        next_url = type_url["href"]
        type_name = type_url["name"]
        form_dict = {}
        form_list = []
        while next_url is not None:
            html_str = self.get_response(next_url)
            html = etree.HTML(html_str)
            # 分组
            groups = html.xpath("//ul[@class='m-cvrlst f-cb']/li")
            for group in groups:
                item = {}
                # 歌单的名称
                item['name'] = group.xpath("./p[@class='dec']/a/@title")[0] if len(
                    group.xpath("./p[@class='dec']/a/@title")) > 0 else None
                # 歌单的地址
                item['href'] = "https://music.163.com" + group.xpath("./p[@class='dec']/a/@href")[0] if len(
                    group.xpath("./p[@class='dec']/a/@href")) > 0 else None
                form_list.append(item)
            # 获取下一页的地址,直到最后一页
            next_url = "https://music.163.com" + html.xpath("//div[@class='u-page']/a[@class='zbtn znxt']/@href")[
                0] if len(
                html.xpath("//div[@class='u-page']/a[@class='zbtn znxt']/@href")) > 0 else None
        form_dict[type_name] = form_list
        return form_dict

    def save_content(self, form_dict):
        with open('douban.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(form_dict))
            f.write('\n')

    def run(self):
        # 请求歌单地址，获取网页数据
        html_str = self.get_response(self.type_url)
        # 提取网页数据，获取歌区种类地址
        type_url_list = self.collect_tpye_info(html_str)
        # 对歌曲种类地址进行遍历，获取每种歌曲种类的歌单信息
        for type_url in type_url_list:
            form_dict = self.get_music_form(type_url)
            self.save_content(form_dict)

if __name__ == '__main__':
    spider = WangYiYun()
    spider.run()
