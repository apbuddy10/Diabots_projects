import os
import shutil
from settings import Settings
from vq400connector import TubeResults
from logger import errorlogger
from datetime import date,datetime,timedelta
from settings import Color
import pysftp
from urllib.parse import urlparse
import os



class FileManager:    
    sourceFolderPath:str=Settings.sourcepath
    destinationFolderPath:str=Settings.destpath
    resultsPath:str=Settings.resultsPath
    filesMoved:bool = False
    
    async def processFiles(self,tubeResults:TubeResults):
        current=datetime.now()
        if not(os.path.exists(self.sourceFolderPath)):
            errorlogger.error("Invalid source path configured")
            return False

        filename=os.path.join(self.resultsPath,"{0}.csv".format(tubeResults.barCode))
        file = open(filename, "w")
        file.write("{0};{1};{2}".format(tubeResults.barCode,tubeResults.color.name, tubeResults.plasmaLevel))
        file.close()

        # folderPath=os.path.join(self.destinationFolderPath,"OK",current.strftime('%d.%m.%Y'),newBarcode + '_' + (datetime.now().strftime('%d.%m.%Y.%H.%M')), "Vor_Centrifugation")
        # if not(os.path.exists(folderPath)):
        #     os.makedirs(folderPath)

        # file_csv = open(os.path.join(folderPath,"results.csv"), "w")
        # file_csv.write("Color: {0}, Barcode: {1}, Blood level: {2}, Plasma level: {3}".format(tubeResults.color.name,newBarcode,tubeResults.bloodLevel,tubeResults.plasmaLevel))
        # file_csv.close()

        # gather all files
        # allfiles = os.listdir(self.sourceFolderPath)

        # iterate on all files to move them to destination folder
        # for fname in allfiles:
        #     src_path = os.path.join(self.sourceFolderPath, fname)
        #     dst_path = os.path.join(folderPath, fname)
        #     shutil.move(src_path, dst_path)
            #path = os.path.join(self.sourceFolderPath, fname)
            #os.remove(path)

    async def processFilesAfterCentrifugation(self,tubeResults:TubeResults):
        current=datetime.now()
        if not(os.path.exists(self.sourceFolderPath)):
            errorlogger.error("Invalid source path configured")
            return False

        newBarcode = (tubeResults.barCode)[:-1]
        if tubeResults.color == Color.RED:
            newBarcode = newBarcode + Settings.redPostFix
        elif tubeResults.color == Color.GREEN:
            newBarcode = newBarcode + Settings.greenPostFix
        elif tubeResults.color == Color.ORANGE:
            newBarcode = newBarcode + Settings.orangePostFix

        self.filesMoved = False
        folderPresentDay=os.path.join(self.destinationFolderPath,"OK",current.strftime('%d.%m.%Y'))
        await self.processFilesWithFindingBarcode(folderPresentDay, tubeResults, newBarcode)
        if not self.filesMoved:
            # Yesterday date
            yesterday = date.today() - timedelta(days = 1)
            folderPreviousDay=os.path.join(self.destinationFolderPath,"OK",yesterday.strftime('%d.%m.%Y'))
            await self.processFilesWithFindingBarcode(folderPreviousDay, tubeResults, newBarcode)

    async def processFilesWithFindingBarcode(self, folder_path, tubeResults, newBarcode):
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                sub_dir = os.path.join(folder_path, file)
                if os.path.isdir(sub_dir):
                    save_folder_fullname = file.split("_")
                    if save_folder_fullname[0] == newBarcode:
                        folder_after_centri = os.path.join(sub_dir, "Nach_Centrifugation")
                        if not os.path.exists(folder_after_centri):
                            os.makedirs(folder_after_centri)

                        file_csv = open(os.path.join(folder_after_centri,"results.csv"), "w")
                        file_csv.write("Color: {0}, Barcode: {1}, Blood level: {2}, Plasma level: {3}".format(tubeResults.color.name,newBarcode,tubeResults.bloodLevel,tubeResults.plasmaLevel))
                        file_csv.close()

                        # gather all files
                        allfiles = os.listdir(self.sourceFolderPath)

                        # iterate on all files to move them to destination folder
                        for fname in allfiles:
                            src_path = os.path.join(self.sourceFolderPath, fname)
                            dst_path = os.path.join(folder_after_centri, fname)
                            shutil.move(src_path, dst_path)
                        self.filesMoved = True

    async def processFailedFiles(self, tubeResults:TubeResults):
        current=datetime.now()
        if not(os.path.exists(self.sourceFolderPath)):
            errorlogger.error("Invalid source path configured")
            return False             
        folderPath=os.path.join(self.destinationFolderPath,"NG",current.strftime('%d.%m.%Y'),datetime.now().strftime('%d.%m.%Y_%H_%M_%S'))
        if not(os.path.exists(folderPath)):
            os.makedirs(folderPath)            

        file = open(os.path.join(folderPath,"results.csv"), "w")
        file.write("Color: {0}, Barcode: {1}, Blood level: {2}, Plasma level: {3}".format(tubeResults.color.name,tubeResults.barCode,tubeResults.bloodLevel,tubeResults.plasmaLevel))
        file.close()
        # gather all files
        allfiles = os.listdir(self.sourceFolderPath)
        
        # iterate on all files to move them to destination folder
        for fname in allfiles:
            src_path = os.path.join(self.sourceFolderPath, fname)
            dst_path = os.path.join(folderPath, fname)
            shutil.move(src_path, dst_path)
        return True

    async def processFailedFilesAfterCentrifugation(self, tubeResults:TubeResults):
        current=datetime.now()
        if not(os.path.exists(self.sourceFolderPath)):
            errorlogger.error("Invalid source path configured")
            return False             
        folderPath=os.path.join(self.destinationFolderPath,"NG_NachCentrifugation",current.strftime('%d.%m.%Y'),datetime.now().strftime('%d.%m.%Y_%H_%M_%S'))
        if not(os.path.exists(folderPath)):
            os.makedirs(folderPath)            

        file = open(os.path.join(folderPath,"results.csv"), "w")
        file.write("Color: {0}, Barcode: {1}, Blood level: {2}, Plasma level: {3}".format(tubeResults.color.name,tubeResults.barCode,tubeResults.bloodLevel,tubeResults.plasmaLevel))
        file.close()
        # gather all files
        allfiles = os.listdir(self.sourceFolderPath)
        
        # iterate on all files to move them to destination folder
        for fname in allfiles:
            src_path = os.path.join(self.sourceFolderPath, fname)
            dst_path = os.path.join(folderPath, fname)
            shutil.move(src_path, dst_path)
        return True
    

