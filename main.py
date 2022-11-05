import telebot

from menu_models.bot_delete_menu import DeleteMenu
from menu_models.bot_login_menu import LoginMenu
from menu_models import MainMenu, StockManager, StockEditor
from bot_telegram.enums_schemas import MenuState, Status


class MainBot():
    menus = {
        MenuState.main: MainMenu(),
        MenuState.login_menu: LoginMenu(),
        MenuState.delete_menu: DeleteMenu(),
        MenuState.stock_manager: StockManager(),
        MenuState.stock_editor: StockEditor()
    }

    def __init__(self, bot):
        self.menu_state = MenuState.main
        self.menu = self.menus[self.menu_state]
        self.bot = bot

    def updater(self, state):
        if state in self.menus:
            self.menu_state = state
        self.menu = self.menus[self.menu_state]

    def main_handler(self, message):
        action = str(message.json["text"])
        state = self.menu.handle(self.bot, action, message.json['chat']['id'])
        self.updater(state)
        if state != Status.wait:
            self.bot.send_message(message.json['chat']['id'], self.menu.show())


def main():
    Key = "5743628298:AAH6gmGWyO4jGOr0vFxrlcMX8zic79_GCrc"
    bot = telebot.TeleBot(Key)
    app = MainBot(bot)

    @bot.message_handler(func=app.main_handler)
    def wrapper(message): ...

    bot.polling()


if __name__ == '__main__':
    main()
