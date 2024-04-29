import time

class Timings:
    def __init__(self) -> None:
        self.records = []
        self.startTime: float = None
    
    def start(self):
        self.startTime = time.time()
    
    def finish(self):
        if self.startTime != None:
            self.records.append(time.time() - self.startTime)
            self.startTime = None
    
    def abort(self):
        self.startTime = None
    
    def getMax(self): return max(self.records)
    def getMin(self): return min(self.records)
    def getSum(self): return sum(self.records)
    def getLen(self): return len(self.records)
    def getAvg(self): return self.getSum() / self.getLen()

    def getList(self): return self.records

    def print(self): print("(max/min/avg/sum)", self.getMax(), self.getMin(), self.getAvg(), self.getSum())
    def printList(self): print(self.records)