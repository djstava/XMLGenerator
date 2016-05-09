# -*- coding: utf-8 -*-
__author__ = 'djstava@gmail.com'

import os
import sys
import xml.etree.ElementTree as ET

from common.constant import *
from checksum.md5 import *

FirstRoundImages = {'pmp.toc':PMP_ADDRESS,'secboot.toc':SECBOOT_ADDRESS,'secos.toc':SECOS_ADDRESS,'secosbak.toc':SECOS_BACK_ADDRESS,
                    'u-boot.toc':UBOOT_ADDRESS,'u-bootbak.toc':UBOOT_BACK_ADDRESS,'splash.dat':SPLASH_ADDRESS}

SecondRoundImages = {'factorytest.img':FACTORYTEST_ADDRESS,'boot.img':BOOT_ADDRESS,'system.img':SYSTEM_ADDRESS,'dvbdata.img':DVBDATA_ADDRESS,
                     'userdata.img':USERDATA_ADDRESS,'cache.img':CACHE_ADDRESS,'otaloader.img':OTALOADER_ADDRESS,'iploader.img':IPLOADER_ADDRESS,
                     'recovery.img':RECOVERY_ADDRESS}

class GenerateConfigXML(object):
    firstRoundImageDict = {}
    secondRoundImageDict = {}

    def __init__(self,path):
        self.path = path

    def buildConfigXML(self):
        '''
		:param path: images dir
		:return:
		'''

        self.listDir(self.path)

        root = ET.Element("root")

        self.firstRound = ET.SubElement(root,"FirstRound")
        for image in self.firstRoundImageDict.keys():
            if image == "pmp.toc":
                imagePmp = ET.SubElement(self.firstRound,image)
                imagePmp.set("name",image)
                imagePmp.set("address",self.firstRoundImageDict[image])
                imagePmp.set("path",os.path.relpath(self.path + "/" + image))
                imagePmp.set("md5",CalcMD5.calcFileMd5(self.path + "/" + image))
                self.firstRoundImageDict.pop(image)
                break

        for image in self.firstRoundImageDict.keys():
            if image == "secboot.toc":
                imagePmp = ET.SubElement(self.firstRound,image)
                imagePmp.set("name",image)
                imagePmp.set("address",self.firstRoundImageDict[image])
                imagePmp.set("path",os.path.relpath(self.path + "/" + image))
                imagePmp.set("md5",CalcMD5.calcFileMd5(self.path + "/" + image))
                self.firstRoundImageDict.pop(image)
                break

        for image in self.firstRoundImageDict.keys():
            if image == "secos.toc":
                imagePmp = ET.SubElement(self.firstRound,image)
                imagePmp.set("name",image)
                imagePmp.set("address",self.firstRoundImageDict[image])
                imagePmp.set("path",os.path.relpath(self.path + "/" + image))
                imagePmp.set("md5",CalcMD5.calcFileMd5(self.path + "/" + image))
                self.firstRoundImageDict.pop(image)
                break

        for image in self.firstRoundImageDict.keys():
            if image == "secosbak.toc":
                imagePmp = ET.SubElement(self.firstRound,image)
                imagePmp.set("name",image)
                imagePmp.set("address",self.firstRoundImageDict[image])
                imagePmp.set("path",os.path.relpath(self.path + "/" + 'secos.toc'))
                imagePmp.set("md5",CalcMD5.calcFileMd5(self.path + "/" + 'secos.toc'))
                self.firstRoundImageDict.pop(image)
                break


        for (name,address) in self.firstRoundImageDict.items():
            if name == "pmp.toc":
                continue

            if name == "u-bootbak.toc":
                imageName = ET.SubElement(self.firstRound,name)
                imageName.set("name",name)
                imageName.set("address",address)
                imageName.set("path",os.path.relpath(self.path + "/u-boot.toc"))
                imageName.set("md5",CalcMD5.calcFileMd5(self.path + "/u-boot.toc"))
                continue

            imageName = ET.SubElement(self.firstRound,name)
            imageName.set("name",name)
            imageName.set("address",address)
            imageName.set("path",os.path.relpath(self.path + "/" + name))
            imageName.set("md5",CalcMD5.calcFileMd5(self.path + "/" + name))

        self.secondRound = ET.SubElement(root,"SecondRound")
        for (name,address) in self.secondRoundImageDict.items():
            imageName = ET.SubElement(self.secondRound,name)
            imageName.set("name",name)
            imageName.set("address",address)
            imageName.set("path",os.path.relpath(self.path + "/" + name))
            imageName.set("md5",CalcMD5.calcFileMd5(self.path + "/" + name))

        tree = ET.ElementTree(root)
        self.indent(root)
        
        if os.path.exists(XML_CONFIG_FILE):
            os.remove(XML_CONFIG_FILE)

        tree.write("config.xml")


    def listDir(self, path):
        for root,dirs,files in os.walk(path):
            for file in files:
                if file in FirstRoundImages.keys():
                    print("firstRound: " + file)
                    if file == 'secos.toc':
                        self.firstRoundImageDict[file] = FirstRoundImages[file]
                        self.firstRoundImageDict['secosbak.toc'] = FirstRoundImages['secosbak.toc']
                        continue

                    if file == 'u-boot.toc':
                        self.firstRoundImageDict[file] = FirstRoundImages[file]
                        self.firstRoundImageDict['u-bootbak.toc'] = FirstRoundImages['u-bootbak.toc']
                        continue

                    self.firstRoundImageDict[file] = FirstRoundImages[file]

                if file in SecondRoundImages.keys():
                    print("secondRound: " + file)
                    self.secondRoundImageDict[file] = SecondRoundImages[file]



    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for e in elem:
                self.indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
        
        return elem

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 generateConfigXml.py dirOfTheImages")
        sys.exit(1)

    obj = GenerateConfigXML(sys.argv[1])
    obj.buildConfigXML()
