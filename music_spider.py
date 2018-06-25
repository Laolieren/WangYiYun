import requests
from lxml import etree


class WangYiYun(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
        }
        self.type_url = "https://music.163.com/discover/playlist/"

    def get_response(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def collect_tpye_info(self, html_str):
        html = etree.HTML(html_str)
        groups = html.xpath("//dl[@class='f-cb']/dd/a")
        type_url_list = []
        for group in groups:
            item = {}
            item['name'] = group.xpath("@data-cat")[0] if len(group.xpath("@data-cat")) > 0 else None
            item['href'] = "https://music.163.com" + group.xpath("@href")[0] if len(group.xpath("@href")) > 0 else None
            type_url_list.append(item)
        return type_url_list

    def get_music_form(self, type_url):
        next_url = type_url["href"]
        type_name = type_url["name"]
        form_dict = {}
        form_list = []
        while next_url is not None:
            html_str = self.get_response(next_url)
            html = etree.HTML(html_str)
            groups = html.xpath("//ul[@class='m-cvrlst f-cb']/li")
            for group in groups:
                item = {}
                item['name'] = group.xpath("./p[@class='dec']/a/@title")[0] if len(
                    group.xpath("./p[@class='dec']/a/@title")) > 0 else None
                item['href'] = "https://music.163.com" + group.xpath("./p[@class='dec']/a/@href")[0] if len(
                    group.xpath("./p[@class='dec']/a/@href")) > 0 else None
                form_list.append(item)
            next_url = "https://music.163.com" + html.xpath("//div[@class='u-page']/a[@class='zbtn znxt']/@href")[
                0] if len(
                html.xpath("//div[@class='u-page']/a[@class='zbtn znxt']/@href")) > 0 else None
        form_dict[type_name] = form_list
        return form_dict

    def save_content(self):
        pass

    def run(self):
        html_str = self.get_response(self.type_url)
        type_url_list = self.collect_tpye_info(html_str)
        for type_url in type_url_list:
            form_dict = self.get_music_form(type_url)


if __name__ == '__main__':
    spider = WangYiYun()
    spider.run()