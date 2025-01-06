# 作为 solve_data 模块
# 转换数据功能
import pandas as pd
from datetime import datetime


def parse_date(date_str) -> datetime:
    """
    尝试使用不同格式解析日期
    :param date_str: 
    :return: datetime
    """
    # 添加到 dates 嵌套列表
    date_formats = ['%Y-%m-%d', '%Y', '%Y-%m', '%m', '%m-%d']
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue


# 处理日期格式
def parse_date_location(date_str: str) -> [datetime, str]:
    """
    解析上映日期的 日期-地点 格式
    :param date_str: str
    :return: [datetime, str]
    """
    dates = []
    for item in date_str.split('/'):
        # 找到左右括号位置
        left_paren_index = item.find('(')
        right_paren_index = item.find(')')

        # 提取日期字符串并装换为 datetime 对象
        date = parse_date(item[:left_paren_index])

        # 提取地点字符串
        location = item[left_paren_index + 1:right_paren_index]

        dates.append([date, location])

    return dates


# 首先处理缺失值，然后对有需要的数据进行转换
def data_washing() -> pd.DataFrame:
    """
    从 MovieInfo_str.csv 读入 data, 进行缺失值处理和数据类型转换后返回
    :return: pd.DataFrame
    """
    data = pd.read_csv('MovieInfo_str.csv', dtype=str)

    # 预览数据
    pd.set_option('display.max_columns', None)  # 设置显示全部列
    print(data.head())

    # 统计每列缺失值个数
    columns_null_num = data.isnull().sum()
    print(columns_null_num)

    if data['name'].hasnans:
        # 输出 NaN 值的 index
        print('name lose:', data['name'][data['name'].isna()].index)

    if data['year'].hasnans:
        print('year lose:', data['year'][data['year'].isna()].index)
        data['year'] = data['year'].map(lambda x: '' if pd.isna(x) else x)
    data['year'] = data['year'].map(lambda x: int(x[1:-1]))
    # print(data['year'])

    if data['director'].hasnans:
        print('director lose:', data['director'][data['director'].isna()].index)

    if data['writers'].hasnans:
        # 输出 NaN 值的 index
        print('writer lose:', data['writers'][data['writers'].isna()].index)
        data['writers'] = data['writers'].map(lambda x: '' if pd.isna(x) else x)
    data['writers'] = data['writers'].map(lambda x: [writer.strip() for writer in x.split('/')])
    # print(data['writers'])

    if data['actors'].hasnans:
        # 输出 NaN 值的 index
        print('writer lose:', data['actors'][data['actors'].isna()].index)
        data['actors'] = data['actors'].map(lambda x: '' if pd.isna(x) else x)
    data['actors'] = data['actors'].map(lambda x: [writer.strip() for writer in x.split('/')])

    if data['types'].hasnans:
        print('type lose:', data['types'][data['types'].isna()].index)
        data['types'] = data['types'].map(lambda x: '' if pd.isna(x) else x)
    data['types'] = data['types'].map(lambda x: [type_str.strip() for type_str in x.split('/')])
    # print(data['types'].head())

    if data['regions'].hasnans:
        print('region lose:', data['regions'][data['regions'].isna()].index)
        data['regions'] = data['regions'].map(lambda x: '' if pd.isna(x) else x)
    data['regions'] = data['regions'].map(lambda x: [region.strip() for region in x.split('/')])
    # print(data['regions'].head())

    if data['languages'].hasnans:
        print('language lose:', data['languages'][data['languages'].isna()].index)
        data['languages'] = data['languages'].map(lambda x: '' if pd.isna(x) else x)
    data['languages'] = data['languages'].map(lambda x: [language.strip() for language in x.split('/')])
    # print(data['languages'].head())

    if data['dates'].hasnans:
        print('date lose:', data['dates'][data['dates'].isna()].index)
        data['dates'] = data['dates'].map(lambda x: '' if pd.isna(x) else x)
    data['dates'] = data['dates'].map(parse_date_location)
    # print(data['dates'].head())

    if data['length'].hasnans:
        print('length lose:', data['length'][data['length'].isna()].index)
        data['length'] = data['lengths'].map(lambda x: '0' if pd.isna(x) else x)
    data['length'] = data['length'].map(lambda x: int(x[0:x.find('分钟')]))
    # print(data['length'].head())

    if data['rating'].hasnans:
        print('rating lose:', data['rating'][data['rating'].isna()].index)
        data['rating'] = data['rating'].map(lambda x: 0.0 if pd.isna(x) else x)
    data['rating'] = data['rating'].map(lambda x: float(x))
    # print(data['rating'].head())

    if data['rating_people'].hasnans:
        print('rating_people lose:', data['rating_people'][data['rating_people'].isna()].index)
        data['rating_people'] = data['rating_people'].map(lambda x: 0 if pd.isna(x) else x)
    data['rating_people'] = data['rating_people'].map(lambda x: int(x))
    # print(data['rating_people'].head())

    if data['stars'].hasnans:
        print('stars lose:', data['stars'][data['stars'].isna()].index)
        data['stars'] = data['stars'].map(lambda x: '' if pd.isna(x) else x)
    data['stars'] = data['stars'].map(lambda x: [float(star[:-1]) for star in x.split('/')])
    # print(data['stars'].head())

    return data
