import json
import zmq
import datetime
import chatmsg
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description='Chat server')
    parser.add_argument('-a', '--address', action='store',
                        default="tcp://*:7778",
                        help='Chat server bind address')
    return parser.parse_args()

class server:
    def __init__(self,url):
        self.messages={} # user -> list of messages
        self.context=context = zmq.Context()
        self.socket=self.context.socket(zmq.REP)
        self.socket.bind(url)
        self.log(f'Chat server started at {self.socket.last_endpoint.decode('utf-8')}')

    def read(self):
        msg = self.socket.recv()
        return json.loads(msg.decode('utf-8'))

    def write(self,data):
        self.socket.send(json.dumps(data).encode("utf-8"))

    def responce(self, s):
        resp = {"responce":s}
        self.write(resp)

    def log(self, logmsg):
        dt=datetime.datetime.now()
        print(f'{dt.strftime("%y.%m.%d %H:%M")} {logmsg}')

    def start(self):
        while True:
            request = self.read()
            request_type = request['request']
            if request_type == 'hello':
                username=request['username']
                self.log(f'{username} connected')
                self.responce('ok')
            elif request_type == 'pop':
                username=request['username']
                msg_list=[]
                if username in self.messages:
                    for m in self.messages[username]:
                        msg_list.append(m.to_dict())
                self.write(msg_list)
                self.messages[username]=[]
                self.log(f'{username} pop {len(msg_list)} message(s)')
            elif request_type == 'push':
                msg=request["message"]
                msg=chatmsg.message_from_dict(request["message"])
                if msg.to not in self.messages:
                    self.messages[msg.to]=[msg]
                else:
                    self.messages[msg.to].append(msg)
                self.responce('ok')
            else:
                self.responce('ko')

def main(args):
    server(args.address).start()

if __name__ == "__main__":
    try:
        main(parse_args())
    except KeyboardInterrupt:
        print('')
