from applications.config import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET
from flask import (Flask, request, abort, render_template,
                   make_response, jsonify)
from flask_wtf.csrf import CSRFProtect
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = '5ca5d261647a39ae9f9c82a1413a39b8'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
event_handler = WebhookHandler(CHANNEL_SECRET)

from applications import upload_helper
from applications import handler


@app.route("/")
def index():
    return 'Hello World'


@app.route("/testing", methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        try:
            # data = request.form.get('file')
            # print(data.filename)
            pdf_file = request.files['file']
            pdf_file = upload_helper.save_file(pdf_file)
            res = make_response(jsonify({"message": "File Uploaded"}), 200)
            print(res)
        except Exception as e:
            print(e)

    return render_template('UploadFile.html')


@app.route('/callback', methods=['POST'])
@csrf.exempt
def callack():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('\nRequest Data: \n' + body)

    try:
        event_handler.handle(body, signature)
    except InvalidSignatureError as e:
        app.logger.error(e)
        abort(400)

    return 'OK'
