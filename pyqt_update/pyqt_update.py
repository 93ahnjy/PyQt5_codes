import sys
import os
import glob

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem, QListWidget, QLabel, QMainWindow, QHBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class Display_images(QThread):

    finished = pyqtSignal(str)

    def __init__(self, root_dir, filelist, delay):
        super().__init__()

        os.chdir(root_dir)
        self.filelist = filelist
        self.idx = 0
        self.delay = delay


    def run(self):
        while self.idx < len(self.filelist):
            new_filename = self.filelist[self.idx]
            self.idx += 1
            self.finished.emit(new_filename)                 # update_img_list 함수라고 보면 됨.
            self.msleep(self.delay)



class MyApp(QWidget):

    def __init__(self, root_dir, img_type='png', delay=100):
        super().__init__()

        #os.chdir("/your/root/path")
        os.chdir(root_dir)

        self.root_dir = root_dir
        self.filelist = glob.glob("*." + img_type)
        self.idx = 0
        self.delay = delay

        self.displayer = Display_images(self.root_dir, self.filelist, self.delay)
        self.displayer.finished.connect(self.update_img_list)          # QThread 함수가 끝날 시, 발생 이벤트를 self.update_img_list 로.


        self.listWidget = QListWidget()
        self.listWidget.setFixedSize(200, 400)
        self.listWidget.itemClicked.connect(self.imshow_file)
        self.layout = QHBoxLayout()
        self.lbl_img = QLabel()

        self.btn1_clicked()


    def imshow_file(self):
        curr_filename = self.listWidget.currentItem().text()

        it1 = QListWidgetItem(curr_filename)
        pixmap = QPixmap(curr_filename)
        pixmap = pixmap.scaledToWidth(300)

        self.lbl_img.setPixmap(pixmap)
        self.lbl_img.setAlignment(Qt.AlignCenter)

        self.listWidget.addItem(it1)
        self.layout.addWidget(self.lbl_img)


    def update_img_list(self, filename):

        it1 = QListWidgetItem(filename)
        pixmap = QPixmap(filename)
        pixmap = pixmap.scaledToWidth(300)

        self.lbl_img.setPixmap(pixmap)
        self.lbl_img.setAlignment(Qt.AlignCenter)

        self.listWidget.addItem(it1)
        self.listWidget.insertItem(self.idx, filename)

        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.lbl_img)

        self.setLayout(self.layout)

        self.idx += 1
        self.resize(500, 450)
        if self.idx == len(self.filelist) - 1:
            QMessageBox.about(self, "Message Box", "All ImageName Ready ~!")

        self.show()


    # 이미지 로드 버튼 클릭 이벤트 처리 --------------------
    def btn1_clicked(self):
        self.displayer.start()





if __name__ == '__main__':

   root_dir = "﻿/your/root/path"
   img_type = 'png'
   delay = 100  # ms

   app = QApplication(sys.argv)
   ex = MyApp(root_dir, img_type, delay)
   sys.exit(app.exec_())



