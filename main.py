try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract
from urllib.request import urlretrieve
import requests
from wand.image import Image as WImage
import os
import shutil


bv_url = "https://marknad.byggvesta.se/byggvesta/files/pdf/file13"
download_err = 0
convert_err = 0
read_err = 0


def download_all_pdfs():
    global download_err
    for file_id in range(200, 400):
        full_url = bv_url + str(file_id) + ".pdf"
        print(full_url)
        try:
            urlretrieve(full_url, str(file_id) + ".pdf")
            r = requests.get(full_url)
            with open(str(file_id) + ".pdf", "wb") as code:
                code.write(r.content)
        except Exception:
            download_err = download_err + 1
            pass


def convert_to_jpeg():
    global convert_err
    for file_id in range(200, 400):
        try:
            pdf_path = "img/" + str(file_id) + ".pdf"
            with WImage(filename=pdf_path, resolution=200) as img:
                img.format = "jpeg"
                img.save(filename=str(file_id) + ".jpg")
        except Exception as e:
            print(e)
            convert_err = convert_err + 1
            pass


def filter_nice_areas():
    global read_err
    for file_id in range(200, 400):
        try:
            img_path = "img/" + str(file_id) + ".jpg"
            text = pytesseract.image_to_string(Image.open(img_path))
            if "Djurgardstaden" in text and "Stud" in text:
                shutil.move(img_path, "/Users/zinokader/Documents/Projekt/Programmering/ByggvestaScanner/img/filtered")
        except Exception as e:
            print(e)
            read_err = read_err + 1
            pass

#download_all_pdfs()
#convert_to_jpeg()
filter_nice_areas()