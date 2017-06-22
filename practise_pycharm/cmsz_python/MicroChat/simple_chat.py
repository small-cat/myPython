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


class CommandHandler:
    """
    简单命令处理程序
    """
    def __init__(self):
        pass

    def unknown(self, session, cmd):
        session.push('Unknown command: %s\r\n' % cmd)

    def handle(self, session, line):
        """
        处理从给定的会话中接受到的行, 除 login 和 logout 外，
        其余均作为普通输入
        """
        if not line.strip():
            return
        parts = line.split(' ', 1) # into two parts
        cmd = parts[0]
        try:
            remain_line = parts[1].strip()  # line 剩余的部分
        except IndexError:
            remain_line = ''
        # 查找处理程序, 只有 login 和 logout 这两个命令
        method = getattr(self, 'do_'+cmd, None)
        try:
            method(session, remain_line)
        except TypeError, e:           # 正常运行，但是抛出了一个 TypeError
            # print e
            method = getattr(self, 'do_default', None)  # 如果在 ChatRoom 中，除 look 和 who 外都是普通输入
            if hasattr(method, '__call__'):
                method(session, line)
            else:       # 若在 LoginRoom 中，除 login 和 logout 外，其余命令不识别
                self.unknown(session, cmd)


class Room(CommandHandler):
    """
    负责基本的命令处理和广播
    """
    def __init__(self, server):
        # CommandHandler.__init__(self)
        self.server = server
        self.sessions = []

    def add(self, session):
        self.sessions.append(session)

    def remove(self, session):
        """
        离开房间
        """
        self.sessions.remove(session)

    def broadcast(self, line):
        for session in self.sessions:
            if session.myself:
                session.myself = False
                continue
            else:
                session.push(line)

    def do_logout(self, session, line):
        """
        logout
        """
        raise EndSession


class LoginRoom(Room):
    """
    为刚连接上的用户准备的房间
    """

    def __init__(self, server):
        Room.__init__(self, server)

    def add(self, session):
        # Room.add(self, session)    # 这句代码，因为 add 方法不是静态的，直接用类调用，会出现 TypeError: unbound
        # method add() must be called with A instance as first argument, 这里直接改成往 sessions 里添加
        self.sessions.append(session)
        # 当用户进入是时，问候
        session.push('Welcome to %s\r\n' % self.server.name)

    def unknown(self, session, cmd):
        session.push('Use "login <nickname>"\r\n')

    def do_login(self, session, line):
        name = line.strip()
        # 确保输入了正确的，不相同的用户名
        if not name:
            session.push('Please enter a name\r\n')
        elif name in self.server.users:
            session.push('The name "%s" is taken\r\n' % name) # push just one argument
            session.push('Please try again\r\n')
        else:
            session.name = name
            session.enter(self.server.main_room)

    def do_info(self,session, line):
        """
        info command to show some information:
        status: unlogin, please login first
        """
        session.push('status: unlogin, please login first.(Type "help" to get more information\r\n)')

    def do_help(self, session, line):
        """
        show help info
        """
        session.push('login <nickname>     login with a nickname\r\n')
        session.push('info                 show information\r\n')
        session.push('help                 show help info\r\n')
        session.push('logout               exit\r\n')


class ChatRoom(Room):

    def __init__(self, server):
        Room.__init__(self, server)

    def add(self, session):
        self.broadcast(session.name + ' has entered room\r\n')
        self.server.users[session.name] = session
        # Room.add(session) # add is not a static function, so this sentence will cause TypeError
        self.sessions.append(session)

    def remove(self, session):
        Room.remove(self, session)
        # 广播有用户离开
        self.broadcast(session.name + ' has left room\r\n')

    """
    def do_say(self, session, line):
        self.broadcast(session.name + ': ' + line + '\r\n')
    """

    def do_default(self, session, line):
        """
        停用 do_say，出了 login 和 logout 命令外，其他都作为普通发言
        """
        self.broadcast(session.name + ': ' + line + '\r\n')

    def do_look(self, session, line):
        """
        查看谁在房间内
        """
        session.push('The following are in this room:\r\n')
        for user in self.sessions:
            session.push(user.name + '\r\n')

    def do_who(self, session, line):
        """
        查看谁登录了
        """
        session.push('The following are logged in:\r\n')
        for name in self.server.users:
            session.push(name + '\r\n')

    def do_info(self, session, line):
        """
        show some information
        """
        session.push('status: login in %s\r\n' % 'Chat Room')
        session.push('nickname: %s\r\n' % session.name)

    def do_help(self, session, line):
        """
        show help information
        """
        session.push('look      show all users in current chat room\r\n')
        session.push('who       show all logined users\r\n')
        session.push('info      show information\r\n')
        session.push('help      show help information\r\n')
        session.push('logout    exit')


class LogoutRoom(Room):
    """
    为单用户准备的房间，只用于将用户从服务器删除
    """
    def add(self, session):
        try:
            del self.server.users[session.name]
        except KeyError:
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
        # 所有的会话都开始于单独的 LoginRoom
        self.enter(LoginRoom(server))

    def enter(self, room):
        """
        从当前房间移除自身，并且将自身加入下一个房间
        第一次进入 LoginRoom，进入之后，在 Room.sessions 中添加了当前session，此时是与 LoginRoom绑定的，这是还没登录，即没
        输入用户名。当输入 login Jack 之后，session 方法获取输入，调用 room.handle，因为 LoginRoom 没有 handle 方法，调用的
        是父类 CommandHandler 的 handle 方法，解析回掉 LoginRoom 中的 do_login 方法，输入用户名作为当前 session 的用户名，
        然后 enter 进入 server.main_room，在 enter 中，首先获取原绑定的 LoginRoom 对象，然后调用 room.remove，这里还是使用
        的父类 Room 的 remove 方法，将当前session 从 server.sessions 中删除，然后将 self.room = room 赋值，将 room 更改为
        server.main_room，及 ChatRoom，并将 ChatRoom 中的 add 方法将当前 session 重新加入到 Room.sessions，此时，这个
        session 绑定的就是 ChatRoom，正式进入了聊天室
        """
        try:
            cur = self.room
        except AttributeError:
            pass
        else:
            cur.remove(self)
        self.room = room
        room.add(self)

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
        try:
            self.room.handle(self, line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))


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
        self.users = {}
        self.main_room = ChatRoom(self)

    def disconnect(self, session):
        self.sessions.remove(session)

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)


if __name__ == '__main__':
    sock = ChatServer(PORT, NAME, BACKLOG)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print
