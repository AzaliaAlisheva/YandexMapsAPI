import tkinter as tk
from tkinter import ttk
from urllib import request
from PIL import Image, ImageTk
import requests


class Application(tk.Frame):
    entry: tk.Entry
    map_canvas: tk.Canvas
    w_canvas: tk.Canvas
    photo: tk.PhotoImage
    position: str
    lang = 'ru'
    reg = 'RU'
    dictLng: {}
    dictUn: {}

    def __init__(self, root=None):
        super().__init__(root)
        self.window = root
        self.window.title("AzaliaMaps")
        self.window.geometry("500x600")

    def create_canvas(self, canvas_width, canvas_height):
        my_canvas = tk.Canvas(self.window, height=canvas_height, width=canvas_width)
        return my_canvas

    def create_image(self, url, canvas):
        image = request.urlopen(url).read()
        self.photo = tk.PhotoImage(data=image)
        canvas.create_image(0, 0, anchor='nw', image=self.photo)

    def create_combobox_lang(self):
        languages = ["английский", "украинский", "русский", "турецкий"]
        self.create_dict_lng()
        self.combo = tk.ttk.Combobox(self.window, values=languages)
        self.combo.bind("<<ComboboxSelected>>", self.lang_changed)
        self.combo.pack()

    def create_combobox_units(self):
        units = ["мили", "метры"]
        self.create_dict_un()
        self.combo2 = tk.ttk.Combobox(self.window, values=units)
        if self.lang != "en":
            self.combo2.bind("<<state>>", 'disabled')
        else:
            self.combo2.bind("<<ComboboxSelected>>", self.unit_changed)
        self.combo2.pack()

    def create_dict_lng(self):
        self.dictLng = {'английский': 'en', 'украинский': 'uk', 'русский': 'ru', 'турецкий': 'tr'}

    def create_dict_un(self):
        self.dictUn = {'мили': 'US', 'метры': 'RU'}

    def create_entry(self):
        self.entry = tk.Entry(self.window, width="50")
        self.entry.pack(pady=10)

    def create_scale(self):
        self.sc = tk.Scale(self.window, orient="horizontal", resolution=1, from_=3, to=18, )
        self.sc.set(16)
        self.sc.bind("<<command>>", self.sc_move)
        self.sc.pack()

    def create_button(self):
        button = tk.Button(text="Показать", command=self.click_button)
        button.pack(pady=10)

    def lang_changed(self, event):
        self.lang = self.dictLng[self.combo.get()]
        print(self.lang)
        if self.lang == 'tr':
            self.reg = 'TR'
        elif self.lang == 'uk':
            self.reg = 'UA'
        elif self.lang == 'ru':
            self.reg = 'RU'

    def unit_changed(self, event):
        self.reg = self.dictUn[self.combo2.get()]
        print(self.reg)

    def click_button(self):
        self.position = self.geocoder(self.entry.get())
        # self.weather(p[0], p[1])
        self.show_map(self.position, self.sc.get())

    def sc_move(self, event):
        self.show_map(self.position, self.sc.get())

    def geocoder(self, pl):
        params = {"apikey": "1169a4b9-d994-409b-9520-bcad05f2020f",
                  "geocode": pl,
                  "format": "json"
                  }
        url = "https://geocode-maps.yandex.ru/1.x/"
        try:
            response = requests.get(url, params=params)
            if response:
                pos = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'][
                    'pos']
                coords = pos.split()
                return coords
            else:
                label = tk.Label(text="Ошибка выполнения запроса: url")
                label.pack()
                label2 = tk.Label(text=f"Http статус: {response.status_code} ({response.reason})")
                label2.pack()
        except:
            label = tk.Label(text="Запрос не удалось выполнить. Проверьте подключение к сети Интернет.")
            label.pack()

    def show_map(self, pos, z):
        if pos is None:
            return
        else:
            params = {"l": "map",
                      "ll": f"{pos[0]},{pos[1]}",
                      "z": z,
                      "size": "400,400",
                      "lang": f"{self.lang}_{self.reg}",
                      "pt": f"{pos[0]},{pos[1]},pmwtm1"
                      }
            url = "https://static-maps.yandex.ru/1.x"
            response = requests.get(url, params=params)
            self.create_image(response.url, self.map_canvas)

    def weather(self, lat, lon):
        params = {"lat": lat,
                  "lon": lon
                  }
        headers = {'X-Yandex-API-Key': '8ca46753-c778-4a18-a8f7-fb5efa72d9e4'
                   }
        url = "https://api.weather.yandex.ru/v2/forecast/"
        response = requests.get(url, params=params, headers=headers)
        icon = response.json()["fact"]["icon"]
        pic = f"https://yastatic.net/weather/i/icons/blueye/color/svg/{icon}.svg"
        self.create_image(pic, self.w_canvas)
        print()


def main():
    root = tk.Tk()
    app = Application(root=root)
    app.create_entry()
    app.create_scale()
    app.create_combobox_lang()
    app.create_combobox_units()
    app.create_button()
    app.w_canvas = app.create_canvas(50, 50)
    # app.w_canvas.pack(pady=10)
    app.map_canvas = app.create_canvas(400, 400)
    app.map_canvas.pack(pady=10)

    root.mainloop()


if __name__ == '__main__':
    main()
