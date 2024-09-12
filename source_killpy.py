import os
datastr = os.popen("ps -e|grep python").read()
print(datastr)
data = datastr.split(" ")
pid = data[0]
if pid == "" and len(data) != 1:
    pid = data[1]
    os.system("kill -9 "+pid)
    print("Killed "+pid)
elif len(data) == 1:
    print("No Process")
else:
    os.system("kill -9 "+pid)
    print("Killed "+pid)
