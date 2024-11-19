import sys,datetime
import numpy as np
import tkinter.messagebox as messagebox
from models import ReadCSV,FileDIalog,CountTime
from models.YCodeBranch import branchYCode

def fileSelect(label):
    print("ファイル選択ダイアログでファイルを選択してください...（瞬快の端末一覧を選択(アクセスログ【yyyymmdd】)")
    return FileDIalog.OpenFileDialog("瞬快の端末一覧を選択(アクセスログ【yyyymmdd】)",False)


malutiLogFile = True

terminal_file_name = fileSelect("ファイル選択ダイアログでファイルを選択してください...（瞬快の端末一覧を選択(アクセスログ【yyyymmdd】)")
if terminal_file_name == '':
    sys.exit()

ylog_file_name = fileSelect("ファイル選択ダイアログでファイルを選択してください...（クエリ(Y全て)_yyyymmdd-mmdd)")
if ylog_file_name == '':
    sys.exit()

print("ファイルを読み込んでいます...")
terminals_list = ReadCSV.ReadCSV(terminal_file_name)
ylog_list = ReadCSV.ReadCSV(ylog_file_name)

terminal_place_dic = {}
for tm in terminals_list:
    terminal_place_dic[tm[0]] = tm[1]

terminal_dic = {}
for tm in terminals_list:
    terminal_dic[tm[0]] = []

isErrors = False
ErrorMessage = ""

print("データをDictionaryに加工中...")
for yl in ylog_list:
    if yl[7] not in terminal_dic:
        terminal_dic[yl[7]] = []
        terminal_place_dic[yl[7]] = "空白"
    log_datetime = ""
    try:
        log_datetime = datetime.datetime.strptime(yl[0], '%Y/%m/%d %H:%M')
    except Exception as e:
        print("Error",f"{e.__class__.__name__}: {e}")
        messagebox.showerror("Error",f"{e.__class__.__name__}: {e}")
        isErrors = True
        break
    terminal_dic[yl[7]].append([log_datetime,branchYCode(yl[8])])

if isErrors:
    sys.exit()

CalcCounts = []
header = ['端末番号','名称']
for h in range(0,24):
    header.append(str(h)+"時")

CalcCounts.append(header)

print("データ解析・集計しています...")
for key,val in terminal_dic.items():
    list_countTime = []
    isLogin = False

    if len(val) > 0:
        base_countTime = CountTime.CountDic(key)
        base_countTime.timeTable[1] = terminal_place_dic[key]
        tmpStartHour = 0
        if val[0][1] == 'OUT' or val[0][1] == 'ScreenON':
            isLogin = True

        currentDateTime = datetime.datetime(val[0][0].year,val[0][0].month,val[0][0].day,0,0,0)
        countTime = CountTime.CountDic(key)
        for v in val:
            if key == "KHDT0001" and v[0].hour == 8:
                pass
            if isLogin:
                temp = currentDateTime
                while int(str(temp.year)+str(temp.month)+str(temp.day)+str(temp.hour)) <= int(str(v[0].year)+str(v[0].month)+str(v[0].day)+str(v[0].hour)) :
                    countTime.timeTable[temp.hour+2] = 1
                    temp = temp + datetime.timedelta(hours=1)
                    pass
                currentDateTime = v[0]
                pass
            if int(str(currentDateTime.year)+str(currentDateTime.month)+str(currentDateTime.day)) != int(str(v[0].year)+str(v[0].month)+str(v[0].day)):
                list_countTime.append(countTime.timeTable)
                countTime = CountTime.CountDic(key)
            countTime.timeTable[1] = terminal_place_dic[key]

            if v[1] == 'IN':
                isLogin = True
                countTime.timeTable[v[0].hour+2] = 1
            elif v[1] == 'ScreenOFF':
                isLogin = True
                countTime.timeTable[v[0].hour+2] = 1
            elif v[1] == 'OUT':
                isLogin = False
                countTime.timeTable[v[0].hour+2] = 1
            elif v[1] == 'ScreenON':
                isLogin = False
                countTime.timeTable[v[0].hour+2] = 1
            else:
                isLogin = False
                pass
            currentDateTime = v[0]
        list_countTime.append(countTime.timeTable)    
        for i in range(0,len(list_countTime)):
            for j in range(2,len(list_countTime[0])-2):
                base_countTime.timeTable[j] += list_countTime[i][j]

        CalcCounts.append(base_countTime.timeTable)
    pass

print("ファイルに書き出しています...")
with open("outnp.csv", "w", encoding="utf-8-sig", newline="") as f:
    np.savetxt(f, CalcCounts, delimiter=",", fmt='%s')
print("完了しました！")
input("エンターを入力するか、コンソールを閉じて終了してください")


def main():

    return

main()