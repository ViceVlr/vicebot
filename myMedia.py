# -----------------------------------------------------------------------
class film:
    def __init__(self, name, buttons=None, parent=None, action=None):
        self.kinopoiskID = ""  # ID на сайте КиноПоиск
        self.imdbID = ""  # ID на сайте IMDB
        self.name = ""  # Наименование (оригинальное)
        self.nameRUS = ""  # Наименование-RUS
        self.nameENG = ""  # Наименование-ENG
        self.coverURL = ""  # Обложка_url 
        self.year = ""  # Год
        self.countries = ""  # Страны (списо)
        self.genres = ""  # Жанры (список)
        self.duration = ""  # Продолжительность
        self.director = ""  # Режиссёр
        self.actors = ""  # Актёры (список)
        self.trailerURL = ""  # Трейлер_url
        self.onlineURL = ""  # фильм_url

    # -----------------------------------------------------------------------

    def getRandomFilm(self):
        import requests
        import bs4

        req_film = requests.post("https://mc.yandex.ru/watch/22663942?page-url=btn://www.kinopoisk.ru/?p=PA1A2A1AA2%C2%89&ty=button&page-ref=https://www.kinopoisk.ru/chance/&charset=utf-8&browser-info=ar:1:gdpr:13-0:vf:7oivoclvhnrnrlctj3z:fu:3:en:utf-8:la:ru-RU:v:760:cn:1:dp:1:ls:309502594847:hid:847542542:z:180:i:20220321182147:et:1647876108:c:1:rn:785773250:rqn:82:u:1621317942202710756:w:382x969:s:1920x1080x24:sk:1:cpf:1:eu:0:ns:1647876072279:wv:2:co:0:adb:1:pp:3629563401:rqnl:1:st:1647876108:t:Случайный фильм!&t=gdpr(13-0)mc(p-8)lt(116200)aw(1)ti(0)&force-urlencoded=1")
        # "https://www.kinopoisk.ru/search/?query={searchTerms}"

        url = "https://www.kinopoisk.ru/chance/"
        "movieBlock _NO_HIGHLIGHT_"

        req_film = requests.get(url)
        soup = bs4.BeautifulSoup(req_film.text, "html.parser")
        result_find = soup.find('div', align="center", style="width: 100%")
        infoFilm["Наименование"] = result_find.find("h2").getText()
        names = infoFilm["Наименование"].split(" / ")
        infoFilm["Наименование_rus"] = names[0].strip()
        if len(names) > 1:
            infoFilm["Наименование_eng"] = names[1].strip()

        images = []
        for img in result_find.findAll('img'):
            images.append(url + img.get('src'))
        infoFilm["Обложка_url"] = images[0]

        details = result_find.findAll('td')
        infoFilm["Год"] = details[0].contents[1].strip()
        infoFilm["Страна"] = details[1].contents[1].strip()
        infoFilm["Жанр"] = details[2].contents[1].strip()
        infoFilm["Продолжительность"] = details[3].contents[1].strip()
        infoFilm["Режиссёр"] = details[4].contents[1].strip()
        infoFilm["Актёры"] = details[5].contents[1].strip()
        infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
        infoFilm["фильм_url"] = url + details[7].contents[0]["href"]
