class CountDic:
    def __init__(self,input_name) -> None:
        self.timeTable = {}
        for i in range(24):
            self.timeTable[i] = 0