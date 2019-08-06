from applications.config import CHANNEL_ACCESS_TOKEN,CHANNEL_SECRET
from flask import Flask, request, abort, render_template, url_for
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)
app.config['SECRET_KEY'] = '5ca5d261647a39ae9f9c82a1413a39b8'

lineBot = LineBotApi(CHANNEL_ACCESS_TOKEN)
eventHandler = WebhookHandler(CHANNEL_SECRET)

from applications import handler

@app.route("/")
def index():
    return 'Hello World'

@app.route('/callback' , methods=['POST'])
def callack():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info('\nRequest Data: \n' + body)

    try:
        eventHandler.handle(body,signature)

    except InvalidSignatureError as e:
        app.logger.error(e)
        abort(400)

    return 'OK'

