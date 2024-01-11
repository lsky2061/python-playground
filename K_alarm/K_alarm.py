import os
import PyQt5


image_file_name = 'test_image.png'
#Below is the command that should give us the path to the directory that
#contains this file, regardless of where we run it from
working_dir = f'{os.getcwd()}/{os.path.dirname(__file__)}'
#print('If this worked correctly, this file is in',working_dir)

# Create input window or text
# Get input for time and text

hour = 19
minute = 44
caption = 'This caption is from a variable 2'
# Write text to a new file (overwrite existing file)
caption_file = f'{working_dir}/images/captions/{image_file_name}.txt'
with open (caption_file, 'w') as f:
	f.write(caption)

# Run 'at' with  .sh file
#os.system(f'at -f {working_dir}/PicDisplay.sh {hour}:{minute}')
os.system(f'{working_dir}/PicDisplay.sh {working_dir}')
# End
