#-*- coding: utf-8 -*-
import base64
import hmac
import hashlib
import random

from app.models import *

def random_str(length):
    chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    code = ""
    for i in range(0, length):
        index = random.randint(0, len(chars) - 1)
        code = code + chars[index]
    return code

def generate(app, length):
    code = random_str(length)

    try:
        invite_code = InviteCode.objects.get(code=code, app=app)
        generate(app, length)
    except Exception as e:
        return code

def check_sig(request):
    params = None
    if request.method == 'POST':
        params = request.POST
    elif request.method == 'GET':
        params = request.GET
    params = params.dict()

    if not params.has_key('sig'):
        msg = {"code":"2002", "desc":"签名参数不存在"}
        return False, msg

    try:
        appid = params['appid']
        sig = params['sig']
        app = App.objects.get(appid=appid)

        params = sorted(params.items(), lambda x, y : cmp(x[0], y[0]))
        origin_str = ""
        
        index = 0
        for pair in params:
            index = index + 1

            if not pair[0] == 'sig':
                origin_str = origin_str + "%s=%s" % (pair[0], pair[1])
                if index < len(params):
                    origin_str = origin_str + "&"

        hmac_str = hmac.new(app.access.encode('utf-8'), origin_str, digestmod=hashlib.sha1).hexdigest()

        mysig = base64.b64encode(hmac_str)
        if sig == mysig:
            return True, {"code":"1000", "desc":""}
        else:
            return False, {"code":"2002", "desc":"签名错误"}
    except Exception as e:
        print e

        msg = {"code":"2001", "desc":"应用不存在"}
        return False, msg
