# -*- coding: utf-8 -*-
__author__ = 'djstava@gmail.com'

import hashlib

class CalcMD5(object):
    def __init__(self):
        pass

    @classmethod
    def calcFileMd5(self,filePath):
        '''
        :param filePath:
        :return: file checksum value
        '''

        md5 = hashlib.md5()

        fp = open(filePath,'rb')
        md5.update(fp.read())

        while True:
            block = fp.read(1048576)
            if not block:
                break
            md5.update(block)

        fp.close()
        return md5.hexdigest()

    @classmethod
    def calcStringMd5(self,str):
        '''
        :param str:
        :return: string checksum value
        '''

        return hashlib.md5(str.encode("utf-8")).hexdigest()