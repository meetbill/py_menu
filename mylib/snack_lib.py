#!/usr/bin/python
#coding=utf8
from snack import *
 
class Mask:
    """
    An input mask.
    """
    
    def __init__(self, screen, title="unnamed mask", width=30):
        """
        Creates an input mask with a title.
        The width is applied to the right side of the window.
        """
        self._width = width
        self._screen = screen
        self.g = GridForm(self._screen, title, 1, 20)
        self.subgrid = Grid(2, 20)
        self._row = 0
        self._row_grid = 0
        self._elements = {}
        self._buttons = 0
        self._checks_box=0
        self._checks_entrylist=[]
        
    def entry(self, label, name, text="", password=0):
        """
        Creates an entry for text.
        """
        self.subgrid.setField( Label( label ), 0, self._row, (0,0,1,1) )
        
        self._elements[name] = Entry(self._width, text, password=password)
        self.subgrid.setField( self._elements[name], 1, self._row, (0,0,0,1) )
        self._row += 1
    
    def text(self, label="",text=""):
        """
        Creates  text.
        """
        self.subgrid.setField( Label( label ), 0, self._row, (0,0,0,1) )
        #self.subgrid.setField( TextboxReflowed(self._width,text) , 1, self._row, (0,0,0,1) )
        self.subgrid.setField( TextboxReflowed(self._width,text, flexDown = 5, flexUp = 10, maxHeight = -1) , 1, self._row, (0,0,0,1) )
        self._row += 1
        
    def password(self, label, name, text=""):
        """
        Creates an password entry.
        """
        self.entry(label, name, text, password=1)
        
    def buttons(self, yes=u"确定",no = u"取消"):
        """
        Creates a set of buttons given as kwargs.
        IE: mask.buttons(yes="Yes", no="No")
        """
        self._buttons = ButtonBar(self._screen, ((yes, "yes"), (no, "no")))
        self.g.add( self.subgrid, 0, self._row_grid)
        self.g.add( self._buttons, 0, self._row_grid+1)
        #self.g.add( self.subgrid, 0, self._row_grid)
        #self.g.add( self._buttons, 0, self._row_grid+1)
        
    def radios(self, label, name, options):
        """
        Creates a radio group.
        Options are given as [ (label, value, checked), ... ] where
        checked equ. 0/1.
        """
        self.subgrid.setField( Label( label ), 0, self._row, (0,0,1,1) )
        
        self._elements[name] = RadioBar(self._screen, options)
        self.subgrid.setField( self._elements[name], 1, self._row, (0,0,0,1), anchorLeft=1 )
        
        self._row += 1
        
    def list(self, label, name, options, height=None, scroll=1):
        """
        Creates a single choice list.
        Options are given as [ (label, value, checked), ... ] where
        checked equ. 0/1.
        """
        self.subgrid.setField( Label( label ), 0, self._row, (0,0,1,1) )
        
        if height is None:
            height = len(options)
        self._elements[name] = Listbox(height=height, width=self._width, scroll=scroll)
        
        for option in options:
            (key, value, selected) = option
            self._elements[name].append( key, value )
            if selected:
                self._elements[name].setCurrent(value)
        
        self.subgrid.setField( self._elements[name], 1, self._row, (0,0,0,1), anchorLeft=1 )
        
        self._row += 1
        
    def checks(self, label, name, options, height=None, scroll=1):
        """
        Creates a set of checkboxes.
        Options are given as [ (label, value, checked), ... ] where
        checked equ. 0/1.
        """
        self.subgrid.setField( Label( label ), 0, self._row, (0,0,1,1) )
        
        if height is None:
            height = len(options)
        
        self._elements[name] = CheckboxTree(height=height, scroll=scroll, width=self._width)
        
        for option in options:
            (key, value, selected) = option
            self._elements[name].append( key, value, selected )
        self.subgrid.setField( self._elements[name], 1, self._row, (0,0,0,1), anchorLeft=1, growx=1 )
        
        self._row += 1
    def checks_entry(self, label,name,checked,entry_list):
        """
            (labelname,name,checked,[ (label, name,text), ... ])
        """
        self._checks_box=name
        self.subgrid.setField( Label( label ), 0, self._row)
        self._elements[name] = Checkbox("")
        self.subgrid.setField( self._elements[name], 1, self._row,anchorLeft=1)
        self._elements[name].setCallback(self.checkBox_flag)
        if checked:
            self._elements[name].setValue('*')
        self._row += 1
        for option in entry_list:
            (label,name,text) = option
            self.subgrid.setField( Label( label ), 0, self._row)
            self._elements[name] = Entry(self._width, text)
            self._checks_entrylist.append(name)
            self.subgrid.setField( self._elements[name], 1, self._row, (0,0,0,1) )
            self._row += 1
        self.checkBox_flag()
        
    def checkBox_flag(self):
        if self._checks_box:
            if self._elements[self._checks_box].selected():
                state = FLAGS_SET
            else:
                state = FLAGS_RESET

            for i in self._checks_entrylist:
                self._elements[i].setFlags(FLAG_DISABLED, state)

    def run(self,width = 0,height = 0):
        """
        Runs until a button is pressed.
        Returns [ button, { values } ].
        """
        if  width and  height: 
            btn = self.g.runOnce(width,height)
        else:
            btn = self.g.runOnce()
        button = self._buttons.buttonPressed(btn)
        
        cmd = None
        results = {}
        
        cmd = button
        if btn == 'F12':
            cmd = 'F12'
        
        for name in self._elements:
            if 'value' in dir( self._elements[name] ):
                results[name] = self._elements[name].value()
            if 'getSelection' in dir( self._elements[name] ):
                results[name] = self._elements[name].getSelection()
            if 'current' in dir( self._elements[name] ):
                results[name] = self._elements[name].current()
        
        return [ cmd, results ]

if __name__ == "__main__":
    import os
    import sys
    root_path = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(root_path, '..'))
    from mylib.snack_lib import *

    screen = SnackScreen()
    screen.setColor("ROOT", "white", "blue")
    screen.setColor("ENTRY","white","blue")
    screen.setColor("LABEL","black","white")
    screen.setColor("HELPLINE","white","blue")
    screen.setColor("TEXTBOX","black","yellow")
    def test():
         m = Mask( screen, "test_windows", 35 )
         m.text("label_test1","ceshi_text")
         m.entry( "label_test1", "entry_test1", "0" )
         m.entry( "label_test2", "entry_test2", "0" )
         m.checks( "复选框","checks_list",[
             ('checks_name1','checks1',0),
             ('checks_name2','checks2',0),
            ('checks_name3','checks3',0),
             ('checks_name4','checks4',1),
             ('checks_name5','checks5',0),
             ('checks_name6','checks6',0),
             ('checks_name7','checks7',0),
         ],
         height= 3
         )    
         m.radios( "单选框","radios", [ 
             ('radios_name1','radios1', 0), 
             ('radios_name2','radios2', 1), 
             ('radios_name3','radios3', 0) ] )  
         m.checks_entry( "空格选择下","checks_entry", 1,[ 
             ('c_entry1','c_entry1','c_entry1')])  
         
         m.buttons( yes="Sava&Quit", no="Quit" )
         #(cmd, results) = m.run(12,3)
         (cmd, results) = m.run()
         screen.finish() 
         return cmd,results

    try:
        (cmd,results) = test()
        print cmd,results
    except Exception ,e:
        print e
    finally:
        screen.finish()

