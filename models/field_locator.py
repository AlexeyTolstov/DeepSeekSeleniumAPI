class FieldLocator:
    """ Хранит локализованные ключевые слова для поиска полей ввода на веб-странице. """

    def __init__(self, lang: str, phone_email: str, password: str, log_in: str, msg_deepseek: str):
        self.lang = lang
        self.phone_email = phone_email
        self.password = password
        self.log_in = log_in
        self.msg_deepseek = msg_deepseek


field_locators_RU = FieldLocator(
    lang="ru",
    phone_email="Номер телефона / адрес электронной почты",
    password="Пароль",
    log_in="Войти",
    msg_deepseek="Сообщение для "
)

field_locators_EN = FieldLocator(
    lang="en",
    phone_email="Phone number / email address",
    password="Password",
    log_in="Log in",
    msg_deepseek="Message "
)