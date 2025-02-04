from flask import Blueprint
import os,sys,os.path as path
import json as js
from flask import request,redirect,make_response
from Utils.user import vrfSession
from Utils import File 
from Control.rpc.webrpc import rjs
from CourseMgmt import homework as hmwk


api = Blueprint('hmwk_api', __name__)
@api.route('/api/hmwk/list',methods=['POST','GET'])
def list_hwmk():
    data = request.get_data()
    try:
        data = js.loads(data)
    except:
      return rjs(400,"无效请求")
    if not "session" in data:
      return rjs(400,"参数缺失")
    userid=vrfSession(data['session'])
    if not userid:
      return rjs(-1,"登录失效")
    if  "classid" in data:
       classid=data['classid']
    data,msg=hmwk.list_user_task(userid)
    return rjs(1,data)


@api.route('/api/hmwk/update',methods=['POST','GET'])
def update_hwmk():
    data = request.form
    try:
        data =dict(data)
    except:
      return rjs(400,"无效请求")
    if not "session" in data:
      return rjs(400,"参数缺失")
    userid=vrfSession(data['session'])
    if not userid:
      return rjs(-1,"登录失效")
    del data['session']
    data['userId']=userid
    data['taskId']=int(data['taskId'])
    id,msg=hmwk.update_hmwk(data)
    print(rjs(id,msg))
    return rjs(id,msg)

@api.route('/api/hmwk/view',methods=['POST','GET'])
def view_hwmk():
    data =request.get_data()
    try:
        data = js.loads(data)
    except:
      return rjs(400,"无效请求")
    if not "session" in data:
      return rjs(400,"参数缺失")
    userid=vrfSession(data['session'])
    if not userid:
      return rjs(-1,"登录失效")
    del data['session']
    data['userId']=userid
    data,msg=hmwk.view_hmwk(userid,int(data['taskId']))
    return rjs(1,data)
