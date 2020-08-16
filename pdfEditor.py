"""
This is a generic pdf searcher for one string, it searches all the files in one directory; NOT MULTITHREAED YET
Picture Perfect 2020
"""

import os
from pathlib import Path
import re
import PyPDF4
import pdfminer
import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from xmlParse import XMLParser

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
#fullFilePath = [os.path.join(folderPath + '\\', x) for x in fileNames]

#used for testing one file, above commented out will search who dir
fullFilePath = [r'C:\Users\wloeffler\PycharmProjects\xmlParserUse\trialReplace.pdf']
# print(str(fullFilePath)

#xml part
xmllistClass = XMLParser()
parsedXmlList  = xmllistClass.fileParser()


# pdf checker part
for x in range(0, fullFilePath.__len__()):
    flag = False
    pdfObject = PyPDF4.PdfFileReader(str(fullFilePath[x]))
    # searches each page for the string
    text = convert_pdf_to_txt(fullFilePath[x])
    print(text)
    for y in range(0, len(parsedXmlList)):
        if parsedXmlList[y][0] in text:
            flag = True
            text = text.replace(parsedXmlList[y][0],parsedXmlList[y][1])

    print(str(text))

    tempFile = open('temp.txt','w')
    tempFile.write(text)


    add = PyPDF4.PdfFileReader(tempFile)

    if(flag):
        pdfWriter = PyPDF4.PdfFileWriter()
        pdfWriter.cloneDocumentFromReader(add)
        outfile = open('testfile.pdf', 'w')
        pdfWriter.write(outfile)



