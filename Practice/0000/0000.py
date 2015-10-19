#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Image, ImageDraw, ImageFont, ImageFilter

image=Image.open('.\kobe.jpg')
# 创建Font对象:
font = ImageFont.truetype('Arial.ttf', 200)
# 创建Draw对象:
draw = ImageDraw.Draw(image)
# 输出文字:    
draw.text((1000 , 100), "24", font=font, fill='red')   

image.save('0000.jpg', 'jpeg');
