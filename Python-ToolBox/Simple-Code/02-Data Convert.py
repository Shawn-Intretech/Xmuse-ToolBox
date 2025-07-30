import mne
import pandas as pd
from datetime import datetime, timedelta
"该导入的EDF文件是Xmuse Lab导出的EDF数据格式"
# 读取EDF文件
edf_file = 'xmuselab_recording(45).edf'
raw = mne.io.read_raw_edf(edf_file, preload=True)
# 获取EEG数据和通道名称
data = raw.get_data()  # 数据是一个二维数组，形状为 (通道数, 时间点数)
channel_names = raw.info['ch_names']
# 获取采样率和开始时间
sfreq = raw.info['sfreq']  # 采样率（Hz）
start_time = raw.info['meas_date']  # 开始时间
# 如果开始时间包含时区信息，转换为UTC时间
if start_time.tzinfo is not None:
    start_time = start_time.replace(tzinfo=None) - start_time.utcoffset()
# 生成时间戳序列（相对于开始时间的秒数）
n_samples = data.shape[1]  # 总样本数
time_seconds = [i / sfreq for i in range(n_samples)]  # 每个样本的时间点（秒）
# 生成ISO格式的时间戳字符串
time_iso = [(start_time + timedelta(seconds=t)).isoformat() for t in time_seconds]
# 将EEG数据乘以1,000,000 (从伏特转换为微伏)
scaled_data = data * 1000000  # 所有通道同时缩放
# 将数据转换为DataFrame
df = pd.DataFrame(scaled_data.T, columns=channel_names)  # 转置数据，使得每一列代表一个通道
# 添加时间戳列
df['timestamp_seconds'] = time_seconds  # 相对于开始时间的秒数
df['timestamp_iso'] = time_iso          # ISO格式的完整时间戳
# 保存为CSV文件
csv_file = '1100.csv'
df.to_csv(csv_file, index=False)
print(f"EDF文件已成功转换为CSV格式并保存为 {csv_file}")