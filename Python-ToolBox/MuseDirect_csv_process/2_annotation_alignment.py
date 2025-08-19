import numpy as np
import pandas as pd

eventtime = pd.read_csv(rf'D:\Projects\Toolbox\timestamprecorder\click_records_20250812_142803.csv').iloc[:,0]
eventlabel = pd.read_csv(rf'D:\Projects\Toolbox\timestamprecorder\click_records_20250812_142803.csv').iloc[:,2]

eegdatafile = pd.read_csv(rf'D:\Projects\Toolbox\splitmuseDirectCSV\1754979359838744\EEG.csv').iloc[:,0:5]
#时间戳转换到秒
eegtimestamp = eegdatafile.iloc[:,0]/1e6
#eeg转换到V
eegdata = eegdatafile.iloc[:,1:5]/1e6

def find_closest_time_point(timestamp, time_point):
    return np.abs(timestamp - time_point).argmin()

#不用世界时间/256，用sample数量/256在mne中对齐。
devicetime= [find_closest_time_point(eegtimestamp,eventtime[i])/256 for i in range(len(eventtime))]


import mne
ch_names = ['TP9','AF7','AF8','TP10']
ch_types = ['eeg','eeg','eeg','eeg']
info = mne.create_info(ch_names=ch_names,ch_types=ch_types,sfreq=256)
raw = mne.io.RawArray(eegdata.T,info)



# 创建注释对象（支持直接存储文字标签）
annotations = mne.Annotations(
    onset=devicetime,         # 事件开始时间（秒）
    duration=0,   # 持续时间（秒）
    description=eventlabel  # 直接使用文字标签
)

# 添加到Raw对象
raw.set_annotations(annotations)


raw.plot()