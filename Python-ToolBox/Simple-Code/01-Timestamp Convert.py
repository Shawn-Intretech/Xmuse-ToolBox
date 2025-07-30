# 这是一个示例 Python 脚本。
import datetime
import csv
# 输入和输出文件路径
input_csv = "EEG_signal.csv"  # 替换为您的原始 CSV 文件路径
output_csv = "EEG_signal455.csv" # 输出的 CSV 文件路径
# 打开输入文件并转换时间戳
with open(input_csv, mode="r", encoding="utf-8") as infile, open(output_csv, mode="w", encoding="utf-8", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    # 读取标题行
    header = next(reader)
    # 添加新列名到标题
    header.append("BeiJing-Time")
    writer.writerow(header)
    # 逐行读取并转换时间戳
    for row in reader:
        try:
            # 读取时间戳并转换为浮点数
            timestamp = float(row[0])  # 假设时间戳在第一列
            "如果是通过PYLSL保存的数据格式，把下面注释的代码取消注释"
            #timestamp = timestamp / 1000000.0    # 将微秒转换为秒（除以1,000,000）
            "转换为北京时间（针对Xmuse Lab保存的数据格式）"
            beijing_time = datetime.datetime.utcfromtimestamp(timestamp) + datetime.timedelta(hours=8)
            # 格式化为字符串，例如 "YYYY-MM-DD HH:MM:SS.ffffff" (保留到微秒)
            beijing_time_str = beijing_time.strftime("%Y-%m-%d %H:%M:%S.%f")  # 精确到微秒
            # 如果只需要到毫秒，手动截取字符串
            beijing_time_str = beijing_time_str[:-3]  # 去掉最后三位，保留到毫秒
            # 添加到行
            row.append(f'"{beijing_time_str}"')  # 确保时间戳是作为文本处理
        except ValueError:
            # 如果转换失败，直接将"无效时间戳"写入
            row.append("无效时间戳")
        writer.writerow(row)
print(f"转换完成！结果已保存到 {output_csv}")




