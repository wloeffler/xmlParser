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

from fpdf import FPDF

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
    #print(text)
    for y in range(0, len(parsedXmlList)):
        if parsedXmlList[y][0] in text:
            flag = True
            text = text.replace(parsedXmlList[y][0],parsedXmlList[y][1])

    #print(str(text))

    tempFile = open('temp.txt','w')
    tempFile.write(text)
    '''
    for line in text:
        print(len(line))
        if len(line)>84:
            print('called')
            iterations = len(line) % 84
            for ix in range(0, iterations):
                tempFile.write(line[int(ix * 84): int(((ix + 1) * 84))] + '')
        else:
            tempFile.write(line)
'''

    tempFile.close()

    readinFile = open('temp.txt')
    pdfLineSize = 84


    if(flag):

        pdf = FPDF(orientation= 'P', unit= 'mm', format='letter')
        pdf.set_right_margin(margin='10')
        pdf.add_page(orientation='P')
        #pdf.accept_page_break()
        pdf.set_font("Courier", size=10)
        outfile = open('testfile1.pdf', 'w')
        lineNum =0
        for line in readinFile:
            # adds support for lines greater than x char
            print(f"called  {len(line)}")
            tempText = line.replace('\n', '')
            tempText = tempText.replace('\r', '')
            tempText = tempText.replace('\t', '')
            iterations = len(line) // pdfLineSize
            if(iterations == 0):
                iterations =1
            for ix in range(0, iterations):
                if('MRN' in line and lineNum != 0):
                    pdf.add_page()
                pdf.cell(pdfLineSize, 3.5, txt=tempText[int(ix * pdfLineSize):int(((ix + 1) * pdfLineSize))], ln=1,
                         align='l')
                lineNum = lineNum+1

        '''
        
        pdf = FPDF(orientation= 'P', unit= 'mm', format='letter')
        pdf.set_right_margin(margin='10')
        pdf.add_page(orientation='P')
        #pdf.accept_page_break()
        pdf.set_font("Courier", size=7)
        outfile = open('testfile1.pdf', 'w')
        for line in readinFile:
            #adds support for lines greater than x char
            if(len(line)>pdfLineSize):
                print(f"called  {len(line)}")
                tempText = line.replace('\n','')
                tempText = tempText.replace('\r','')
                tempText = tempText.replace('\t', '')
                iterations = len(line)%pdfLineSize
                for ix in range(0,iterations):
                    pdf.cell(pdfLineSize, 3, txt=tempText[int(ix*pdfLineSize):int(((ix+1)*pdfLineSize))], ln=1, align='l')
            #for only one line
            else:
                if('MRN' in line):
                    pdf.add_page()
                pdf.cell(pdfLineSize,3, txt=line, ln=1, align='l')
           # print(line)
           '''







        pdf.output('testfile1.pdf')
        outfile.close()



