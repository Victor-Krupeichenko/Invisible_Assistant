import pystray
import PIL.Image
from settings_env import icon_tray, exit_program


class IconTray:
    """
    Класс для работы с иконкой в трее
    """

    def __init__(self, starter, icon=icon_tray):
        """
        Инициализация иконки в трее
        :param starter: Основной процесс, который будет завершен при нажатии на иконку в трее
        :param icon: Путь к иконке в формате PNG
        """
        self.starter = starter
        self.image = PIL.Image.open(icon)

    def click_on_icon(self, close_process, item):
        """
        Обработчик клика по иконке в трее
        :param close_process: процесс, который нужно будет закрыть
        :param item: раздел 'выход' появляющегося меню над иконкой
        """
        if str(item).lower() == exit_program:
            # Остановка основного процесса (предположим, icon.stop() это остановка основного процесса)
            self.starter.stop_program()
            close_process.stop()

    def create_icon_tray(self):
        """
        Создание иконки в трее
        """
        create_icon = pystray.Icon(
            name='invisible_assistant',
            icon=self.image,
            title='Invisible Assistant',
            menu=pystray.Menu(pystray.MenuItem(text=exit_program.upper(), action=self.click_on_icon))
        )
        create_icon.run()
