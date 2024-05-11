import pandas as pd
import numpy as np

# 定义样本数据和标签
samples = np.array([
    [5.1, 3.5, 1.4, 0.2],  # setosa
    [7.0, 3.2, 4.7, 1.4],  # versicolor
    [6.3, 3.3, 6.0, 2.5]  # virginica
])
labels = ["setosa", "versicolor", "virginica"]


def generate_similar_samples(base_samples, labels, num_samples=10):
    num_base_samples = base_samples.shape[0]
    new_samples = []

    # 为每个标签生成 num_samples/num_base_samples 的数据点
    num_samples_per_label = num_samples // num_base_samples

    for index in range(num_base_samples):
        for _ in range(num_samples_per_label):
            # 添加随机扰动
            perturbation = np.random.normal(0, 0.1, base_samples[index].shape)
            new_sample = base_samples[index] + perturbation
            new_samples.append(np.append(new_sample, labels[index]))

    # 将数据转换为 DataFrame
    new_samples_df = pd.DataFrame(new_samples,
                                  columns=["sepal_length", "sepal_width", "petal_length", "petal_width", "species"])

    return new_samples_df


# 生成数据
new_iris_data = generate_similar_samples(samples, labels, num_samples=10)

# 保存为 CSV
output_csv_path = 'simulated_iris_data0.csv'
new_iris_data.to_csv(output_csv_path, index=False)
