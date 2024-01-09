from PIL import Image
from PIL.ExifTags import TAGS
import os
import shutil
import sys

#This function from https://www.blog.pythonlibrary.org/2010/03/28/getting-photo-metadata-exif-using-python/

def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def main():
    #path = '/home/luke/Uhura/GitHub/python-playground/PicTest'
    path = sys.argv[1]
    debug = False
    dir_list = os.listdir(path)
    for file in dir_list:
        #print(file)
        img_full_path = os.path.join(path,file)
        ls_path = os.path.join(path,'landscape/')
        portrait_path = os.path.join(path,'portrait/')
        other_path = os.path.join(path,'other/')
        orient = 1
        try:
            img = Image.open(img_full_path)
            format = img.format
            try:
                exif_info = get_exif(img_full_path)
                try:
                    orient= exif_info['Orientation']
                except:
                    orient= 1
                width = exif_info['ExifImageWidth']
                height = exif_info['ExifImageHeight']
                print(f'name: {img_full_path}; Width: {width}; Height: {height}; Orientation: {orient} ')
                #shutil.copyfile(src, dst)
                if(width > 0 and (height >= width or (height < width and orient >=5 and orient <=8))):
                    if debug:
                        print('Classified as PORTRAIT')
                    else:
                        shutil.copyfile(img_full_path,os.path.join(portrait_path,file))
                elif(width == 0):
                    shutil.copyfile(img_full_path,os.path.join(other_path,file))
                else:
                    if debug:
                        print('Classified as LANDSCAPE')
                    else:
                        shutil.copyfile(img_full_path,os.path.join(ls_path,file))
            except Exception as ex:
                print(f"File: {img_full_path}; Error: {ex}")
                if not debug:
                    shutil.copyfile(img_full_path,os.path.join(other_path,file))
        except Exception as e:
            print(f"File: {img_full_path}; Error: {e}")
            print("not an image, apparently")
        #exif_info = get_exif(path+file)
        #print(exif_info['Orientation'])


    #print(exif_info.keys())

def find_in_range(min,max,path):
    #path = sys.argv[1]
    dir_list = os.listdir(path)
    for file in dir_list:
        #print(file)
        img_full_path = os.path.join(path,file)
        try:
            img = Image.open(img_full_path)
            format = img.format
            exif_info = get_exif(img_full_path)
            try:
                orient= exif_info['Orientation']
            except:
                orient= 1
            width = exif_info['ExifImageWidth']
            height = exif_info['ExifImageHeight']
            if height > 0:
                AR = width/height
                if orient >=5 and orient <=8: AR = height/width #Orientation is 90 degrees from expected
                if AR > min and AR <= max:
                    print(f'name: {img_full_path}; Width: {width}; Height: {height}; Orientation: {orient} ')
        except Exception as e:
            pass
           # print(f"File: {img_full_path}; Error: {e}")
        

            

if __name__ == '__main__':
    main()
