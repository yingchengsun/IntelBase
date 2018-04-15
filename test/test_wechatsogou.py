# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import os
import unittest

from nose.tools import assert_equal, assert_true, assert_in, assert_greater_equal

from wechatsogou.const import WechatSogouConst
from wechatsogou.api import WechatSogouAPI
from wechatsogou.identify_image import identify_image_callback_by_hand
from test import gaokao_keyword
from test.rk import identify_image_callback_ruokuai_sogou, identify_image_callback_ruokuai_weixin

ws_api = WechatSogouAPI(captcha_break_time=3)

# 直连
ws_api = WechatSogouAPI()
# 验证码输入错误的重试次数，默认为1
ws_api = WechatSogouAPI(captcha_break_time=3)

# 配置代理，代理列表中至少需包含1个 HTTPS 协议的代理, 并确保代理可用
ws_api = WechatSogouAPI(proxies={
    "http": "127.0.0.0.1:8888",
    "https": "127.0.0.0.1:8888",
})



ws_api =WechatSogouAPI()
ws_api.get_gzh_info('南航青年志愿者')

