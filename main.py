import tkinter.filedialog, os,sys

from models.TerminalClass import Terminal
from models import ReadCSV,FileDIalog,CountTime
import datetime
import tkinter.messagebox as messagebox
from models.YCodeBranch import branchYCode
import pandas as pd
import csv
import numpy as np

malutiLogFile = True

terminal_file_name = FileDIalog.OpenFileDialog("瞬快の端末一覧を選択(アクセスログ【yyyymmdd】)",False)
if terminal_file_name == '':
    sys.exit()

ylog_file_name = FileDIalog.OpenFileDialog("Yログファイルを選択(クエリ(Y全て)_yyyymmdd-mmdd)",malutiLogFile)
if ylog_file_name == '':
    sys.exit()

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
log_date_min = datetime.datetime(year=datetime.MAXYEAR, month=12, day=30, hour=23, minute=59, second=59)
log_date_max = datetime.datetime(year=datetime.MINYEAR, month=1, day=1, hour=0, minute=0, second=0)
for yl in ylog_list:
    if yl[7] not in terminal_dic:
        terminal_dic[yl[7]] = []
        terminal_place_dic[yl[7]] = "空白"
    log_datetime = ""
    try:
        log_datetime = datetime.datetime.strptime(yl[0], '%Y/%m/%d %H:%M')
    except Exception as e:
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
for key,val in terminal_dic.items():

    base_countTime = CountTime.CountDic(key)
    base_countTime.timeTable[1] = terminal_place_dic[key]
    list_countTime = []
    isLogin = False
    if len(val) > 0:
        tmpStartHour = 0
        if val[0][1] == 'OUT' or val[0][1] == 'ScreenON':
            isLogin = True

        currentDateTime = datetime.datetime(val[0][0].year,val[0][0].month,val[0][0].day,0,0,0)

        for v in val:
            countTime = CountTime.CountDic(key)
            countTime.timeTable[1] = terminal_place_dic[key]
            if isLogin:
                while currentDateTime < v[0]:
                    countTime.timeTable[v[0].hour+2] = 1
                    currentDateTime = v[0]
                pass
            if v[1] == 'IN':
                isLogin = True
            elif v[1] == 'ScreenOFF':
                isLogin = True
            elif v[1] == 'OUT':
                isLogin = False
                countTime.timeTable[v[0].hour+2] = 1
            elif v[1] == 'ScreenON':
                isLogin = False
                countTime.timeTable[v[0].hour+2] = 1
            else:
                pass
            currentDateTime = v[0]
            list_countTime.append(countTime.timeTable)
        for i in range(0,len(list_countTime)):
            for j in range(2,len(list_countTime[0])-2):
                base_countTime.timeTable[j] += list_countTime[i][j]
    CalcCounts.append(base_countTime.timeTable)
    pass

np.savetxt("outnp.csv", CalcCounts, delimiter=",", fmt='%s')