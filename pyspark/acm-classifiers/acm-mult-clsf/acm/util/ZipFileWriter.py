#!/usr/bin/env python
import zipfile
import os


class ZipFileWriter(object):
    pass
    
    def zip(self, outputFileName, targetDir):
        myzip = zipfile.ZipFile(outputFileName, "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(targetDir):
            for fname in files:
                if fname != outputFileName:
                    myzip.write(os.path.join(root,fname))

        myzip.close()
        
