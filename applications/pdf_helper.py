from applications import app
from flask_wtf import FlaskForm 
from flask_wtf.file import FileAllowed 
from wtforms import FileField, SubmitField, HiddenField, StringField
from wtforms.validators import DataRequired, ValidationError
from PyPDF2 import PdfFileReader
import os

class UploadForm(FlaskForm):
    pdfFileForm = FileField('Upload PDF File', validators=[FileAllowed(['pdf'],message='Upload file dalam bentuk PDF'), 
                                                           DataRequired(message='Pilih dokumen')])
    submit = SubmitField('Upload Document') 

def savePdfFile(pdfFile):
    path = os.path.join(app.root_path,'cust_file/',pdfFile.filename)
    pdfFile.save(path)
    return path

def parsePDFMeta(pdfPath):
    with open(pdfPath, 'rb') as pdfFile:
        pdfData = PdfFileReader(pdfFile)
        pdfMeta = {'pdf_info': pdfData.getDocumentInfo(), 'num_pages': pdfData.getNumPages()}
    return pdfMeta


    

