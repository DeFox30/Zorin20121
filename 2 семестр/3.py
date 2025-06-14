from string import ascii_lowercase, digits


class TextInput:
    CHARS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" + ascii_lowercase
    CHARS_CORRECT = CHARS + CHARS.upper() + digits

    def __init__(self, name, size = 10):
        self.check_name(name)
        self.name = name
        self.size = size

    @classmethod
    def check_name(cls, name):
        if not 3 <= len(name) <= 50 or any(c not in cls.CHARS_CORRECT for c in name):
            raise ValueError("некорректное поле name")

    def get_html(self):
        return f'<p class="login"><имя поля>: <input type="text" size=<размер поля> />'

class PasswordInput:
    CHARS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" + ascii_lowercase
    CHARS_CORRECT = CHARS + CHARS.upper() + digits

    def __init__(self, name, size=10):
        self.check_name(name)
        self.name = name
        self.size = size

    @classmethod
    def check_name(cls, name):
        if not 3 <= len(name) <= 50 or any(c not in cls.CHARS_CORRECT for c in name):
            raise ValueError("некорректное поле name")

    def get_html(self):
        return f'<p class="password"><имя поля>: <input type="text" size=<размер поля> />'


class FormLogin:
    def __init__(self, ign, psw):
        self.login = ign
        self.password = psw

    def render_template(self):
        return "/n".join(['<form action="#">', self.login.get_html(), self.password.get_html(), '</form>'])


login = FormLogin(TextInput("Логин"), PasswordInput("Пароль"))
html = login.render_template()
