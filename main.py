import tkinter.filedialog, os,sys

from models.TerminalClass import Terminal
from models import ReadCSV,FileDIalog
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

start_Date = datetime.date(log_date_min.year,log_date_min.month,log_date_min.day)
End_Date = datetime.date(log_date_max.year,log_date_max.month,log_date_max.day)
print(f"min:{start_Date} max:{End_Date}")

while start_Date < End_Date:
    start_Date = start_Date + datetime.timedelta(days=1)
    print(f"min:{start_Date} max:{End_Date}")

