from snack import *
#coding=utf8
 
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
        self.g = GridForm(self._screen, title, 1, 2)
        self.subgrid = Grid(2, 20)
        self._row = 0
        self._elements = {}
        self._buttons = 0
        
    def entry(self, label, name, text="", password=0):
        """
        Creates an entry for text.
        """
        self.subgrid.setField( Label( label ), 0, self._row, (0,0,1,1) )
        
        self._elements[name] = Entry(self._width, text, password=password)
        self.subgrid.setField( self._elements[name], 1, self._row, (0,0,0,1) )
        
        self._row += 1
        
    def password(self, label, name, text=""):
        """
        Creates an password entry.
        """
        self.entry(label, name, text, password=1)
        
    def buttons(self, ok=u"确定",cancel = u"取消"):
        """
        Creates a set of buttons given as kwargs.
        IE: mask.buttons(yes="Yes", no="No")
        """
        self._buttons = ButtonBar(self._screen, ((ok, "ok"), (cancel, "cancel")))
        self.g.add( self.subgrid, 0, 0)
        self.g.add( self._buttons, 0, 1 )
        
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
