import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from datetime import datetime
import csv
import time

class ClickRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.clicks = []
        
    def initUI(self):
        # 设置窗口
        self.setWindowTitle('任务态实验点击记录器')
        self.setGeometry(300, 300, 400, 300)
        
        # 创建布局
        layout = QVBoxLayout()
        
        # 信息标签
        self.info_label = QLabel('请点击下面的按钮进行实验操作：')
        layout.addWidget(self.info_label)
        
        # 创建多个按钮
        buttons = ['EC','EO','Blink', 'Jaw', 'Frown','sacc','nod','talk','updown','empty']
        self.buttons = {}
        
        for btn_text in buttons:
            button = QPushButton(btn_text, self)
            button.clicked.connect(self.recordClick)
            layout.addWidget(button)
            self.buttons[btn_text] = button
        
        # 保存按钮
        save_btn = QPushButton('保存记录', self)
        save_btn.clicked.connect(self.saveToCSV)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
    
    def recordClick(self):
        # 获取被点击的按钮文本
        clicked_button = self.sender()
        button_text = clicked_button.text()
        
        # 获取当前时间戳
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        unixstamp = time.time()

        # 记录点击事件
        self.clicks.append((unixstamp, timestamp, button_text))
        
        # 更新界面显示
        self.info_label.setText(f'已记录: {timestamp} - {button_text}')
        print(f'记录: {timestamp} - {button_text}')
    
    def saveToCSV(self):
        if not self.clicks:
            self.info_label.setText('没有记录可保存')
            return
            
        filename = f'click_records_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['unix', 'timestamp', 'Event'])
            writer.writerows(self.clicks)
        
        self.info_label.setText(f'已保存 {len(self.clicks)} 条记录到 {filename}')
        self.clicks = []  # 清空记录

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClickRecorder()
    ex.show()
    sys.exit(app.exec_())