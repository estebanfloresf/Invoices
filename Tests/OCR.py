from PIL import Image
from PIL import ImageFilter
import sys

import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[2]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'


image = Image.open('Images/test4.jpg')
image.filter(ImageFilter.SHARPEN)
txt = tool.image_to_string(
    image,
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)

print(str(txt).encode('utf-8'))

