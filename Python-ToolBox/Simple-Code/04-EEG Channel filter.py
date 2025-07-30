import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 设置字体
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# FFT 频率域滤波函数
def fft_filter(data, fs, filter_type, cutoff):
    try:
        n_samples = data.shape[0]
        freqs = np.fft.rfftfreq(n_samples, 1 / fs)
        fft_data = np.fft.rfft(data, axis=0)

        if filter_type == 'highpass':
            mask = freqs > cutoff
        elif filter_type == 'lowpass':
            mask = freqs < cutoff
        elif filter_type == 'bandpass':
            mask = (freqs > cutoff[0]) & (freqs < cutoff[1])
        elif filter_type == 'notch':
            mask = ~((freqs > cutoff[0]) & (freqs < cutoff[1]))
        else:
            raise ValueError("Unsupported filter type!")
        fft_data[~mask] = 0
        filtered_data = np.fft.irfft(fft_data, n=n_samples, axis=0)
        return filtered_data
    except Exception as e:
        print(f"滤波过程中出现错误: {e}")

# 绘图函数
def plot_filter_comparison(time, original_signal, filtered_signal, title, ylabel, color, channel):
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    axs[0].plot(time, original_signal, label="原始信号", color="black")
    axs[0].set_title(f"通道 {channel + 1} - 原始信号")
    axs[0].set_ylabel("幅值")
    axs[0].legend()
    axs[1].plot(time, filtered_signal, label=title, color=color)
    axs[1].set_title(f"通道 {channel + 1} - {title}")
    axs[1].set_xlabel("时间 (秒)")
    axs[1].set_ylabel(ylabel)
    axs[1].legend()
    plt.tight_layout()
    plt.show()
def main(csv_filename):
    # 加载数据(这里输出的数据是只有时间戳和EEG的数据)
    eeg_data = np.genfromtxt(csv_filename, delimiter=',',skip_header=1)
    eeg_data = eeg_data[:, 1:]
    fs = 256
    # 滤波参数
    high_cutoff = 2
    low_cutoff = 40
    band_cutoff = [2, 40]
    notch_cutoff = [49, 51]
    # 滤波操作
    eeg_highpass = fft_filter(eeg_data, fs, 'highpass', high_cutoff) + np.mean(eeg_data, axis=0)
    eeg_lowpass = fft_filter(eeg_data, fs, 'lowpass', low_cutoff)
    eeg_bandpass = fft_filter(eeg_data, fs, 'bandpass', band_cutoff) + np.mean(eeg_data, axis=0)
    eeg_notch = fft_filter(eeg_data, fs, 'notch', notch_cutoff)
    # 绘图
    channels = eeg_data.shape[1]
    time = np.arange(eeg_data.shape[0]) / fs
    for ch in range(channels):
        plot_filter_comparison(time, eeg_data[:, ch], eeg_highpass[:, ch], "高通滤波 (恢复基线)", "幅值", "blue", ch)
        plot_filter_comparison(time, eeg_data[:, ch], eeg_lowpass[:, ch], "低通滤波", "幅值", "green", ch)
        plot_filter_comparison(time, eeg_data[:, ch], eeg_bandpass[:, ch], "带通滤波 (恢复基线)", "幅值", "red", ch)
        plot_filter_comparison(time, eeg_data[:, ch], eeg_notch[:, ch], "陷波滤波", "幅值", "purple", ch)

if __name__ == '__main__':
    #这里导入的数据格式是经过预处理的，只有时间戳和4通道的EEG数据
    main(csv_filename='EEG_signal.csv')
