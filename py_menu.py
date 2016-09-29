#!/usr/bin/python
#encoding=utf-8

import traceback, os, re, time, sys, getopt
from snack import * #导入图形界面
from mylib.snack_lib import *
from mylib.BLog import Log


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

class Menu_tool:
    def __init__(self):
        debug=False
        logpath = "/var/log/menu_tool/acc.log"
        self.logger = Log(logpath,level="debug",is_console=debug, mbs=5, count=5)
        self.screen = SnackScreen()
        self.screen.setColor("ROOT", "white", "blue")
        self.screen.setColor("ENTRY","white","blue")
        self.screen.setColor("LABEL","black","white")
        self.screen.setColor("HELPLINE","white","blue")
        self.screen.setColor("TEXTBOX","black","yellow")
        self.screen.pushHelpLine("<Version 1.0.2> Powered by Billwang139967...请使用TAB在选项间切换")

    def main(self):
      try:
        self.first_menu()
      except Exception,e:
        self.screen.finish()
        print e
        print traceback.format_exc()
      finally:
        self.screen.finish()
        print "感谢使用！"
        return ''
    
    def QUIT(self):
    #调用退出到命令行，输入exit返回
        buttons = ("是", "否")
        bb = ButtonBar(self.screen, buttons)
        g = GridForm(self.screen, "返回登陆界面？" , 20,16)
        g.add(bb,1,3,(10,0,10,0), growx = 1)
        rq = g.runOnce(32,8)
        self.screen.popWindow()
        if rq == "ESC" or bb.buttonPressed(rq) == "否":
            return self.first_menu()
        else:
            self.screen.finish()
            return

    def first_menu(self):
    #主界面
        # 主memu菜单项位置
        global mainl
        global adpl
        self.screen = SnackScreen()
        self.screen.finish()
        self.screen = SnackScreen()
        self.screen.setColor("ROOT", "white", "blue")
        self.screen.setColor("ENTRY","white","blue")
        self.screen.setColor("LABEL","black","white")
        self.screen.setColor("HELPLINE","white","blue")
        self.screen.setColor("TEXTBOX","black","yellow")
        self.screen.pushHelpLine("<Version 1.0.2> Powered by Billwang139967...请使用TAB在选项间切换")
        adpl = 1
        li = Listbox(height = 15, width = 18, returnExit = 1, showCursor = 0)
        li.append("a)一级目录1", 1)
        li.append("b)一级目录2", 2)
        li.append("c)一级目录3", 3)
        li.setCurrent(mainl)
      
        bb = CompactButton('|->退出<-|')
        g = GridForm(self.screen, "manager", 1, 10)
        g.add(li, 0, 1)
        g.add(bb, 0, 2)
        g.add(Label(" "),0,3)
        g.add(Label("[管理利器]"),0,4)

        rc=g.run(1,3)
        mainl = li.current()
        if rc == 'ESC' or 'snack.CompactButton' in str(rc) :
            return self.QUIT()
        if li.current() == 1:
            return self.secondary_menu()
        elif li.current() == 2:
            return self.secondary_menu()
        elif li.current() == 3:
            return self.secondary_menu()

    # 第二层menu
    def secondary_menu(self):
        global adpl
        re = []
        li = Listbox(height = 15, width = 14, returnExit = 1, showCursor = 0)
        n = 0
        n1 = 1
        bb = CompactButton('返回')
        li.append("a)二级目录1", 1)
        li.append("b)二级目录2", 2)
        h = GridForm(self.screen, "请选择", 1, 16)
        li.setCurrent(adpl)
        h.add(li, 0, 1)
        h.add(bb, 0, 9)
        rc = h.run(24,3)
        #print str(rc)
        if "snack.CompactButton" in str(rc) or rc == 'ESC':
            return self.first_menu()
        else :
            adpl = li.current()
            num = str(li.current() - 1)
            if li.current() == 1:
                return self.three_menu()
            if li.current() == 2:
                return self.three_menu()

    # 三级menu
    def three_menu(self):
         m = Mask(self.screen, "test_windows", 35 )
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
         
         self.logger.debug(str(cmd)+str(results))
         if cmd == "yes":
            rx = conformwindows(self.screen, "确认操作")
            if rx[0] == "yes" or rx[1] == "F12":
                return self.secondary_menu()
            else:
                return self.secondary_menu()
         else:
            return self.secondary_menu()


mainl = 1
adpl = 1
try:
    if len(sys.argv) > 1:
        opts, args = getopt.getopt(sys.argv[1:], "h")
        for op, value in opts:
            if op == "-h":
                usage()
                sys.exit()
    menu = Menu_tool()
    menu.main()
except Exception,e:
    print e
    print "指定的参数无效"
    usage()
