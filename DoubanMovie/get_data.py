# 使用requests库爬取电影信息并保存到 MovieInfo_str.csv

import requests
from bs4 import BeautifulSoup
import pandas as pd


# 下载网页
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


# 爬取单个电影信息
def get_movie(url) -> list:
    """
    爬取单个电影的信息(除短评), 预处理成合适的字符串, 返回字符串列表
    :param url:
    :return:
    """
    # 下载网页并解析
    res = getHtml(url)
    bs = BeautifulSoup(res.text, 'html.parser')

    name = bs.find('span', property='v:itemreviewed').text

    year_str = bs.find('span', class_='year').text

    director = bs.find('a', rel="v:directedBy").text

    writer_span = bs.find('span', string='编剧')
    if writer_span:
        writers_set = writer_span.find_next('span', class_='attrs').find_all('a')
        writers_str = '/'.join([writer.get_text() for writer in writers_set])
    else:
        # 纪录片没有编剧，需要判断否则抛出 AttributeError
        print("There is no writer")
        writers_str = ''
    # 转换为字符串

    actor_set = bs.find_all('a', rel='v:starring')
    actors_str = '/'.join([actor.get_text() for actor in actor_set])
    # 转换为字符串

    type_set = bs.find_all('span', property='v:genre')
    types_str = '/'.join([movie_type.get_text() for movie_type in type_set])

    region_span = bs.find('span', string='制片国家/地区:')
    regions_str = region_span.next_sibling
    # regions_str = '/'.join([region.strip() for region in region_set.split('/')])

    language_span = bs.find('span', string='语言:')
    language_str = language_span.next_sibling

    date_set = bs.find_all('span', property='v:initialReleaseDate')
    dates_locations_str = '/'.join([date.get_text() for date in date_set])

    # 爬取首个片长信息
    length_str = bs.find('span', property='v:runtime').text

    rating_str = bs.find('strong', class_='ll rating_num', property='v:average').text
    # rating = float(rating_str)
    rating_people_str = bs.find('span', property='v:votes').text

    ratings_on_weight = bs.find('div', class_='ratings-on-weight').find_all('span', class_='rating_per')
    stars_str = '/'.join([star.get_text() for star in ratings_on_weight])

    return [name, year_str, director, writers_str, actors_str, types_str, regions_str, language_str,
            dates_locations_str, length_str, rating_str, rating_people_str, stars_str]


# 爬取所有电影信息并保存到 data.csv
def get_all_movie_urls() -> list:
    """
    从分类界面(每页25部)获取每部电影链接, 汇总返回 list
    :return: list
    """
    movie_urls = []  # 创建空列表存储所有电影链接
    top250url = 'https://movie.douban.com/top250'
    # 不断爬取单页信息直到最后一页
    while top250url:
        # 爬取单页所有电影信息
        # 下载网页并解析
        res = getHtml(top250url)
        bs = BeautifulSoup(res.text, 'html.parser')

        # 找到所有电影链接并添加到列表
        movies_set = bs.find_all('div', class_='pic')
        movie_urls.extend([movie.find('a')['href'] for movie in movies_set])

        # 如果有下一页就切换到下一页
        top250url = bs.find('link', rel='next')
        if top250url:
            top250url = 'https://movie.douban.com/top250' + top250url['href']

    return movie_urls


movieUrls = get_all_movie_urls()
# print(len(movieUrls))

test_urls = [
    'https://movie.douban.com/subject/26430107/',
    'https://movie.douban.com/subject/1292052/',
    'https://movie.douban.com/subject/1291546/',
    'https://movie.douban.com/subject/1292720/',
    'https://movie.douban.com/subject/1292722/',
    'https://movie.douban.com/subject/1291561/',
    'https://movie.douban.com/subject/1292063/'
]
# movieInfo = []
# for test_url in test_urls:
#     movieInfo.append(get_movie(test_url))
# print(movieInfo)

movieInfo = []
num = 0
for url in movieUrls:
    movieInfo.append(get_movie(url))
    num += 1
    print(f"Progress:{num}/250")

head = ['name', 'year', 'director', 'writers', 'actors', 'types', 'regions', 'languages', 'dates', 'length', 'rating',
        'rating_people', 'stars']
movieInfoDf = pd.DataFrame(movieInfo, columns=head, dtype=str)
movieInfoDf.to_csv('MovieInfo_str.csv', index=False, encoding='utf-8-sig')
print(movieInfoDf.head())
