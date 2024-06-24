from datetime import datetime
from typing import List

class start_dispositives():
    type: str
    name: str
    date: datetime

    def __init__(self, name:str, type: str):
        self.type = type
        self.name = name
        self.date = datetime.now()
        
    def toSave(self):
        return {"type": self.type ,"name": self.name, "date": self.date.strftime('%d/%m/%Y %H:%M:%S')}
