import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import os

font = QFont("Times",32)

image_file_name = 'default_image.jpg'
#Below is the command that should give us the path to the directory that
#contains this file, regardless of where we run it from
#working_dir = f'{os.getcwd()}/{os.path.dirname(__file__)}'
working_dir = f'{os.getcwd()}'
caption_file = f'{working_dir}/images/captions/{image_file_name}.txt'

print(f'getcwd(): {os.getcwd()}')
print(f'dirname: {os.path.dirname(__file__)}')
print(f'File: {__file__}')
#print(f'Working Directory: {working_dir}')

