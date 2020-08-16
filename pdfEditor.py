"""
This is a generic pdf searcher for one string, it searches all the files in one directory; NOT MULTITHREAED YET
Picture Perfect 2020
"""

import os
from pathlib import Path
import re
import PyPDF4
import pdfminer3
import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# basic info
folderPath = r"C:\Users\wloeffler\Downloads\nbCITI_MRN385548\home\biblen"


# charsToRemove =['1','2','3','4','5','6','7','8','9','0']
# filepathDirs = ['1816','2840','5585','12900','43076', '115066','146208','161649','166591','839624','1000139']


def capitalizeFirstLetterofAllWords(stringInput):
    return ' '.join(elem.capitalize() for elem in stringInput.split())


# taxed from stackoverflow
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    text = retstr.getvalue()
    retstr.close()
    return text


badString = "Verify Patient Status/Charges"

# gets the local file name
fileNames = os.listdir(folderPath)
# gets the full file path
fullFilePath = [os.path.join(folderPath + '\\', x) for x in fileNames]
# print(str(fullFilePath)

# pdf checker part
for x in range(0, fullFilePath.__len__()):

    pdfObject = PyPDF4.PdfFileReader(str(fullFilePath[x]))
    # searches each page for the string
    text = convert_pdf_to_txt(fullFilePath[x])

    if badString in text:
        print("error in file " + fileNames[x] + "\n it contains " + badString)

print('---done---')