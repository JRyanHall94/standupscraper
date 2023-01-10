#   The current form of this file will open an image file named
# 'some_image.png' and run it through the OCR app and store its text contents
# in the variable 'text', then print that string.
#   Eventually, I plan to expand this into a function that can be called on
# each screenshot taken by the scraper script.
from PIL import Image
from pytesseract import pytesseract

tessa_path = r'/opt/homebrew/bin/tesseract'
# image_path = r'324390314_1519805381865932_7093926702738867279_n.jpg'

# img = Image.open(image_path)
# pytesseract.tesseract_cmd = tessa_path

# text = pytesseract.image_to_string(img)
# print(text)


def scan_image(image_path):
    img = Image.open(image_path)
    pytesseract.tesseract_cmd = tessa_path

    text = pytesseract.image_to_string(img)
    return text
