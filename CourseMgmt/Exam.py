"""The implementation principle of this module 
    is highly similar task
    you could refer to detail annotation in homework.py/task
"""
import sys,os.path as path
sys.path.append(path.dirname(path.dirname(__file__)))
import Utils
from Utils.Log import *
from Utils.Time import *
from Utils.DataFrame import *
from Utils.database import conn
from Utils.Cfg import cfg

tbExam=conn.create("exam")
tb=conn.create("userCourse")
tbCourse=conn.create("course")
###########exam###########
def list_class_exam(classId=-1):
  """list all class when classId=-1"""
  if classId==-1:res=tbExam.find_all({})
  else:res=tbExam.find_all({"classId":classId})
  log("list_class_exam:class="+str(classId),0)
  return res,"这是所有的exam"

def search_class_exam(userId,classId=-1,match="有限状态自动机"):
  """search all class_task when classId=-1"""
  if not tb.find_one({"id":classId,"userId":userId}):return -1,"该学生没有这门课"
  res=tb.find_all({"userId":userId})
  ret=list()
  for x in res:
    ret.extend(tbCourse.find_one({"id":x["id"]}))
  log("search_class_task",0)
  return ret,"返回的是课程的list"


def list_user_exam(userId):
  """
  ret= {
   "1":{"title":"期末考试", "持续时间":2,"教学楼":"n3多功能","教室":108, "classId":24,"examId":234,} ,
   "2":{} ,
  }
  """
  res=tb.find_all({"userId":userId})
  ret=list()
  for x in res:
    temp=list_class_exam(x["id"])
    ret.extend(temp[0])
  log("list_user_exam:user="+userId,0)
  return

def search_user_exam(userId):
  #ret={}
  if not tb.find_one({"id":classId,"userId":userId}):return -1,"该学生没有这门课"
  res=tb.find_all({"userId":userId})
  ret=list()
  for x in res:
    ret.extend(tbCourse.find_one({"id":x["id"]}))
  log("search_class_exam",0)
  return ret,"返回的是课程的list"

def create_class_exam(classId,data):
  '''parameter data will be a dict,contain key
  name, des, attentionId,Deadline
  the func return taksId
  '''
  res=tbExam.find_all({})
  data["classId"]=classId
  data["examId"]=len(res)+1
  tbExam.insert(data)
  log("create_class_exam:class="+str(classId),0)
  """
  data={
    "title":
    "开始时间"：
    "持续时间":
    "教学楼":
    "教室":
  }
    "classId":
    "examId":
  """
  return len(res)+1,"已经创建task"

def view_exam(examId):
  '''return a dict contain key same as "create_task" '''
  res=tbExam.find_one({"examId":examId})
  log("view_task:exam="+str(examId),0)
  ret=list()
  ret.append(res)
  return ret,"已返回该exam"

if __name__ == "__main__":
  data1={
    "title":"期中考试",
    "开始时间":str(now()),
    "持续时间":60,
    "教学楼":"n3",
    "教室":305,
  }
  data2={
    "title":"期末考试",
    "开始时间":str(now()),
    "持续时间":90,
    "教学楼":"n3",
    "教室":303,
  }
  data3={
    "title":"期中考试",
    "开始时间":str(now()),
    "持续时间":90,
    "教学楼":"n3",
    "教室":304,
  }
  create_class_exam(12, data1)
  create_class_exam(12, data2)
  create_class_exam(13, data3)
  print("12: ",list_class_exam(12))
  print("13: ",list_class_exam(13))
  print("2020211839: ",list_user_exam("2020211839"))
  print("task1: ",view_exam(1))
