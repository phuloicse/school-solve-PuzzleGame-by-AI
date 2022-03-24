import os
import string
from PIL import Image
from PIL import ImageFont, ImageDraw, ImageOps

def draw_text( text: str,box_size: int,font_size=100):
    width,height = box_size,box_size
    num_folder_path = os.path.join(os.curdir,"images","number",f'{text}')
    os.makedirs(f'{num_folder_path}', exist_ok=True)
    img = Image.new("L", (width, height), color=0)   # "L": (8-bit pixels, black and white)
    font = ImageFont.truetype("arial.ttf", font_size)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    draw.text(((width-w)/2, (height-h)/2), text=text, fill='white', font=font)
    
    img.save(f'{num_folder_path}/{text}.png')

def get_num_path(number: int=1): 
    return os.path.join(os.curdir,"images","number",f'{number}',f'{number}.png')

def get_tent_img_path(): 
    # return os.path.join(os.curdir,"images","tents_img","tent.png")
    return os.path.join(os.curdir,"images","tents_img","tent2.png")

def get_tree_img_path(): 
    # return os.path.join(os.curdir,"images","tents_img","tree.png")
    return os.path.join(os.curdir,"images","tents_img","tree3.png")

def generate_number_text_image(size: int = 160): 
    for i in range(0,10): 
        draw_text(str(i),size)

