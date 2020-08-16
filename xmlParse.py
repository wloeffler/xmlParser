'''
This goes through the XML file and reads it, then will create a list to be used by the pdf editor
to change strings in the pdf
'''

import xml.etree.ElementTree as ET

keyfile = ET.parse(r'/Users/will/PycharmProjects/xmlParser/BH Columbia-Suicide Severity Rating Scale 8-13-2020@1617 PF.xml')

root = keyfile.getroot()

print((root.tag,root.attrib))

counter =0
temp = ''
for element in root.iter('MODULE'):

        for elem in element.iter():

            if(counter ==1):
                temp = elem.text
                counter = counter+1
            if(counter ==2):
                pass
            if(counter==3):
                temp2 = str(elem.text)
                print(temp2[:40],', ',temp,"\n")
                counter = 0
            if(str(elem.text) in ['caption','discrete_task_assay']):
                counter = counter + 1



