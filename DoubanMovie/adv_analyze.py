# 进阶数据分析模块
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
import wordcloud as wc
import jieba

# 设置中文字体
font_path = r'E:\PycharmProjects\DoubanMovie\SimHei.ttf'  # 替换为实际字体文件的路径
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 导演-编剧 & 导演-演员的合作关系
def collaboration(data: pd.DataFrame):
    """
    绘制网络图,边的粗细由合作次数决定
    使用 networkx 和 matplotlib 库绘制网络图
    :param data:
    :return:
    """
    print("Collaboration Analyzing...")

    """
    统计导演-编剧合作关系
    """
    # 进行数据拆分
    director_writer_list = []
    for director, writers in zip(data['director'], data['writers']):
        director_writer_list.extend([[director, writer] for writer in writers])
    director_writer_df = pd.DataFrame(director_writer_list, columns=['director', 'writer'])

    # 统计导演-编剧合作次数
    director_writer_count = director_writer_df.groupby(['director', 'writer']).size().reset_index(name='count')
    director_writer_sorted = director_writer_count.sort_values(by='count', ascending=False)
    print(director_writer_sorted.head(20))

    # 创建有向图
    G = nx.DiGraph()

    # 添加节点和边
    for _, row in director_writer_sorted.head(20).iterrows():
        G.add_edge(row['director'], row['writer'], weight=row['count'])

    # 设置节点布局
    pos = nx.spring_layout(G, k=5, iterations=500)  # 调整参数以优化显示效果

    fig, ax = plt.subplots(figsize=(8, 8))

    # 绘制自环
    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v, d in edges if u == v],
                           width=[d['weight'] * 2 for u, v, d in edges if u == v], alpha=0.6,
                           connectionstyle='arc3,rad=0.5')

    # 绘制其他边
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v, d in edges if u != v],
                           width=[d['weight'] * 2 for u, v, d in edges if u != v], alpha=0.6)

    # 添加边权重标签
    edge_labels = {(u, v): d['weight'] for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # 绘制节点和标签
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='skyblue')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # 显示图表
    plt.title("导演-编剧合作关系网络图")
    plt.axis('off')
    plt.show()

    """
    统计导演-演员合作关系
    """
    # 进行数据拆分
    director_actor_list = []
    for director, actors in zip(data['director'], data['actors']):
        director_actor_list.extend([[director, actor] for actor in actors])
    director_actor_df = pd.DataFrame(director_actor_list, columns=['director', 'actor'])

    # 统计导演-编剧合作次数
    director_actor_count = director_actor_df.groupby(['director', 'actor']).size().reset_index(name='count')
    director_actor_sorted = director_actor_count.sort_values(by='count', ascending=False)
    print(director_actor_sorted.head(20))

    # 创建有向图
    G = nx.DiGraph()

    # 添加节点和边
    for _, row in director_actor_sorted.head(20).iterrows():
        G.add_edge(row['director'], row['actor'], weight=row['count'])

    # 设置节点布局
    pos = nx.spring_layout(G, k=5, iterations=500)  # 调整参数以优化显示效果

    fig, ax = plt.subplots(figsize=(8, 8))

    # 绘制自环
    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v, d in edges if u == v],
                           width=[d['weight'] * 2 for u, v, d in edges if u == v], alpha=0.6,
                           connectionstyle='arc3,rad=0.5')

    # 绘制其他边
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v, d in edges if u != v],
                           width=[d['weight'] * 2 for u, v, d in edges if u != v], alpha=0.6)

    # 添加边权重标签
    edge_labels = {(u, v): d['weight'] for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # 绘制节点和标签
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='skyblue')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # 显示图表
    plt.title("导演-演员合作关系网络图")
    plt.axis('off')
    plt.show()


# 词云图
def wordcloud(filename):
    with open(filename, encoding='utf-8') as f:
        text = f.read()

    # 加载中文停词表
    with open(r'E:\PycharmProjects\DoubanMovie\stop_words.txt', encoding='utf-8') as f:
        stop_words = f.read().splitlines()

    # 手动扩展停词表
    stop_words.extend(['电影', '演员', '真的', '确实', '更是', '这部', '这是', '一部'])

    # 分词并过滤
    word_list = jieba.cut(text)
    words = [word for word in word_list if len(word) > 1 and word not in stop_words]
    # print(words)

    # 配置词云对象参数
    cl = wc.WordCloud(width=1000, height=700,
                      font_path=font_path,
                      repeat=True)

    cl.generate('/'.join(words))

    # 输出词云文件
    cl.to_file(f'Movie{filename[0]}_ciyun.png')

    # 显示词云图
    plt.figure()
    plt.imshow(cl)
    plt.axis('off')
    plt.show()
