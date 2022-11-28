### Start of the program
#Importing library
import requests
import qrcode
import cv2
import re
import sys

from pyzbar.pyzbar import decode
from sympy import isprime
from bs4 import BeautifulSoup
from PIL import Image

# Command line arguments 

# command line to type in the terminal: python codecodecode.py https://chifu.eu/teachings/mag1/barbar/ MyQRCodeWoop

# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])
 
print("\nArguments passed:", end = " ")
for i in range(1, n):
    print(sys.argv[i], end = " ")
     
# Addition of numbers
link = sys.argv[1]
file_name_qr = sys.argv[2]
     
print("\n\nLink:", link)
print("\nFilename for QR code image file:", file_name_qr, "\n")

#link = 'https://chifu.eu/teachings/mag1/barbar/'
#file_name_qr = 'MyQRCodeWoop'

# Functions

# Make one method to decode the barcode
def BarcodeReader(image):
    # read the image in numpy array using cv2
    img = cv2.imread(image)
    # Decode the barcode image
    detectedBarcodes = decode(img)
    for barcode in detectedBarcodes: 
            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect
            # Put the rectangle in image using
            # cv2 to heighlight the barcode
            cv2.rectangle(img, (x-10, y-10),
                          (x + w+10, y + h+10),
                          (255, 0, 0), 2) 
            if barcode.data!="":  
                txt_barcode.append((barcode.data).decode('utf-8'))

# Extraction of letters from prime numbers
def sommeDeListe(list, size):
    if (size == 0):
        return 0
    else:
        return list[size - 1] + sommeDeListe(list, size - 1)

# Retrieval of urls based on server response
i=0
links = {}

while True:
    i += 1
    link_1 = { i : link + "{0:0>6}".format(i) + '.png'} # to have the correct name of the image
    links.update(link_1)
    body = requests.get(links[i]).text
    if body[:15] == '<!DOCTYPE HTML>': # if the link refers to an html page
        links.pop(i)
        break
    else:
        continue
    
# Image Download Loop
for i in links:
    f = open("{0:0>6}".format(i) + '.png','wb')
    response = requests.get(links[i])
    f.write(response.content)
    f.close()
    
# Barcode reading
# Loop creation of PC storage links               
image_link = []

for i in range(1,len(links)+1):
    image_link.append("{0:0>6}".format(i) + '.png')

# Barcode text retrieval loop
txt_barcode = []
i = 0

while i <=len(link)+1:
    image=image_link[i]
    BarcodeReader(image)
    i += 1

# Extract letters and numbers from barcode text
i=0
letnum_barcode = {}

while i != len(txt_barcode):
    letnum_barcode_1 = {i: {'numbers' : [int(s) for s in re.findall(r'\d', txt_barcode[i])], 
              'letters' : [str(s) for s in re.findall(r'\D', txt_barcode[i])]}}
    letnum_barcode.update(letnum_barcode_1)
    i += 1 

# Sum of digits + get prime numbers
# Extraction of letters from prime numbers
prime_number = {}
word_prime_number = {}        
secret_key = ""

for i in letnum_barcode:
    num_list = letnum_barcode[i]['numbers']
    words_list = letnum_barcode[i]['letters']
    total = sommeDeListe(num_list, len(num_list))
    words = "".join(words_list)
    
    if isprime(total) == True:
        prime_number.update({i : total})
        word_prime_number.update({i : words})
    else:
        continue

for i in word_prime_number:
    secret_key += "".join(word_prime_number[i])
    
print("The secret key is: " + secret_key)
link_secret = link + secret_key

# secret_key = obBVJoFTpekfmuSboXBcLKnXRvoqdvcMsaWDEgYrhvucTQLJeGbmQyqFOYjjxOLyvcWkrI

# Retrieving html code

# Selection first digits first valid code
for first_code_str in sorted(prime_number)[:1]:
    first_code_str = [str(int) for int in letnum_barcode[2]['numbers']]
first_code = "".join(first_code_str)

# Extract paragraph from html page
html = requests.get(link_secret).text
soup = BeautifulSoup(html, 'html.parser')

soup = soup.find(id=first_code)

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

# QR code generation

# Data to be encoded
data = text

# Encoding data using make() function
qr_img = qrcode.make(data)

# Saving as an image file
qr_img.save(file_name_qr + '.png')

# Show the QR
im = Image.open(file_name_qr + '.png') 
im.show()