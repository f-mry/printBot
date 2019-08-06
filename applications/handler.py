from applications import eventHandler, lineBot, app
from flask import render_template, request, url_for
from applications.pdf_helper import UploadForm, parsePDFMeta, savePdfFile
from linebot.exceptions import LineBotApiError
from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage, FollowEvent, 
        )
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def createUploadURL(user_id):
    print(user_id)
    tokenizer = Serializer(app.config['SECRET_KEY'],600)
    userToken = tokenizer.dumps({ 'user_id': user_id }).decode('utf-8')
    url = "{}".format(url_for('upload', token=userToken, _external=True))
    return url

def verifyToken(token):
    tokenLoader = Serializer(app.config['SECRET_KEY'])
    try:
        user_id = tokenLoader.loads(token)['user_id']
    except :
        return None
    return user_id

def totalPrice(num_pages):
    pricePerPage = 500
    return num_pages*pricePerPage

def sendConfirmation(user_id,num_pages,totalPrice):
    lineBot.push_message( user_id,[ TextSendMessage(text='Total print untuk {} lembar = Rp. {}'.format(num_pages,totalPrice)) ])


@eventHandler.add(MessageEvent, message=TextMessage)
def textMessageHandler(event):
    user_id = event.source.user_id
    print("Handler: "+user_id)
    text = event.message.text
    profile = lineBot.get_profile(user_id)

    if text == 'Print':
        uploadURL = createUploadURL(user_id)
        lineBot.reply_message(
                event.reply_token,[
                    TextMessage(text='Hai '+ profile.display_name),
                    TextMessage(text='Silahkan upload file dalam bentuk pdf ke link berikut ini\n"'+uploadURL+'"')
                    ]
                )

@app.route('/test/<user_id>')
def testing(user_id):
    url = createUploadURL(user_id)
    return url

@app.route('/upload/<token>', methods=['GET','POST'])
def upload(token):
    form = UploadForm()
    user_id = verifyToken(token)
    if form.validate_on_submit():
        try:
            pdfFile = request.files['pdfFileForm']
            pdfPath = (savePdfFile(pdfFile))
            pdfInfo =  parsePDFMeta(pdfPath)
        except Exception as e:
            print(e)
        num_pages = pdfInfo['num_pages']
        sendConfirmation(user_id,num_pages,totalPrice(num_pages))
        return render_template('success.html')
    else:
        if user_id != None:
            return render_template('upload.html', form=form)
        else:
            return 'Oops Time Out'


