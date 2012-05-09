from engine import *

pagelets = Pagelets()
exam = pagelets.addPagelet("exam")

exam.addField(Field("Q"))                  #Question
exam.addField(Field("A"))                  #Answer
exam.addField(Field("G"))                  #Grade

exam.addUserToView("S")
exam.addUserToView("T")

exam.addFieldToView("T","Q","rw")

# setting initial state

stated={}
stated["S"]="ready"
stated["T"]="setting"
state = State(stated)

exam.setInitialState(state)

#defining 1st transition

newstated={}
newstated["S"]="writing"
newstated["T"]="waiting"
newstate = State(newstated)

perm = {}
perm["S"]={}
perm["T"]={}
perm["S"]["Q"]="r-"
perm["S"]["A"]="rw"
perm["T"]["Q"]="r-"

t = Transition(state, newstate, perm)
exam.addTransition(t,"sendpaper")

#defining 2nd transition

state = newstate

newstated={}
newstated["S"]="waiting"
newstated["T"]="grading"
newstate = State(newstated)

perm = {}
perm["S"]={}
perm["T"]={}
perm["S"]["A"]="r-"
perm["T"]["Q"]="r-"
perm["T"]["A"]="r-"
perm["T"]["G"]="rw"

t = Transition(state, newstate, perm)
exam.addTransition(t,"sendanswer")

#defining 3rd transition

state = newstate

newstated={}
newstated["S"]="done"
newstated["T"]="done"
newstate = State(newstated)

perm = {}
perm["S"]={}
perm["T"]={}
perm["S"]["G"]="r-"
perm["T"]["G"]="r-"

t = Transition(state, newstate, perm)
exam.addTransition(t,"sendgrade")

#executing actions

print exam.setFieldByUser("S","Q","abc")    #prints false as student doesnt have permission to set Q
print exam.setFieldByUser("T","Q","abc")    #prints true as teacher has rw permission on Q and sets Q to "abc"
print exam.getFieldByUser("S","Q")          #prints None as student doesnt have permission on Q
print exam.getFieldByUser("T","Q")          #prints Q as teacher has rw permission on Q
print exam.setFieldByUser("S","A","abc")    #prints false as student doesnt have permission to set A

print exam.executeAction("sendanswer")      #prints false as it doesnt matches the transition rules
print exam.executeAction("sendpaper")       #prints true as it matches the transition rules

print exam.setFieldByUser("S","Q","abc")    #prints false as student has r- permission on Q
print exam.getFieldByUser("S","Q")          #prints Q as student has r- permission on Q
print exam.setFieldByUser("T","Q","abc")    #prints false as teacher has r- permission on Q
print exam.setFieldByUser("S","A","abc")    #prints true as student has rw permission on A

print exam.executeAction("sendanswer")      #prints true as it matches the transition rules
print exam.executeAction("sendgrade")       #prints true as it matches the transition rules

