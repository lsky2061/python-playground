import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import os

font = QFont("Times",32)

image_file_name = 'default_image.jpg'
#Below is the command that should give us the path to the directory that
#contains this file, regardless of where we run it from
working_dir = f'{os.getcwd()}/{os.path.dirname(__file__)}'
caption_file = f'{working_dir}/images/captions/{image_file_name}.txt'

print(f'Working Directory: {working_dir}')

main_width = 960
main_height = 540
main_x = 250
main_y = 150
main_margin = 50
buffer = 25

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Set Picture Reminder')
        self.setGeometry(main_x,main_y,main_width,main_height)
        self.UI()

    def UI(self):
        #Hour label
        text1 = QLabel('Hour:',self)
        text1.setFont(font)
        text1.adjustSize() #Makes the size of the lable fit the contents
        text1.move(main_margin,main_margin)
        #print('Text 1 x,y:',text1.x(),text1.y())

        #Hour inbput box
        self.spinBoxhr = QSpinBox(self)
        self.spinBoxhr.move(text1.x() + text1.width() + buffer,main_margin)
        self.spinBoxhr.setFont(font)
        self.spinBoxhr.setRange(0,12)
        self.spinBoxhr.setSingleStep(1)
        

        text2 = QLabel('Minute:',self)
        text2.setFont(font)
        text2.adjustSize() 
        text2.move(self.spinBoxhr.x() + self.spinBoxhr.width() + 2*buffer,main_margin)

        #print('Text 2 x,width:',text2.x(),text2.width())
        #Minute Input Box
        self.spinBoxmin = QSpinBox(self)
        self.spinBoxmin.move(text2.x() + text2.width() + buffer,main_margin)
        self.spinBoxmin.setFont(font)
        self.spinBoxmin.setRange(0,59)
        self.spinBoxmin.setSingleStep(1)

        #AM/PM selector
        self.combo = QComboBox(self)
        self.combo.setFont(font)
        self.combo.addItem("AM")
        self.combo.addItem("PM")
        self.combo.adjustSize()
        self.combo.move(self.spinBoxmin.x() + self.spinBoxmin.width() + buffer,main_margin)
               
        #Button to set reminder
        button_set = QPushButton("Set Reminder",self)
        button_set.setFont(font)
        button_set.adjustSize()
        button_set_dist_from_bottom = buffer + button_set.height()
        button_set.move(main_width - buffer - button_set.width(),main_height - button_set_dist_from_bottom)
        button_set.clicked.connect(self.getValue)
        #button_set.clicked.connect(self.messageBox)

        #Caption Input
        text_cap = QLabel('Caption:',self)
        text_cap.setFont(font)
        text_cap.adjustSize()
        text_cap.move(main_margin,text1.y() + text1.height() + buffer)
        
        self.editor = QTextEdit(self)
        editor_x = text_cap.x() + text_cap.width() + buffer
        editor_y = self.spinBoxmin.y() + self.spinBoxmin.height() + 2*buffer
        
        self.editor.move(editor_x,editor_y)
        self.editor.resize(main_width - buffer - editor_x,main_height - editor_y - button_set_dist_from_bottom - buffer)
        self.editor.setFont(font)

        

        self.show()

    def getValue(self):
        #Zero padding to prevent errors when hour or minute is single digits.
        hour = f'{self.spinBoxhr.value():02d}'
        minute = f'{self.spinBoxmin.value():02d}'
        ampm = self.combo.currentText()
        caption = self.editor.toPlainText()

        

        ##
        print(f'{hour}:{minute}')
        with open (caption_file, 'w') as f:
            f.write(caption)
        #The somewhat convoluted construction below is due to os using dash (rather than bash) in Ubuntu
        #https://stackoverflow.com/questions/16045139/redirector-in-ubuntu
        os.system(f'echo \'{working_dir}/PicDisplay.sh {image_file_name}\' | at {hour}:{minute} {ampm}')
        ##
        mbox = QMessageBox.information(self,"Reminder Set!",f"Reminder set for {hour}:{minute} {ampm}",QMessageBox.Ok)
        if mbox == QMessageBox.Ok:
           sys.exit()

def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
     main()
