from .bot_base_menu import MenuProtocol


class VerifyManagerMenu(MenuProtocol):
    def __init__(self,stock,pending_clients):
        super(VerifyManagerMenu, self).__init__(stock)

        self.pending_clients = pending_clients

        self.reply_msg = str(pending_clients)


    def show(self):
        return self.reply_msg

    def handle(self, bot, message,sender,context) -> str:
        ...


