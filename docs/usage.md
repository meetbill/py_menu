## usage

* [一级及二级目录](#一级及二级目录)
* [三级编辑窗口功能实现](#三级编辑窗口功能实现)
* [二级菜单配置中往三级编辑窗口函数跳转实现](#二级菜单配置中往三级编辑窗口函数跳转实现)

### 说明

界面修改操作仅需要修改 config.py 和 three_page.py 两个文件

### 一级及二级目录

一级及二级目录显示，只需要修改config.py文件
```
config_first = {
        'name': '主目录',
        'items':  ['a)功能分类1', 
                   'b)功能分类2',
                   'c)功能分类3',
        ],
    }

config_secondary = [{
        'name': 'window1',
        'items':  [("二级目录1_1","three1_1funtion"),
                   ("二级目录1_2","three1_2funtion"),
                   ("二级目录1_3","three1_3funtion"),
        ],
    },
    {
        'name': 'window2',
        'items':  [("二级目录2_1","three2_1funtion"),
                   ("二级目录2_2","three2_2funtion"),
        ],
    },
    {
        'name': 'window3',
        'items':  [("二级目录3_1","three3_1funtion"),
        ],
    },
]
```
> * 一级目录中的items[列表]即使终端菜单界面上的列表显示
> * 二级目录中的items[列表]即使终端菜单界面上的列表显示，items列表中的元素是元组，元组的第一个元素是二级菜单的列表项，第二个元素是指定三级的功能
> * config_first中items的元素个数必须和config_secondary列表的元素个数一致，即保证一级目录都有对应的二级目录窗口

### 三级编辑窗口功能实现

三级编辑窗口,编辑three_page.py
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


### 二级菜单配置中往三级编辑窗口函数跳转实现

二级菜单中，二级菜单配置是一个列表，列表中的元素是元组，第一个参数是二级菜单中的显示内容，第二个参数是跳转到的三级函数名字

'items':  [("二级目录3_1","three3_1funtion")],
