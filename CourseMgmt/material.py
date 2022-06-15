import sys,os.path as path
sys.path.append(path.dirname(__file__))
sys.path.append(path.dirname(path.dirname(__file__)))
import Utils
from Utils.Time import datetime,timedelta
from Utils.DataFrame import *
from Utils.database import conn

"""The implementation principle of this module 
    is highly similar to hmwt module
    you could refer to detail annotation in homework.py/hmwt
"""
tbMaterial=conn.create("material")
tb=conn.create("userCourse")
tbCourse=conn.create("course")
tbMaterialRollBack=conn.create("materialRollBack")
################class_material##################
def list_class_material(classId=-1):
  """list all class when classId=-1"""
  if classId==-1:res=tbMaterial.find_all({})
  else:res=tbMaterial.find_all({"id":classId})
  return res,"这是所有的task"

def search_class_material(classId=-1,match="有限状态自动机"):
  """search all class_material when classId=-1"""
  if not tb.find_one({"id":classId,"userId":userId}):return -1,"该学生没有这门课"
  res=tb.find_all({"userId":userId})
  ret=list()
  for x in res:
    ret.extend(tbCourse.find_one({"id":x["id"]}))
  return ret,"返回的是课程的list"

def view_material(materialId):
  """return all version """
  res=tbMaterial.find_one({"materialId":materialId})
  return res,"已返回该material"

def rollback_class_material(materialId,version):
  """恢复到历史版本"""
  res=tbMaterialRollBack.find_one({"materialId":materialId,"version":version})
  if not res:return 0,"不存在该版本"
  tbMaterial.update({"materialId":materialId},res)
  return

def create_class_material(classId,data):
  """
  data={
    "title":"课件1",
    "descript":"the ppt of the first chapter",
    "attachId":2435,
  }
  "classId":
  "materialId"
  """
  res=tbMaterial.find_all({})
  data["id"]=classId
  data["materialId"]=len(res)+1
  data["version"]=0
  tbMaterial.insert(data)
  return len(res)+1,"已经创建资料"

def update_class_material(materialId,data):
  "refer to the descript of update_hmwk"
  res=tbMaterial.find_one({"materialId":materialId})
  if not res:return 0,"materialId错误"
  data["version"]=res["version"]+1
  tbMaterialRollBack.update({"materialId":materialId,"version":res["version"]},res)
  tbMaterial.update({"materialId":materialId},data)
  return data["version"],"已更新资料"

def delete_class_material(materialId):
  res=tbMaterial.find_one({"materialId":materialId})
  tbMaterial.remove(res)
  ret=tbMaterialRollBack.find_all({"materialId":materialId})
  for x in range(len(ret)):
    tbMaterialRollBack.remove(ret[x])
  return 1,"已删除资料"

if __name__ == "__main__":
  data1={
    "title":"课件1",
    "descript":"the ppt of the first chapter",
    "attachId":2435,
  }
  data2={
    "title":"课件2",
    "descript":"the ppt of the second chapter",
    "attachId":2436,
  }
  data3={
     "title":"课件1",
    "descript":"the ppt",
    "attachId":2437,
  }
  create_class_material(12, data1)
  create_class_material(12, data2)
  create_class_material(13, data3)
  print("12: ",list_class_material(12))
  print("13: ",list_class_material(13))
  print("material1: ",view_material(1))
  data4={
    "title":"课件4",
    "descript":"the ppt of the 4 chapter",
    "attachId":2438,
  }
  update_class_material(1, data4)
  print("12: ",list_class_material(12))
  delete_class_material(2)
  print("12: ",list_class_material(12))
