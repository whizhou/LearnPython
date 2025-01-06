# 爬取短评
import requests
from bs4 import BeautifulSoup


def getHtml(url) -> requests.Response:
    """
    :param url:
    :return requests.Response:
    """
    head = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.114 Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }
    while 1:
        try:
            res = requests.get(url, headers=head, timeout=30)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            return res
        except TimeoutError:
            print('getHtml: request Error')
            continue


def get_comments(url, filename: str) -> str:
    """
    爬取单部电影的全部短评并保存到文件
    :param filename:
    :param url:
    :return: str
    """
    comment_url = url + 'comments?status=P'  # 首先获取“全部短评”连接

    comments = ''

    # 爬取一定页数的短评
    page_num = 11
    while comment_url and page_num > 0:
        # 爬取单页所有短评
        # 下载网页并解析
        print(comment_url)
        res = getHtml(comment_url)
        bs = BeautifulSoup(res.text, 'html.parser')

        # 找到所有短评信息,添加到 comments
        short_comments = bs.find_all('span', class_='short')
        # 用换行符分隔
        comments = comments + '\n'.join([short_comment.get_text() for short_comment in short_comments])

        # 如果有下一页就切换到下一页
        comment_url = bs.find('a', class_='next')
        if comment_url:
            comment_url = url + 'comments' + comment_url['href']

        page_num -= 1

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(comments)

    return comments


movie_urls = [
    'https://movie.douban.com/subject/1292052/',
    'https://movie.douban.com/subject/1291546/'
]
num = 0
for test_url in movie_urls:
    num += 1
    get_comments(test_url, str(num) + '.txt')
