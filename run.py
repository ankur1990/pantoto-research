from engine import *

#initial conditions
system = System()

#pagelets
system.addPagelet("exam")

#users
system.addUser("S")
system.addUser("T")

#Initial Field View for state (s: ready | t: ready)
system.addField("exam",Field("Q"))                      #Question
system.addFieldToView("T","exam","Q","rw")

# setting initial state
state = State({"S":"ready", "T":"ready"})
system.setInitialState(state)

#defining 1st transition
newstate = State({"S":"writing", "T":"waiting"})

def hook1(system):
    system.addField("exam",Field("A"))                  #Answer
    system.updateFieldView("S","exam","Q","r-")
    system.updateFieldView("S","exam","A","rw")
    system.updateFieldView("T","exam","Q","r-")

t = Transition(state, newstate, hook1)
system.addTransition(t,"sendpaper")                     # "sendpaper" is an event
# Since the event is just a string (name), we ignore making another class for it.

#defining 2nd transition
state = newstate
newstate = State({"S":"waiting", "T":"grading"})

def hook2(system):
    system.addField("exam",Field("G"))                  #Grade
    system.updateFieldView("S","exam","A","r-")
    system.updateFieldView("T","exam","A","r-")
    system.updateFieldView("T","exam","G","rw")

t = Transition(state, newstate, hook2)
system.addTransition(t,"sendanswer")

#defining 3rd transition
state = newstate
newstate = State({"S":"done", "T":"done"})

def hook3(system):
    system.updateFieldView("S","exam","G","r-")
    system.updateFieldView("T","exam","G","r-")

t = Transition(state, newstate, hook3)
system.addTransition(t,"sendgrade")

#executing actions

#init state
print system.setFieldByUser("S","exam","Q","abc")       #prints false as student doesnt have permission to set Q
print system.setFieldByUser("T","exam","Q","abc")       #prints true as teacher has rw permission on Q and sets Q to "abc"
print system.getFieldByUser("S","exam","Q")             #prints None as student doesnt have permission on Q
print system.getFieldByUser("T","exam","Q")             #prints Q as teacher has rw permission on Q
print system.setFieldByUser("S","exam","A","abc")       #prints false as student doesnt have permission to set A

# paper has not been delivered yet
print system.executeAction("sendanswer")                #prints false as it doesnt matches the transition rules
# paper sent
print system.executeAction("sendpaper")                 #prints true as it matches the transition rules

# state t: waiting, s:writing
#s cannot change the question
print system.setFieldByUser("S","exam","Q","abc")       #prints false as student has r- permission on Q
#s can read the question
print system.getFieldByUser("S","exam","Q")             #prints Q as student has r- permission on Q
#t cannot change the question
print system.setFieldByUser("T","exam","Q","abc")       #prints false as teacher has r- permission on Q
#s can answer
print system.setFieldByUser("S","exam","A","abc")       #prints true as student has rw permission on A
print system.executeAction("sendanswer")                #prints true as it matches the transition rules
#state t:grading, s: waiting
print system.executeAction("sendgrade")                 #prints true as it matches the transition rules


