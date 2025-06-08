class Server:
    def __init__(self):
        self.buffer = []
        self.ip = None

    def send_data(self, data):
        router.send_data(data)

    def get_data(self):
        result = self.buffer.copy()
        self.buffer.clear()
        return result

    def get_ip(self):
        return self.ip


class Router:
    def __init__(self):
        self.servers = {}
        self.buffer = []

    def link(self, server):
        server.ip = len(self.servers) + 1
        self.servers[server.ip] = server

    def unlink(self, server):
        if server.ip in self.servers:
            del self.servers[server.ip]
            server.ip = None

    def send_data(self):
        for data in self.buffer:
            if data.ip in self.servers:
                self.servers[data.ip].buffer.append(data)
        self.buffer.clear()



class Data:
    def __init__(self, data, ip):
        self, data = data
        self.ip = ip


#Проверка
router = Router()
sv_from = Server()
sv_from2 = Server()
router.link(sv_from)
router.link(sv_from2)
router.link(Server())
router.link(Server())
sv_to = Server()
router.link(sv_to)
sv_from.send_data(Data("Hello", sv_to.get_ip()))
sv_from2.send_data(Data("Hello", sv_to.get_ip()))
sv_to.send_data(Data("Hi", sv_from.get_ip()))
router.send_data()
msg_lst_from = sv_from.get_data()
msg_lst_to = sv_to.get_data()