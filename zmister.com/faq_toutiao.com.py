#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ovwane'
__time__ = '2017.12.28 14:36'


import time
import hashlib
#as和cp是用来提取和验证访问者页面停留时间的参数，cp对浏览器的时间进行了加密混淆，as通过md5来对时间进行验证。
"""
function(t) {
    var e = {};
    e.getHoney = function() {
        var t = Math.floor((new Date).getTime() / 1e3),
            e = t.toString(16).toUpperCase(),
            i = md5(t).toString().toUpperCase();
        if (8 != e.length) return {
            as: "479BB4B7254C150",
            cp: "7E0AC8874BB0985"
        };
        for (var n = i.slice(0, 5), a = i.slice(-5), s = "", o = 0; 5 > o; o++) s += n[o] + e[o];
        for (var r = "", c = 0; 5 > c; c++) r += e[c + 3] + a[c];
        return {
            as: "A1" + s + e.slice(-3),
            cp: e.slice(0, 3) + r + "E1"
        }
    },
"""

def get_as_cp():
    zz ={}
    now = round(time.time())
    e = hex(int(now)).upper()[2:]
    i = hashlib.md5(str(int(now)).encode("utf-8")).hexdigest().upper()
    if len(e)!=8:
        zz = {'as': "479BB4B7254C150",
            'cp': "7E0AC8874BB0985"}
        return zz
    n=i[:5]
    a=i[-5:]
    r = ""
    s = ""
    for i in range(5):
        s = s+n[i]+e[i]
    for j in range(5):
        r = r+e[j+3]+a[j]
    zz = {
            'as': "A1" + s + e[-3:],
            'cp': e[0:3] + r + "E1"
        }
    print(zz)
    return zz

get_as_cp()