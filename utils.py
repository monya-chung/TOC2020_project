import os
import configparser

from flask import Flask, jsonify, request, abort, send_file, render_template, Response
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.models import *

channel_access_token = os.getenv("43w6EaGdRCMmS8Gn33VglbTL5g/Fk3K+Q3153eezsPWVKx4HJVi8xuZC23UVS/NPwbntFIXafsVolK1s21TcdQvVqOGWqLm1Sl5MhEPkq5FKnbU1D4DaoZ1OcC0MP++GDaw/KP+n4p1I99Ezt8n8pQdB04t89/1O/w1cDnyilFU=", None)
config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))

def send_text_message(reply_token, text):
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text=text)
    )
    return "OK"
    
def send_image_message(reply_token, url):
    line_bot_api.reply_message(
        reply_token,
        ImageSendMessage(
            original_content_url=url, 
            preview_image_url=url
        )
    )
    return "OK"

def send_text_button_message(reply_token, title, text, btn):
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            #thumbnail_image_url = url,
            actions = btn
        )
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"

def send_button_message(id, img, title, uptext, labels, texts):
    acts = []
    for i, lab in enumerate(labels):
        acts.append(
            MessageTemplateAction(
                label=lab,
                text=texts[i]
            )
        )

    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
        thumbnail_image_url=img,
        title=title,
        text=uptext,
        actions=acts
        )
    )
    line_bot_api.push_message(id, message)
    return "OK"