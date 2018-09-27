import pytesseract as pt
from PIL import Image


image = Image.open('/home/captain/1.jpg')

text = pt.image_to_string(image)
print(text)