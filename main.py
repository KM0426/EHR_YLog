import tkinter.filedialog, os,sys

from models.TerminalClass import Terminal
from models import ReadCSV,FileDIalog,CountTime
import datetime
import tkinter.messagebox as messagebox

malutiLogFile = True

terminal_file_name = FileDIalog.OpenFileDialog("瞬快の端末一覧を選択(アクセスログ【yyyymmdd】)",False)
if terminal_file_name == '':
    sys.exit()

ylog_file_name = FileDIalog.OpenFileDialog("Yログファイルを選択(クエリ(Y全て)_yyyymmdd-mmdd)",malutiLogFile)
if ylog_file_name == '':
    sys.exit()

terminals_list = ReadCSV.ReadCSV(terminal_file_name)
ylog_list = ReadCSV.ReadCSV(ylog_file_name)

terminal_dic = {}
for tm in terminals_list:
    terminal_dic[tm[0]] = []

isErrors = False
ErrorMessage = ""
log_date_min = datetime.datetime(year=datetime.MAXYEAR, month=12, day=30, hour=23, minute=59, second=59)
log_date_max = datetime.datetime(year=datetime.MINYEAR, month=1, day=1, hour=0, minute=0, second=0)
for yl in ylog_list:
    if yl[7] not in terminal_dic:
        terminal_dic[yl[7]] = []
    log_datetime = ""
    try:
        log_datetime = datetime.datetime.strptime(yl[0], '%Y/%m/%d %H:%M')
        if log_datetime < log_date_min:
            log_date_min = log_datetime
        if log_datetime > log_date_max:
            log_date_max = log_datetime
    except Exception as e:
        messagebox.showerror("Error",f"{e.__class__.__name__}: {e}")
        isErrors = True
        break
    terminal_dic[yl[7]].append([log_datetime,yl[8]])

if isErrors:
    sys.exit()


for key,val in terminal_dic.items():
    timeTable = CountTime.CountDic(key)
    isLogin = False
    if len(val) > 0:
        if val[0][1] == 'Y1000':
            isLogin = True
        for h in range(0,val[0][0].hour):
            if isLogin:
                timeTable[h] += 1
        for v in val:
            if v[1] == 'Y1000':
                isLogin = True
                timeTable[v[0].hour] += 1
            pass


