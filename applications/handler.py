from flask import render_template, request, url_for
from applications import event_handler, line_bot_api, app
from linebot.exceptions import LineBotApiError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,
                            FollowEvent)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def create_upload_url(user_id):
    tokenizer = Serializer(app.config['SECRET_KEY'],600)
    token = tokenizer.dumps({ 'user_id': user_id }).decode('utf-8')
    url = "{}".format(url_for('upload_pdf', token=token, _external=True))
    return url


def send_billing(billing_info):
    user_id = billing_info.get('user_id')
    total_pages = billing_info.get('total_pages')
    colored_pages = billing_info.get('colored_pages')
    bw_pages = billing_info.get('bw_pages')
    total_prices = billing_info.get('total_prices')

    text_message = (f'Total print untuk {total_pages} lembar\n'
                    + f'Halaman warna : {colored_pages}\n'
                    + f'Halaman hitam-putih : {bw_pages}\n'
                    + f'Total = Rp. {total_prices}')

    try:
        line_bot_api.push_message(user_id,[TextSendMessage(text=text_message)])
    except Exception as e:
        print(e)


@event_handler.add(MessageEvent, message=TextMessage)
def text_handler(event):
    user_id = event.source.user_id
    message_text = event.message.text
    user_profile = line_bot_api.get_profile(user_id)

    if message_text == '/Print' or '/print':
        upload_url = create_upload_url(user_id)
        reply_text = (
            'Silahkan upload file dalam bentuk pdf ke link berikut ini\n' 
            + upload_url)

        line_bot_api.reply_message(event.reply_token,
                                   TextMessage(text=reply_text))


@app.route('/test/<user_id>')
def testing(user_id):
    url = create_upload_url(user_id)
    return url
