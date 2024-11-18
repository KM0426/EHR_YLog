class CountDic:
    def __init__(self,input_name) -> None:
        self.timeTable = []
        self.timeTable.append(input_name)
        for i in range(24+1):
            self.timeTable.append(0)