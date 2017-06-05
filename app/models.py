#-*- coding: utf-8 -*-
from django.db import models

import datetime, pytz
import json

from django.utils.timezone import utc
from django.conf import settings

# Create your models here.
STATE = {(0, '上线'), (1, '下线')}
class App(models.Model):
    appid = models.AutoField(primary_key=True, verbose_name="应用ID")
    access = models.CharField(max_length=16, verbose_name="访问KEY")
    secret = models.CharField(max_length=16, verbose_name="秘钥")
    
    title = models.CharField(max_length=64, verbose_name="标题")
    
    state = models.PositiveSmallIntegerField(default=0, choices=STATE, verbose_name="状态")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "应用"

class InviteCode(models.Model):
    uid = models.CharField(max_length=64, verbose_name="用户ID")
    code = models.CharField(max_length=16, verbose_name="邀请码")
    app = models.ForeignKey(App, verbose_name="所属应用")

    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "邀请码"

READ_STATE = {(0, '未读'), (1, '已读')}
class InviteEcho(models.Model):
    uid = models.CharField(max_length=64, verbose_name="用户ID")
    echo_uid = models.CharField(max_length=64, verbose_name="相应的用户")
    
    read_statu = models.PositiveSmallIntegerField(default=0, choices=READ_STATE, verbose_name="状态")
    app = models.ForeignKey(App, verbose_name="所属应用")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def to_json(self):
        keys = ['uid', 'echo_uid', 'read_statu']

        msg = {}
        for key in keys:
            msg[key] = getattr(self, key)
        return msg

    class Meta:
        verbose_name = "邀请响应"
    
