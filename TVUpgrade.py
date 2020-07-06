import math

#input size and return distances
def res_size(screen_size,unit="cm"):
    size_convert = 1
    #Assume all units are in cm unless otherwise indicated
   # if(unit == "cm"):
   #     pass
   # elif(unit == "in"):
   #     size_convert = 2.54
   # else:
   #     print("unknown units")
    #    return -1
    
   # screen_size *= size_convert
    
    #calc vertical and horizontal screen dimensons
    #z = sqrt(x^2 + y^2), y/x = 16/9, solve for y
    screen_v = (9/(math.sqrt(337)))*screen_size
    screen_w = (16/(math.sqrt(337)))*screen_size
    
    #check
    print("Vertical =",screen_v)
    print("Width = ",screen_w)
   # print("16:9 = ",16.0/9.0)
    
    print("{0:.3f}".format(screen_w/screen_v))
    
    
    
    #At what distance will a 480p pixel be the same size as 20/20 vision? (pixel = 1 arc minute) We assume square pixels
    #res_v = 2160
    #Specify array of resolution names and sizes
    resolutions = [480, 720, 1080, 2160, 4320, 18000]
    vision_size = (1/60)*(math.pi/180) #1 arc minute (resolution of 20/20 vision) in radians
    
    for res_v in resolutions: 
        pixel_v = screen_v/res_v
        dist = pixel_v /(math.tan(vision_size))
        print('If you are closer than {0:.3f} {2}, you can see the pixels in {1:.0f}p resolution'
              .format(dist,res_v,unit) )
    
    #return dist;
    

def res_dist(view_dist,unit):
    #Calc what size of pixel is equal to resolution of 20/20
    vision_size = (1/60)*(math.pi/180) #1 arc minute (resolution of 20/20 vision) in radians
    pixel_v = view_dist*(math.tan(vision_size))
    print('Here')
    
    #calc overall size of TV from that pixel size
    resolutions = {'SD':480, 'HD (720p)':720, 'FHD':1080, 'UHD 4K':2160, 'UHD 8K':4320}
    
    #You need a TV of at least this size for upgrading to be worthwhile
    print('At this viewing distance, you need a TV of size at least...')
    for name, res in resolutions.items():
        screen_v = pixel_v*res
        screen_w = screen_v*(16/9)
        screen_size = math.sqrt(math.pow(screen_v,2) + math.pow(screen_w,2))
        print('... {0:.1f} {1} to justify upgrading from {2}'
              .format(screen_size,unit,name))

#res_dist(8*12,"in")
