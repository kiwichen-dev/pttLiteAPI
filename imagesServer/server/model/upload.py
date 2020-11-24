from flask import Response
from flask_restful import Resource
from server import InitAPP
import os
from server import InitAPP

class Upload(InitAPP):
    def uploadFiles(self,img_files):
        response = list()
        imgs_uri = list()
        for _ in img_files:
            is_img = self.is_allowed_file(_)
            if _ and is_img[0]:
                dirname = 'static/'
                os.makedirs(dirname,mode=0o777,exist_ok=True)
                ext = is_img[2]
                filename = self.random_image_name + '.' + ext
                save_path = os.path.join(dirname,filename)
                _.save(save_path)
                response.append(True)
                imgs_uri.append("https://pttlite.firewall-gateway.com/images/{}".format(filename))
                del _
                del is_img
            else:
                response.append(False)
                del _
                del is_img
        if False in response:
            return False,imgs_uri
        else:
            return True,imgs_uri

    def is_allowed_file(self,uploadFile):
        if '.' in uploadFile.filename:
            filename = uploadFile.filename
            ext = uploadFile.filename.rsplit('.')[-1].lower()
            if ext in {'png','jpg','jpeg'}:
                del uploadFile
                return True,filename,ext
            else:
                del uploadFile
                return False,filename,ext
        else:
            del uploadFile
            return False,None