# 基本数据分析模块
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体
font_path = 'SimHei.ttf'  # 替换为实际字体文件的路径
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 制片地区分布
def region_analyze(data: pd.DataFrame) -> None:
    """
    直接输出各地区数量;饼状图对比各地区占比;柱状图输出前十
    :param data:
    :return: None
    """
    print("Region Analyzing...")

    # 预览 data['regions'] 数据格式
    print(data['regions'].head())

    # 进行数据拆分和分组
    regions_list = []
    for regions in data['regions']:
        regions_list.extend(regions)
    regions_df = pd.DataFrame(regions_list, columns=['region'])
    # 按 region 列分组
    region_group = regions_df.groupby('region')
    # print(type(regions_df))

    # 按各地区影片数降序排序
    region_count = region_group.size().sort_values(ascending=False)

    # 查看各地区电影数量
    print(region_count)
    print(region_count.sum())

    # 创建区域绘制饼图和Pareto图
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))

    """
    绘制比例饼图:
    1.计算每个地区的比例
    2.将占比小于一定阈值的地区合并为“其它”
    3.按比例顺序排序数据
    4.绘制饼图
    """
    # 计算每个类别比例
    total = region_count.sum()
    region_percent = (region_count / total) * 100

    # 将占比小于阈值的数据合并为“其它”
    threshold = 2.5  # 设定阈值为 5%
    region_percent_filtered = region_percent[region_percent >= threshold]
    other_percent = region_percent[region_percent < threshold].sum()
    region_percent_filtered['其它地区'] = other_percent

    # 按比例排序
    region_percent_filtered = region_percent_filtered.sort_values(ascending=False)

    # 绘制饼图
    # plt.figure()
    # region_percent_filtered.plot.pie(autopct='%1.1f%%', label='', startangle=90, counterclock=False)
    # plt.title('制片地区比例分布图')
    # plt.show()
    axes[0].pie(region_percent_filtered, autopct='%1.1f%%', startangle=90, counterclock=False,
                labels=region_percent_filtered.index)
    axes[0].axis('off')
    axes[0].set_title('制片地区比例分布图', fontproperties=font_prop)

    """
    绘制 Pareto Chart
    """
    # 获取影片数量前十的地区
    top_regions = region_count.head(10)

    # 计算累计百分比
    region_percent_sorted = region_percent.sort_values(ascending=False)
    cumulative_percent = region_percent_sorted.cumsum().head(10)

    # 绘制帕累托图
    # fig, ax1 = plt.subplots()

    # 条形图
    bars = axes[1].bar(top_regions.index, top_regions, color='C0')
    axes[1].set_ylabel('影片数量', color='C0', fontproperties=font_prop)
    axes[1].tick_params(axis='y', labelcolor='C0')

    # 显示累计百分比的次坐标轴
    ax2 = axes[1].twinx()
    ax2.plot(top_regions.index, cumulative_percent, color='C1', marker='D', ms=7, linestyle='--')
    ax2.set_ylabel('累计百分比', color='C1', fontproperties=font_prop)
    ax2.tick_params(axis='y', labelcolor='C1')

    # 设置次坐标轴的范围
    ax2.set_ylim(0, 100)

    # 显示网格线
    axes[1].grid(axis='y')

    # 显示图表
    axes[1].set_title('影片数量前十的地区的帕累托图', fontproperties=font_prop)
    plt.show()


# 类型分布
def type_analyze(data: pd.DataFrame) -> None:
    """
    柱状统计图；比例饼图；
    :param data:
    :return: None
    """
    print("Type Analyzing...")

    # 预览 data['types'] 数据格式
    print(data['types'].head())

    # 进行数据拆分和分组
    types_list = []
    for types in data['types']:
        types_list.extend(types)
    types_group = pd.DataFrame(types_list, columns=['type']).groupby('type')

    # 按影片数降序排序
    type_count = types_group.size().sort_values(ascending=False)
    # 查看各类型影片数
    print(type_count)

    # 创建区域绘制饼图和Pareto图
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))

    """
    绘制比例饼图
    """
    # 计算每个类别比例
    total = type_count.sum()
    type_percent = (type_count / total) * 100

    # 将占比小于阈值的数据合并为“其它”
    threshold = 2.5  # 设定阈值为 5%
    type_percent_filtered = type_percent[type_percent >= threshold]
    other_percent = type_percent[type_percent < threshold].sum()
    type_percent_filtered['其它类型'] = other_percent

    # 按比例排序
    type_percent_filtered = type_percent_filtered.sort_values(ascending=False)

    # 绘制饼图
    # plt.figure()
    # type_percent_filtered.plot.pie(autopct='%1.1f%%', label='', startangle=90, counterclock=False)
    # plt.title('电影类型比例分布图')
    # plt.show()

    axes[0].pie(type_percent_filtered, autopct='%1.1f%%', startangle=90, counterclock=False,
                labels=type_percent_filtered.index)
    axes[0].axis('off')
    axes[0].set_title('电影类型比例分布图', fontproperties=font_prop)

    """
    绘制 Pareto Chart
    """
    # 获取前10影片类型,计算累计百分比
    top_types = type_count.sort_values(ascending=False).head(10)
    cumulative_percent = type_percent.cumsum().head(10)

    # 条形图
    bars = axes[1].bar(top_types.index, top_types, color='C0')
    axes[1].set_ylabel('影片数量', color='C0', fontproperties=font_prop)
    axes[1].tick_params(axis='y', labelcolor='C0')

    # 显示累计百分比的次坐标轴
    ax2 = axes[1].twinx()
    ax2.plot(top_types.index, cumulative_percent, color='C1', marker='D', ms=7, linestyle='--')
    ax2.set_ylabel('累计百分比', color='C1', fontproperties=font_prop)
    ax2.tick_params(axis='y', labelcolor='C1')

    # 设置次坐标轴的范围
    ax2.set_ylim(0, 100)

    # 显示网格线
    axes[1].grid(axis='y')

    # 显示图表
    axes[1].set_title('影片数量前十的类型的帕累托图', fontproperties=font_prop)
    plt.show()


# 影片数量前10的导演 & 影片平均评分前20的导演
def director_analyze(data: pd.DataFrame) -> None:
    """
    统计影片数量前10的导演 & 影片平均评分前20的导演
    :param data:
    :return: None
    """
    print("Director Analyzing...")

    # 预览数据格式
    print(data['director'].head())

    """
    统计影片数量前10的导演及其影片和影片评分
    """
    # 统计导演影片数量并降序排列
    director_group = data.groupby('director')  # 按照导演分组
    director_count = director_group.size().sort_values(ascending=False)

    # 计算每个导演的平均评分
    director_avg_rating = director_group['rating'].agg(['mean', 'count'])
    print(director_avg_rating.sort_values(by='count', ascending=False).head(18))

    # 获取影片数量前十的导演
    top_directors = director_count.head(18).index

    # 筛选出对应导演的影片
    top_directors_movies = data[data['director'].isin(top_directors)]

    # 按导演分组并获取每个导演的影片列表
    movies_list = top_directors_movies.groupby('director')['name'].apply(list).reindex(top_directors)

    # 设置列宽度以完整显示列表
    pd.set_option('display.max_colwidth', None)
    print(movies_list)

    """
    统计影片平均评分前20的导演及其影片数
    """
    # 对评分排序,获取前20名导演
    top_directors_avg_rating = director_avg_rating.sort_values(by='mean', ascending=False)

    print(top_directors_avg_rating.head(20))


# 影片数量前10的演员 & 影片平均评分前20的演员
def actor_analyze(data: pd.DataFrame) -> None:
    """
    统计影片数量前10的演员 & 影片平均评分前20的演员
    :param data:
    :return: None
    """
    print("Actor Analyzing...")

    # 预览数据格式
    print(data['actors'])

    # 进行数据拆分和分组,保留 name, actors, rating 数据
    actor_list = []
    # for actors, rating in zip(data['actors'], data['rating']):
    #     actor_list.extend([[actor, rating] for actor in actors])
    for index, row in data.iterrows():
        actor_list.extend([[row['name'], actor, row['rating']] for actor in row['actors']])
    actor_group = pd.DataFrame(actor_list, columns=['name', 'actor', 'rating']).groupby('actor')

    """
    统计影片数量前10的演员并输出其影片平均评分
    """
    # 计算每个演员参演电影的平均评分
    actor_avg_rating = actor_group['rating'].agg(['mean', 'count'])
    print(actor_avg_rating.sort_values(by='count', ascending=False).head(12))

    """
    统计影片平均评分前20的演员
    """
    # 对评分排序,获取前20名演员
    actor_avg_rating_sorted = actor_avg_rating.sort_values(by='mean', ascending=False)

    print(actor_avg_rating_sorted.head(20))
