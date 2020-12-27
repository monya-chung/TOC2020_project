import os
import sys
import configparser

from flask import Flask, jsonify, request, abort, send_file, render_template, Response
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from fsm import TocMachine, chg_state_rule, act_state_rule
from utils import send_text_message, send_image_message

load_dotenv()

machine = TocMachine(
    states=["user", "menu", "fsm", "island"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "fsm",
            "conditions": "is_going_to_fsm",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "island",
            "conditions": "is_going_to_island",
        },    
        {"trigger": "go_back", "source": ["menu", "fsm", "island"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

now_state = 0
new_state = 0
ini_state = 0
chg_state = 0

app = Flask(__name__, static_url_path="")

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
parser = WebhookParser(config.get('line-bot', 'channel_secret'))

@app.route("/webhook", methods=['POST'])
def webhook_handler():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: \n" + body)
    
    try:
        events = parser.parse(body, signature)  
    except InvalidSignatureError:
        abort(400)

    global now_state, new_state, ini_state, chg_state
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        #print(f"\nFSM STATE: {machine.state}")
        #print(f"\n user Id : \n{event.source.user_id}")
        #print(f"REQUEST BODY: \n{body}")
        #response = machine.advance(event)
        #print(response)
        print('old_state = ',now_state)
        if now_state == ini_state: 
            chg_state = 1
            now_state = chg_state_rule(now_state, chg_state)
        else:
            if event.message.text.isdigit():
                chg_state = int(event.message.text)
                if chg_state == 1 or chg_state == 2 or chg_state == 3 or chg_state == 0:
                    now_state = chg_state_rule(now_state, chg_state)
                else:
                    send_text_message(event.reply_token,"請輸入正確號碼")
            else:
                send_text_message(event.reply_token,"請輸入號碼")
        
        act_state_rule(now_state, event)

    print('new_state = ',now_state)
    return 'OK'

@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("show-fsm.png", prog="dot", format="png")
    return send_file("show-fsm.png", mimetype="image/png")

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)