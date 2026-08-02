import npyscreen

# --- Общие данные (имитация контента сайта) ---
GTNH_DATA = {
    "mods": [
        {"name": "GregTech", "category": "Core", "status": "Stable"},
        {"name": "IndustrialCraft2", "category": "Energy", "status": "Stable"},
        {"name": "Thaumcraft", "category": "Magic", "status": "Experimental"},
        {"name": "Applied Energistics 2", "category": "Storage", "status": "Stable"},
    ],
    "guides": [
        {"title": "Начало игры", "steps": ["Создать мир", "Выбрать сборку", "Первые машины"]},
        {"title": "Энергетика", "steps": ["Паровые машины", "Ядерные реакторы", "Передача энергии"]},
    ],
    "links": [
        {"label": "Discord", "url": "https://discord.gg/..."},
        {"label": "Wiki", "url": "https://wiki.gtnh.net"},
        {"label": "Форум", "url": "https://forum.gtnh.com"},
    ]
}


# --- Форма: список модов (аналог страницы Mods) ---
class ModsForm(npyscreen.Form):
    def create(self):
        self.name = "GTNH — Моды"
        self.add(npyscreen.TitleText, name="Статус сборки:", value="GTNH 2.8.x (Stable)", editable=False, rely=2, relx=2)
        self.add(npyscreen.TitleFixedText, name="Список модов:", rely=4, relx=2)

        # Простой список в виде TitleText (в npyscreen нет нативных таблиц)
        for i, mod in enumerate(GTNH_DATA["mods"]):
            line = f"{mod['name']} | {mod['category']} | {mod['status']}"
            self.add(
                npyscreen.TitleText,
                name=f"  {i+1}.",
                value=line,
                editable=False,
                rely=6 + i,
                relx=2,
                max_width=80
            )

        btn_back = self.add(
            npyscreen.ButtonPress,
            name="← Назад в меню",
            rely=len(GTNH_DATA["mods"]) + 8,
            relx=2,
            when_pressed_function=self.on_back
        )

    def on_back(self):
        self.parentApp.switchForm("MAIN")


# --- Форма: гайды (аналог страницы Guides) ---
class GuidesForm(npyscreen.Form):
    def create(self):
        self.name = "GTNH — Гайды"
        self.add(npyscreen.TitleFixedText, name="Доступные гайды:", rely=2, relx=2)

        for i, guide in enumerate(GTNH_DATA["guides"]):
            # Заголовок гайда
            self.add(
                npyscreen.TitleText,
                name=f"{i+1}. {guide['title']}",
                editable=False,
                rely=4 + i * 3,
                relx=4
            )
            # Шаги гайда
            for j, step in enumerate(guide["steps"]):
                self.add(
                    npyscreen.TitleText,
                    name=f"   • {step}",
                    editable=False,
                    rely=5 + i * 3 + j,
                    relx=6,
                    max_width=70
                )

        btn_back = self.add(
            npyscreen.ButtonPress,
            name="← Назад в меню",
            rely=len(GTNH_DATA["guides"]) * 3 + 6,
            relx=2,
            when_pressed_function=self.on_back
        )

    def on_back(self):
        self.parentApp.switchForm("MAIN")


# --- Форма: ссылки (аналог блока Links/Social) ---
class LinksForm(npyscreen.Form):
    def create(self):
        self.name = "GTNH — Ссылки"
        self.add(npyscreen.TitleFixedText, name="Полезные ссылки:", rely=2, relx=2)

        for i, link in enumerate(GTNH_DATA["links"]):
            self.add(
                npyscreen.TitleText,
                name=f"{link['label']}: {link['url']}",
                editable=False,
                rely=4 + i,
                relx=4,
                max_width=90
            )

        btn_back = self.add(
            npyscreen.ButtonPress,
            name="← Назад в меню",
            rely=len(GTNH_DATA["links"]) + 6,
            relx=2,
            when_pressed_function=self.on_back
        )

    def on_back(self):
        self.parentApp.switchForm("MAIN")


# --- Главное меню (аналог главной страницы/навигации сайта) ---
class MainMenuForm(npyscreen.Form):
    def create(self):
        self.name = "GTNH TUI — Главное меню"
        self.add(npyscreen.FixedText, value="GregTech New Horizons — консольный интерфейс", rely=2, relx=2)
        self.add(npyscreen.FixedText, value="(адаптировано из shadowtheage.github.io/gtnh)", rely=3, relx=2)
        self.add(npyscreen.FixedText, value="", rely=4, relx=2)

        # self.btn_mods = self.add(
        #     npyscreen.ButtonPress,
        #     name="[1] Моды",
        #     rely=5, relx=4,
        #     when_pressed_function=self.to_mods
        # )
        # self.btn_guides = self.add(
        #     npyscreen.ButtonPress,
        #     name="[2] Гайды",
        #     rely=7, relx=4,
        #     when_pressed_function=self.to_guides
        # )
        # self.btn_links = self.add(
        #     npyscreen.ButtonPress,
        #     name="[3] Ссылки",
        #     rely=9, relx=4,
        #     when_pressed_function=self.to_links
        # )
        # self.add(
        #     npyscreen.ButtonPress,
        #     name="[0] Выход",
        #     rely=11, relx=4,
        #     when_pressed_function=self.exit_app
        # )

    def to_mods(self):
        self.parentApp.switchForm("MODS")

    def to_guides(self):
        self.parentApp.switchForm("GUIDES")

    def to_links(self):
        self.parentApp.switchForm("LINKS")

    def exit_app(self):
        self.parentApp.setNextForm(None)


class GTNHApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", MainMenuForm)
        # self.registerForm("MODS", ModsForm)
        # self.registerForm("GUIDES", GuidesForm)
        # self.registerForm("LINKS", LinksForm)


if __name__ == "__main__":
    GTNHApp().run()
