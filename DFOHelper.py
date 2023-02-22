import sys
import os
import platform
import string
import codecs
from dumper import *

# use:
# warn(" debug: %s" % value["name"]) to print a value to debug window!!!
# warn(" debug: %s" % value["name"].string()) to print a char* value to debug window!!!
# warn(" debug: %s" % d.encodedUtf16ToUtf8(d.encodeString(value["IconName"], 255))) to print a QString value to debug window!!!

def svDebugInfo(value):
  f = open("/tmp/DebugInfo.txt","w")
  f.write(str(value))
  f.close()

def svDebugInfoToFile(value, fname):
  f = open(fname,"w")
  f.write(str(value))
  f.close()

def debugInfo():
  exinfo = sys.exc_info()
  ty,vl,tr = exinfo
  return "line:"+str(tr.tb_lineno)+ ";" + str(exinfo)

def toHexString(value):
  return str("{0:#x}".format(int(value)))

#TODO: encoding for windows-1251
def QStringValue(d, value, maxlen=255):
  return str(d.encodeStringUtf8(value, maxlen))
#not accessible on 1251: str(d.call(d.call(value, "toUtf8"),"constData").string())
#  return d.encodeStringUtf8(value, maxlen)
#  return d.encodedUtf16ToUtf8(d.encodeString(value, maxlen))

def DFOName(d, value):
  pinfo = value["d_ptr"]["wp"]["value"]
  typ = d.lookupType(d.qtNamespace() + "DFOPrivate")
  privateQInstance = d.createValue(d.extractPointer(pinfo), typ)
  if value["IconName"] == 0:
    iconname = "no icon"
  else:
    iconname = value["IconName"].string()
  return iconname + ":" + QStringValue(d, d.call(privateQInstance["m_finfo"], "absoluteFilePath"))

#value["Record"]["RecordName"].string() "UTF-8"

def qdump__DFO(d, value):
  try:
#first: get Private instance from QPointer<DFOPrivate> d_ptr;...
    pinfo = value["d_ptr"]["wp"]["value"]
    typ = d.lookupType(d.qtNamespace() + "DFOPrivate")
    privateInstance = d.createValue(d.extractPointer(pinfo), typ)

#    svDebugInfo(value["d_ptr"])
    retv = DFOName(d,value)
#    retv += str(privateInstance["m_mainStatusCode"])
#    retv += " ("+toHexString(value["key"])+") "
#    retv += str(value["IsCallSuccessful"])

    d.putValue(retv)

#    smopath = ""
#    parentSmo = value["m_parentSmo"]
#    while not d.isNull(parentSmo):
#      smopath = DFOName(d, parentSmo) + " / " + smopath
#      parentSmo = parentSmo["m_parentSmo"]
    

    d.putNumChild(1)
    if d.isExpanded():
      with Children(d):
        d.putSubItem(  "Private =",  privateInstance)
#	    d.putGenericItem("Smo path=", "debug", smopath)
        d.putFields(value)

  except RuntimeError:
    d.putValue(debugInfo())

def qdump__DeviceInfo(d, value):
  try:
    d.putValue(DFOName(d,value["m_deviceSmo"]))
    d.putPlainChildren(value)
  except RuntimeError:
    d.putValue(debugInfo())
    
def qdump__DFOPrivate(d, value):
  try:
    d.putPlainChildren(value)
  except RuntimeError:
    d.putValue(debugInfo())


#TODO:
#def qdump__QTreeWidgetItem(d, value):
#  try:
#    d.putValue("QTreeWidgetItem:"+str(value) + str(d))
#    d.putPlainChildren(value)
#  except RuntimeError:
#    d.putValue(debugInfo())
  
  
