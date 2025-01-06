# 将 solve_data.py 合并，进行数据处理，数据分析和可视化

import pandas as pd
import solve_data
import fund_analyze
import corr_analyze
import adv_analyze


# 基本信息分析
def fund_analysis(data: pd.DataFrame) -> None:
    """
    :param data:
    :return: None
    """
    print("Fundamental Analyzing...")

    # (1) 首先查看数值型列的基本统计信息
    print(data.describe())

    # (2) 制片地区分布
    fund_analyze.region_analyze(data)

    # (3) 类型分布
    fund_analyze.type_analyze(data)

    # (4) 影片数量前10的导演 & 影片平均评分前20的导演
    fund_analyze.director_analyze(data)

    # (5) 影片数量前10的演员 & 影片平均评分前20的演员
    fund_analyze.actor_analyze(data)


# 关联性分析
def corr_analysis(data: pd.DataFrame) -> None:
    """
    :param data:
    :return:
    """
    print("Correlation Analyzing...")

    # (1) 上映年份-影片数量
    corr_analyze.year_movies(data)

    # (2) 类型-评分-评分人数 综合分析
    corr_analyze.types_rating_people(data)


# 进阶分析
def adv_analysis(data: pd.DataFrame) -> None:
    """
    :param data:
    :return:
    """
    print("Advance Analyzing...")

    # (1) 导演-编剧 & 导演-演员的合作关系
    # adv_analyze.collaboration(data)

    # (2) 词云图分析
    adv_analyze.wordcloud('1.txt')
    adv_analyze.wordcloud('2.txt')


# data = pd.read_csv('MovieInfo_str.csv', dtype=str)
data = solve_data.data_washing()
# 查看数据集信息
print("Data Info:")
print(data.info(verbose=False))
pd.set_option('display.max_columns', None)  # 设置显示全部列
print(data.head())

fund_analysis(data)

corr_analysis(data)

adv_analysis(data)
