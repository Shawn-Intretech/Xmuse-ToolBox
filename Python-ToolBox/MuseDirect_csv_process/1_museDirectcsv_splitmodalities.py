import pandas as pd
import os
import time



def split_by_packettype(input_file):
    # Read the input CSV file
    df = pd.read_csv(input_file)
    outdir = str(df['Timestamp'][0])

    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # 处理每个PacketType分组
    for packet_type, group in df.groupby("PacketType"):
        # 创建处理副本
        group_data = group.copy()
        
        # 清理Data列：移除引号并按逗号分割
        group_data["Data"] = group_data["Data"].str.replace('"', '')
        split_data = group_data["Data"].str.split(",", expand=True)
        
        # 自动生成列名 (Data_1, Data_2, ...)
        split_data.columns = [f"Data_{i+1}" for i in range(split_data.shape[1])]
        
        # 组合结果：保留Timestamp和处理后的数据
        result = pd.concat([group_data["Timestamp"], split_data], axis=1)
        
        # 保存结果到CSV
        output_filename = f"{outdir}/{packet_type}.csv"
        result.to_csv(output_filename, index=False)
        print(f"✅ 已创建: {output_filename} ({len(result)}行数据)")


split_by_packettype(rf'D:\Projects\Data&Labels\TestData\2025-08-12-14-15-59.csv')


