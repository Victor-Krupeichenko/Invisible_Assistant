import pystray
import PIL.Image
from settings_env import icon_tray


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

    def click_on_icon(self, icon, item):
        """
        Обработчик клика по иконке в трее
        """
        if str(item) == 'Выход':
            # Остановка основного процесса (предположим, icon.stop() это остановка основного процесса)
            self.starter.stop_program()
            icon.stop()

    def create_icon_tray(self):
        """
        Создание иконки в трее
        """
        create_icon = pystray.Icon(
            name='invisible_assistant',
            icon=self.image,
            title='Invisible Assistant',
            menu=pystray.Menu(pystray.MenuItem(text='Выход', action=self.click_on_icon))
        )
        create_icon.run()
