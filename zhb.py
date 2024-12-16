import requests
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, filedialog
import warnings

# 忽略matplotlib的libpng警告
warnings.filterwarnings("ignore", category=UserWarning, module='matplotlib')

class DataProcessor:
    def __init__(self, url):
        self.url = url
        self.data = None

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
            print(self.data.head())  # 打印数据框的前几行数据
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV file: {e}")

    def process_data(self):
        # 数据处理逻辑
        pass

    def visualize_data(self):
        # 数据可视化逻辑
        plt.plot(self.data['Time'], self.data['Data'], label='Value')
        plt.xlabel('Time')
        plt.ylabel('Data')
        plt.title('Time Series Line Chart')
        plt.ylim(0, 100)  # 设置Y轴范围为0到100
        plt.legend()
        plt.show()

def main():
    url = 'https://raw.githubusercontent.com/zhb0119/ZJUT--/main/processData.csv'  # 使用GitHub原始URL
    processor = DataProcessor(url)
    try:
        processor.fetch_data()
        processor.load_data()
        processor.process_data()
        processor.visualize_data()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
