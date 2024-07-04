import json
import zmq
import chatmsg
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description='Chat client')
    parser.add_argument('-u', '--user', action='store',
                        default="Nemo",
                        help='User name')
    parser.add_argument('-s', '--server', action='store',
                        default="tcp://localhost:7778",
                        help='Chat server URL')
    return parser.parse_args()

class client:
    def __init__(self,name, url):
        self.name=name
        self.context=context = zmq.Context()
        self.socket=self.context.socket(zmq.REQ)
        self.socket.connect(url)
        req={"request":"hello","username":self.name}
        self.write(req)

    def write(self,req):
        data=json.dumps(req)
        self.socket.send(data.encode("utf-8"))
        resp=self.socket.recv()
        return json.loads(resp.decode('utf-8'))

    def push(self):
        user_input = input("Enter a message: ")
        space_idx = user_input.find(" ")
        username = user_input[:space_idx]
        message_text = user_input[space_idx + 1:]
        msg = chatmsg.message(self.name, username, message_text)
        req={"request":"push","message":msg.to_dict()}
        self.write(req)

    def pop(self):
        req={"request":"pop","username":self.name}
        resp=self.write(req)
        lst=[]
        for d in resp:
            lst.append(chatmsg.message_from_dict(d))
        return lst

def main(args):
    clnt=client(args.user, args.server)
    print(f'{clnt.name} connected to {args.server}')

    while True:
        for msg in clnt.pop():
            print(f'{msg.frm} {msg.time.strftime("%y.%m.%d %H:%M")}: {msg.text}')
        clnt.push()

if __name__ == "__main__":
    try:
        main(parse_args())
    except KeyboardInterrupt:
        print('')
