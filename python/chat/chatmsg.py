import json
import datetime

class message:
    def __init__(self, frm, to, text, time=datetime.datetime.now()):
        self.frm=frm
        self.to=to
        self.text=text
        self.time=time

    def to_json(self):
         return json.dumps(self.to_dict())

    def __repr__(self):
        return f'{str(self.time)} {self.frm}->{self.to}: {self.text}'

    def to_dict(self):
        return {
        "from":self.frm,
        "to":self.to,
        "text":self.text,
        "time":str(self.time)}

def message_from_dict(o)->message:
    return message(o["from"],o["to"],o["text"],
            datetime.datetime.fromisoformat(o["time"]))

