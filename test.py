'''
Created on 14/05/2019

@author: mgs
'''

import sys
import json
from PIL import Image,ImageFilter,ImageOps,ImageDraw


def main():
    
    if(len(sys.argv) != 2):
        print("Two arguments required: filename1.py filename2.json")
    else: 
        
        try:  
            with open(sys.argv[1], encoding='utf-8') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            print('Sorry, this file does not exist')
            sys.exit(1)
        except ValueError:
            print('Decoding JSON has failed. Please check if the JSON file is well formatted')
            sys.exit(1)
        
        filename_open = data["inputImage"]
        filename_save = data["outputImage"]
        
        try:
            image_origin = Image.open(filename_open)
        except IOError:
            print(filename_open, ' does not exist')
            sys.exit(1)
            
        try:
            for n in data['operations']:
                if(n['operationType'] == "Resize"):
                    width = n["width"]
                    height = n["height"]
                    pAR = n["preserveAspectRatio"]
                    if(pAR):
                        img_size = image_origin.size
                        ratio = img_size[0]/img_size[1]
                        width = round(width * ratio)
                        image_final = image_origin.resize((width,height))
                    else:
                        image_final = image_origin.resize((width,height))       
                elif(n['operationType'] == "Blur"):
                    rad = n["radius"]
                    image_final = image_final.filter(ImageFilter.GaussianBlur(radius= rad))
                elif(n['operationType'] == "Invert"):
                    image_final = ImageOps.invert(image_final)
                elif(n['operationType'] == "DrawBox"):
                    width_b = n["width"]
                    height_b = n["height"]
                    color = n["color"]
                    draw = ImageDraw.Draw(image_final)
                    draw.rectangle(((width - width_b, height_b), (width,0)), outline = color)               
                else:
                    print('The json file has operations that are not specified in the python file. Please implement them')
                    sys.exit(1)
        except Exception:
            print('Something went wrong with the operations')
            sys.exit(1)
        print('Operations performed successfully')        
        image_final.save(filename_save)
        print('Image saved')
            
if __name__ == "__main__": 
    main()
