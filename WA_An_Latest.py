import re
import datetime    
import matplotlib.pyplot as plt

print("WA Alpha Analysis v0.2\nWilliam R. Ebenezer, July 2020")

uname = str(input("Enter your first name as in WA: "))
if len(uname) < 1: uname = "William"

fname = str(input("Enter file name with extension: "))
if len(fname) < 3: fname = "Text.txt"

try:
    fhand = open(fname, "r")
except:
    print("Fatal Error: Could not open file. Exiting immediately.")
    exit()

line_count = 0
err_count = 0
counter = 0
fl = 0

node1 = dict() #total : K: datetime object V: Count
me = dict() #outgoing
other = dict() #incoming

oname = None

for line in fhand:
    line_count += 1
    
    if re.search(".*end-to-end encryption. Tap for more info.", line): 
        err_count += 1
        continue
        
    if not re.search("^\d{1,2}/\d{1,2}/\d{2},.\d{1,2}:\d{2}.*", line): 
    	err_count += 1
    	continue
    
    line_list = line.split()
    
    tme = line_list[1].split(":")
    
    lzt = line_list[0].split("/")
    year = "20"+lzt[2][:(len(lzt[2])-1)]
    z = datetime.datetime(int(year), int(lzt[0]), int(lzt[1]), int(tme[0]), int(tme[1]))
    
    if oname is None and not line_list[3] == uname:
    	if line_list[3].endswith(":") : fl = 1 
    	oname = line_list[3][:len(line_list[3])-fl]
    
    node1[z.date()] = node1.get(z.date(), 0) + 1
    try: 
        if line_list[3] == uname:
            me[z.date()] = me.get(z.date(), 0) + 1
            other[z.date()] = other.get(z.date(), 0)
        else:
            other[z.date()] = other.get(z.date(), 0) + 1
            me[z.date()] = me.get(z.date(), 0)
    except:
        print("E")
    
print(line_count - err_count, "Messages Found.")

for (x, y), (a, b) in zip(me.items(), other.items()):
    print(x, y, b)

p1 = plt.bar(list(node1.keys()), list(me.values()))
p2 = plt.bar(list(node1.keys()), list(other.values()), bottom=list(me.values()))

plt.legend((p1[0], p2[0]), (uname, oname)) 

plt.show()
exit()

