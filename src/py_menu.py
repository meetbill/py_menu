#!/usr/bin/python
# encoding=utf-8

import traceback
import os
import sys
import getopt
import inspect

root_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.insert(0, os.path.join(root_path, 'w_lib'))
from pysnack.snack import *
from pysnack import snack_lib

import config
import three_page
import blog

blog.init_log("./log/pymenu")
_version_ = "1.2.4"


def usage():
    print "<使用方法>"
    print "-h 本帮助"


class MenuTool(object):
    def __init__(self):

        self.screen = SnackScreen()
        self.screen.setColor("ROOT", "white", "blue")
        self.screen.setColor("ENTRY", "white", "blue")
        self.screen.setColor("LABEL", "black", "white")
        self.screen.setColor("HELPLINE", "white", "blue")
        self.screen.setColor("TEXTBOX", "black", "yellow")
        self.main_location = 1
        self.sec_location = 1

    def main(self):
        try:
            self.first_menu()
        except Exception as e:
            self.screen.finish()
            print e
            print traceback.format_exc()
        finally:
            self.screen.finish()
            print "感谢使用！"
            return ''

    def quit(self):
        # 调用退出到命令行，输入exit返回
        buttons = ("是", "否")
        bb = ButtonBar(self.screen, buttons)
        g = GridForm(self.screen, "返回登陆界面？", 20, 16)
        g.add(bb, 1, 3, (10, 0, 10, 0), growx=1)
        rq = g.runOnce(32, 8)
        self.screen.popWindow()
        if rq == "ESC" or bb.buttonPressed(rq) == "否":
            self.first_menu()
        else:
            self.screen.finish()
            return

    def first_menu(self):
        # 主界面
        # 主memu菜单项位置
        while True:
            self.screen = SnackScreen()
            self.screen.finish()
            self.screen = SnackScreen()
            self.screen.setColor("ROOT", "white", "blue")
            self.screen.setColor("ENTRY", "white", "blue")
            self.screen.setColor("LABEL", "black", "white")
            self.screen.setColor("HELPLINE", "white", "blue")
            self.screen.setColor("TEXTBOX", "black", "yellow")
            self.screen.pushHelpLine("<%s> Powered by meetbill...请使用 TAB 在选项间切换" % _version_)
            li = Listbox(height=15, width=18, returnExit=1, showCursor=0)

            items_n = 1
            for items in config.config_first["items"]:
                li.append(items, items_n)
                items_n += 1
            li.setCurrent(self.main_location)

            bb = CompactButton('|->退出<-|')
            g = GridForm(self.screen, "manager", 1, 10)
            g.add(li, 0, 1)
            g.add(bb, 0, 2)
            g.add(Label(" "), 0, 3)
            g.add(Label("[管理利器]"), 0, 4)
            rc = g.run(1, 3)
            self.main_location = li.current()
            if rc == 'ESC' or 'snack.CompactButton' in str(rc):
                return self.quit()
            if li.current() in range(1, len(config.config_first["items"]) + 1):
                self.secondary_menu()

    # 第二层menu
    def secondary_menu(self):
        li = Listbox(height=15, width=14, returnExit=1, showCursor=0)
        bb = CompactButton('返回')
        secondary_window = config.config_secondary[self.main_location - 1]
        items_n = 1
        for items in secondary_window["items"]:
            li.append(items[0], items_n)
            items_n += 1
        while True:
            h = GridForm(self.screen, "请选择", 1, 16)
            if len(secondary_window["items"]) < self.sec_location:
                li.setCurrent(1)
            else:
                li.setCurrent(self.sec_location)
            h.add(li, 0, 1)
            h.add(bb, 0, 9)
            rc = h.run(24, 3)

            if "snack.CompactButton" in str(rc) or rc == 'ESC':
                return 0
            else:
                self.sec_location = li.current()
                if self.sec_location in range(1, len(secondary_window["items"]) + 1):
                    name, func_name, func_kargs = secondary_window["items"][self.sec_location - 1]
                    if func_name in dir(three_page):
                        for fun in inspect.getmembers(three_page, callable):
                            if func_name == fun[0]:
                                fun[1](self.screen, **func_kargs)
                    else:
                        snack_lib.warwindows(self.screen, "警告", "没有找到对应的函数!")
                else:
                    snack_lib.warwindows(self.screen, "测试", "xxx")


try:
    if len(sys.argv) > 1:
        opts, args = getopt.getopt(sys.argv[1:], "h")
        for op, value in opts:
            if op == "-h":
                usage()
                sys.exit()

    if len(config.config_first["items"]) != len(config.config_secondary):
        print "一级目录个数与二级窗口个数不对应"
        sys.exit()
    if os.getenv('STY'):
        print "not support screen"
        sys.exit()

    menu = MenuTool()
    menu.main()
except Exception as e:
    print e
    print "指定的参数无效"
    usage()
