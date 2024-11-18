def branchYCode(ycode):
    LoginY = ['Y0000','Y0001','Y0002','Y0003','Y3000']
    ScreenON = ['Y2010','Y2011']
    Logooff = ['Y1000','Y1001','Y1002','Y1003','Y1004','Y1005','Y1006','Y1007','Y1008','Y1009','Y1010','Y2100','Y2101','Y2104','Y0116']
    ScreenOFF =['Y2000','Y2001']
    if ycode in LoginY:
        return 'IN'
    elif ycode in Logooff:
        return 'OUT'
    elif ycode in ScreenON:
        return 'ScreenON'
    elif ycode in ScreenOFF:
        return 'ScreenOFF'
    else:
        return 'OT'
