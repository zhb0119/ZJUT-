import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pykalman import KalmanFilter
import warnings
import random

# 忽略matplotlib的libpng警告
warnings.filterwarnings("ignore", category=UserWarning, module='matplotlib')

class DataProcessor:
    def __init__(self, url):
        self.url = url
        self.data = None
        self.filtered_data = None

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            with open('data.csv', 'w', encoding='utf-8') as file:
                file.write(response.text)
        else:
            raise Exception("Failed to fetch data")

    def load_data(self):
        try:
            self.data = pd.read_csv('data.csv', on_bad_lines='skip')
            print("Data columns:", self.data.columns)  # 打印数据框的列名
            print(self.data)  # 打印数据框的前几行数据
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV file: {e}")

    def generate_new_data(self):
        # 生成新数据
        last_time = self.data['Time'].iloc[-1]
        new_data = []
        for i in range(50):
            new_time = last_time + (i + 1) * 10
            new_value = 50 + random.uniform(-20, 20)
            new_data.append([new_time, new_value])
        new_df = pd.DataFrame(new_data, columns=['Time', 'Data'])
        self.data = pd.concat([self.data, new_df], ignore_index=True)
        self.data.to_csv('data.csv', index=False)  # 将新数据写入CSV文件

    def process_data(self):
        # 卡尔曼滤波算法
        kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
        self.filtered_data = kf.em(self.data['Data'].values).smooth(self.data['Data'].values)[0]

    def visualize_data(self):
        # 数据可视化逻辑
        plt.plot(self.data['Time'], self.data['Data'], label='Original Data')
        plt.plot(self.data['Time'], self.filtered_data, label='Filtered Data', linestyle='--')
        plt.xlabel('Time')
        plt.ylabel('Data')
        plt.title('Time Series Line Chart with Kalman Filter')
        plt.ylim(0, 100)  # 设置Y轴范围为0到100
        plt.legend()
        plt.show()

def main():
    url = 'https://raw.githubusercontent.com/zhb0119/ZJUT--/main/processData.csv'  # 使用GitHub原始URL
    processor = DataProcessor(url)
    try:
        processor.fetch_data()
        processor.load_data()  # 先加载数据
        processor.generate_new_data()  # 然后生成并写入新数据
        processor.load_data()  # 再次加载数据以包含新生成的数据
        processor.process_data()
        processor.visualize_data()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
