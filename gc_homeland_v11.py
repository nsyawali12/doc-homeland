# -*- coding: utf-8 -*-
import numpy as np
import pdf2image
from pdf2image import convert_from_path
import easyocr
import PIL
from PIL import ImageDraw, Image, ImageFont
import spacy

from IPython.display import display, Image

import os
import tempfile
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

import json

def plot_img(images, titles):
  fig, axs = plt.subplots(nrows = 1, ncols = len(images), figsize = (15, 15))
  for i, p in enumerate(images):
    axs[i].imshow(p, 'gray')
    axs[i].set_title(titles[i])
    #axs[i].axis('off')
  plt.show()

def draw_boxes(image, bounds, color='yellow', width=2):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
        try:
          draw.text(p0, bound[1], font=font, fill='red')
        except:
          print(bound[1])
    return image

def read_preprocessing(filename_pdf):
  # path to read pdf
  file_pdf = filename_pdf

  # this section finish if the user only need the image pdf not the pages
  # Store all the page
  pdf_pages = convert_from_path(file_pdf, 500)

  # the index counter store for each images
  image_counter = 1 

  # iterate all the pages stored in the pdf file
  for page in pdf_pages:
    filename = "page_" + str(image_counter) + ".jpg"
    page.save(filename, 'JPEG')
  
    #Increment the counter to update filename
    image_counter = image_counter + 1
  
  pdf_img = cv2.imread('page_1.jpg')
  test_img = PIL.Image.fromarray(pdf_img)

  ## Preprocessing Phase

  ### Input Threshold Preprocess  
  img = pdf_img
  img = cv2.medianBlur(img, 5)

  ### Input Threshold Preprocess  
  ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

  # Plotting the images
  result_img = [img, th1]
  # titles = ['Original Image', 'Thresh Binary']
  # plot_img(result_img, titles)

  return th1

"""### **OCR Phase**
tahap penggunaan OCR, hasil dari OCR dapat dilihat dengan box-box pada tulisan yang ada pada images

#### Inisiasi OCR
Mendfinisikan bahasa dan font yang akan digunakan, yaitu bahasa indonesia
"""

def ocr_json_phase(pre_img):
  # 'en' = English
  # 'id' = Indonesia
  reader = easyocr.Reader(['id'])
  font = ImageFont.load_default()

  bounds = reader.readtext(np.array(pre_img), min_size=0, slope_ths=0.2, 
                         ycenter_ths=0.7, height_ths=0.6, width_ths=0.8,
                         decoder='beamsearch', beamWidth=10)

  # # th1_copy = cv2.cvtColor(th1, cv2.COLOR_GR)
  # draw_boxes(th1.copy(), bounds, color='red')
  pre_copy = PIL.Image.fromarray(pre_img)

  # draw_boxes(test_img.copy(), bounds, color='red')
  draw_boxes(pre_copy, bounds, color='red')

  text=''
  result_text = []
 
  for i in range(len(bounds)):
    # text = text + bounds[i][1] + '\n'
    text = bounds[i][1]
    result_text.append(text)
    
  
  ### Result OCR 
  result_json = {
    "semua_text_ocr": result_text
  }

  return result_json