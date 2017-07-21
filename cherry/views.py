# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import urllib
import re
import time
from django.core import serializers
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, render_to_response
from cherry import models as crm
from market import models as mkm

# Create your views here.


@login_required()
def get_index_html(request):
    return render(request, "cherry/index.html")


@login_required()
def get_market_html(request):
    return render(request, "cherry/market.html", locals())


@login_required()
def get_user_html(request):
    return render(request, "cherry/user.html", locals())


@login_required()
def get_order_html(request):
    return render(request, "cherry/order.html", locals())


def get_symbol_data(request):
    symbol_obj_list = mkm.Symbol.objects.filter(enabled=True)
    symbol_list = []
    for i in symbol_obj_list:
        symbol=i.toJSON()
        symbol["creater"]=i.creater.name
        symbol_list.append(symbol)
    return JsonResponse({"data":symbol_list})


@login_required()
def set_symbol_data(request):
    if request.method == "POST":
        my_post = urllib.unquote(request.body)
        action = request.POST.get('action')
        id = re.findall(r"&data\[(\d*?)]\[name]", my_post)[0]
        name = request.POST.get('data[' + id + '][name]')
        refresh = request.POST.get('data[' + id + '][refresh]')
        description = request.POST.get('data[' + id + '][description]')
        #print action
        #print my_post
        if action == "create":
            try:
                symbol_obj = mkm.Symbol.objects.create(
                    name=name,
                    refresh=refresh,
                    description=description,
                    creater=mkm.UserProfile.objects.get(id=request.user.id),
                    enabled=True
                )
                symbol_obj.save()
                symbol=symbol_obj.toJSON()
                symbol["creater"]=symbol_obj.creater.name
                return JsonResponse({"data": [symbol]})
            except Exception as e:
                print "Create Symbol fail, ", e
                return JsonResponse({"data": []})
        else:
            pass
        if action == "edit":
            try:
                symbol_obj = mkm.Symbol.objects.get(id=id)
                symbol_obj.name = name
                symbol_obj.refresh = refresh
                symbol_obj.description = description
                symbol_obj.save()
                symbol=symbol_obj.toJSON()
                symbol["creater"]=symbol_obj.creater.name
                return JsonResponse({"data": [symbol]})
            except Exception as e:
                print "Edit Symbol fail, ", e
                return JsonResponse({"data": []})
        else:
            pass
        if action == "remove":
            try:
                symbol_obj = mkm.Symbol.objects.get(id=id)
                symbol_obj.enabled = False
                symbol_obj.save()
                return get_symbol_data(request)
            except Exception as e:
                print "Delete Symbol fail, ", e
                return JsonResponse({"data": []})
        else:
            pass
    else:
        
        return JsonResponse({"data": []})

def get_platform_data(request):
    symbol_id = request.POST.get("symbol")
    if symbol_id:
        pass
    else:
        return JsonResponse({"data":[]})
    platform_obj_list = mkm.Platform.objects.filter(symbol_id=symbol_id).filter(enabled=True)
    platform_list = []
    for i in platform_obj_list:
        platform = i.toJSON()
        platform["creater"] = i.creater.name
        platform["symbol"] = i.symbol.name
        platform_list.append(platform)
    return JsonResponse({"data":platform_list})

        
        
def set_platform_data(request):
    if request.method == "POST":
        my_post = urllib.unquote(request.body)
        action = request.POST.get('action')        
        id = re.findall(r"&data\[(\d*?)]\[name]", my_post)[0]
        symbol = request.POST.get('data[' + id + '][symbol]')
        name = request.POST.get('data[' + id + '][name]')
        home = request.POST.get('data[' + id + '][home]')
        url = request.POST.get('data[' + id + '][url]')
        xpath = request.POST.get('data[' + id + '][xpath]')
        refresh = request.POST.get('data[' + id + '][refresh]')
        description = request.POST.get('data[' + id + '][description]')
        #print action
        #print my_post
        if action == "create":
            try:
                platform_obj = mkm.Platform.objects.create(
                    symbol=mkm.Symbol.objects.get(id=symbol),
                    name=name,
                    home=home,
                    url=url,
                    xpath=xpath,
                    refresh=refresh,
                    description=description,
                    creater=mkm.UserProfile.objects.get(id=request.user.id),
                    enabled=True
                )
                platform_obj.save()
                platform = platform_obj.toJSON()
                platform["creater"] = platform_obj.creater.name
                platform["symbol"] = platform_obj.symbol.name
                return JsonResponse({"data": [platform]})
            except Exception as e:
                print "Create Platform fail, ", e
                return JsonResponse({"data": []})
        else:
            pass
        if action == "edit":
            try:
                platform_obj = mkm.Platform.objects.get(id=id)
                platform_obj.symbol = mkm.Symbol.objects.get(id=symbol)
                platform_obj.name = name
                platform_obj.home = home
                platform_obj.url = url
                platform_obj.xpath = xpath
                platform_obj.refresh = refresh
                platform_obj.description = description
                platform_obj.save()
                platform = platform_obj.toJSON()
                platform["creater"] = platform_obj.creater.name
                platform["symbol"] = platform_obj.symbol.name
                return JsonResponse({"data": [platform]})
            except Exception as e:
                print "Edit Platform fail, ", e
                return JsonResponse({"data": []})
        else:
            pass
        if action == "remove":
            try:
                platform_obj = mkm.Platform.objects.get(id=id)
                platform_obj.refresh = False
                platform_obj.enabled = False
                platform_obj.save()
                return get_platform_data(request)
            except Exception as e:
                print "Delete Platform fail, ", e
                return JsonResponse({"data": []})
        else:
            pass
    else:
        
        return JsonResponse({"data": []})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print username, password
        user = auth.authenticate(username=username, password=password)
        print "user", user
        if user is not None:
            try:
                auth.login(request, user)
                request.session.set_expiry(60 * 60 * 24 * 7)
                print 'session expires at :', request.session.get_expiry_date()
                return HttpResponseRedirect('/index/')
            except ObjectDoesNotExist:
                return render(request, 'cherry/login.html',
                              {'login_err': u"Account not exist ! Pls retry or contact administrator!!"})
        else:
            return render(request, 'cherry/login.html', {'login_err': 'Wrong username or password!'})
    else:
        return render(request, 'cherry/login.html')
