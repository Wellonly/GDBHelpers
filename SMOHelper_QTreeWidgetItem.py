import sys
import os
import platform
import string
from dumper import *

# use:
# warn("debug: %s" % value["name"]) to print a value to debug window!!!
# warn("debug: %s" % value["name"].string()) to print a char* value to debug window!!!
# warn("debug: %s" % d.encodedUtf16ToUtf8(d.encodeString(value["IconName"], 48))) to print a QString value to debug window!!!

def svDebugInfo(value):
    f = open("/tmp/debugInfo.txt","w")
    f.write(str(value))
    f.close()

def debugInfo():
    exinfo = sys.exc_info()
    ty,vl,tr = exinfo
    return "line:"+str(tr.tb_lineno)+ ";" + str(exinfo)

#  d.putValue('(0x%x)' % value)
def toHexString(value):
  return str("{0:#x}".format(int(value)))

#TODO: encoding for windows-1251
def SMOName(d, value):
  return d.encodedUtf16ToUtf8(d.encodeString(value["m_shortName"], 48))
#svDebugInfo("str:%s" % d.encodedUtf16ToUtf8(d.encodeString(value["m_shortName"], 48)))
#value["Record"]["RecordName"].string() "UTF-8"

# available for a value...
#    retv += str(parentSmo.integer())
#    retv += str(parentSmo.pointer())
#    retv += str(parentSmo.address())
#    retv += str(parentSmo.dereference())

def BoolValueToStr(value):
  if value == 0:
    return "false"
  return "true"

def putGenericItem(d, name, value):
  with SubItem(d, name):
    d.putValue(value)
    d.putType("generic")
    d.putNumChild(0)

# to hex only...
def qdump__smokey(d, value):
  d.putValue('(0x%x)' % value)
  d.putNumChild(0)

# to hex only...
def qdump__smoKey(d, value):
  d.putValue('(0x%x)' % value)
  d.putNumChild(0)

def qdump__SMO(d, value):
  try:
    retv = SMOName(d,value)
    retv += " ("+toHexString(value["key"])+") "
    retv += BoolValueToStr(value["IsCallSuccessful"].integer())
    d.putValue(retv)

    smopath = ""
    parentSmo = value["m_parentSmo"]
    while parentSmo.integer() > 0:
      smopath = SMOName(d, parentSmo) + " / " + smopath
      parentSmo = parentSmo["m_parentSmo"]

    devinfo = value["deviceInfo"]["wp"]["value"]
    typ = d.lookupType(d.qtNamespace() + "DeviceInfo")
    devInfoInstance = d.createValue(d.extractPointer(devinfo), typ)

    d.putNumChild(1)
    if d.isExpanded():
      with Children(d):
        d.putSubItem("Device  =",  devInfoInstance)
        putGenericItem(d,"Smo path=", smopath)
        d.putFields(value)

  except RuntimeError:
    d.putValue(debugInfo())


def qdump__DeviceInfo(d, value):
  try:
    d.putValue(SMOName(d,value["m_deviceSmo"]))
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
  
  
