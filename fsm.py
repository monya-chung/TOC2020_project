import os
import sys
import configparser

from transitions.extensions import GraphMachine
from graphviz import *
from flask import Flask, jsonify, request, abort, send_file, render_template, Response
from utils import *
from linebot.models import *
from linebot import LineBotApi, WebhookParser, WebhookHandler

config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "go to menu"

    def is_going_to_fsm(self, event):
        text = event.message.text
        return text.lower() == "go to fsm"

    def is_going_to_island(self, event):
        text = event.message.text
        return text.lower() == "go to island"

    def on_enter_user(self, event):
        print("I'm entering initial user")
        reply_token = event.reply_token
        send_text_message(reply_token, "Hello!")
        return text.lower() == "initial user"

    def on_enter_menu(self, event):
        print("I'm entering menu")
        reply_token = event.reply_token
        send_text_message(reply_token, "您好，歡迎來到孟岳的旅遊日記!\n您要看:\n1->離島\n2->環島")
        return text.lower() == "menu state"

    def on_enter_fsm(self, event):
        print("I'm entering fsm")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger fsm")
        return text.lower() == "go to island"

    def on_enter_island(self, event):
        print("I'm entering island")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger island")
        return text.lower() == "go to island"


def chg_state_rule(now_state, chg):
    #global now_state
    global new_state
    if now_state == 0: 
        if chg == 1: new_state = 1
    if now_state == 1:
        if chg == 1: new_state = 2
        if chg == 2: new_state = 3
        if chg == 3: new_state = 6
    if now_state == 2:
        if chg == 1: new_state = 4
    if now_state == 3:
        if chg == 1: new_state = 5    
    if now_state == 2 or now_state == 3 or now_state == 4 or now_state == 5 or now_state == 6:
        if chg == 0: new_state = 1
    return new_state

def act_state_rule(now_state, event):
    if now_state == 1:
        title = '歡迎來到孟岳的旅遊日記!'
        text = '您想要看:'
        btn = [
            MessageTemplateAction(
                label = '離島風光',
                text ='1'
            ),
            MessageTemplateAction(
                label = '單車環島',
                text = '2'
            ),
            MessageTemplateAction(
                label = 'FSM圖片',
                text = '3'
            ),
        ]
        send_text_button_message(event.reply_token, title, text, btn)
        #send_text_message(event.reply_token,"歡迎來到孟岳的旅遊日記!\n您想要看:\n1->離島風光\n2->單車環島\n請選號")
    if now_state == 2:
        title = '孟岳的離島風光旅遊日記!'
        text = '看照片 或 返回選單'
        btn = [
            MessageTemplateAction(
                label = '看照片',
                text ='1'
            ),
            MessageTemplateAction(
                label = '返回選單',
                text = '0'
            ),
        ]
        send_text_button_message(event.reply_token, title, text, btn)
        #send_text_message(event.reply_token,"孟岳的離島風光旅遊日記! \n按1看照片\n按0回選單")
    if now_state == 3:
        title = '孟岳的單車環島旅遊日記!'
        text = '看照片 或 返回選單'
        btn = [
            MessageTemplateAction(
                label = '看照片',
                text ='1'
            ),
            MessageTemplateAction(
                label = '返回選單',
                text = '0'
            ),
        ]
        send_text_button_message(event.reply_token, title, text, btn)
        #send_text_message(event.reply_token,"孟岳的單車環島旅遊日記! \n按1看照片\n按0回選單")
    if now_state == 4:
        reply_token = event.reply_token
        id = event.source.user_id
        img = "https://9d439982e52d.ngrok.io/my_travel_image/IMG_1.jpg"
        #img = "https://img.ltn.com.tw/Upload/news/600/2018/05/28/2439579_4.jpg"
        title = '蘭嶼地下屋'
        uptext = '為了擋強風而建的屋子'
        labels = ['返回選單']
        texts = ['0']
        send_button_message(id, img, title, uptext, labels, texts)
    if now_state == 5:
        reply_token = event.reply_token
        id = event.source.user_id
        img = "https://9d439982e52d.ngrok.io/my_travel_image/IMG_2.jpg"
        #img = "https://attach.mobile01.com/attach/201011/mobile01-c09b537686f7e4e2d5ac88f8cb13158b.jpg"
        title = '美麗的東海岸'
        uptext = '台東釋迦現採的喔!'
        labels = ['返回選單']
        texts = ['0']
        send_button_message(id, img, title, uptext, labels, texts)

    if now_state == 6:
        img = "https://9d439982e52d.ngrok.io/my_travel_image/myfsm.jpg"
        send_image_message(event.reply_token, img)

    return 'ok'