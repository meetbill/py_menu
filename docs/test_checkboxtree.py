#!/usr/bin/env python

from snack import *

screen = SnackScreen()

g = GridForm(screen, "My Test", 1, 4)
# --------------------------------------------------------------------
li = Listbox(height = 3, width = 20, returnExit = 1)
li.append("First", 1)
li.append("Second", 2)
li.append("Third", 3)
g.add(li, 0, 0, padding = (0, 0, 0, 1))
# --------------------------------------------------------------------
rb = RadioBar(screen, (
 ("This", -1, 0),
 ("Default", "default", 1),
 ("That", "that", 0) ))
g.add(rb, 0, 1, padding = (0, 0, 0, 1))
# --------------------------------------------------------------------
ct = CheckboxTree(height = 5, scroll = 1)
ct.append("Colors")
ct.addItem("Red", (0, snackArgs['append']))
ct.addItem("Yellow", (0, snackArgs['append']))
ct.addItem("Blue", (0, snackArgs['append']))
ct.append("Flavors")
ct.append("Numbers")
ct.addItem("1", (2, snackArgs['append']))
ct.addItem("2", (2, snackArgs['append']))
ct.addItem("3", (2, snackArgs['append']))
ct.append("Names")
ct.append("Months")
ct.append("Events")
g.add(ct, 0, 2, padding = (0, 0, 0, 1))
# --------------------------------------------------------------------
bb = ButtonBar(screen, (("Ok", "ok"), ("Cancel", "cancel")))
g.add(bb, 0, 3)
# --------------------------------------------------------------------
result = g.runOnce()
screen.finish()
# --------------------------------------------------------------------
print result
print "listbox:", li.current()
print "rb:", rb.getSelection()
print "bb:", bb.buttonPressed(result)
print "checkboxtree:", ct.getSelection()
