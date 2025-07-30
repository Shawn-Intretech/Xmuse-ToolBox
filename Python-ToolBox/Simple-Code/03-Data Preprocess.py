# -*-coding: Utf-8 -*-
# @File : 03- Data Preprocess.py
# author: Gion Hua
# Time：2025/7/30
import pandas as pd
def analyze_eeg_data(csv_path):
    try:
        # 读取CSV文件
        data = pd.read_csv(csv_path)
        # 提取时间戳和4个通道的脑电数据
        selected_data = data[['timestamps', 'eeg_1', 'eeg_2', 'eeg_3', 'eeg_4']]
        # 数据清洗，去除包含缺失值的行和含有0的行。
        clean_data = selected_data.dropna()
        clean_data = clean_data[(clean_data[['eeg_1', 'eeg_2', 'eeg_3', 'eeg_4']] != 0).all(axis=1)]
        # 计算时间戳差值（相对于第一个时间戳）
        first_timestamp = clean_data['timestamps'].iloc[0]
        clean_data['time_diff'] = clean_data['timestamps'] - first_timestamp
        # 数据统计分析
        print("数据基本统计信息：")
        print(clean_data.describe())
        # 保存处理后的数据到新的CSV文件
        clean_data.to_csv('processed_eeg_data.csv', index=False)
        print("处理后的数据已保存为 processed_eeg_data.csv")
    except FileNotFoundError:
        print(f"找不到文件: {csv_path}")
    except Exception as e:
        print(f"发生错误: {e}")
if __name__ == '__main__':
    #放入你脑电文件的地址
    analyze_eeg_data("xmuselab_recording(45).csv")


