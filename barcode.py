from fastapi import FastAPI , UploadFile,File
import cv2
import os
import numpy as np
from pyzbar import pyzbar
import glob

app = FastAPI()

def barcode(image):
    img = cv2.imread(image)
    decoded_objects = pyzbar.decode(img)
    code_list = []
    for obj in decoded_objects:
        code_list.append(obj.data)
    return code_list

@app.post('/decode')
async def get_barcode_data(uploaded_file: UploadFile = File(...)):
    input_file_path =r"C:\Users\saivineeth.k\Desktop\input"
    path = input_file_path
    
    files_to_delete=os.listdir(path)
    for i in files_to_delete:
        os.remove(path+'/'+i)
    file_location = f"{path}/{uploaded_file.filename}"
    with open(file_location, "wb") as file_object:
        file_object.write(uploaded_file.file.read())
    try:          
        final_result = barcode(file_location)

        if len(final_result)!=0:
            try:
                decoded_text = ','.join(final_result)        
                return {"barcode_data" : decoded_text}
            except:
                final_result = [data.decode() for data in final_result]
                decoded_text = ','.join(final_result)        
                return {"barcode_data" : decoded_text}
        else:
            return {"barcode_data" : 'no barcode detected.'}
    except Exception as e:
        raise(e)
    