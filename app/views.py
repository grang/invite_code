#-*- coding: utf-8 -*-
from django.shortcuts import render

from app.models import *
from app import utils

from django.shortcuts import render_to_response
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def test(request):
    return HttpResponse("OK")

def get_code(request):
    uid = request.GET.get('uid').encode('utf-8')
    appid = request.GET.get('appid')
    sig = request.GET.get('sig')

    ok, msg = utils.check_sig(request)
    if ok:
        try:
            invite_code = InviteCode.objects.get(uid=uid)

            msg = {"code":"1000", "desc":invite_code.code}
            return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
        except Exception as e:
            # generate code
            app = App.objects.get(appid=appid)
            code = utils.generate(app, settings.CODE_LENGTH)

            invite_code = InviteCode(uid=uid, code=code, app=app)
            invite_code.save()
            
            msg = {"code":"1000", "desc":invite_code.code}
            return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
    else:
        return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))

def is_code_enable(request):
    uid = request.GET.get('uid').encode('utf-8')
    code = request.GET.get('code').encode("utf-8")
    appid = request.GET.get('appid')
    
    ok, msg = utils.check_sig(request)
    if ok:
        app = App.objects.get(appid=appid)
        try:
            invite_echo = InviteEcho.objects.get(app=app, echo_uid=uid)

            msg = {"code":"2003", "desc":"该用户已经响应过别人的邀请了"}
            return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
        except Exception as e:
            try:
                invite_code = InviteCode.objects.get(code=code, app=app)

                if invite_code.uid == uid:
                    msg = {"code":"2005", "desc":"不能使用自己的邀请码"}
                    return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
                else:
                    msg = {"code":"1000", "desc":"邀请码可以使用"}
                    return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
            except Exception as e:
                msg = {"code":"2004", "desc":"非法的邀请码"}
                return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
    else:
        return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
    

def use_code(request):
    uid = request.GET.get('uid').encode('utf-8')
    code = request.GET.get('code').encode("utf-8")
    appid = request.GET.get('appid')
    
    ok, msg = utils.check_sig(request)
    if ok:
        app = App.objects.get(appid=appid)
        try:
            invite_echo = InviteEcho.objects.get(app=app, echo_uid=uid)

            msg = {"code":"2003", "desc":"该用户已经响应过别人的邀请了"}
            return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
        except Exception as e:
            try:
                invite_code = InviteCode.objects.get(code=code, app=app)

                if invite_code.uid == uid:
                    msg = {"code":"2005", "desc":"不能使用自己的邀请码"}
                    return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
                else:
                    echo = InviteEcho(uid=invite_code.uid, echo_uid=uid, app=app)
                    echo.save()

                    msg = {"code":"1000", "desc":"邀请响应成功"}
                    return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
            except Exception as e:
                msg = {"code":"2004", "desc":"非法的邀请码"}
                return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
    else:
        return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))

def get_echos(request):
    uid = request.GET.get('uid').encode('utf-8')
    appid = request.GET.get('appid')

    types = 0
    if request.GET.has_key('type'):
        types = request.GET.get('type')

    ok, msg = utils.check_sig(request)
    if ok:
        app = App.objects.get(appid=appid)
        if types == '1':
            results = InviteEcho.objects.filter(read_statu=0, app=app, uid=uid)
        else:
            results = InviteEcho.objects.filter(app=app, uid=uid)
        
        msg = []
        for result in results:
            msg.append(result.to_json())
        return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
    else:
        return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))

def write_statu(request):
    uid = request.GET.get('uid').encode('utf-8')
    appid = request.GET.get('appid')

    ok, msg = utils.check_sig(request)
    if ok:
        app = App.objects.get(appid=appid)
        results = InviteEcho.objects.filter(read_statu=0, app=app, uid=uid)
        
        for result in results:
            result.read_statu = 1
            result.save()

        msg = {"code":"1000", "desc":"完成状态变化"}
        return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
    else:
        return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))

def is_active(request):
    uid = request.GET.get('uid').encode('utf-8')
    appid = request.GET.get('appid')

    ok, msg = utils.check_sig(request)
    if ok:
        try:
            app = App.objects.get(appid=appid)
            results = InviteEcho.objects.get(app=app, echo_uid=uid)

            msg = {"code":"1001", "desc":"接受过别人邀请"}
            return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
        except Exception as e:
            msg = {"code":"1000", "desc":"没有接受过邀请"}
            return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
    else:
        return HttpResponse(json.dumps(msg, ensure_ascii=False, indent=4))
    
