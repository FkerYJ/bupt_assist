import os,sys
import os.path as path
sys.path.append(path.dirname(__file__))
import json as js
import shutil
from Log import log
pwd=path.dirname(path.dirname(path.abspath(__file__)))+"/Database/"# father directory

class Table:
  def __init__(self,tbname):
    self.name=tbname
    try: 
      fr=open(pwd+tbname+".json",encoding='utf-8')
      fs=fr.read()
      self.lines=js.loads(fs)
      fr.close()
    except:
      self.lines=list()
    try: 
      fr=open(pwd+tbname+".ukVals",encoding='utf-8')
      fs=fr.read()
      self.ukVals=js.loads(fs)
      self.ukeys=list(self.ukVals.keys())
      fr.close()
    except:
      self.ukeys=list()
      self.ukVals=dict()
    self._save()

  def set_ukey(self,keyX):
    if keyX in self.ukeys:
      log("Waring: ukey "+str(keyX)+" has been existed,Jump",1)
      return 1
    self.ukeys.append(keyX)
    self.ukVals[keyX]=list()
  def del_ukey(self,keyX):
    if keyX not in self.ukeys: return 1
    del self.ukVals[keyX]
    self.ukeys.remove(keyX)
  def show_ukey(self):
    return self.ukeys.copy()

  def find_one(self,fiter):
    '''
      adapt to find precise one with ukey
      while have many item, the earliest will be response 
    '''
    for x in self.lines:
      for key in fiter:
        if x[key]!=fiter[key]: break
      if x[key]!=fiter[key]: continue
      return x.copy()

  def _find_all(self,fiter):
    '''
      adapt for fuzzy lookup with some value
      return orgin line
    '''
    ret=list()
    for x in self.lines:
      flag=True
      for key in fiter:
        if x[key]!=fiter[key]: flag=False
      if flag:ret.append(x)
    return ret

  def find_all(self,fiter):
    "return copy of orgin line"
    ret=list()
    res=self._find_all(fiter)
    for x in res : ret.append(x.copy())
    return ret

  def update(self,fiter,newline):
    """If data existing,then Update it,else try to insert """
    items=self._find_all(fiter)
    if len(items)==0:
      self.insert(newline)
    if len(items)==1:
      items[0].update(newline)
      self._save()
    if len(items)>=2:
      raise ValueError("find Multiple eligible lines")
    return True

  def insert(self,dataX):
    keysX=dataX.keys()
    for ukey in self.ukeys:
      if ukey not in dataX or dataX[ukey]==None:
        raise Exception(f"ukey:{ukey} should't be empty")
      if dataX[ukey] in self.ukVals[ukey]:
        raise Exception(f"ukey:{ukey} has been existing")
    for ukey in self.ukeys:
      self.ukVals[ukey].append(dataX[ukey])
    self.lines.append(dataX)
    self._save()
    
  def remove(self,dataX):
    '''必须传入完整的数据才可删除'''
    for ukey in self.ukeys:
      self.ukVals[ukey].remove(dataX[ukey])
    self.lines.remove(dataX)
    self._save()
  
  def _save(self):
      fw=open(pwd+self.name+".json","w+",encoding='utf-8')
      js.dump(self.lines, fw,ensure_ascii=False,indent=2)
      fw.close()
      fw=open(pwd+self.name+".ukVals","w+",encoding='utf-8')
      js.dump(self.ukVals, fw,ensure_ascii=False,indent=4)
      fw.close()

  def _bak(self):
    # shutil.move()
    pass

class DataBase:
  def __init__(self,bufferTime=0):
    # print(os.getcwd())
    try: os.makedirs(pwd+"db")
    except:pass
    try:
      fr=open(pwd+"db/tbs.json")
      self.tbsIndex=js.load(fr)
      fr.close()
    except:self.tbsIndex=list()
    self.all=dict()
    for x in self.tbsIndex:
      self.all[x]=Table(x)
        
  def __getitem__(self, tbname):
    if tbname not in self.tbsIndex:
      log(f"Try to access unexisting table {tbname}",level=3)
      return None
    return self.all[tbname]

  def create(self,tbname):
    if tbname in self.tbsIndex:
      log("Waring:"+tbname+" has been existed,Jump")
      return self.all[tbname]
    self.all[tbname]=Table(tbname)
    self.tbsIndex.append(tbname)
    self._save()
    return self.all[tbname]

  def delete(self,tbname):
    if tbname not in self.tbsIndex:
      raise NameError("Try to delete unexisting table")
    self.tbsIndex.remove(tbname)
    self.all[tbname].delete()
    del self.all[tbname]
    self._save()

  def _save(self):
    fw=open(pwd+"db/tbs.json","w+",encoding='utf-8')
    js.dump(self.tbsIndex,fw,ensure_ascii=False)
    fw.close()

conn=DataBase()

if __name__ == '__main__':
  tb=conn.create("testTb")
  tb.update({"name":"wyj"},{"name":"wyj","id":2020222333})
  tb.set_ukey("id")
  print(tb.find_one({"name":"bd1"}))
  print("all: ",tb.find_all({}))
  tb=conn["user"]
  tb.update({"id":"2020211838"},{"name":"珠峰","role":"学生","id":"2020211838"})
  tb.update({"id":"2002211838"},{"name":"彭木","role":"教师"})
  tb=conn["user"]
  print("all: ",tb.find_all({}))
