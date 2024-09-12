import os
import re
import time
import datetime
debug = "Phone"
print("""心情复杂自动刷经验 For MI 8 device v3.1.2
v2.0更新:新增网页访问功能
v2.1更新:在网页中添加最新手机截图,避免反复scrcpy排查问题
v2.1.1更新:代码优化
v3.0更新:双刷功能
v3.0.1更新:代码优化,提高稳定性
v3.0.2更新:修复16小时数值溢出问题
v3.1更新:双修,签到
v3.1.1更新:修复24小时后无法双修,签到问题
v3.1.2更新:更多电池信息输出,错误输出
""")

first = 15
fstatus = 0
second = 17
sstatus = 0
third = 19
tstatus = 0
dailysignin = 9
dstatus = 0

lastimg = 0
datelast = 0
batttime = 0
start = time.time()
os.system("adb devices")
i = 0
# 练度等级
lev1 = 26
lev2 = 20

if debug == False:
    sleeptime = 260 #Normal
    device = "emulator-5554"
    wait = 15
elif debug == True:
    sleeptime = 10
    device = "4cad6f0d"
    wait = 2

#Other
device = "192.168.3.22:5555"
# ==End==
print(device)
html = "<head><title>AutoXQFZ-Debug</title></head>"+device+"<br>"
def tapsend():
    tap(965,2049,100)
def openchat():
    tap(0,550,100)
    time.sleep(1)
    tap(238,2049,100)
def userswitch(uid):
    time.sleep(1)
    os.system("adb shell am switch-user "+str(uid))
    time.sleep(5)
    swipe(477,2144,537,0,100)
    time.sleep(1)
    os.system("adb shell monkey -p com.tencent.mobileqq 1")
    time.sleep(1)
def gettime():
    return datetime.datetime.now().strftime("[%H:%M:%S]")
def getdate():
    return int(datetime.datetime.now().strftime("%d"))
def gettimelist():
    return datetime.datetime.now().strftime("%H:%M:%S").split(":")
def tap(x,y,t):
    os.system("adb -s "+device+" shell input tap "+str(x)+" "+str(y)+" "+str(t))
def ins(data):
    os.system("adb -s "+device+" shell am broadcast -a ADB_INPUT_TEXT --es msg '"+data+"'")
    time.sleep(0.1)
def swipe(x1,y1,x2,y2,t):
    os.system("adb -s "+device+" shell input swipe "+str(x1)+" "+str(y1)+" "+str(x2)+" "+str(y2)+" "+str(t))
def enter():
    os.system("adb shell input keyevent KEYCODE_ENTER")
def send(rwn,data):
    print("["+str(i)+"]"+gettime()+"处理任务"+str(rwn))
    ins("@")
    ins("心情复杂")
    tap(274,384,100)
    ins(data)
    tapsend()
def secondtohms(second):
    hour = second // 3600
    minsec = second % 3600
    min = minsec // 60
    sec = minsec % 60
    return str(int(hour))+":"+str(int(min))+":"+str(int(sec))
def signin():
    send(0,"修仙签到")
    time.sleep(3)
    send(0,"宗门签到")
    time.sleep(1)
    userswitch(10)
    openchat()
    send(0,"修仙签到")
    time.sleep(3)
    send(0,"宗门签到")
    time.sleep(1)
    userswitch(0)
    openchat()
def twoget():
    send(0,"发起双修268426")
    time.sleep(1)
    userswitch(10)
    openchat()
    send(0,"接受双修283764")
    time.sleep(1)
    userswitch(0)
    openchat()
    
def main(accountid,uid,lev):
    global fstatus
    global sstatus
    global tstatus
    global dstatus
    global html
    global lastimg
    global datelast
    global battall
    global fstatus
    global sstatus
    global tstatus
    global dstatus
    global battstart
    global batttime
    
    date = getdate()
    if date != datelast:
        fstatus = 0
        sstatus = 0
        tstatus = 0
        dstatus = 0
        datelast = date
        
    openchat()
    
    if accountid == 1:
        hour = gettimelist()[0]
        if int(hour) == dailysignin and dstatus == 0:
            signin()
            dstatus = 1
        elif int(hour) == first and fstatus == 0:
            twoget()
            fstatus = 1
        elif int(hour) == second and sstatus == 0:
            twoget()
            sstatus = 1
        elif int(hour) == third and tstatus == 0:
            twoget()
            tstatus = 1
        else:
            print("Passed.")

    send(1,"修炼")
    print("["+str(i)+"]"+gettime()+"等待5秒...")
    time.sleep(5)

    send(2,"开采")
    print("["+str(i)+"]"+gettime()+"等待5秒...")
    time.sleep(5)

    send(3,"前往宗门洞府")
    print("["+str(i)+"]"+gettime()+"等待5秒...")
    time.sleep(5)
    
    send(4,"猎杀妖兽"+str(lev))
    print("["+str(i)+"]"+gettime()+"等待5秒...")
    time.sleep(5)
    
    print("["+str(i)+"]"+gettime()+"输出信息")
    now = time.time()
    tc = now-start
    battery = os.popen("adb -s "+device+" shell dumpsys battery").read().split("\n")
    if len(re.findall("true",battery[1])) == 1:
        charge = "AC-Charging"
        ch = True
    elif len(re.findall("true",battery[2])) == 1:
        charge = "USB-Charging"
        ch = True
    else:
        charge = "No-Charging"
        ch = False
    print("["+str(i)+"]"+gettime()+charge+":"+battery[10].split(" ")[-1])
    ins("["+str(i)+"]"+gettime())
    enter()
    ins("Runned"+":"+secondtohms(tc))
    enter()
    ins(charge)
    enter()
    batt = battery[10].split(" ")[-1]
    ins("BatteryLevel:"+batt+"%")
    enter()
    if ch == True:
        battstart = batt
        batttime = 0
    batttime += 1
    battavg = int(int(int(batt)-int(battstart))/batttime*100)/100
    battall = battall[-11:-1]+[battall[-1],batt]
    battlast1h = int(batt)-int(battall[0])
    ins("Batt_Avg/Last1h:"+str(battavg)+"/"+str(battlast1h))
    enter()
    now = time.time()
    nexthms = time.strftime('%H:%M:%S',time.localtime(now+2*sleeptime+10))
    ins("NextTime:"+nexthms)
    tapsend()

    # Low Battery Alert
    if int(batt) <= 20 and int(batt) > 10:
        ins("LowBattery:LessThan20%")
        tapsend()
    elif int(batt) <= 10 and int(batt) > 5:
        ins("LowBattery:LessThan10%")
        tapsend()
    elif int(batt) <= 5:
        ins("@")
        ins("{")
        tap(274,384,100)
        ins("LowBattery:LessThan5%-PleaseChargeAsSoonAsPossible!")
        tapsend()
    else:
        print("Battery OK")
    
    data = "<a>["+str(i)+"][Account"+str(accountid)+"]"+gettime()+charge+":BatteryLevel"+battery[10].split(" ")[-1]+"% status:"+str(fstatus)+str(sstatus)+str(tstatus)+str(dstatus)+"</a><br>"
    html += data
    now = int(time.time())
    with open("index.html","w") as f:
        f.write(html+"<img src=img"+str(now)+".png>")
    print("["+str(i)+"]"+gettime()+"Debug Wrote.")
    os.system("adb exec-out screencap -p > img"+str(now)+".png")
    os.system("rm img"+str(lastimg)+".png")
    lastimg = now
    print("["+str(i)+"]"+gettime()+"Screen Copied.")

    if uid == 0:
        userswitch(10)
    elif uid == 10:
        userswitch(0)
    
    print("["+str(i)+"]"+gettime()+"等待"+str(sleeptime)+"s...")
    time.sleep(sleeptime)
    
if __name__ == "__main__":
    print("这里使用本机adb模式,此模式执行效率更高并且耗电更低，但如果无法使用请先root下执行wifidebug.sh,再重启termux")
    print("请先调整到QQ页面,输入法调整为ADB Keyboard,你还有15秒钟时间")
    time.sleep(wait)
    print("开始执行")
    battery = os.popen("adb -s "+device+" shell dumpsys battery").read().split("\n")
    battstart = battery[10].split(" ")[-1]
    battall = [battstart]*12
    while True:
        i = i + 1
        try:
            main(1,0,lev1)
            main(2,10,lev2)
        except Exception as e:
            print(e)
            a = str(e).split(" ")
            exc = ""
            for i in a:
                exc = exc + i + "_"
            ins("FatalError:"+exc)
            ins("@")
            ins("{")
            tap(274,384,100)
            tapsend()
            

        
