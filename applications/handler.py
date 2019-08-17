from flask import render_template, request, url_for
from applications import event_handler, line_bot_api, app
from linebot.exceptions import LineBotApiError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,
                            FollowEvent, QuickReply, QuickReplyButton,
                            PostbackAction, ConfirmTemplate, PostbackEvent,
                            TemplateSendMessage, LocationAction,
                            ButtonsTemplate, URIAction, MessageAction)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def create_upload_url(user_id):
    tokenizer = Serializer(app.config['SECRET_KEY'], 600)
    token = tokenizer.dumps({'user_id': user_id}).decode('utf-8')
    # url = "{}".format(url_for('upload_pdf', token=token, _external=True))
    url = "{}".format(url_for('upload_testing', token=token, _external=True))
    return url


def create_upload_url_testing(user_id):
    tokenizer = Serializer(app.config['SECRET_KEY'], 600)
    token = tokenizer.dumps({'user_id': user_id}).decode('utf-8')
    url = "{}".format(url_for('upload_testing', token=token, _external=True))
    return url


def send_billing(billing_info):
    user_id = billing_info.get('user_id')
    total_pages = billing_info.get('total_pages')
    colored_pages = billing_info.get('colored_pages')
    bw_pages = billing_info.get('bw_pages')
    total_prices = billing_info.get('total_prices')

    confirm_template = ConfirmTemplate(
        text='Lanjutkan Print?',
        actions=[PostbackAction(label='Lanjutkan', data=True),
                 PostbackAction(label='Batal', data=False)])

    text_message = (f'Total print untuk {total_pages} lembar\n' +
                    f'Halaman warna : {colored_pages}\n' +
                    f'Halaman hitam-putih : {bw_pages}\n' +
                    f'Total = Rp. {total_prices}')

    try:
        line_bot_api.push_message(
            user_id, [TextSendMessage(text=text_message),
                      TemplateSendMessage(alt_text='Konfirmasi',
                                          template=confirm_template)])
    except Exception as e:
        print(e)


@event_handler.add(MessageEvent, message=TextMessage)
def text_handler(event):
    user_id = event.source.user_id
    message_text = event.message.text
    print(message_text)
    user_profile = line_bot_api.get_profile(user_id)

    if message_text in ['/Print', '/print']:
        upload_url = create_upload_url(user_id)

        buttons_template = ButtonsTemplate(
            text="Silahkan upload file pdf dengan klik tombol di bawah ini",
            actions=[URIAction(label="Upload File",
                               uri=upload_url)]
        )
        template = TemplateSendMessage(alt_text='Upload File',
                                       template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template)

    elif message_text == 'testing':
        upload_url = create_upload_url_testing(user_id)

        buttons_template = ButtonsTemplate(
            text="Silahkan upload file pdf dengan klik tombol di bawah ini",
            actions=[URIAction(label="Upload File",
                               uri=upload_url)]
        )
        template = TemplateSendMessage(alt_text='Upload File',
                                       template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template)

    elif message_text == 'quick':
        quick_reply = QuickReply(items=[
                                    QuickReplyButton(
                                        action=PostbackAction(label='Accept',
                                                              data='accept')
                                    )
        ])
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='Quick',
                                                   quick_reply=quick_reply))

    elif message_text == 'confirm':
        confirm_template = ConfirmTemplate(text='Confirm?',
                                           actions=[
                                               PostbackAction(
                                                   label='Accept',
                                                   data='accept'),

                                               PostbackAction(
                                                   label='Deny', data='deny')]
                                           )

        template = TemplateSendMessage(alt_text='alt',
                                       template=confirm_template)

        line_bot_api.reply_message(event.reply_token, template)

    elif message_text == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons',
            actions=[
                URIAction(label='Go to line.me',
                          uri='https://line.me'),
                PostbackAction(label='ping', data='ping'),
                LocationAction(label='Location'),
                MessageAction(label='Translate Rice',
                              text='米')]
        )
        template = TemplateSendMessage(alt_text='alt',
                                       template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template)


def request_location(user_id, reply_token):
    buttons_template = ButtonsTemplate(
        text="Silahkan kirim lokasi pengantaran",
        actions=[LocationAction(label="Kirim Lokasi")]
    )
    line_bot_api.reply_message(reply_token,
                               TemplateSendMessage(alt_text="Kirim Lokasi",
                                                   template=buttons_template))


@event_handler.add(PostbackEvent)
def postback_handler(event):
    data = event.postback.data
    user_id = event.source.user_id
    reply_token = event.reply_token
    if data:
        request_location(user_id, reply_token)





@app.route('/test/<user_id>')
def testing(user_id):
    url = create_upload_url(user_id)
    return url
