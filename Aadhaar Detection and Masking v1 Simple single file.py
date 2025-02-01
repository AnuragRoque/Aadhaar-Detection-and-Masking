from tkinter import *
from tkinter import filedialog
import cv2
import numpy as np
import re
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# Utility to find potential UID numbers in extracted text
def find_text(text):
    n = len(text)
    if n < 12:
        return 0
    for i in range(14, n):
        s = text[i - 14:i]
        if s[4] == " " and s[9] == " ":
            s = s.replace(" ", "")
            n1 = len(s)
            s1 = s[n1 - 12:n1]
            if i == 125:
                pass
            if s1.isnumeric() and len(s1) >= 12:
                return 1
    return 0

# Checks for presence of UID in the image
def addhar_check(file_name):
    img = Image.open(file_name)
    u = 0
    for i in range(25):
        try:
            img.seek(i)
            u += 1
            array = np.array(img)
            c = len(array.shape)
            if c == 2:  # Grayscale image
                if array[0][0] == True or array[0][0] == False:
                    array = array * 255
                    img10 = array.astype(np.uint8)
                    array = np.array(img10)
            elif c == 3:  # Color image
                if array[0][0][0] == True or array[0][0][0] == False:
                    array = array * 255
                    img10 = array.astype(np.uint8)
                    array = np.array(img10)
            text = pytesseract.image_to_string(array)
            v = find_text(text)
            if v:
                break
            else:
                gaussianBlur = cv2.GaussianBlur(array, (5, 5), cv2.BORDER_DEFAULT)
                text = pytesseract.image_to_string(gaussianBlur)
                v = find_text(text)
                if v:
                    break
        except EOFError:
            u = 0
            break
    return u

# Verhoeff checksum algorithm to validate UID
def compute_checksum(number):
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
        (9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
    )

    permutation_table = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
        (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
        (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
        (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
        (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
        (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
        (7, 0, 4, 6, 9, 1, 3, 2, 5, 8)
    )

    # Transform number list
    number = tuple(int(n) for n in reversed(str(number)))

    # Calculate checksum
    checksum = 0
    for i, n in enumerate(number):
        checksum = multiplication_table[checksum][permutation_table[i % 8][n]]

    return checksum

# Search Possible UIDs with Bounding Boxes
def Regex_Search(bounding_boxes):
    possible_UIDs = []
    Result = ""

    for character in range(len(bounding_boxes)):
        if len(bounding_boxes[character]) != 0:
            Result += bounding_boxes[character][0]
        else:
            Result += '?'

    matches = re.finditer(r'\d{12}', Result)

    for match in matches:
        UID = int(Result[match.start():match.end()])
        if compute_checksum(UID) == 0 and UID % 10000 != 1947:
            possible_UIDs.append([UID, match.start()])

    return possible_UIDs

# Mask the identified UIDs
def Mask_UIDs(image_path, possible_UIDs, bounding_boxes):
    img = cv2.imread(image_path)
    height = img.shape[0]

    for UID in possible_UIDs:
        digit1 = bounding_boxes[UID[1]].split()
        digit8 = bounding_boxes[UID[1] + 7].split()

        h1 = min(height - int(digit1[4]), height - int(digit8[4]))
        h2 = max(height - int(digit1[2]), height - int(digit8[2]))

        top_left_corner = (int(digit1[1]), h1)
        bottom_right_corner = (int(digit8[3]), h2)

        img = cv2.rectangle(img, top_left_corner, bottom_right_corner, (0, 0, 0), -1)

    file_name = image_path.split('/')[-1].split('.')[0] + "_masked" + "." + image_path.split('.')[-1]
    cv2.imwrite(file_name, img)
    return file_name

# Extract and Mask UIDs
def Extract_and_Mask_UIDs(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    settings = '-l eng --oem 3 --psm 11'

    bounding_boxes = pytesseract.image_to_boxes(Image.fromarray(gray), config=settings).split(" 0\n")
    possible_UIDs = Regex_Search(bounding_boxes)

    if len(possible_UIDs) > 0:
        masked_img = Mask_UIDs(image_path, possible_UIDs, bounding_boxes)
        return masked_img, possible_UIDs

    return None, None

# Handles the image masking process
def masking_file(input_path):
    masked_img, possible_UIDs = Extract_and_Mask_UIDs(input_path)

    if masked_img is None:
        s = "UID not found!!"
    else:
        uids = [uid[0] for uid in possible_UIDs]
        s = "Found UIDs :" + str(uids)

    return s

# GUI function to browse files
def browseFiles():
    filename = filedialog.askopenfilename(title="Select a File", filetypes=(("image files", "*.png*"), ("image files", "*.jpeg*"), ("image files", "*.jpg*"), ("all files", "*.*")))
    label_file_explorer.configure(text="Masking in Progress: " + filename)
    s = masking_file(filename)
    label_file_explorer.configure(text=s)

# Tkinter GUI setup
window = Tk()
window.title('Aadhaar Masking')
window.config(background="white")

label_file_explorer = Label(window, text="Upload Here", width=100, height=4, fg="blue")

button_explore = Button(window, text="Browse Files", command=browseFiles)
button_exit = Button(window, text="Exit", command=exit)

label_file_explorer.grid(column=1, row=1)
button_explore.grid(column=1, row=2)
button_exit.grid(column=1, row=3)

window.mainloop()
