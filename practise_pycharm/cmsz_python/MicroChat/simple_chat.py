# -*- encoding: utf-8 -*-
import socket, asyncore
from asyncore import dispatcher
from asynchat import async_chat

__author__ = 'Scholegance'
__metaclass__ = type

PORT = 5005
NAME = 'Alien Chat Room'
BACKLOG = 5


class EndSession(Exception):
    pass


class ChatSession(async_chat):
    """
    处理服务器与用户时间的连接
    """
    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator('\r\n')
        self.data = []
        self.myself = False
        self.name = None
        self.room = None
        # 在 asyn_chat 对象中写入数据，使用 push() 方法
        self.push('Welcome to %s\r\n' % self.server.name)

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        """
        如果读到终止对象，上面设置的set_terminator('\r\n')，说明读完了一行
        将其广播给所有人
        """
        line = ''.join(self.data)
        self.data = []
        self.myself = True
        self.server.broadcast(line)

    def handle_close(self):
        async_chat.handle_close(self)
        self.server.disconnect(self)


class ChatServer(dispatcher):
    """
    接收连接，并产生会话，并能够处理其他会话的广播
    """
    def __init__(self, port, name, backlog):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(backlog)
        self.name = name
        self.sessions = []

    def disconnect(self, session):
        self.sessions.remove(session)

    def broadcast(self, data):
        for session in self.sessions:
            if session.myself:
                session.myself = False
                continue
            else:
                session.push(data + '\r\n')

    def handle_accept(self):
        conn, addr = self.accept()
        self.sessions.append(ChatSession(self, conn))       # 此处的 self 指的是 server


if __name__ == '__main__':
    sock = ChatServer(PORT, NAME, BACKLOG)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print
