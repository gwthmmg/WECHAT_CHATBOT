# -*- coding: utf-8 -*-
import hashlib
import time
import falcon
import xmltodict
import argparse
import uuid
import time
import dialogflow
import os

#Set google environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "VoiceOnly-2a3bb40ee705.json"

WECHAT_TOKEN = "wechat_token"

class WeChatApiResource(object):
  def __init__(self, token):
    self.token = token

#Check whether the message received in correct format
  def validate_message(self, message):
    return (
      message != None and
      message['xml'] != None and
      message['xml']['MsgType'] != None and
      message['xml']['MsgType'] == 'text' and
      message['xml']['Content'] != None
    )

#format the message asa accepted by wechat
  def format_message(self, original_message, content):
    return (
      "<xml>"
      "<ToUserName><![CDATA[%s]]></ToUserName>"
      "<FromUserName><![CDATA[%s]]></FromUserName>"
      "<CreateTime>%s</CreateTime>"
      "<MsgType><![CDATA[text]]></MsgType>"
      "<Content><![CDATA[%s]]></Content>"
      "</xml>"
    ) % (
      original_message['xml']['FromUserName'], # From and To must be inverted in replies ;)
      original_message['xml']['ToUserName'], # Same as above!
      time.gmtime(),
      content
    )


  def on_get(self, request, response):
    signature = request.get_param('signature')
    timestamp = request.get_param('timestamp')
    nonce = request.get_param('nonce')
    echostr = request.get_param('echostr')
    verification_elements = [self.token, timestamp, nonce]
    verification_elements.sort()
    verification_string = "".join(verification_elements)
    verification_string = hashlib.sha1(verification_string.encode('utf-8')).hexdigest()

    if signature == verification_string:
      response.status = falcon.HTTP_200
      response.body = echostr
    else:
      response.status = falcon.HTTP_500
      response.body = ""

  def on_post(self, request, response):
    message = xmltodict.parse(request.bounded_stream.read())
    if self.validate_message(message):
      reply = "%s" % (message['xml']['Content'])   #message sent by user
      repl=reply
      lc='en-US'
      for c in reply: 
          if (ord(c)>128): #check for message in chinese
              lc='zh-CN'
      session_client = dialogflow.SessionsClient()
      session = session_client.session_path("voiceonly-937a4", "12345")
      text_input = dialogflow.types.TextInput(
            text=repl, language_code=lc)  

      query_input = dialogflow.types.QueryInput(text=text_input)    #send the message to dialogflow

      respons = session_client.detect_intent(
            session=session, query_input=query_input)
      result = format(respons.query_result.fulfillment_text)   #response from dialogflow
      response.status = falcon.HTTP_200
      response.body = self.format_message(message, result)
    else:
      response.status = falcon.HTTP_200
      response.body = "Message was sent in a wrong format."

api = application = falcon.API()
api.add_route('/wechat', WeChatApiResource(WECHAT_TOKEN))

