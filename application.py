#coding:utf-8
#author:the5fire
from urls import urls
from model import uimodules

import tornado.web
import os

SETTINGS=dict(
	template_path=os.path.join(os.path.dirname(__file__),"templates"),
	static_path=os.path.join(os.path.dirname(__file__),"static"),
	ui_modules=uimodules
	)

application=tornado.web.Application(handlers=urls,**SETTINGS)
