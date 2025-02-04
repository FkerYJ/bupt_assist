from flask import Blueprint
import os,sys,os.path as path
import json as js
from flask import request,redirect,make_response,send_file
from Utils.user import vrfSession
from Control.rpc.webrpc import rjs
from Utils import File as File

filedir=path.join(path.dirname(__file__),"../../Upload/tmp/")

api = Blueprint('file_api', __name__)
@api.route('/api/file/down',methods=['POST','GET'])
def down_file():
    try:
      data =dict(request.form)
      fileid=data['id']
    except Exception as e:
      fileid=0
    filepath=File.getFile(fileid)
    return send_file(filepath,as_attachment=True)

@api.route('/api/file/upload',methods=['POST','GET'])
def update_file():
    data = request.form
    file=request.files.get("file.raw")
    try:
        data =dict(data)
    except:
      return rjs(400,"无效请求")
    if not "session" in data:
      return rjs(400,"参数缺失")
    userid=vrfSession(data['session'])
    if not userid:
      return rjs(-1,"登录失效")
    if  file:
      filepwd=filedir+file.filename
      file.save(filepwd)
      fileid=File.saveFile(filepwd)
      return rjs(1,fileid)
    else:return rjs(2,"未上传作业文件")