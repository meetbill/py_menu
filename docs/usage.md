## py_menu 使用手册

<!-- vim-markdown-toc GFM -->
* [1 项目简介](#1-项目简介)
* [2 使用篇](#2-使用篇)
    * [2.1 简介](#21-简介)
    * [2.2 一级及二级菜单](#22-一级及二级菜单)
    * [2.3 三级菜单](#23-三级菜单)
        * [2.3.1 三级编辑窗口功能实现](#231-三级编辑窗口功能实现)
        * [2.3.2 三级 output 窗口](#232-三级-output-窗口)
    * [2.4 添加调试日志](#24-添加调试日志)
* [3 原理篇](#3-原理篇)
    * [3.1 整体显示](#31-整体显示)
    * [3.2 构图](#32-构图)
        * [3.2.1 一层和二层](#321-一层和二层)
        * [3.2.2 三层目录](#322-三层目录)
    * [3.3 函数实现](#33-函数实现)
        * [3.3.1 一级及二级菜单](#331-一级及二级菜单)
        * [3.3.2 三级编辑窗口](#332-三级编辑窗口)
        * [3.3.3 二级菜单配置中往三级编辑窗口函数跳转实现](#333-二级菜单配置中往三级编辑窗口函数跳转实现)

<!-- vim-markdown-toc -->

## 1 项目简介

本项目主要更新两部分

> * py_menu 整体框架
> * 第三级编辑页的底层函数库 [mylib/snack_lib.py](./snack_lib.md) ,此库可以单独使用

## 2 使用篇
### 2.1 简介

界面修改操作仅需要修改 config.py 和 three_page.py 两个文件

### 2.2 一级及二级菜单

一级及二级目录显示，只需要修改 config.py 文件
```
config_first = {
        'name': '主目录',
        'items':  ['a) 功能分类 1',
                   'b) 功能分类 2',
                   'c) 功能分类 3',
        ],
    }

config_secondary = [{
        'name': 'window1',
        'items':  [("二级目录 1_1","three1_1funtion"),
                   ("二级目录 1_2","three1_2funtion"),
                   ("二级目录 1_3","three1_3funtion"),
        ],
    },
    {
        'name': 'window2',
        'items':  [("二级目录 2_1","three2_1funtion"),
                   ("二级目录 2_2","three2_2funtion"),
        ],
    },
    {
        'name': 'window3',
        'items':  [("二级目录 3_1","three3_1funtion"),
        ],
    },
]
```
> * 一级目录中的 items『列表』即使终端菜单界面上的列表显示
> * 二级目录中的 items『列表』即使终端菜单界面上的列表显示，items 列表中的元素是元组，元组的第一个元素是二级菜单的列表项，第二个元素是指定三级的功能
> * config_first 中 items 的元素个数必须和 config_secondary 列表的元素个数一致，即保证一级目录都有对应的二级目录窗口

### 2.3 三级菜单
#### 2.3.1 三级编辑窗口功能实现

三级编辑窗口，编辑 three_page.py
```
def three1_1funtion(screen):
     m = Mask(screen, "test_windows1_1", 35 )
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

     logger.debug(str(cmd)+" "+str(results))
     if cmd == "yes":
        rx = conformwindows(screen, "确认操作")
        if rx[0] == "yes" or rx[1] == "F12":
            """exe"""
            return
        else:
            logger.debug("cancel this operation")
            return
     else:
        return
```
#### 2.3.2 三级 output 窗口

三级 output 窗口，编辑 three_page.py
```
def three1_2funtion(screen):
    m = Snack_output(screen, "test_windows1_2", 35 )
    m.text("ceshijjjjjjjjjjjxdffffffffffffffff")
    m.text("xxxfffxxxxxxxxxxxxxx")
    m.text("xxxxxxxxxxxxxxxxx")
    m.text("xxxxxxxxxxxxxxxxx")
    m.text("xxxxxxxxxxxxxxxxx")
    m.run(43,3)
```
### 2.4 添加调试日志

在 `three_page.py` 中添加功能时，可能需要输出下调试日志，可以通过添加下面操作实现

```
# messages 是需要输出的信息
logger.debug(str(messages))
```

## 3 原理篇
### 3.1 整体显示

```
+--------++-------++--------------+
|        ||       ||              |
|        ||       ||              |
|        ||       ||              |
|        ||       ||              |
|        ||       || +--+   +--+  |
|        ||       || +--+   +--+  |
|        ||       |+--------------+
| +----+ || +---+ |
| +----+ || +---+ |
+--------++-------+

```
> * 第一个列表窗口使用 g.run(1,3)-- 跳转到第二个窗口后仍然显示
> * 第二个列表窗口使用 g.run(24,3)-- 跳转到第三个窗口后仍然显示
> * 第三个编辑窗口使用 g.runOnce(45,3)-- 点击确定 / 取消后消失


### 3.2 构图

#### 3.2.1 一层和二层

```
+-----------------+
| +-------------+ |
| |    list     | |
| +-------------+ |
| +-------------+ |
| |    back     | |
| +-------------+ |
+-----------------+
```

#### 3.2.2 三层目录

```
+-------------------------------+
| +-------------+-------------+ |
| |  label      |   text      | |
| +-------------+-------------+ |
| |  label      |   entry     | |
| +-------------+-------------+-+---------subgrid
| |  label      |   checks    | |
| +-------------+-------------+ |
| |  label      |   radios    | |
| +-------------+-------------+ |
| |  label      |checks_entry | |
| +-------------+-------------+ |
| +---------------------------+ |
| |                           | |
| |          button           +-+---------buttons
| |                           | |
| +---------------------------+ |
+-------------------------------+---------gridform
```
第三层编辑窗口具体实现可查看 [snack_lib](snack_lib.md)

### 3.3 函数实现

#### 3.3.1 一级及二级菜单

一级及二级菜单均是列表，故二级菜单可以进行复用，通过传入不同的列表值显示不同的菜单项

> * self.main_location 标记一级菜单选择的第几行，会根据此参数，传给第二级菜单列表参数，显示对应二级窗口
> * self.sec_location 标记二级菜单选择的第几行

#### 3.3.2 三级编辑窗口

三级编辑窗口是对复选框、单选框、编辑框等进行了封装。点击确定后会继续弹出确认框。同时返回的是 json 串，非常容易处理
#### 3.3.3 二级菜单配置中往三级编辑窗口函数跳转实现

二级菜单中，二级菜单配置是一个列表，列表中的元素是元组，第一个参数是二级菜单中的显示内容，第二个参数是跳转到的三级函数名字

'items':  [("二级目录 3_1","three3_1funtion")],
