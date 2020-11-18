from flask import Response
from flask_restful import Resource
from server import InitAPP
import os

class Upload():
    def uploadFiles(self,img_file):
        is_img = self.is_allowed_file(img_file)
        if img_file and is_img[0]:
            dirname = 'static/'
            os.makedirs(dirname,mode=0o777,exist_ok=True)
            save_path = os.path.join( dirname, img_file.filename )
            img_file.save(save_path)
            del img_file
            del is_img
            return True
        else:
            del img_file
            del is_img
            return False

    def is_allowed_file(self,uploadFile):
        if '.' in uploadFile.filename:
            filename = uploadFile.filename
            ext = uploadFile.filename.rsplit('.', 1)[1].lower()
            if ext in {'png','jpg', 'jpeg'}:
                del uploadFile
                return True,filename,ext
            else:
                del uploadFile
                return True,filename,ext
        else:
            del uploadFile
            return False