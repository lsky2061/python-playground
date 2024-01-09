import os
import PyQt5

image_file_name = 'test_image.png'
working_dir = '/home/luke/git/python-playground/K_alarm'

# Create input window or text
# Get input for time and text

hour = 19
minute = 44
caption = 'This caption is from a variable'
# Write text to a new file (overwrite existing file)
caption_file = f'{working_dir}/images/captions/{image_file_name}.txt'
with open (caption_file, 'w') as f:
	f.write(caption)

# Run 'at' with  .sh file
os.system(f'at -f {working_dir}/PicDisplay.sh {hour}:{minute}')
# End