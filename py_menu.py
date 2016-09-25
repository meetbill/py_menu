#!/usr/bin/python
#encoding=utf-8

import traceback, os, re, time, sys, getopt
from snack import * #导入图形界面
from mylib.snack_lib import *


def usage():
  print "<使用方法>"
  print "-h 本帮助"
def warwindows(screen, title, text, help = None):
    #警告窗口
    btn = Button("确定")
    war = GridForm(screen, title, 1, 15)
    war.add(Label(text),0,1)
    war.add(Label(""),0,2)
    war.add(btn, 0, 3)
    war.runOnce(35,10)

def conformwindows(screen, text, help = None):
    #确认窗口
    bb = ButtonBar(screen, (("确定", "yes"), ("取消", "no")),compact = 1)
    g = GridForm(screen, text, 20, 16)
    g.add(Label(text),0,2)
    g.add(bb,0,3,(10,0,10,0), growx = 1)
    re = g.runOnce(43, 8)
    return (bb.buttonPressed(re), re)

def sc():
#刷新屏幕
    global screen
    screen = SnackScreen()
    screen.finish()
    screen = SnackScreen()
    screen.setColor("ROOT", "white", "blue")
    screen.setColor("ENTRY","white","blue")
    screen.setColor("LABEL","black","white")
    screen.setColor("HELPLINE","white","blue")
    screen.setColor("TEXTBOX","black","yellow")

def QUIT():
#调用退出到命令行，输入exit返回
    buttons = ("是", "否")
    bb = ButtonBar(screen, buttons)
    g = GridForm(screen, "返回登陆界面？" , 20,16)
    g.add(bb,1,3,(10,0,10,0), growx = 1)
    rq = g.runOnce(32,8)
    screen.popWindow()
    if rq == "ESC" or bb.buttonPressed(rq) == "否":
        screen.finish()
        return mainform()
    else:
        screen.finish()
        return

# 一级menu
def mainform():
#主界面
    #刷新屏幕
    sc()
    # 主memu菜单项位置
    global mainl
    global adpl
    adpl = 1
    li = Listbox(height = 15, width = 18, returnExit = 1, showCursor = 0)
    li.append("a)一级目录1", 1)
    li.append("b)一级目录2", 2)
    li.append("c)一级目录3", 3)
    li.setCurrent(mainl)
  
    bb = CompactButton('|->退出<-|')
    g = GridForm(screen, "manager", 1, 10)
    g.add(li, 0, 1)
    g.add(bb, 0, 2)
    g.add(Label(" "),0,3)
    g.add(Label("[管理利器]"),0,4)

    screen.pushHelpLine("<Version 1.0.1> Powered by Billwang139967...请使用TAB在选项间切换")
    rc=g.run(1,3)
    mainl = li.current()
    if rc == 'ESC' or 'snack.CompactButton' in str(rc) :
        return QUIT()
    if li.current() == 1:
        return secondary_menu()
    elif li.current() == 2:
        return secondary_menu()
    elif li.current() == 3:
        return secondary_menu()

# 第二层menu
def secondary_menu():
  global adpl
  re = []
  li = Listbox(height = 15, width = 14, returnExit = 1, showCursor = 0)
  n = 0
  n1 = 1
  bb = CompactButton('返回')
  li.append("a)二级目录1", 1)
  li.append("b)二级目录2", 2)
  h = GridForm(screen, "请选择", 1, 16)
  li.setCurrent(adpl)
  h.add(li, 0, 1)
  h.add(bb, 0, 9)
  rc = h.run(24,3)
  if "snack.CompactButton" in str(rc) or rc == 'ESC':
    return mainform()
  else :
    adpl = li.current()
    num = str(li.current() - 1)
    if li.current() == 1:
      return three_menu()
    if li.current() == 2:
      return three_menu()

# 三级menu
def three_menu():
     m = Mask(screen, "test_windows", 35 )
     m.text("label_test0","ceshi_text")
     m.entry( "label_test1", "entry_test1", "0" )
     m.entry( "label_test2", "entry_test2", "0" )
     m.entry( "label_test3", "entry_test3", "127.0.0.1" )
     m.checks( "复选框","checks_list",[
         ('checks_name1','checks1',0),
         ('checks_name2','checks2',0),
         ('checks_name3','checks3',0),
         ('checks_name4','checks4',1),
         ('checks_name5','checks5',0),
         ('checks_name6','checks6',0),
         ('checks_name7','checks7',0),
     ],
     height= 5
     )    
     m.radios( "单选框","radios", [ 
         ('radios_name1','radios1', 0), 
         ('radios_name2','radios2', 1), 
         ('radios_name3','radios3', 0) ] )  
     
     m.buttons( yes="Sava&Quit", no="Quit" )
     (cmd, results) = m.run(43,3)
     if cmd == "yes":
        rx = conformwindows(screen, "确认操作")
        if rx[0] == "yes" or rx[1] == "F12":
            return secondary_menu()
        else:
            return secondary_menu()
     else:
        return secondary_menu()

def main():
  try:
    mainform()
  except Exception,e:
    screen.finish()
    print e
    print traceback.format_exc()
  finally:
    screen.finish()
    print "感谢使用！"
    return ''

mainl = 1
adpl = 1
try:
  if len(sys.argv) > 1:
    opts, args = getopt.getopt(sys.argv[1:], "h")
    for op, value in opts:
      if op == "-h":
        usage()
        sys.exit()
  main()
except Exception,e:
  print e
  print "指定的参数无效"
  usage()
