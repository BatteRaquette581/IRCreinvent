import datetime
import os
from .message import Message
class Logging:
    def __init__(self,path="./logs",dateSeparatorLength=30):
        self.path = path
        if not os.path.exists(path):
            os.mkdir(path)
        self.dateSeparatorLength = dateSeparatorLength

    def log(self,message:str | Message):
        print(str(message),file=open(f'{self.path}/log-{datetime.date.today().strftime("%d-%m-%Y")}.log',"a"))

    def getLatestMessages(self,n=30):
        logfiles = self.__getLogFiles()
        messages = []
        for file in logfiles:
            if len(messages)>=n: break
            messages.append(self.__addDateSeparator(file,self.dateSeparatorLength))
            messages += self.__getLinesFromLogFile(os.path.join(self.path,file),n-len(messages))
        return messages
    
    def __addDateSeparator(self,filename :str,length=30):
        return format(self.__getDateFromFilename(filename), '-^'+str(length))+"\n"

    def __getDateFromFilename(self,filename:str):
        return filename[4:-4] # filename[4:-4]: log-01-23-4567.log -> 01-23-4567
    
    def __getLinesFromLogFile(self,filename:str,n):
        messages = []
        with open(filename,"r") as f:
            [messages.append(line) for line in f if len(messages)<n]
        return messages

    def __getLogFiles(self):
        return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
