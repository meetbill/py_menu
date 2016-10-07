#!/usr/bin/python
#encoding=utf-8

import traceback, os, re, time, sys, getopt
from snack import * #导入图形界面
from mylib.snack_lib import *
from mylib.BLog import Log
from config import config_first
from config import config_secondary
import inspect
__version__ = "1.1.0"

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
        self.screen.pushHelpLine("<%s> Powered by Billwang139967...请使用TAB在选项间切换"%__version__)
        self.main_location = 1
        self.sec_location = 1

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
        self.screen = SnackScreen()
        self.screen.finish()
        self.screen = SnackScreen()
        self.screen.setColor("ROOT", "white", "blue")
        self.screen.setColor("ENTRY","white","blue")
        self.screen.setColor("LABEL","black","white")
        self.screen.setColor("HELPLINE","white","blue")
        self.screen.setColor("TEXTBOX","black","yellow")
        self.screen.pushHelpLine("<%s> Powered by Billwang139967...请使用TAB在选项间切换"%__version__)
        li = Listbox(height = 15, width = 18, returnExit = 1, showCursor = 0)

        items_n = 1
        for items in config_first["items"]:
            li.append(items, items_n)
            items_n += 1
        li.setCurrent(self.main_location)
      
        bb = CompactButton('|->退出<-|')
        g = GridForm(self.screen, "manager", 1, 10)
        g.add(li, 0, 1)
        g.add(bb, 0, 2)
        g.add(Label(" "),0,3)
        g.add(Label("[管理利器]"),0,4)

        rc=g.run(1,3)
        self.main_location = li.current()
        if rc == 'ESC' or 'snack.CompactButton' in str(rc) :
            return self.QUIT()
        if li.current() in range(1,len(config_first["items"])+1):
            return self.secondary_menu()

    # 第二层menu
    def secondary_menu(self):
        re = []
        li = Listbox(height = 15, width = 14, returnExit = 1, showCursor = 0)
        n = 0
        n1 = 1
        bb = CompactButton('返回')
        secondary_window = config_secondary[self.main_location - 1]
        items_n = 1
        for items in secondary_window["items"]:
            li.append(items[0], items_n)
            items_n += 1
        h = GridForm(self.screen, "请选择", 1, 16)
        li.setCurrent(self.sec_location)
        h.add(li, 0, 1)
        h.add(bb, 0, 9)
        rc = h.run(24,3)
        if "snack.CompactButton" in str(rc) or rc == 'ESC':
            return self.first_menu()
        else :
            self.sec_location = li.current()
            if self.sec_location in range(1,len(secondary_window["items"])+1):
                for fun in inspect.getmembers(self, predicate=inspect.ismethod):
                    if secondary_window["items"][self.sec_location-1][1] == fun[0]:
                        return fun[1]()
                return self.three_example()

    # 三级
    # 第一个二级窗口的三级页面
    def three1_1funtion(self):
         m = Mask(self.screen, "test_windows1_1", 35 )
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
    def three1_2funtion(self):
         m = Mask(self.screen, "test_windows1_2", 35 )
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
    def three1_3funtion(self):
         m = Mask(self.screen, "test_windows1_3", 35 )
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
    
    # 第二个二级窗口的三级页面
    def three2_1funtion(self):
         m = Mask(self.screen, "test_windows2_1", 35 )
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

    def three2_2funtion(self):
         m = Mask(self.screen, "test_windows2_2", 35 )
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

    # 第三个二级窗口的三级页面
    def three3_1funtion(self):
         m = Mask(self.screen, "test_windows3_1", 35 )
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
    def three_example(self):
         m = Mask(self.screen, "test_example", 35 )
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
            


try:
    if len(sys.argv) > 1:
        opts, args = getopt.getopt(sys.argv[1:], "h")
        for op, value in opts:
            if op == "-h":
                usage()
                sys.exit()
    
    if len(config_first["items"]) != len(config_secondary):
        print "一级目录个数与二级窗口个数不对应"
        sys.exit()
    menu = Menu_tool()
    menu.main()
except Exception,e:
    print e
    print "指定的参数无效"
    usage()
