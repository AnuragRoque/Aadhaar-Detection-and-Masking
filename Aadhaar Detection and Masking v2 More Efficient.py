from tkinter import *
from tkinter import filedialog
import cv2
import numpy as np
import numpy
import re
from PIL import Image
import pytesseract
from ISR.models import RRDN
import pdf2image
import img2pdf
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2 import PdfFileMerger
import tifftools
SR_Model = RRDN(weights='gans')
pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract'

def find_text(text):
  n=len(text)
  if(n<12):
    return 0
  for i in range(14,n):
    s=text[i-14:i]
    if(s[4]==" " and s[9]==" "):
      s=s.replace(" ","")
      n1=len(s)
      s1=s[n1-12:n1]
      if(i==125):
        pass
      if(s1.isnumeric() and len(s1)>=12):
        return 1
  return 0
#-------------------------------------------------------------------------------------------------------#
def addhar_check(file_name):
  img = Image.open(file_name)
  u=0
  for i in range(25):
    try:
        img.seek(i)
        u=u+1
        array=numpy.array(img)
        c=len(array.shape)
        if(c==2):
          if(array[0][0]==True or array[0][0]==False):
             array=array*255
             img10 = array.astype(numpy.uint8)
             array=numpy.array(img10)

        elif(c==3):
          if(array[0][0][0]==True or array[0][0][0]==False):
             array=array*255
             img10 = array.astype(numpy.uint8)
             array=numpy.array(img10)     
        text=pytesseract.image_to_string(array)
        v=find_text(text)
        if(v):
                break
        else:
                gaussianBlur = cv2.GaussianBlur(array,(5,5),cv2.BORDER_DEFAULT)
                text=pytesseract.image_to_string(gaussianBlur)
                v=find_text(text)
                if(v):
                    break
                else:
                    pass
    except EOFError:
        u=0
        break
  return u


#----------------------------------------------------------------------------------------------------#

"""Remove the unmasked aadhar page from a pdf file and add a new page of masked aadhar into the pdf file."""
def merger(original,masked,page_no,flag):
   pass

"""Split a pdf into multiple pages and merge them all to a single TIF file."""
def pdf2tiff(pdf_path):
# Store Pdf with convert_from_path function
  images = pdf2image.convert_from_path(pdf_path,300,poppler_path=r'C:\Program Files\poppler\Library\bin')
  
  li=[] 
  for i in range(len(images)):
        # Save pages as images in the pdf
      images[i].save(str(i)+".tif", 'TIFF')
      li.append(str(i)+'.tif')
  tifftools.tiff_merge(li,'final.tif')

multiplication_table = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0))

permutation_table = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8))

#---------------------------------------------------------------------------------------------------------#

def compute_checksum(number):
    
    """Calculate the Verhoeff checksum over the provided number. The checksum
    is returned as an int. Valid numbers should have a checksum of 0."""
    
    # transform number list
    number = tuple(int(n) for n in reversed(str(number)))
    #print(number)
    
    # calculate checksum
    checksum = 0
    
    for i, n in enumerate(number):
        checksum = multiplication_table[checksum][permutation_table[i % 8][n]]
    
    #print(checksum)
    return checksum

#---------------------------------------------------------------------------------------------------------#

# Search Possible UIDs with Bounding Boxes

def Regex_Search(bounding_boxes):
    possible_UIDs = []
    Result = ""

    for character in range(len(bounding_boxes)):
        if len(bounding_boxes[character]) != 0:
            Result += bounding_boxes[character][0]
        else:
            Result += '?'

    # Function to find overlapping matches
    def find_overlapping_matches(pattern, string):
        matches = []
        for match in re.finditer(pattern, string):
            matches.append(match.span())
            start = match.start() + 1
            while start < len(string):
                match = re.search(pattern, string[start:])
                if match:
                    matches.append((start + match.start(), start + match.end()))
                    start += match.start() + 1
                else:
                    break
        return matches

    matches = find_overlapping_matches(r'\d{12}', Result)

    for match in matches:
        UID = int(Result[match[0]:match[1]])
        if compute_checksum(UID) == 0 and UID % 10000 != 1947:
            possible_UIDs.append([UID, match[0]])

    possible_UIDs = np.array(possible_UIDs)
    return possible_UIDs
#---------------------------------------------------------------------------------------------------------#

def Mask_UIDs(image_path, possible_UIDs, bounding_boxes, rtype, SR=False, SR_Ratio=[1, 1]):
    img = cv2.imread(image_path)

    if rtype == 2:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif rtype == 3:
        img = cv2.rotate(img, cv2.ROTATE_180)
    elif rtype == 4:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    height = img.shape[0]

    if SR:
        height *= SR_Ratio[1]

    for UID in possible_UIDs:
        digit1 = bounding_boxes[UID[1]].split()
        digit8 = bounding_boxes[UID[1] + 7].split()

        h1 = min(height - int(digit1[4]), height - int(digit8[4]))
        h2 = max(height - int(digit1[2]), height - int(digit8[2]))

        if not SR:
            top_left_corner = (int(digit1[1]), h1)
            bottom_right_corner = (int(digit8[3]), h2)
            botton_left_corner = (int(digit1[1]), h2 - 3)
            thickness = h1 - h2
        else:
            top_left_corner = (int(int(digit1[1]) / SR_Ratio[0]), int(h1 / SR_Ratio[1]))
            bottom_right_corner = (int(int(digit8[3]) / SR_Ratio[0]), int(h2 / SR_Ratio[1]))
            botton_left_corner = (int(int(digit1[1]) / SR_Ratio[0]), int(h2 / SR_Ratio[1] - 3))
            thickness = int(h1 / SR_Ratio[1]) - int(h2 / SR_Ratio[1])

        # Debugging output to verify bounding box coordinates
        print(f"UID: {UID[0]}, Top Left: {top_left_corner}, Bottom Right: {bottom_right_corner}")

        img = cv2.rectangle(img, top_left_corner, bottom_right_corner, (0, 0, 0), -1)

    if rtype == 2:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif rtype == 3:
        img = cv2.rotate(img, cv2.ROTATE_180)
    elif rtype == 4:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    file_name = image_path.split('/')[-1].split('.')[0] + "_masked" + "." + image_path.split('.')[-1]
    cv2.imwrite(file_name, img)
    return file_name

#---------------------------------------------------------------------------------------------------------#

def Extract_and_Mask_UIDs(image_path, SR=False, sr_image_path=None, SR_Ratio=[1,1], regions=None):
    if not SR:
        img = cv2.imread(image_path)
    else:
        img = cv2.imread(sr_image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if regions is None:
        regions = [(0, 0, gray.shape[1], gray.shape[0])]  # Default to entire image if no regions provided

    settings = '-l eng --oem 3 --psm 11'

    masked_img = None
    possible_UIDs = []

    for region in regions:
        x, y, w, h = region
        cropped_gray = gray[y:y+h, x:x+w]

        rotations = [
            [cropped_gray, 1],
            [cv2.rotate(cropped_gray, cv2.ROTATE_90_COUNTERCLOCKWISE), 2],
            [cv2.rotate(cropped_gray, cv2.ROTATE_180), 3],
            [cv2.rotate(cropped_gray, cv2.ROTATE_90_CLOCKWISE), 4],
            [cv2.GaussianBlur(cropped_gray, (5, 5), 0), 1],
            [cv2.GaussianBlur(cv2.rotate(cropped_gray, cv2.ROTATE_90_COUNTERCLOCKWISE), (5, 5), 0), 2],
            [cv2.GaussianBlur(cv2.rotate(cropped_gray, cv2.ROTATE_180), (5, 5), 0), 3],
            [cv2.GaussianBlur(cv2.rotate(cropped_gray, cv2.ROTATE_90_CLOCKWISE), (5, 5), 0), 4]
        ]

        for rotation in rotations:
            rotated_img = rotation[0]
            rg_img=image_path+"rotated_grayscale.png"
            cv2.imwrite(rg_img, rotated_img)

            bounding_boxes = pytesseract.image_to_boxes(Image.open(rg_img), config=settings).split(" 0\n")

            region_UIDs = Regex_Search(bounding_boxes)

            if len(region_UIDs) > 0:
                possible_UIDs.extend(region_UIDs)

                if not SR:
                    masked_img = Mask_UIDs(image_path, region_UIDs, bounding_boxes, rotation[1])
                else:
                    masked_img = Mask_UIDs(image_path, region_UIDs, bounding_boxes, rotation[1], True, SR_Ratio)

                # No need to continue once UIDs are detected and masked
                break

    return masked_img, possible_UIDs

# Example usage:
# Define specific regions (x, y, width, height) to focus OCR on the back side only

#--------------------------------------------------------------------------------------------------------
def masking_file(input_path):
    k = 0
    masked_img = None
    possible_UIDs = None
    
    # Determine file type
    file_type = input_path.split('.')[-1].lower()

    if file_type == "pdf":    
        print("PDF file detected. Processing...")
        # Convert PDF to images and process each page as an image.
        images = pdf2image.convert_from_path(input_path, 300, poppler_path=r'C:\Program Files\poppler\Library\bin')
        for i, img in enumerate(images):
            img.save(f"page_{i}.png")
            masked_img, possible_UIDs = Extract_and_Mask_UIDs(f"page_{i}.png")
            if masked_img:
                break
    
    elif file_type == "tif":
        print("TIF file detected. Processing...")
        masked_img, possible_UIDs = Extract_and_Mask_UIDs(input_path)
    
    else:
        print(f"Image file ({file_type}) detected. Processing...")
        masked_img, possible_UIDs = Extract_and_Mask_UIDs(input_path)

    if masked_img is None:
        s = "UID not found!!"
    else:
        s = f"Found UIDs: {possible_UIDs[:, 0]}"
    
    print(s)  # Debugging output
    return s

#----------------------------------------------------------------------------------------------------
def browseFiles():
    import os
    folder_name1 = r"C:\Users\anura\Pictures\doc\root3_mix\New folder"
    
    for folder_name in os.listdir(folder_name1):
        folder_path = os.path.join(folder_name1, folder_name)
        
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                # Filter files by extension if needed
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.pdf')):
                    path_filename = os.path.join(folder_path, filename)
                    
                    # Print the file path for debugging
                    print(f"Processing file: {path_filename}")
                    
                    try:
                        s = masking_file(path_filename)
                        
                        # Print or update UI with the result
                        print(s)  # To see the result in the console
                        # label_file_explorer.configure(text=s)  # Uncomment this if using Tkinter UI
                        
                    except Exception as e:
                        print(f"Error processing file {path_filename}: {e}")

browseFiles()
