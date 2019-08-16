from applications import app
from flask import render_template, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from applications.pdf_color import get_pdf_info
from applications.handler import send_billing
import os

UPLOAD_FOLDER = 'UPLOAD_FOLDER/'


class UploadForm(FlaskForm):
    file_form = FileField(
            'File PDF',
            validators=[FileAllowed(['pdf']),
                        DataRequired(message='Pilih Dokumen')]
            )
    submit = SubmitField('Upload Document')


def save_file(pdf_file):
    path = os.path.join(app.root_path, UPLOAD_FOLDER, pdf_file.filename)
    print(path)
    pdf_file.save(path)
    return path


def verify_token(token):
    tokenLoader = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = tokenLoader.loads(token)['user_id']
    except:
        return None
    return user_id


def create_billing(user_id,page_info):
    total_pages = page_info.get('total_pages')
    colored_pages = page_info.get('colored_pages')
    bw_pages = page_info.get('bw_pages')

    colored_pages_prices = 700
    bw_pages_prices = 500
    total_prices = ((colored_pages_prices * colored_pages)
                     + (bw_pages_prices * bw_pages))

    billing_info = {'user_id' : user_id,
                    'total_pages' : total_pages,
                    'colored_pages' : colored_pages,
                    'bw_pages' : bw_pages,
                    'total_prices' : total_prices}
    print(billing_info)
    return billing_info


@app.route('/upload/<token>', methods=['GET','POST'])
def upload_pdf(token):
    form = UploadForm()
    user_id = verify_token(token)

    if form.validate_on_submit():
        try:
            pdf_file = request.files['file_form']
            pdf_path = save_file(pdf_file)
        except Exception as e:
            print(e)

        pdf_info = get_pdf_info(pdf_path)
        billing_info = create_billing(user_id,pdf_info)
        send_billing(billing_info)
        return render_template('success.html')

    else:
        if user_id != None:
            return render_template('upload.html', form=form)
        else:
            return 'Time Out'




