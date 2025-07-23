import datetime
from datetime import date

from core.models.footer import FooterCategory
from core.models.book_image import BookImageType

CATEGORIES = [
    {
        "title": "Добірки Yakaboo",
        "slug": "dobirky-yakaboo",
    },
    {
        "title": "Комплекти книжок",
        "slug": "komplekty-knyzhok"
    },
    {
        "title": "Книги іноземними мовами",
        "slug": "knygy-inozemnymy-movamy",
    },
    {
        "title": "Вибір читачів",
        "slug": "vybir-chytachiv"
    },
    {
        "title": "Художня література",
        "slug": "hudozhnia-literatura"
    },
    {
        "title": "Подарункові книжки",
        "slug": "podarunkovi-knyzhky"
    },
    {
        "title": "Бізнес, гроші, економіка",
        "slug": "biznes-groshi-economica",
    },
    {
        "title": "Саморозвиток. Мотивація",
        "slug": "samorozvytok-motyvatsia"
    },
    {
        "title": "Дитяча література",
        "slug": "dytyacha-literatura"
    },
    {
        "title": "Виховання дітей. Книжки для батьків",
        "slug": "vyhovannia-ditei"
    },
    {
        "title": "Навчальна література. Педагогіка",
        "slug": "pedahohika"
    },
    {
        "title": "Суспільство. Держава. Філософія",
        "slug": "syspilstvo"
    },
    {
        "title": "Історія",
        "slug": "istoriya"
    },
    {
        "title": "Біографії й мемуари",
        "slug": "biographii-i-memuary"
    },
    {
        "title": "Здоров'я. Фітнес. Здорове харчування",
        "slug": "zdorovya-fitnes"
    },
    {
        "title": "Вивчення мов світу",
        "slug": "vyvchennia-mov-svity"
    },
    {
        "title": "Мистецтво. Культура. Фотографія",
        "slug": "mystetstvo"
    },
    {
        "title": "Календарі",
        "slug": "calendari"
    },
    {
        "title": "Журнали",
        "slug": "zhurnaly"
    },
    {
        "title": "Комікси і графічні романи",
        "slug": "komiksy"
    },
    {
        "title": "Комп'ютерна література",
        "slug": "compyterna-literatura"
    },
    {
        "title": "Краса, імідж, стиль",
        "slug": "krasa"
    },
    {
        "title": "Кулінарія. Їжа та напої",
        "slug": "kulinariya"
    },
    {
        "title": "Медична література",
        "slug": "medychna-literatura"
    },
    {
        "title": "Наука і техніка",
        "slug": "nauka-i-tehnika"
    },
    {
        "title": "Право. Юриспруденція",
        "slug": "pravo"
    },
    {
        "title": "Психологія і взаємини",
        "slug": "psyhologiya"
    },
    {
        "title": "Мандри і туризм",
        "slug": "mandry-i-turyzm"
    },
    {
        "title": "Релігії світу",
        "slug": "religii-svity"
    },
    {
        "title": "Спорт і активний відпочинок",
        "slug": "sport-i-aktyvnyi-vidpochynok"
    },
    {
        "title": "Хобі і дозвілля",
        "slug": "hobi-i-dozvillya"
    },
    {
        "title": "Езотерика і окультизм",
        "slug": "ezoteryka-i-okultyzm"
    }
]

SUB_CATEGORIES = [
    {
        "title": "Подих весни: душевне читання для гарного настрою",
        "slug": "podyh-vesny-dushevne-chytannia",
        "category_id": 1
    },
    {
        "title": "Вибрана українська класика",
        "slug": "Vybrana-ukrainska-klasyka",
        "category_id": 1
    },
    {
        "title": "70 мастрідів до Дня детективного роману",
        "slug": "70-mastridiv",
        "category_id": 1
    },
    {
        "title": "Головні англомовні релізи сезон",
        "slug": "holovni-anglomovni-relizy",
        "category_id": 1
    },
    {
        "title": "Хітова манга: класика та бестселери",
        "slug": "hitova-manga",
        "category_id": 1
    },
    {
        "title": "Квітневі промінчики: дітям про весну",
        "slug": "kvitnevi prominchyky",
        "category_id": 1
    },
    {
        "title": "Екранізації 2025",
        "slug": "ekranizatcii-2025",
        "category_id": 1
    },
    {
        "title": "День довкілля - плекаємо Землю разом!",
        "slug": "den-dovkillya",
        "category_id": 1
    },
    {
        "title": "Книги про українських митців та їх художній доробок",
        "slug": "knygy-pro-ukrainskych-mytciv",
        "category_id": 1
    },
    {
        "title": "Вперед до зірок! Книги про космос і космонавтів",
        "slug": "vpered-do-zirok",
        "category_id": 1
    },
    {
        "title": "Книжки про книжки: від романів до нонфікшну",
        "slug": "knyzhky-pro-knyzhky",
        "category_id": 1
    },
    {
        "title": "Англійська",
        "slug": "english",
        "category_id": 3
    },
    {
        "title": "Німецька",
        "slug": "german",
        "category_id": 3
    },
    {
        "title": "Іспанська",
        "slug": "spanish",
        "category_id": 3
    },
    {
        "title": "Французька",
        "slug": "french",
        "category_id": 3
    },
    {
        "title": "Італійська",
        "slug": "italian",
        "category_id": 3
    },
    {
        "title": "Польська",
        "slug": "polish",
        "category_id": 3
    },
    {
        "title": "Арабська",
        "slug": "arabian",
        "category_id": 3
    },
    {
        "title": "Китайська",
        "slug": "chinese",
        "category_id": 3
    },
    {
        "title": "Португальска",
        "slug": "portugal",
        "category_id": 3
    },
    {
        "title": "Турецька",
        "slug": "turkish",
        "category_id": 3
    },
    {
        "title": "Сучасна проза за вибором читачів",
        "slug": "suchasna-proza-za-vyborom-chytachiv",
        "category_id": 4
    },
    {
        "title": "Фантастичні та фентезі книги за вибором читачів",
        "slug": "fantastychni-ta-fentezi-knygy",
        "category_id": 4
    },
    {
        "title": "Дитячі та підліткові книги за вибором читачів",
        "slug": "dytiachi-ta-pidlitkovi-knygy",
        "category_id": 4
    },
    {
        "title": "Книги англійською мовою за вибором читачів",
        "slug": "knygy-anhlijskoy-movoju",
        "category_id": 4
    },
    {
        "title": "Книги афоризмів і цитат",
        "slug": "knygy-aforyzmiv-i-cytat",
        "category_id": 5
    },
    {
        "title": "Книги детективи",
        "slug": "knygy-detektyvy",
        "category_id": 5
    },
    {
        "title": "Книги жанру трилер",
        "slug": "knygy-zhnaru-thriller",
        "category_id": 5
    },
    {
        "title": "Книги жанру бойовик",
        "slug": "knygy-zhanry-bojovyk",
        "category_id": 5
    },
    {
        "title": "П'єси",
        "slug": "pjesy",
        "category_id": 5
    },
    {
        "title": "Книги про середньовіччя",
        "slug": "knygy-pro-seredniovicchia",
        "category_id": 5
    },
    {
        "title": "Романтична проза",
        "slug": "suchasna-proza",
        "category_id": 5
    },
    {
        "title": "Кіноромани і екранізації",
        "slug": "kinoromany-i-ekranizatcii",
        "category_id": 5
    },
    {
        "title": "Класична проза",
        "slug": "klasychna-proza",
        "category_id": 5
    },
    {
        "title": "Книги казок, міфи і фольклор",
        "slug": "knygy-kazok-mifiv",
        "category_id": 5
    },
    {
        "title": "Поезія, збірки віршів",
        "slug": "poezia-zbirky-virshiv",
        "category_id": 5
    },
    {
        "title": "Книги проза",
        "slug": "knygy-proza",
        "category_id": 5
    },
    {
        "title": "Алкоголь і тютюн",
        "slug": "alkohol-i-tjutjun",
        "category_id": 6
    },
    {
        "title": "Бізнес література",
        "slug": "biznes-literatura",
        "category_id": 6
    },
    {
        "title": "Біографії й мемуари",
        "slug": "biografii-i-memuary",
        "category_id": 6
    },
    {
        "title": "Міста і країни",
        "slug": "mista-i-krainy",
        "category_id": 6
    },
    {
        "title": "Історія",
        "slug": "istoriya",
        "category_id": 6
    },
    {
        "title": "Кулінарія",
        "slug": "kulinariya",
        "category_id": 6
    },
    {
        "title": "Релігія",
        "slug": "religia",
        "category_id": 6
    },
    {
        "title": "Спорт",
        "slug": "sport",
        "category_id": 6
    },
    {
        "title": "Бухгалтерія, податки, аудит",
        "slug": "buchgalteriya-podatky-audyt",
        "category_id": 7
    },
    {
        "title": "Життя бізнесмена",
        "slug": "zhuttia-bisnesmena",
        "category_id": 7
    },
    {
        "title": "Економіка",
        "slug": "ekonomika",
        "category_id": 7
    },
    {
        "title": "Галузі і професії",
        "slug": "galuzi-i-profesii",
        "category_id": 7
    },
    {
        "title": "Маркетинг і реклама",
        "slug": "marketyng-i-reklama",
        "category_id": 7
    },
    {
        "title": "Антистрес",
        "slug": "antystres",
        "category_id": 8
    },
    {
        "title": "Тайм-менеджмент",
        "slug": "taim-menedzhment",
        "category_id": 8
    },
    {
        "title": "Страхи і фобії",
        "slug": "strahy-i-fobii",
        "category_id": 8
    },
    {
        "title": "Смерть",
        "slug": "smert",
        "category_id": 8
    },
    {
        "title": "Мета.Мрія",
        "slug": "meta-mriya",
        "category_id": 8
    },
    {
        "title": "Щастя",
        "slug": "schastya",
        "category_id": 8
    },
    {
        "title": "Пригодницькі романи для дітей",
        "slug": "pryhodnytski-romany-dlya-ditei",
        "category_id": 9
    },
    {
        "title": "Дитячі книги про творчість і хобі",
        "slug": "dytyachi-knygy-pro-tvorchist-i-hobi",
        "category_id": 9
    },
    {
        "title": "Альбом малюка",
        "slug": "albom-maluka",
        "category_id": 10
    },
    {
        "title": "Дозвілля і творчість дітей",
        "slug": "dozvillya-i-tvorchist-ditey",
        "category_id": 10
    },
    {
        "title": "Здоров'я дитини",
        "slug": "zdorovya-dytyny",
        "category_id": 10
    },
    {
        "title": "Книги для дошкільнят",
        "slug": "knygy-dlya-doshilnyat",
        "category_id": 11
    },
    {
        "title": "Книги школярам і абітурієнтам",
        "slug": "knygy-shkolyaram-i-abiturientam",
        "category_id": 11
    },
    {
        "title": "Нова українська школа",
        "slug": "nova-ukrainska-shkola",
        "category_id": 11
    },
    {
        "title": "Філософія",
        "slug": "filisofiya",
        "category_id": 12
    },
    {
        "title": "Політика. Держава",
        "slug": "polityka-derzhava",
        "category_id": 12
    },
    {
        "title": "Соціологія",
        "slug": "sociologiya",
        "category_id": 12
    },
    {
        "title": "ЗМІ.Книжкова справа",
        "slug": "zmi-knyshkova-sprava",
        "category_id": 12
    },
    {
        "title": "Статистика. Демографія",
        "slug": "statystyka-demographiya",
        "category_id": 12
    },
    {
        "title": "Африка",
        "slug": 'afryka',
        "category_id": 13
    },
    {
        "title": "Південна Америка",
        "slug": "pivdenna-ameryka",
        "category_id": 13
    },
    {
        "title": "Північна Америка",
        "slug": "pivnichna-ameryka",
        "category_id": 13
    },
    {
        "title": "Азія",
        "slug": "aziya",
        "category_id": 13
    },
    {
        "title": "Австралія й Океанія",
        "slug": "avstraliya-i-okeaniya",
        "category_id": 13
    },
    {
        "title": "Європа",
        "slug": "evropa",
        "category_id": 13
    },
    {
        "title": "Архітектори, художники і фотографи",
        "slug": "architectory-fotography",
        "category_id": 14
    },
    {
        "title": "Бізнес-акули, підприємці, економісти",
        "slug": "bisnes-akuly-pidpryemtsi-ekonomisty",
        "category_id": 14
    },
    {
        "title": "Історичні діячі",
        "slug": "istorychni-diyachi",
        "category_id": 14
    },
    {
        "title": "Друга світова війна. Голокост",
        "slug": "druha-svitova-viyna",
        "category_id": 14
    },
    {
        "title": "Політичні фігури",
        "slug": "politychni-figury",
        "category_id": 14
    },
    {
        "title": "Спортсмени",
        "slug": "sportsmeny",
        "category_id": 14
    },
    {
        "title": "Шкідливі звички",
        "slug": "shkidlyvi-zvychky",
        "category_id": 15
    },
    {
        "title": "Старіння і довголіття",
        "slug": "starinnya-i-dovholittya",
        "category_id": 15
    },
    {
        "title": "Альтернативна медицина",
        "slug": "alternatyvna-medycyna",
        "category_id": 15
    },
    {
        "title": "Масаж",
        "slug": "masazh",
        "category_id": 15
    },
    {
        "title": "Домашнє читання",
        "slug": "domashnye-chytania",
        "category_id": 16
    },
    {
        "title": "Розмовники",
        "slug": "rozmovnyky",
        "category_id": 16
    },
    {
        "title": "Словники",
        "slug": "slovnyky",
        "category_id": 16
    },
    {
        "title": "Теорія й історія мови",
        "slug": "teoriya-i-istoriya-movy",
        "category_id": 16
    },
    {
        "title": "Архітектура",
        "slug": "architektura",
        "category_id": 17
    },
    {
        "title": "Бізнес у мистецтві",
        "slug": "bisness-u-mystectvi",
        "category_id": 17
    },
    {
        "title": "Мода",
        "slug": "moda",
        "category_id": 17
    },
    {
        "title": "Музика",
        "slug": "muzyka",
        "category_id": 17
    },
    {
        "title": "Кіно",
        "slug": "kino",
        "category_id": 17
    },
    {
        "title": "Медіа",
        "slug": "media",
        "category_id": 17
    },
    {
        "title": "Місячний календар",
        "slug": "misyacnyi-calendar",
        "category_id": 18
    },
    {
        "title": "Астрологічний календар",
        "slug": "astrologichnyi-calendar",
        "category_id": 18
    },
    {
        "title": "Манга",
        "slug": "manga",
        "category_id": 20
    },
    {
        "title": "Комікси",
        "slug": "komiksy",
        "category_id": 20
    },
    {
        "title": "Супергерої",
        "slug": "superheroi",
        "category_id": 20
    },
    {
        "title": "Apple",
        "slug": "apple",
        "category_id": 21
    },
    {
        "title": "Microsoft",
        "slug": "microsoft",
        "category_id": 21
    },
    {
        "title": "Бізнес і менеджмент",
        "slug": "bisnes-i-menedzhment",
        "category_id": 21
    },
    {
        "title": "Косметика і парфумерія",
        "slug": "kosmetyka-i-parfumeria",
        "category_id": 22
    },
    {
        "title": "Макіяж і манікюр",
        "slug": "makiyazh-i-manikyr",
        "category_id": 22
    },
    {
        "title": "Випічка",
        "slug": "vypichka",
        "category_id": 23
    },
    {
        "title": "Напої і вино",
        "slug": "napoi-i-vyno",
        "category_id": 23
    },
    {
        "title": "Десерти",
        "slug": "deserty",
        "category_id": 23
    },
    {
        "title": "Ветеринарія",
        "slug": "veterynaria",
        "category_id": 24
    },
    {
        "title": "Внутрішні хвороби",
        "slug": "vnutrishni-chvoroby",
        "category_id": 24
    },
]

SIDEBAR = [
    {
        "title": "Акції",
        "slug": "promo",
        "visible": True,
        "order_number": 1,
    },
    {
        "title": "Сертифікати",
        "slug": "podarunkovi-sertyfikaty",
        "visible": True,
        "order_number": 2,
    },
    {
        "title": "Програма лояльності",
        "slug": "programa-loyalnosti",
        "visible": True,
        "order_number": 3
    },
    {
        "title": "Остання ціна",
        "slug": "ostannia-tsina",
        "visible": True,
        "order_number": 4
    },
    {
        "title": "Друковані книги",
        "slug": "books",
        "visible": True,
        "icon": "/icons/book.svg",
        "order_number": 5
    },
    {
        "title": "Електронні книги",
        "slug": "ebooks",
        "visible": True,
        "icon": "/icons/mobile.svg",
        "order_number": 6
    },
    {
        "title": "Аудіокниги",
        "slug": "audiobooks",
        "visible": True,
        "icon": "/icons/audio.svg",
        "order_number": 7,
    },
    {
        "title": "Настільні ігри",
        "slug": "table-games",
        "visible": True,
        "icon": "/icons/table-games.svg",
        "order_number": 8,
    },
    {
        "title": "Творчість, хобі",
        "slug": "hobby",
        "visible": True,
        "icon": "/icons/art.svg",
        "order_number": 9
    },
    {
        "title": "Книжкові аксесуари",
        "slug": "book-souvenirs",
        "visible": True,
        "icon": "/icons/accessouris.svg",
        "order_number": 10
    },
    {
        "title": "Блокноти",
        "slug": "notes",
        "visible": True,
        "icon": "/icons/notes.svg",
        "order_number": 11
    },
    {
        "title": "Подарунки",
        "slug": "gifts",
        "visible": True,
        "icon": "/icons/gift.svg",
        "order_number": 12
    },
    {
        "title": "Активний відпочинок",
        "slug": "active-rest",
        "visible": True,
        "icon": "/icons/active-rest.svg",
        "order_number": 13
    },
    {
        "title": "Видавництва",
        "slug": "publishing",
        "visible": True,
        "order_number": 14
    }
]

BANNERS = [
    {
        "image_src": "https://static.yakaboo.ua/media/banner/image/120021042025443.jpg",
        "visible": True,
        "link": "/knyzhkovi-mrii"
    },
    {
        "image_src": "https://static.yakaboo.ua/media/banner/image/120011002104253.jpg",
        "visible": True,
        "link": "/do-20-na-knyzhky"
    },
    {
        "image_src": "https://static.yakaboo.ua/media/banner/image/1200144821042511.jpg",
        "visible": True,
        "link": "/flree-delivery"
    },
    {
        "image_src": "https://static.yakaboo.ua/media/banner/image/1200670991529.jpg",
        "visible": True,
        "link": "/cachback"
    },
    {
        "image_src": "https://static.yakaboo.ua/media/banner/image/12002104251142.jpg",
        "visible": True,
        "link": "/rozigrash-sertyfikativ"
    },
    {
        "image_src": 'https://static.yakaboo.ua/media/banner/image/1200X1200_400_400_.png',
        "visible": True,
        "link": "/knyzhkova-kraina"
    }
]

AUTHORS = [
    {
        "first_name": "Джоан",
        "last_name": "Роулінг",
        "slug": "joan-rowling",
        "date_of_birth": date(1965, 7, 31),
        "short_description": """
            Про письменницю Джоан Роулінг не чув хіба глухий. Кожен вихід її нової книжки про юного чарівника 
            Гаррі Поттера викликає неймовірний ажіотаж, б'є всі встановлені раніше рекорди з продажу в 
            літературному світі, а саму письменницю піднімає все вище і вище в рейтингах найбагатших людей 
            то Британії, то світу. Але залишатися довго у таких «хіт-парадах» на перших позиціях Джоан не 
            дозволяють її моральні принципи. Левову часину своїх гонорарів Роулінг жертвує у різні благодійні 
            фонди. Вона чудово пам'ятає час, коли жила на межі бідності й розпачу...
        """,
        "description": """
            Про письменницю Джоан Роулінг не чув хіба глухий. Кожен вихід її нової книжки про юного 
            чарівника Гаррі Поттера викликає неймовірний ажіотаж, б'є всі встановлені раніше рекорди з 
            продажу в літературному світі, а саму письменницю піднімає все вище і вище в рейтингах 
            найбагатших людей то Британії, то світу. Але залишатися довго у таких «хіт-парадах» на 
            перших позиціях Джоан не дозволяють її моральні принципи. Левову часину своїх гонорарів Роулінг 
            жертвує у різні благодійні фонди. Вона чудово пам'ятає час, коли жила на межі бідності й розпачу...
            \n
            Потяги в житті Джоан не раз грали доленосну роль. Почати хоча б з того, що саме вокзал 
            Кінг-Крос Лондона поєднав серця майбутніх батьків Джоан. Її батько Пітер Джеймс Роулінг і мати 
            Енн Волан, познайомилися в потязі по дорозі до Шотландії. У тому 1965 року вони одружилися і 
            переїхали у невелике містечко Йейт графства Глостершир, де через чотири місяці й народилася 
            майбутня британська знаменитість. У своїх перших інтерв'ю Джоан місцем свого народження називала
            не своє рідне місто, яке вважала похмурим, а Чиппінг Сотбері, в якому ніколи не жила. А ще 
            через 23 місяці в сім'ї Роулінг з'явився ще один дитячий голос - сестрички на ім'я Діана (Ді). 
            Через переїзд родини спочатку у Вінтербурн, а потім в Татшилл, що в тій же околиці Брістоля,
            де і Йейт, Джоан спочатку було нелегко заводити нові знайомства. Головним другом і відданим 
            слухачем перших дитячих оповідань про кролика на ім'я Кролик юної письменниці була її сестра Ді. 
            Багато однокласників вважали Джоан замкнутою, такою що живе у своєму вигаданому світі, яка весь 
            час щось записувала в блокнот. Та й сама письменниця говорить про себе одинадцятирічну, як про дуже 
            схожу на свою героїню з «Гаррі Поттера» всезнайка Герміону. Так було до шостого класу, поки Роулінг 
            не подружилася з Шоном Гаррісом, який частково став прототипом для ще одного головного персонажа 
            Поттеріани - Рона Візлі.
            \n
            До 15 років у родині Джоан почалася чорна смуга. Померла її улюблена бабуся. 
            Через нездоланні протиріч і нерозуміння з батьком склалися напружені стосунки. 
            Ну а найжахливіше - її мама захворіла на розсіяний склероз, і з кожним днем їй 
            ставало все гірше. Дізнатися в такому юному віці, що мати невиліковно хвора, 
            для Джоан було великим ударом.
            \n
            Ще з малих років мама Джоан, Енн, прищеплювала дочкам любов до читання. Як у 
            початковій, так і в старшій школах, Роулінг робила акцент на гуманітарні науки: література, 
            мови (англійська, французька та німецька). Після школи, в 1982 році Джоан бачила себе студенткою 
            Оксфорда. Спробувала стати його студенткою, але незважаючи на досить високі бали, двері цього 
            навчального закладу перед нею так і не відчинилися. Тоді майбутня письменниця обрала факультет 
            філології з ухилом на французьку мову в не менше прославленому Ексетерському університеті. 
            І хоча Джоан згадує про себе як про студентку, яка не дуже й сильно захоплювалася навчанням, 
            а більше рок-гуртами й книжками Діккенса, педагоги відгукувалися про неї, як про скромну, 
            але досить тямущу і перспективну ученицю. Завдяки такій характеристиці викладацького складу 
            Роулінг серед інших студентів була відправлена на стажування до Парижа. І в 1986 році, 
            повернувшись на батьківщину, захистила в Ексетері диплом бакалавра з французької мови і 
            класичної філології. З великими амбіціями дівчина подалася до Лондона. Спершу вдалося 
            влаштуватися секретарем-перекладачем, а після стати співробітницею дослідного відділу
             «Міжнародної амністії». Дуже скоро прийшло розуміння, як це все її обтяжує.
            \n
            У 1990 році Джоан вирішила привнести в своє життя щось нове і разом з бойфрендом поміняла 
            Лондон на Манчестер. І знову в житті Роулінг трапляється доленосний момент, який їй 
            приготувала залізниця. Джоан сіла в потяг до Лондона. Десь на середині шляху він був 
            зупинений на цілих чотири години з технічних причин. У якийсь момент в її свідомості
            почала вимальовувати історія у стилі фентезі, причому настільки яскраво, ніби письменниця 
            про це вже десь читала. Зафіксувати цей потік думок не було чим і на чому. Але ця 
            обставина допомогла сформувати купу деталей у голові, не сповільнюючи хід думок. Діставшись додому, 
            Джоан сіла писати своє легендарне творіння про юного чарівника Гаррі Поттера зі знанням справи.

            Письменниця натхненно писала день у день. Здавалося б, ніщо не могло перешкодити її натхненню. 
            Але в грудні того ж року помирає її мама, і це горе вибиває Джоан з колії. Причому настільки 
            сильно, що британка вирішує зовсім залишити Англію і влаштовується викладати англійську мову в... 
            Португалії. Прийшовши до тями, у вільний від роботи час Джоан продовжила розписувати життя в школі 
            чарівництва Гоґвортс. Тим часом доля зводить її з місцевим тележурналістом Хорхе Арантесом, і в 
            жовтні 1992 року вони стають законним подружжям. А 27 липня 1993 року Джоан стає мамою Джесіки 
            Ізабель Роулінг Арантес. Відомо, що дівчинка названа на честь Джесіки Мітфорд, американської 
            журналістки, письменниці і правозахисниці, біографію якої Роулінг прочитала ще підлітком з подачі 
            двоюрідної бабусі... Сімейному щастю прийшов кінець рівно через три місяці: Хорхе виставив Джоан з 
            донькою на руках за двері. Є думки, що письменниця потерпала від домашнього насильства. Єдиною людиною, 
            на яку вона могла розраховувати, опинившись в такій жахливій ситуації, була її сестра Діана в Единбурзі. 
            Взявши найцінніше, що було у письменниці в Португалії, дочку і три розділи «Гаррі Поттера», Джоан і 
            переїхала до Ді
            \n
            «Гаррі Поттера» можна прочитати на 65 мовах світу.
            Вважається, що саме романи Роулінг змогли пробудити у підлітків бажання до читання, яке затьмарювали 
            комп'ютери і телебачення.
            Одна із слабкостей Джоан - браслети з підвісками. Дізнавшись про це, редактор видавництва 
            Bloomsbury Емма у день презентації сьомої книжки «Поттеріани», подарувала письменниці золотий б
            раслет, обвішаний кулями за мотивами її книжки. Ця прикраса для Роулінг на другому місці після обручки.
            Життя письменниці було екранізоване у вигляді фільму-біографії «Магія слів: Історія Дж. К. Роулінг». 
            Головну героїню зіграла австралійська акторка Поппі Монтгомері.
            Для шанувальників «Поттеріани» у 2012 році був створений веб-проект Pottermore. Там може зареєструватися
            будь-хто охочий і отримати доступ до будь-якої інформації про «Гаррі Поттера».
            Письменниця так і не дотрималась слова, коли говорила, що, дописавши сьому книгу про «Гаррі Поттера», 
            поставила крапку в цій історії. 30 липня 2016 року в Лондоні в театрі Palace відбулася прем'єра п'єси 
            «Гаррі Поттер і Прокляте дитя», восьмої частини циклу про Гаррі Поттера. Книга з текстом п'єси 
            побачила світ 31 липня 2016 року.
        """
    },
    {
        "first_name": "Джордж",
        "last_name": "Оруелл",
        "slug": "george-orwell",
        "date_of_birth": date(1903, 6, 25),
        "description": """
        Сучасному читачеві потрібно купити книги Джорджа Орвелла, тому що описана у них дійсність 
        дивовижно нагадує нашу. Тому так вагомо звучать зроблені автором застереження. У творах Д. 
        Орвелла відбилися його погляди на події у суспільно-політичному житті Європи і Росії. Причому 
        авторська позиція не вписується у рамки лівого чи правого руху, що не заважає тим та іншим
        спиратися на неї у суперечках з опонентами.
        """,
        "short_description": """
            Сучасному читачеві потрібно купити книги Джорджа Орвелла, тому що описана у них дійсність дивовижно
            нагадує нашу. Тому так вагомо звучать зроблені автором застереження. У творах Д. Орвелла відбилися його
            погляди на події у суспільно-політичному житті Європи і Росії. 
        """,
    },
    {
        "first_name": "Пауло",
        "last_name": "Коельйо",
        "slug": "paulo-coelho",
        "date_of_birth": date(1947, 8, 24),
        "description": "Бразильський письменник, один з найвідоміших сучасних авторів.",
        "short_description": "Автор «Алхіміка»",
        "is_active": True
    },
    {
        "first_name": "Джон",
        "last_name": "Бойн",
        "slug": "john-boyne",
        "date_of_birth": date(1971, 4, 30),
        "description": "Ірландський письменник, автор «Хлопчика у смугастій піжамі».",
        "short_description": "Пише дитячу і дорослу прозу",
        "is_active": True
    },
    {
        "first_name": "Діана",
        "last_name": "Вінн Джонс",
        "slug": "diana-wynne-jones",
        "date_of_birth": date(1934, 8, 16),
        "description": "Британська письменниця фентезі.",
        "short_description": "Авторка «Мандрівного замку Хаула»",
        "is_active": False
    },
    {
        "first_name": "Ґабрієль",
        "last_name": "Ґарсія Маркес",
        "slug": "gabriel-garcia-marquez",
        "date_of_birth": date(1927, 3, 6),
        "description": "Колумбійський письменник, лауреат Нобелівської премії.",
        "short_description": "Автор «Сто років самотності»",
        "is_active": False
    },
    {
        "first_name": "Антуан",
        "last_name": "де Сент-Екзюпері",
        "slug": "antoine-de-saint-exupery",
        "date_of_birth": date(1900, 6, 29),
        "description": "Французький письменник, пілот і філософ.",
        "short_description": "Автор «Маленького принца»",
        "is_active": False
    },
    {
        "first_name": "Гарпер",
        "last_name": "Лі",
        "slug": "harper-lee",
        "date_of_birth": date(1926, 4, 28),
        "description": "Американська письменниця, авторка «Вбити пересмішника».",
        "short_description": "Лауреат Пулітцерівської премії",
        "is_active": False
    },
    {
        "first_name": "Іван",
        "last_name": "Франко",
        "slug": "ivan-franko",
        "date_of_birth": date(1856, 8, 27),
        "description": "Український письменник, поет, філософ, публіцист.",
        "short_description": "Автор «Захара Беркута»",
        "is_active": False
    },
    {
        "first_name": "Іван",
        "last_name": "Багряний",
        "slug": "ivan-bahrianyi",
        "date_of_birth": date(1906, 10, 2),
        "description": "Український письменник, публіцист, політик.",
        "short_description": "Автор «Тигроловів»",
        "is_active": False
    },
    {
        "first_name": "Михайло",
        "last_name": "Коцюбинський",
        "slug": "mykhailo-kotsiubynskyi",
        "date_of_birth": date(1864, 9, 17),
        "description": "Український класик, автор новел та повістей.",
        "short_description": "Автор «Тіней забутих предків»",
        "is_active": False
    }
]

IMAGE_GALLERIES = [
    {
        "image_path": "https://static.yakaboo.ua/media/entity/author/1/_/1_71.jpg",
        "author_id": 1
    },
    {
        "image_path": "https://static.yakaboo.ua/media/entity/author/4/_/4_48.jpg",
        "author_id": 1
    },
    {
        "image_path": "https://static.yakaboo.ua/media/entity/author/2/_/2_1_48.jpg",
        "author_id": 1
    },
    {
        "image_path": "https://static.yakaboo.ua/media/entity/author/3/_/3_2_26.jpg",
        "author_id": 1
    },
    {
        "image_path": "https://static.yakaboo.ua/media/entity/author/f/i/file_15_4.jpg",
        "author_id": 2
    },
    {
        "image_path": "https://static.yakaboo.ua/media/entity/author/o/-/o-i-met-jk-rowling-facebook.jpg",
        "author_id": 2
    },
    {
        "image_path": "https://static.yakaboo.ua/media/entity/author/2/1/21.jpg",
        "author_id": 2
    },
    {
        "image_path": "https://static.yakaboo.ua/media/entity/author/2/2/22.jpg",
        "author_id": 2
    },
    {
        "image_path": "https://static.yakaboo.ua/media/entity/author/4/6/4645.jpg",
        "author_id": 2
    }
]

KNOWLEDGES = [
    {
        "title": "Доставка",
        "slug": "delivery",
        "content": """
            <div className="w-[80%] bg-white rounded-md p-5 flex flex-col gap-4">
        <div className="flex flex-col gap-1">
            <p className="font-bold">
                Друзі, ми робимо все можливе, аби доставити ваші книжечки вчасно! Але через передсвяткове 
                навантаження можливі затримки. Дякуємо за розуміння!
            </p>
            <p>
                Працюємо без вихідних! Клієнти з України можуть отримати замовлення протягом 2–4 робочих днів, в залежності від розташування 
                населеного пункту та обраного способу доставки. Доставка можлива в ті населені пункти, де працюють відділення Нової Пошти чи Укрпошти. 
                Точні терміни та вартість доставки ви можете побачити під час оформлення замовлення після вибору потрібної служби доставки та міста.
            </p>
            <p className="font-bold">
                Ми щодня працюємо для вас – 24/7. Незважаючи на воєнний стан, ми докладаємо всіх зусиль, щоб виконати всі замовлення вчасно.
            </p>
        </div>
        <div className="flex flex-col gap-1">
            <p className="font-semibold text-gray-600 border-b border-b-gray-300 pb-3 text-[1.1rem]">
                Комплектація і цілісність товару
            </p>
        </div>
        <div className="flex flex-col gap-1">
            <ul className="flex flex-col gap-1 list-disc ml-4 marker:text-pink-500">
                <li className="text-left">
                    Будь ласка, перевіряйте комплектацію, цілісність упаковки, відсутність механічних пошкоджень і документи при отриманні замовлення.
                    Це можливо зробити при працівниках служби доставки.
                </li>
                <li>
                    Ми не несемо відповідальності за товар, який не був перевірений на наявність механічних пошкоджень або відсутність частин 
                    безпосередньо при отриманні у відділенні перевізника.
                </li>
                <li>
                    разі виявлення некомплекту або пошкоджень, ви маєте право не оплачувати товар і відмовитися від його отримання.
                </li>
            </ul>  
            <p className="font-bold max-w-[20%] border-b border-black pb-1">
                Способи оплати замовлення
            </p>  
        </div>
        <div className="flex flex-col gap-1">
            <p className="font-semibold text-gray-600 border-b border-b-gray-300 pb-3 text-[1.1rem]">
                Книгарня / Самовивіз
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p>
                м. Київ, вул. Хрещатик, 22, 1 поверх (Головпоштамт).
            </p>
            <p className="font-bold text-[1.1rem] mt-2">
                Графік роботи:
            </p>
            <p>
                Пн–Нд 9:00–20:00
            </p>
            <p>
                Телефон: 0-800-335-425.
            </p>
            <p className="mt-2">
                Книжковий магазин у центрі Києва – Yakaboo.ua на Хрещатику. Книжкові стелажі і зона видачі інтернет-замовлень. 
                У магазині обладнана спеціальна зона з останніми новинками та бестселерами.
            </p>
            <p>
                <span className="font-bold">
                    Зверніть увагу:
                </span> {" "}
                замовлення на самовивіз сплачуються онлайн чи при отриманні. Замовлення, оформлені до 16:00 доставляються до книгарні протягом 
                2–3 днів з дати оформлення. Замовлення, оформлені після 16:00 доставляються до книгарні протягом 3–4 днів з дати оформлення. 
                Після переміщення замовлення до книгарні Yakaboo ви отримаєте SMS про готовність до видачі вашого замовлення.
            </p>
            <p>
                Вартість переміщення замовлення до книгарні Yakaboo – БЕЗКОШТОВНО.
            </p>
            <p>
                Замовлення може зберігатися на самовивозі 4 робочі дні. На 5 день замовлення автоматично відправляється назад Відправникові.
            </p>
            <p>
                Для отримання відправлення необхідний паспорт або інше посвідчення особи.
            </p>
        </div>
        <div className="flex flex-col gap-1 mt-3">
            <p className="font-extrabold text-black border-b border-b-gray-300 pb-3 text-[1.1rem]">
                Доставка Укрпошта Експрес
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p>
                Вартість доставки становить <span className="font-bold">39 грн.</span> Замовлення буде доставлено у відділення Укрпошти протягом 1–3 робочих днів. 
                Замовлення може безкоштовно зберігатися у відділенні Укрпошти протягом 7 календарних днів. На 8 
                день замовлення автоматично відправляється назад Відправникові.. Для отримання замовлення необхідно пред’явити паспорт 
                або інший документ, що посвідчує особу.
            </p>
            <p>
                Усі замовлення на суму від <span className="font-bold">349 грн</span> доставляються до відділень Укрпошти безкоштовно.
            </p>
            <p>
                <span className="font-bold">
                    Зверніть увагу:
                </span> {" "}
                замовлення відправляються на наступний робочий день після оформлення.
            </p>
        </div>

        <div className="flex flex-col gap-1 mt-3">
            <p className="font-extrabold text-black border-b border-b-gray-300 pb-3 text-[1.1rem]">
                Кур'єрська доставка Укрпошти(склад - двері)
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p>
                Вартість доставки складає <span className="font-bold">75 грн</span>. Без комісій. Замовлення буде доставлене протягом 4–5 днів.
            </p>
            <p>
                <span className="font-bold">
                    Зверніть увагу: 
                </span> {" "}
                замовлення відправляються на наступний робочий день після оформлення.
            </p>
            <p className="font-bold">
                Доставка можлива в ті населені пункти, де наразі працюють відділення Укрпошти.
            </p>
        </div>
        <div className="flex flex-col gap-1 mt-3">
            <p className="font-extrabold text-black border-b border-b-gray-300 pb-3 text-[1.1rem]">
                Доставка на відділення Нової пошти
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p>
                Вартість доставки фіксована і складає <span className="font-bold">60 грн,</span> тому додаткові витрати \
                за пересилку коштів не стягуються. Замовлення буде 
                доставлене у пункт самовивозу протягом 1–3 робочих днів. Нова пошта проінформує SMS-повідомленням про те, що замовлення чекає у 
                відділенні Нової пошти.
            </p>
            <p>
                Всі замовлення на суму від <span className="font-bold">799 грн </span>доставляємо до відділень Нової пошти безкоштовно.
            </p>
            <p>
                <span className="font-bold">
                    Зверніть увагу:
                </span>
                {" "}
                замовлення, оформлені до 15:00, доставляються до відділення Нової пошти на наступний робочий день (у віддалені населені пункти на 2–3 день). 
                Замовлення, оформлені після 15:00, будуть відправлені на наступний день. Замовлення може безкоштовно зберігатися на відділенні Нової 
                пошти 6 робочі дні. На 7 день замовлення автоматично відправляється назад Відправникові. Для отримання відправлення необхідний паспорт, 
                посвідчення особи або додаток Нової пошти. 
            </p>
        </div>
        <div className="flex flex-col gap-1 mt-3">
            <p className="font-extrabold text-black border-b border-b-gray-300 pb-3 text-[1.1rem]">
                Кур'єрська доставка Нової пошти(склад - двері)
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p>
                Вартість доставки складає <span className="font-semibold">95 грн.</span> Без комісій.     
            </p>
        </div>
        <div className="flex flex-col gap-1 mt-3">
            <p className="font-extrabold text-black border-b border-b-gray-300 pb-3 text-[1.1rem]">
                Доставка у поштомат Нової пошти
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p>
                Поштомат – це термінал самообслуговування, де ви можете забрати своє замовлення. 
                Вартість доставки складає <span className="font-bold">60 грн. </span>
                Оплата замовлення можлива онлайн на сайті чи у додатку Нової пошти.
            </p>
            <p>
                Всі замовлення на суму від <span className="font-bold">600 грн</span> доставляємо до поштоматів Нової пошти безкоштовно. 
            </p>
            <p>
                Замовлення буде доставлено у поштомат протягом 1–3 робочих днів. Коли посилка прибуде у поштомат – ви зможете 
                відкрити комірку через додаток Нової пошти, вказавши геолокацію. Замовлення може безкоштовно зберігатися у поштоматі 
                Нової пошти 3 робочі дні. На 4 день замовлення автоматично відправляється назад Відправникові.
            </p>
            <p className="font-bold">
                Доставка можлива в ті населені пункти, де наразі працюють відділення Нової пошти.
            </p>
        </div>
        <div className="flex flex-col gap-1 mt-3">
            <p className="font-semibold text-gray-600 border-b border-b-gray-300 pb-3 text-[1.1rem]">
                Міжнародна доставка Nova Post
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p>
                Nova Post надає послуги міжнародної експрес-доставки для своїх клієнтів, відправляючи документи, посилки, вантажі в 
                Україну та за кордон у найкоротші терміни. Детальну інформацію про послуги та відстеження 
                відправлень можна знайти на сайті {" "}
                <Link className="font-extrabold text-blue-800 underline" href="https://novapost.com/">novapost.com.</Link>
            </p>
            <p>
                <span className="font-bold">
                    Вартість доставки
                </span> {" "}
                а обробки замовлення залежить від країни призначення, ваги, габаритів відправлення, обраних додаткових послуг та способу доставки 
                (доставка на відділення або за адресою). Точну вартість можна дізнатися під час оформлення замовлення.
            </p>
            <p>
                Рекомендуємо ознайомитися з умовами ввезення товару до країни призначення перед оформленням замовлення на сайті {" "}
                <Link className="font-extrabold text-blue-800 underline" href="https://novapost.com/">novapost.com.</Link>
            </p>
            <p>
                Yakaboo.ua не несе відповідальності за затримки на митниці або конфіскацію замовлень.
            </p>
            <p>
                <span className="font-bold">
                    Додаткові витрати:
                </span> {" "}
                Оскільки митна політика та імпортні мита відрізняються в різних країнах, Yakaboo.ua не може точно 
                передбачити розмір цих зборів на етапі оформлення замовлення на сайті. Тому вартість доставки не включає {" "}
                <Link href="https://novaposhta.ua/international_delivery/mytne_oformlennia" 
                className="text-blue-800 font-extrabold underline">митне оформлення товару</Link> та податок на додану вартість 
                (ПДВ). Якщо загальна вартість замовлення перевищує 150 євро, в 
                такому випадку надаються брокерські послуги. Вартість цих послуг додається до вартості доставки під час оформлення замовлення.
            </p>
            <table className="border border-black max-w-[30%] mb-3">
                <thead>
                    <tr>
                        <th className="py-2 px-4 border border-black">Країна</th>
                        <th className="py-2 px-4 border border-black">Ставка ПДВ</th>
                    </tr>
                </thead>
                <tbody>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Австрія</td>
                        <td className="py-2 px-4 border border-black">20%</td>
                    </tr>

                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Бельгія</td>
                        <td className="py-2 px-4 border border-black">21%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Болгарія</td>
                        <td className="py-2 px-4 border border-black">20%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Угорщина</td>
                        <td className="py-2 px-4 border border-black">5-18-27%(залежить від товару)</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Великобританія</td>
                        <td className="py-2 px-4 border border-black">20%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Греція</td>
                        <td className="py-2 px-4 border border-black">23%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Німеччина</td>
                        <td className="py-2 px-4 border border-black">19%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Данія</td>
                        <td className="py-2 px-4 border border-black">25%</td>
                    </tr><tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Італія</td>
                        <td className="py-2 px-4 border border-black">22%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Ірландія</td>
                        <td className="py-2 px-4 border border-black">23%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Іспанія</td>
                        <td className="py-2 px-4 border border-black">21%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Кіпр</td>
                        <td className="py-2 px-4 border border-black">18%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Люксембург</td>
                        <td className="py-2 px-4 border border-black">21%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Латвія</td>
                        <td className="py-2 px-4 border border-black">21%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Литва</td>
                        <td className="py-2 px-4 border border-black">21%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Мальта</td>
                        <td className="py-2 px-4 border border-black">18%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Нідерланди</td>
                        <td className="py-2 px-4 border border-black">21%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Португалія</td>
                        <td className="py-2 px-4 border border-black">23%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Польща</td>
                        <td className="py-2 px-4 border border-black">23%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Румунія</td>
                        <td className="py-2 px-4 border border-black">24%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Словенія</td>
                        <td className="py-2 px-4 border border-black">22%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Словаччина</td>
                        <td className="py-2 px-4 border border-black">20%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Франція</td>
                        <td className="py-2 px-4 border border-black">20%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Фінляндія</td>
                        <td className="py-2 px-4 border border-black">24%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Хорватія</td>
                        <td className="py-2 px-4 border border-black">25%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Чехія</td>
                        <td className="py-2 px-4 border border-black">21%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Швеція</td>
                        <td className="py-2 px-4 border border-black">21%</td>
                    </tr>
                    <tr className="border border-black">
                        <td className="py-2 px-4 border border-black">Естонія</td>
                        <td className="py-2 px-4 border border-black">21%</td>
                    </tr>
                </tbody>
            </table>
            <p>
                <span className="font-bold">
                    Спосіб оплати:
                </span> {" "}
                для міжнародних відправлень доступна лише оплата платіжною карткою онлайн.
            </p>
            <p>
                <span className="font-bold">
                    Спосіб доставки:
                </span> {" "}
                здійснюється кур'єром за вказаною Вами адресою. Доставка в поштові скриньки або іншими альтернативними способами недоступна.
            </p>
            <p>
                <span className="font-bold">
                    Трекінг:
                </span>
                Ви можете відстежувати відправлення на сайті логістичного оператора за {" "}
                <Link className="font-bold underline" href="https://novapost.com/uk-ua/tracking/">посиланням.</Link>
            </p>
            <p>
                <span className="font-bold">
                    Зверніть увагу
                </span> {" "}
                    Якщо ви не отримали товар за адресою доставки у терміни, які передбачені умовами міжнародного перевезення, вчасно не сплатили митні послуги, 
                    неправильно вказали адресу або телефон отримувача, не відповіли на дзвінок кур'єра під час організації доставки, товар вважається прийнятим і 
                    Yakaboo.ua не компенсує вартість товару і вартість послуг доставки міжнародного відправлення.    
            </p>
        </div>
    </div>
        """
    },
    {
        "title": "Оплата",
        "slug": "payment",
        "content": """
            <div className="w-[80%] bg-white rounded-md p-5 flex flex-col gap-4 mb-4">
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Оплата онлайн
        </p>
        <div className="flex flex-col gap-2">
            <p>
                Для оплати замовлень онлайн оберіть під час оформлення замовлення спосіб «Оплата карткою On-line». Після підтвердження замовлення вас 
                буде перенаправлено на сайт платіжної системи, де потрібно ввести реквізити платіжної картки та пройти верифікацію за допомогою SMS-повідомлення. 
                Якщо з якихось причин оплата карткою не буде здійснена, вас автоматично повернеться на сайт yakaboo.ua, де ви зможете обрати інший спосіб оплати.
            </p>
            <p className="font-bold">
                Доступні способи онлайн-оплати: {" "}
                <Link className="text-blue-800 underline" href="https://www.liqpay.ua/uk">LiqPay</Link> та {" "}
                <Link className="text-blue-800 underline" href="https://www.xpay.com.ua/">XPay</Link>
            </p>
            <p className="font-bold">
                Кешбек 5% при оплаті онлайн
            </p>
            <p>
                Оплачуючи замовлення онлайн, ви отримуєте кешбек 5% від суми замовлення на бонусний рахунок Yakaboo. 1 бонус дорівнює 1 гривні.
            </p>
            <p className="font-bold">
                Зверніть увагу:
            </p>
            <ul className="flex flex-col gap-1 list-disc ml-4 marker:text-pink-500">
                <li>
                    Бонусами можна оплатити не більше 50% вартості замовлення.
                </li>
                <li>
                    Бонуси не можна використовувати для оформлення замовлення на іншого отримувача.
                </li>
                <li>
                    Кешбек не нараховується, якщо одночасно застосовуються інші бонуси програми лояльності Yakaboo.
                </li>
                <li>
                    Кешбек нараховується після успішної оплати замовлення та діє протягом 30 днів.
                </li>
            </ul>
        </div>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem] mt-2">
            Готівкою або картою
        </p>
        <div className="flex flex-col gap-2">
            <p>
                Оплатити замовлення можна готівкою або банківською карткою при отриманні посилки на поштовому відділенні. 
                До кожного замовлення додається товарний чек.
            </p>
        </div>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem] mt-2">
            Банківським переказом
        </p>
        <div className="flex flex-col gap-2">
            <p>
                Щоб оплатити замовлення банківським переказом, виконайте наступні дії:
            </p>
            <ul className="flex flex-col gap-1 list-disc ml-4 marker:text-pink-500">
                <li>
                    Оберіть спосіб оплати «Банківський переказ» під час оформлення замовлення.
                </li>
                <li>
                    Очікуйте дзвінка від нашого менеджера для уточнення деталей та отримання реквізитів для оплати.
                </li>
            </ul>
        </div>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem] mt-2">
            Покупка частинами від monobank
        </p>
        <div className="flex flex-col gap-2">
            <p>
                Щоб скористатися послугою «Покупка частинами» від monobank, вам необхідно мати картку monobank і оформити замовлення 
                на суму від <span className="font-bold">700 грн</span>. Оплата ділиться на 3 рівні платежі, 
                перший з яких ви вносите одразу. Наступні платежі будуть 
                автоматично списані з вашої картки щомісяця.
            </p>
            <p>
                Як оформити замовлення з оплатою частинами:
            </p>
            <ul className="flex flex-col gap-1 list-disc ml-4 marker:text-pink-500">
                <li>
                    Додайте потрібні товари в кошик на сайті <Link href="/" className="text-blue-800 font-extrabold underline">Yakaboo.ua.</Link>
                </li>
                <li>
                    Під час оформлення замовлення оберіть спосіб оплати «Покупка частинами від monobank».
                </li>
                <li>
                    Виберіть кількість платежів (3).
                </li>
                <li>
                    Підтвердіть покупку в мобільному додатку monobank.
                </li>
            </ul>
            <p className="font-bold">
                Зверніть увагу:
            </p>
            <ul className="flex flex-col gap-1 list-disc ml-4 marker:text-pink-500">
                <li>
                    Послуга «Покупка частинами» доступна лише для товарів, які є в наявності на момент оформлення замовлення.
                </li>
                <li>
                    Передзамовлення не підлягають оплаті частинами.
                </li>
            </ul>
        </div>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem] mt-2">
            Оплата частинами від ПриватБанку
        </p>
        <div className="flex flex-col gap-2">
            <p>
                Для використання функції <span className="font-bold">«Оплата частинами від ПриватБанку»</span> необхідно мати активну кредитну картку ПриватБанку з 
                підключеною послугою «Оплата частинами». Розділивши оплату на кілька частин (від 2 до 4 платежів), ви сплачуєте 
                перший внесок одразу, а решту суми буде автоматично списано з вашої картки щомісяця. Скористатися цією послугою 
                можна при оформленні замовлення від 700 грн. Оплата частинами доступна тільки для товарів, що є в наявності на момент оформлення замовлення.
            </p>
            <p>
                Як оформити замовлення з оплатою частинами:
            </p>
            <ul className="flex flex-col gap-1 list-disc ml-4 marker:text-pink-500">
                <li>
                    Оберіть потрібні товари на сайті <Link href="/" className="font-blue-800 font-extrabold underline">Yakaboo.ua</Link> та додайте їх у кошик.
                </li>
                <li>
                    Під час оформлення замовлення виберіть спосіб оплати «Оплата частинами від ПриватБанку»
                </li>
                <li>
                    Виберіть бажану кількість платежів (від 2 до 4).
                </li>
                <li>
                    Підтвердіть покупку в мобільному додатку Приват24.
                </li>
            </ul>
        </div>
    </div>
        """
    },
    {
        "title": "Програма лояльності Yakaboo",
        "slug": "bonus",
        "content": """
            <div className="w-[80%] bg-white rounded-md p-5 flex flex-col gap-4 mb-4">
        <div className="flex flex-col gap-2">
            <p>
                На сайті Yakaboo.ua діє програма лояльності з бонусними умовами.
            </p>
            <p className="font-bold">
                Нарахування бонусів
            </p>    
            <ul className="flex flex-col gap-1 list-disc ml-4 marker:text-pink-500">
                <li>
                    <span className="font-bold">
                        Бонуси нараховуються у вигляді кешбеку
                    </span> {" "}
                    відповідно до умов акційних пропозицій
                </li>
                <li>
                    <span className="font-bold">
                        Бонуси нараховуються у вигляді  5% кешбеку
                    </span> {" "}
                    при оплаті замовлення онлайн
                </li>
            </ul>
            <p className="font-bold">
                Використання бонусів
            </p>
            <ul className="flex flex-col gap-1 list-disc ml-4 marker:text-pink-500">
                <li className="font-bold">
                    Бонусами можна сплатити до 50% вартості замовлення
                </li>
                <li>
                    <span className="font-bold">
                        Термін дії бонусів
                    </span> {" "}
                    визначається умовами акційних пропозицій, за якими вони були нараховані, та є вказаним у вашому особистому кабінеті
                </li>
                <li>
                    <span className="font-bold">
                        Кешбек 5% діє протягом 30 днів
                    </span> {" "}
                    після оплати замовлення
                </li>
                <li>
                    <span className="font-bold">
                        Кешбек нараховується за всі товари на сайті,
                    </span> {" "}
                    за винятком сертифікатів. 1 бонус = 1 гривня
                </li>
            </ul>
            <p className="font-bold">
                Додаткові умови
            </p>
            <ul className="flex flex-col gap-1 list-disc ml-4 marker:text-pink-500">
                <li className="font-bold">
                    Бонуси не можна використовувати для замовлень на інших отримувачів
                </li>
                <li>
                    <span className="font-bold">
                        Кешбек 5% не нараховується,
                    </span> {" "}
                    якщо діють інші форми кешбеку в рамках промоакцій
                </li>
                <li>
                    <span className="font-bold">
                        При скасуванні замовлення до відправки
                    </span> {" "}
                    бонуси повертаються, вони будуть відображені у вашому особистому кабінеті
                </li>
                <li>
                    <span className="font-bold">
                        При відмові від отримання замовлення під час доставки
                    </span> {" "}
                    бонуси не повертаються
                </li>
            </ul>
            <p className="font-bold">
                Залишайтеся в курсі
            </p>
            <p>
                Не забувайте слідкувати за новинами на сайті Yakaboo.ua та в наших соцмережах! Там ви завжди знайдете вигідні 
                пропозиції: кешбеки, знижки, промокоди та інші акції. Не проґавте шанс купити книжки вигідно!
            </p>
        </div>
    </div>
        """
    },
    {
        "title": "Безпека та захист даних",
        "slug": "safety_and_protection",
        "content": """
            <div className="w-[80%] bg-white rounded-md p-5 flex flex-col gap-4 mb-4">
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Політика конфіденційності
        </p>
        <div className="flex flex-col gap-2">
            <p>
                Ласкаво просимо в інтернет-магазин Yakaboo.ua (далі іменується «ЯКАБУ» або сайт yakaboo.ua), цей сайт є власністю ТОВ «ЯКАБУ».    
            </p>
            <p>
                Уважно прочитайте нашу Політику конфіденційності
            </p>
            <p>
                Дана Політика конфіденційності роз'яснює наші правила збору, використання і поширення інформації, 
                яку ви можете передати на наш сайт і діє для всього сайту yakaboo.ua. Користувач має всі права щодо захисту 
                його персональних даних, які передбачені чинним законодавством України, зокрема, Законом України «Про захист персональних даних».
            </p>
            <p>
                У деяких випадках ми можемо публікувати окремі примітки про конфіденційність для певних розділів сайту.
            </p>
            <p>
                Якщо вам потрібна додаткова інформація про способи обробки ваших особистих даних на сайті yakaboo.ua, 
                надішліть запит електронною поштою на адресу {" "}
                <Link href="mailto:support@yakaboo.com" className="text-blue-800 font-extrabold underline">support@yakaboo.com</Link>
            </p>
            <p>
                Останнє оновлення: 24 червня 2021 р.
            </p>
        </div>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Політика обробки персональних даних
        </p>
        <div className="flex flex-col gap-2">
            <p>
                Ця політика обробки персональних даних (далі – Політика) встановлює умови збору, зберігання, обробки, зміни, 
                передачі, знищення (видалення) персональних даних наданих ТОВ «ЯКАБУ РІТЕЙЛ» (далі – Володілець), а також 
                умови згоди на обробку персональних даних суб’єктів персональних даних.
            </p>
            <p>
                Ця Політика розроблена у відповідності до Закону України «Про захист персональних даних» (в редакції від 23.04.2021).
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                1.{" "}Терміни вжиті в цій Політиці означають наступне:
            </p>
            <p>
                1.1. Володілець – юридична особа, яка надає послуги Суб’єкту з доступу до Сервісу «Yakaboo», здійснює Обробку 
                персональних даних відповідно до мети та інших умов цієї Політики. Для виконання своїх зобов’язань перед Суб’єктом термін 
                «Володілець» також включає будь-яких афілійованих осіб Володільця, які приймають на себе зобов’язання щодо правомірної 
                Обробки та захисту персональних даних відповідно до умов цієї Політики.
            </p>
            <p>
                В розумінні Закону України «Про захист персональних даних» термін «Володілець» включає одержувача, 
                володільця та розпорядника персональних даних.
            </p>
            <p>
                1.2. Сервіс «Yakaboo» - сукупність програмних засобів Володільця (в тому числі мобільного додатку Yakaboo), 
                які надають можливість користувачам таких програмних засобів здійснювати доступ до електронних примірників
                 літературних творів та аудіо виконань літературних творів.
            </p>
            <p>
                1.3. Суб’єкт – фізична особа, користувач Сервісу «Yakaboo», яка надає свої персональні дані, а 
                також безумовну згоду на Обробку персональних даних, шляхом завантаження та встановлення Сервісу «Yakaboo» 
                на власний пристрій, проходження процедури реєстрації в Сервісі «Yakaboo», а також іншими способами визначеними в цій Політиці.
            </p>
            <p>
                1.4. Обробка – дії Володільця зі збирання, збереження, накопичення, зміна, використання та будь-яка інша 
                обробка персональних даних, яка відповідає меті Обробки персональних даних та іншим умовам цієї Політики.
            </p>
            <p>
                1.5. Згода – добровільне волевиявлення Суб’єкта щодо надання дозволу на Обробку своїх персональних даних 
                Володільцю, здійснене шляхом: проставлення відповідної відмітки при реєстрації в Сервісі «Yakaboo», та/або 
                проходженням процедури реєстрації в Сервісі «Yakaboo», та/або використанням будь-яких послуг Сервісу «Yakaboo», в 
                тому числі здійснення будь-яких платежів за послуги Сервісу «Yakaboo».
            </p>
        </div>
        <div className='flex flex-col gap-2'>
            <p className="font-bold">
                2.      Умови обробки персональних даних.
            </p>
            <p>
                2.1.1.       Суб’єкт персональних даних надає свою Згоду Володільцю на Обробку персональних даних, шляхом вчинення дій, 
                передбачених п. 1.5. цієї Політики, за умови, що перед вчиненням таких дій в Суб’єкта є можливість повністю ознайомитися з 
                умовами цієї Політики. Дії, передбачені п. 1.5. цієї Політики є гарантією повної цивільної дієздатності Суб’єкта персональних даних 
                та повного розуміння ним умов цієї Політики.
            </p>
            <p>
                2.1.2.       Метою Обробки персональних даних є забезпечення Володільцем можливості ідентифікації Суб’єктом власної 
                інформації в Сервісі «Yakaboo», забезпечення можливості Суб’єкта здійснювати доступ до послуг Сервісу «Yakaboo», 
                забезпечення можливості Суб’єкта на отримання технічної та консультативної підтримки щодо використання Сервісу «Yakaboo», 
                а також забезпечення Володільцем надання послуг та виконання своїх зобов’язань відповідно до умов {" "}
                <Link href="#" className="text-blue-800 font-extrabold underline">Публічної оферти</Link> перед Суб’єктом.
            </p>
            <p>
                2.1.3.       Зміст персональних даних, Обробку яких здійснює Володілець складають відомості, які ідентифікують особу, 
                а саме: прізвище, ім’я та по-батькові Суб’єкта; контактна інформація Суб’єкта (в тому числі адреса для листування, 
                номер мобільного телефону т адреса електронної пошти); а також відомості, які допомагають покращити якість послуг, 
                що надаються Володільцем в Сервісі «Yakaboo».
            </p>
            <p>
                2.1.4.       Володілець може отримувати доступ до інших персональних даних Суб’єкта, не передбачених умовами цієї 
                Політики таких як: технічні відомості щодо доступу Суб’єкта до Сервісу «Yakaboo», інформація про пристрій, який 
                використовується Суб’єктом, інформація про інтереси та вподобання Суб’єкта в Сервісі «Yakaboo», інформація щодо 
                геолокації пристрою Суб’єкта, тощо. Володілець може отримати доступ до вказаної вище інформації внаслідок нормальної 
                взаємодії Сервісу «Yakaboo» з іншими програмними та апаратними складовими Суб’єкта. Щодо Обробки персональних даних, 
                отриманих Володільцем відповідно до цього пункту встановлюються такі самі зобов’язання за цією Політикою як і щодо 
                персональних даних, передбачених п. 2.1.3. цієї Політики.
            </p>
            <p>
                2.1.5.       Володілець не здійснює Обробку платіжної інформації Суб’єкта, який останній використовує для оплати послуг 
                Сервісу «Yakaboo». Обробка платіжної інформації Суб’єкта так само як забезпечення процесу оплати послуг Сервісу 
                «Yakaboo» здійснюються сторонніми платіжними системами (третіми особами). Здійснюючи оплату послуг Сервісу «Yakaboo», 
                Суб’єкт погоджується з умовами обробки персональних даних сторонніх платіжних систем (третіх осіб), які доступні 
                Суб’єкту для ознайомлення до моменту оплати.
            </p>
            <p>
                2.1.6.       Суб’єкт, відповідно до умов цієї Політики, надає Згоду на безстрокове зберігання персональних даних 
                Володільцем до моменту отримання від Суб’єкта вимоги про відкликання дозволу та припинення Обробки персональних даних.
            </p>
            <p>
                2.1.7.       Місцем обробки персональних даних є апаратні пристрої Володільця, розташовані за адресом, 
                вказаним в реквізитах Володільця в п. 6.1. цієї Політики.
            </p>
            <p>
                2.1.8.       Будь-які суттєві зміни умов цієї Політики, в тому числі мети, та порядку Обробки персональних 
                даних супроводжуються обов’язковим повідомленням Суб’єкта персональних даних про такі зміни.
            </p>
            <p>
                2.1.9.       Володілець персональних даних забезпечує належний рівень захисту персональних даних 
                Суб’єкта на недопущення несанкціонованого поширення та розповсюдження персональних даних третім особам.
            </p>
            <p>
                2.1.10.   Володілець має право надати дозвіл на Обробку персональних даних третім особам 
                (неафілійованим особам Володільця) за умови отримання відповідного дозволу від Суб’єкта персональних даних.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                3.      Права Суб’єкта персональних даних.
            </p>
            <p>
                3.1. Відповідно до Закону України «Про захист персональних даних» та умов цієї Політики Суб’єкт персональних даних має право:
            </p>
            <p>
                <span className="mr-[40px]">-</span>отримати інформацію про джерела збирання, місцезнаходження, 
                склад та точний зміст своїх персональних даних;
            </p>
            <p>
                <span className="mr-[40px]">-</span>отримати інформацію про мету, способи Обробки та Володільця своїх персональних даних;
            </p>
            <p>
                <span className="mr-[40px]">-</span>пред’явити запит про відкликання згоди на Обробку своїх персональних даних;
            </p>
            <p>
                <span className="mr-[40px]">-</span>пред’явити вмотивовану вимогу знищення (видалення) своїх персональних даних 
                з місця зберігання персональних даних Володільця;
            </p>
            <p>
                <span className="mr-[40px]">-</span>пред’явити вмотивовану вимогу Володільцю щодо внесення змін в склад, зміст та об’єм своїх персональних даних;
            </p>
            <p>
                <span className="mr-[40px]">-</span>на інші способи захисту своїх персональних даних, відповідно до чинного законодавства України та умов цієї Політики.
            </p>
            <p>
                3.2. Реалізація прав Суб’єкта персональних даних, передбачених п. 3.1. цієї Політики можлива шляхом, 
                надсилання Суб’єктом Володільцю відповідного звернення за реквізитами Володільця вказаними в п. 6.1. цієї Політики.
            </p>
            <p>
                3.3. Приймаючи умови цієї Політики, Суб’єкт персональних даних погоджується на отримання від Володільця 
                інформаційних повідомлень, які відповідають меті Обробки персональних даних до моменту отримання Володільцем 
                відмови Суб’єкта від отримання таких повідомлень.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                4.      Обмеження відповідальності Володільця.
            </p>
            <p>
                4.1. Володілець не несе відповідальності за негативні наслідки використання персональних даних Суб’єкта 
                третіми особами, якщо таке використання сталося внаслідок недостатніх засобів захисту Суб’єктом своїх персональних даних.
            </p>
            <p>
                4.2. Володілець не несе відповідальності за негативні наслідки, внаслідок надання Суб’єктом персональних даних недостовірних відомостей.
            </p>
            <p>
                4.3. Володілець не несе відповідальності за негативні наслідки використання персональних даних 
                Суб’єкта третіми особами, якщо таке використання відбулося внаслідок надання Суб’єктом дозволу на Обробку персональних даних третім особам.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                5.      Форс-мажорні обставини.
            </p>
            <p>
                5.1. Обставини, що не залежать від волі Володільця та Суб’єкта і є невідворотними або 
                надзвичайними за даних умов (форс-мажорні обставини), і які безпосередньо впливають на дотримання 
                умов цієї Політики, унеможливлюючи належне виконання договірних обов’язків, виключають відповідальність 
                сторони, для якої вони настали, за недотримання чи неналежне дотримання умов цієї Політики.
            </p>
        </div>

        <div className="flex flex-col gap-2">
            <p className="font-bold">
                6.      Реквізити Володільця.
            </p>
            <p>
                Товариство з обмеженою відповідальністю «ЯКАБУ РІТЕЙЛ»; код ЄДРПОУ: 44987642; адреса місцезнаходження: 
                Україна, 04073, м. Київ, вул. Кирилівська, буд. 160, літера Ю; адреса ел. пошти: support@yakaboo.ua
            </p>
        </div>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Файли cookie, інформація про відвідування
        </p>
        <div className="flex flex-col gap-2">
            <p>
                Коли ви заходите на наш сайт, ми відправляємо один або декілька файлів cookie на ваш комп'ютер або 
                інший пристрій. Файли cookie використовуються для того, щоб підвищувати якість надаваних послуг: 
                зберігати налаштування користувача, відстежувати характерні для користувачів тенденції, наприклад, 
                найпопулярніші сторінки. Yakaboo.ua також використовує файли cookie в рекламних службах, а також здійснює 
                їх передачу, в тому числі транскордонну, щоб керувати оголошеннями на сайтах по всьому Інтернету.
            </p>
            <p>
                При доступі до нашого Сайту через браузер, додаток або інший клієнт наші сервери автоматично записують і передають 
                з метою виконання укладених договорів певну інформацію. Ці журнали серверу можуть містити таку інформацію, 
                як IP-адресу, тип і мова браузера, дата і час запиту, а також один або декілька файлів cookie, 
                за якими можна визначити ваш браузер або аккаунт.
            </p>
        </div>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Інші сайти
        </p>
        <p>
            Дана політика конфіденційності стосується тільки сайту yakaboo.ua. Ми не контролюємо сайти, які використовують інформацію 
            з нашого сайту або на які ведуть посилання з нашого сайту. Ці сайти можуть розміщувати на Ваш комп'ютер власні файли cookie, 
            збирати дані або запитувати у вас особисту інформацію.
        </p>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Інформаційні розсилки
        </p>
        <div className="flex flex-col gap-2">
            <ul className="flex flex-col gap-2 list-disc marker:text-pink-500 ml-4">
                <li>
                    При реєстрації на Сайті ви даєте згоду на отримання від нас розсилок рекламно-інформаційного характеру. 
                    Зазначені розсилки містять інформацію про товари, майбутні акції, розіграші та інші заходи Сайту.
                </li>
                <li>
                    Ви можете відмовитися від розсилки в будь-який момент, перейшовши за відповідним посиланням в листі або написавши в службу підтримки.
                </li>
                <li>
                    Розсилки надходять у вигляді листа на електронну адресу та/або короткого повідомлення (sms) на номер телефону, 
                    які зазначені вами при реєстрації або у своєму Особистому кабінеті. Рекламно-інформаційні матеріали можуть 
                    надаватися у вигляді паперово-поліграфічної та сувенірної продукції, вкладатися в замовлення клієнтів і 
                    доставлятися на вказану поштову адресу у вигляді листів і посилок.
                </li>
            </ul>   
            <p>
                Крім цього, інформація, що збирається нами може бути використана в наступних цілях: 
            </p> 
            <ul className="flex flex-col gap-2 list-disc marker:text-pink-500 ml-4">
                <li>
                    Постачання, підтримка, забезпечення захисту та удосконалення нашого Сайту, а також розробка нових служб. 
                    Захист прав і власності сайту yakaboo.ua і наших користувачів. Перед використанням інформації в інших 
                    цілях, крім тих, що були зазначені при її зборі, ми попросимо у вас дозволу на таке використання.
                </li>
                <li>
                    Сайт yakaboo.ua обробляє особисту інформацію на своїх серверах в різних країнах. У деяких випадках особиста 
                    інформація користувачів обробляється за межами країни користувача.
                </li>
            </ul>
        </div>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Надання доступу до інформації
        </p>
        <div className="flex flex-col gap-2">
            <p>
                Ми не розкриваємо особисту інформацію користувачів компаніям, організаціям і приватним особам, які не пов'язані 
                з сайтом yakaboo.ua, крім таких випадків:
            </p>
            <ul className="list-disc marker:text-pink-500 ml-4">
                <li className="font-bold">Користувач дав на це свою згоду</li>
            </ul>
            <p>
                Ми можемо надати відомості про вас компаніям, організаціям або приватним особам, які не пов'язані 
                з сайтом yakaboo.ua, якщо ви надали на це згоду.
            </p>
            <ul className="list-disc marker:text-pink-500 ml-4">
                <li className="font-bold">Для обробки третіми сторонами</li>
            </ul>
            <p>
                Ми можемо надати персональні дані на обробку нашим дочірнім і афільованим компаніям, а 
                також іншим довіреним організаціям та особам, у відповідності з нашими інструкціями, 
                політикою конфіденційності та іншими вимогами безпеки.
            </p>
            <ul className="list-disc marker:text-pink-500 ml-4">
                <li className="font-bold">На вимогу законодавства</li>
            </ul>
            <p>
                У нас є достатні підстави вважати, що доступ, використання, збереження або розкриття такої 
                інформації розумним чином необхідні з метою:
            </p>
            <ul className="list-disc marker:text-pink-500 ml-4 flex flex-col gap-2">
                <li>
                    Дотримання будь-яких чинних законів, постанов, вимог юридичного процесу або дійсного запиту з державних органів
                </li>
                <li>
                    Дотримання чинних Умов продажу товарів та надання послуг, включаючи розслідування потенційних порушень
                </li>
                <li>
                    Виявлення і запобігання шахрайських дій, а також вирішення проблем безпеки та усунення технічних неполадок
                </li>
                <li>
                    Захисту від безпосередньої загрози заподіяння шкоди правам, власності або безпеки сайту yakaboo.ua, її користувачам 
                    або громадськості, як це вимагається або дозволяється законом.
                </li>
            </ul>
            <p>
                Якщо сайт yakaboo.ua візьме участь у злитті, придбанні або будь-якій іншій формі продажу частини або всіх своїх активів, 
                ми гарантуємо збереження конфіденційності будь-якої особистої інформації, яка може бути залучена в цю угоду.
            </p>
        </div>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Захист інформації
        </p>
        <p>
            Сайт yakaboo.ua здійснює належний захист Персональних і інших даних відповідно до Законодавства і приймає необхідні 
            і достатні організаційні та технічні заходи щодо захисту Персональних даних від неправомірного або випадкового доступу, 
            знищення, зміни, блокування, копіювання, розповсюдження, а також від інших неправомірних дій третіх осіб.
        </p>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Зміна персональних даних
        </p>
        <ul className="flex flex-col gap-2 list-disc marker:text-pink-500 ml-4">
            <li>
                Користувач може в будь-який момент змінити (оновити, доповнити) Персональні дані в Особистому кабінеті або шляхом 
                направлення письмової заяви на адресу {" "}
                <Link href="mailto:support@yakaboo.com" className="text-blue-800 font-extrabold underline">support@yakaboo.com</Link>
            </li>
            <li>
                Користувач в будь-який момент має право видалити Персональні дані шляхом направлення письмової заяви на адресу {" "}
                <Link href="mailto:support@yakaboo.com" className="text-blue-800 font-extrabold underline">support@yakaboo.com</Link>
            </li>
            <li>
                Користувач гарантує, що всі Персональні дані є актуальними і не відносяться до третіх осіб.
            </li>
        </ul>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Дотримання вимог
        </p>
        <p>
            Дана Політика конфіденційності відображає основні принципи використання інформації компанією «ЯКАБУ». 
            Здійснюючи доступ на цей сайт, переглядаючи і використовуючи його, або надаючи компанії «ЯКАБУ» свою особисту 
            інформацію, ви висловлюєте свою згоду з умовами цієї Політики конфіденційності. Якщо ви не згодні з цими умовами, 
            просимо не надавати нам свою особисту інформацію.
        </p>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Ми регулярно перевіряємо дотримання даної Політики конфіденційності.
        </p>
        <p>
            Отримавши офіційну скаргу в письмовій формі, ми вважаємо своїм обов'язком звернутися до користувача, що відправив 
            скаргу з приводу його претензій або побоювань. Ми будемо співпрацювати з відповідними регулюючими органами, включаючи 
            місцевих представників влади, що відповідають за захист даних, для вирішення питань передачі особистих даних, які 
            неможливо вирішити між сайтом yakaboo.ua і приватною особою.
        </p>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Зміна політики конфіденційності
        </p>
        <div className="flex flex-col gap-2">
            <p>
                Сайт yakaboo.ua вправі вносити зміни і доповнення до даної політики конфіденційності.
            </p>
            <p>
                Всі оновлення і доповнення політики конфіденційності публікуються на цій сторінці.
            </p>
        </div>
    </div>
        """
    },
    {
        "title": "Правила публікації відгуків і рецензій",
        "slug": "ruleservices",
        "content": """
            <div className="w-[80%] bg-white rounded-md p-5 flex flex-col gap-4 mb-4">
        <div className="flex flex-col gap-2">
            <p className="text-red-800 font-bold">
                Важливо! Через непросту економічну ситуацію на книжковому ринку України ми змушені з 4 липня 2022 року призупинити нарахування нових бонусів за відгуки та рецензії. 
                Але всі бонуси, які вже у вас є, залишаються дійсними та можуть бути використані при оплаті замовлень.
            </p>
            <p>
                Ці Правила публікації відгуків і рецензій (надалі - Правила) встановлені ТОВ "ЯКАБУ" (надалі - Власник Сайту) і визначають умови 
                публікації відгуків, коментарів і рецензій на сайті <Link href="/" className="text-blue-800 font-extrabold underline">yakaboo.ua</Link>
                {" "}
                (надалі - Сайт).
            </p>
            <p>
                Останнє оновлення: 17.12.2020 р.
            </p>
        </div>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            1. Правила публікації відгуків
        </p>
        <div className="flex flex-col gap-2">
            <p>
                Кожен зареєстрований авторизований користувач може залишити свій відгук про будь-який товар на Сайті. Кожен користувач 
                може залишити будь-яку кількість відгуків. Розмір відгуку про товар не повинен перевищувати довжину у 2000 символів. 
                Для уникнення потрапляння на сайт спаму й іншого небажаного контенту всі залишені на Сайті відгуки проходять попередню модерацію.
            </p>
            <p>
                Модератор має право відхилити запит на публікацію відгуку якщо:
            </p>
            <ul className="flex flex-col gap-2 list-disc marker:text-pink-500 ml-4">
                <li>
                    відгук не має прямого і безпосереднього відношення до обговорюваного товару
                </li>
                <li>
                    відгук використовується з рекламною метою, для публікації посилань на інші веб-сайти
                </li>
                <li>
                    відгук містить спам, дублює попередні відгуки до товару
                </li>
                <li>
                    відгук містить інформацію не по темі, стосується іншого товару або компанії, заснований на чужому досвіді
                </li>
                <li>
                    при складанні відгуку використовуються образи інших користувачів, непристойності, лайливі слова
                </li>
                <li>
                    відгук містить незаконний контент, який порушує чинне законодавство України, авторські права та інші права користувачів
                </li>
            </ul>
            <p>
                Залишайте відгуки, щоб розповісти про свій досвід, а не просто вплинути на оцінку компанії. Пишіть про свої враження, але не 
                дублюйте відгуки і не розміщуйте в них комерційні матеріали. Написаний вами якісний і розгорнутий відгук допоможе зробити 
                вибір товарів для інших користувачів простішим і зручнішим. Також за схвалений та опублікований модератором відгук на куплений 
                користувачем товар можуть бути нараховані бонуси на покупки. Щоб отримати бонуси за відгук на куплений товар необхідно перейти 
                по спеціальному посиланню, яке ви отримаєте на електронну пошту.
            </p>
        </div>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            2. Правила публікації рецензій і коментарів до них
        </p>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                2.1. Публікація рецензій
            </p>
            <p>
                Кожен зареєстрований авторизований користувач може залишити свою рецензію про будь-яку книжку на Сайті. Кожен користувач 
                може залишити тільки одну рецензію про кожну книжку. Для уникнення потрапляння на сайт спаму й іншого небажаного контенту 
                всі залишені на Сайті рецензії проходять попередню модерацію. Рецензія розглядається від 1 до 7 робочих днів.
            </p>
            <p>
                На сайті публікують рецензії, які задовольняють наступні умови модерації:
            </p>
            <ul className="flex flex-col gap-2 list-disc marker:text-pink-500 ml-4">
                <li>
                    текст рецензії містить від 500 до 5000 символів
                </li>
                <li>
                    текст є унікальним (не опублікований на інших сайтах)
                </li>
                <li>
                    рецензія аналізує і дає чітку оцінку книзі
                </li>
                <li>
                    рецензія не містить посилань, образ, нецензурних слів, рекламної та іншої інформації, що не стосується рецензованої книжки
                </li>
                <li>
                    не порушує чинне законодавство України, авторські права і права інших користувачів
                </li>
                <li>
                    текст рецензії написано російською або українською мовою з урахуванням правил граматики й орфографії
                </li>
                <li>
                    в тексті не вживаються слова написані ВЕЛИКИМИ ЛІТЕРАМИ
                </li>
            </ul>
            <p>
                Надсилаючи запит на публікацію рецензії, користувач автоматично передає Сайту всі права на рецензію (у тому числі авторські)
                і дає свою згоду на редагування, копіювання, зміну, переклад, публікацію і розповсюдження рецензії (частково або повністю) 
                будь-якими законними способами. Сайт залишає за собою право на відхилення рецензії без пояснення причини. За схвалену і 
                опубліковану модератором рецензію користувач отримує бонуси на покупки.
            </p>
            <p className="font-bold">
                2.2. Публікація коментарів до рецензій
            </p>
            <p>
                Кожен зареєстрований авторизований користувач може залишити свій коментар до будь-якої рецензії на Сайті. Кожен користувач може
                залишити будь-яку кількість коментарів на Сайті. Для уникнення потрапляння на сайт спаму й іншого небажаного контенту 
                всі залишені на Сайті коментарі проходять попередню модерацію.
            </p>
            <p>
                Коментарі призначені для спілкування, обговорення рецензій і особливостей книжки, на яку була залишена рецензія. 
                Коментарі, які містять спам, рекламу, посилання на інші сайти, образи чи контент, що порушує чинне законодавство України, 
                авторські права і права інших користувачів, не будуть опубліковані.
            </p>
            <p>
                Ці Правила публікації поширюються на весь Сайт <Link href="/" className="font-extrabold text-blue-800 underline">yakaboo.ua</Link>
            </p>
            <p>
                Якщо ви не згодні з цими Правилами, будь ласка, не залишайте на сайті запити на публікацію відгуків, рецензій і коментарів до них.
            </p>
        </div>
    </div>
        """
    },
    {
        "title": "Контакти",
        "slug": "contacts",
        "content": """
            <div className="w-[80%] bg-white rounded-md p-5 flex flex-col gap-4 mb-4">
        <div className="flex flex-col gap-2">
            <p>
                Сайт www.yakaboo.ua приймає замовлення цілодобово. Будь-який товар (якщо він є в наявності на складі) буде доставлений 
                максимально швидко. Для оформлення замовлення ви можете скористатися послугами кол-центру Yakaboo за тел. 0-800-335-425 
                (безплатно по Україні). Наші оператори дадуть відповіді на запитання і допоможуть вирішити будь-яку проблему. 
                Кол-центр Yakaboo працює щодня з 09:00 до 20:00.
            </p>
            <div className="flex flex-col gap-1">
                <p className="font-bold">
                    E-mail:
                </p>
                <p>
                    Консультації та замовлення – {" "}
                    <Link href="mailto:support@yakaboo.com" className="font-extrabold text-blue-800 underline text-[0.8rem]">support@yakaboo.ua</Link>
                </p>
                <p>
                    Для ЗМІ - {" "}
                    <Link href="mailto:press@yakaboo.com" className="font-extrabold text-blue-800 underline text-[0.8rem]">press@yakaboo.ua</Link>
                </p>
                <p>
                    Для авторів - {" "}
                    <Link href="mailto:publishing@yakaboo.com" className="font-extrabold text-blue-800 underline text-[0.8rem]">publishing@yakaboo.ua</Link>
                </p>
                <p>
                    Маркетинг - {" "}
                    <Link href="mailto:marketing@yakaboo.com" className="font-extrabold text-blue-800 underline text-[0.8rem]">marketing@yakaboo.ua</Link>
                </p>
                <p>
                    Для корпоративних клієнтів - {" "}
                    <Link href="mailto:library@yakaboo.com" className="font-extrabold text-blue-800 underline text-[0.8rem]">library@yakaboo.ua</Link>
                </p>
                <p>
                    Запити на благодійне надання книжок для громадських об'єднань - {" "}
                    <Link href="mailto:charity@yakaboo.com" className="font-extrabold text-blue-800 underline text-[0.8rem]">charity@yakaboo.ua</Link>
                </p>
            </div>
        </div>
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
            Книгарня
        </p>
        <div className="flex flex-col gap-2">
            <p>
                м. Київ, вул. Хрещатик, 22, 1 поверх (Головпоштамт).
            </p>
            <div className="flex flex-col gap-1">
                <p className="font-bold">
                    Графік роботи:
                </p>
                <p>
                    Пн–Нд 9:00–20:00
                </p>
                <p>
                    Телефон: 0-800-335-425
                </p>
            </div>
            <p>
                Книжковий магазин у центрі Києва – Yakaboo.ua на Хрещатику. Книжкові стелажі і зона видачі інтернет-замовлень. У 
                магазині обладнана спеціальна зона з останніми новинками та бестселерами.  
            </p>
        </div>
    </div>
        """
    },
    {
        "title": "Умови використання сайту",
        "slug": "conditions-of-use",
        "content": """
            <div className="w-[80%] bg-white rounded-md p-5 flex flex-col gap-4 mb-4">
        <h1 className="text-[1.2rem] font-bold">
            ПУБЛІЧНА ОФЕРТА
        </h1>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                Преамбула
            </p>
            <p>
                Шановний Користувач сайту www.yakaboo.ua, звертаємо Вашу увагу, що використання в будь-якому вигляді 
                Сайту (в тому числі, але не обмежуючись розміщенням Вами Замовлень товарів з використанням сайту www.yakaboo.ua, 
                участь в бонусних програмах, акціях, заповнення заявок, форм і т.п.) означає, що Ви ознайомлені та згодні з умовами 
                використання Сайту www.yakaboo.ua, а також є акцептом Вами даної Публічної оферти. Дана Публічна оферта є обов'язковою 
                для виконання сторонами. У разі Вашої незгоди з умовами даної Публічної оферти, Ви повинні утриматися від використання 
                сайту 
                <Link href="/" className="font-extrabold underline">www.yakaboo.ua.</Link>
            </p>
        </div>
        <h1 className="text-[1.2rem] font-bold">
            ВИЗНАЧЕННЯ ТЕРМІНІВ
        </h1>
        <div className="flex flex-col gap-2">
            <p>
                <span className="font-bold">
                    Адміністрація
                </span> - 
                адміністрація інтернет-магазину «YAKABOO.UA», що розміщено на вeб-сайті www.yakaboo.ua, Товариство з обмеженою 
                відповідальністю «ЯКАБУ РІТЕЙЛ», зареєстроване  в Україні, місцезнаходження за адресою: 04073, 
                м. Київ, вул. Кирилівська, 160, літ. Ю.
            </p>
            <p>
                <span className="font-bold">
                    Акційний контент 
                </span> - 
                контент, що може бути доступний для завантаження за акційною ціною протягом певного проміжку часу 
                про що буде поінформовано у відповідному розділі на сайті.
            </p>
            <p>
                <span className="font-bold">
                    Замовлення
                </span> - 
                належним чином оформлений і розміщений запит Покупця (заповнені відповідні поля на сайті в розділі «Оформлення замовлення»), 
                адресований Продавцю, з пропозицією здійснити продаж обраного на сайті переліку Товару, із зазначенням його кількості.
            </p>
            <p>
                <span className="font-bold">
                    Користувач 
                </span> - 
                фізична особа, яка досягла 18-річного віку, що володіє повною дієздатністю, що використовує даний сайт 
                і/або його окремі інструменти, яка погодилася з умовами Публічної оферти і виконала всі її умови описані нижче.
            </p>
            <p>
                <span className="font-bold">
                    Контент
                </span> - 
                товар, що представлений  на сайті www.yakaboo.ua. у вигляді текстових, зображувальних, аудіо та відео файлів, 
                що надані у різних форматах та представлені для огляду, скачування та інших дій Користувачем.  
            </p>
            <p>
                <span className="font-bold">
                    Обліковий запис
                </span> - 
                унікальні облікові та персональні дані Користувача, які ідентифікують Користувача на Сайті, зберігаються на апаратних 
                ресурсах Адміністрації та надають Користувачеві можливість використання функціоналу Сайту, відповідно до умов цієї Угоди.
            </p>
            <p>
                <span className="font-bold">
                    Одержувач
                </span> - 
                особа, зазначена Платником у розділі «Оформлення замовлення», в якості особи, що уповноважена отримати товар. 
                Якщо інше не зазначено в розділі «Оформлення замовлення», Одержувачем є Платник.
            </p>
            <p>
                <span className="font-bold">
                    Особистий кабінет 
                </span> - 
                комплекс програмних функцій Сайту, які дозволяють Користувачеві, який авторизувався належним чином в свій Обліковий запис, 
                отримувати інформацію про здійснені ним Замовлення, покупки, вносити зміни в облікові та персональні дані Користувача 
                та отримувати доступ до придбаного Контенту
            </p>
            <p>
                <span className="font-bold">
                    Платник
                </span> - 
                особа, яка здійснює оплату замовлення Покупця, якщо інше не зазначено в розділі «Оформлення замовлення», Платником є Покупець.
            </p>
            <p>
                <span className="font-bold">
                    Покупець
                </span> -
                зареєстрований Користувач, що здійснює замовлення та має намір придбати/купує товари, пропоновані до продажу
                 Продавцем та представлені на сайті {" "}
                 <Link href="/" className="font-bold underline">www.yakaboo.ua.</Link>
            </p>
            <p>
                <span className="font-bold">
                    Покупець контенту
                </span> - 
                Покупець, що отримує можливість і здійснює завантаження, пропонованого на сайті www.yakaboo.uа контенту.
            </p>
            <p>
                <span className="font-bold">
                    Правовласник
                </span> - 
                власник Контенту.
            </p>
            <p>
                <span className="font-bold">
                    Продавець
                </span> - 
                Товариство з обмеженою відповідальністю «ЯКАБУ РІТЕЙЛ».
            </p>
            <p>
                <span className="font-bold">
                    Пропозиція
                </span> - 
                відомості про товар, розміщені Продавцем на сайті, які включають в себе інформацію про товар, його ціну, 
                пособи оплати та доставки, інформацію про знижки та акційні пропозиції на товар, а також інші умови 
                придбання товару. Умови Пропозицій, розміщених на сайті, встановлюються Продавцем. Пропозиція є 
                інформацією про можливі умови покупки товару.
            </p>
            <p>
                <span className="font-bold">
                    Сайт
                </span> - 
                вeб-сайт, що має адресу в мережі інтернет www.yakaboo.ua, на окремих сторінках (в розділах) якого розміщено правила 
                (умови) реєстрації, оформлення замовлення, бонусної програми, оплати, доставки, повернення товару, гарантії тощо, 
                а також міститься інформація про Покупця (контактні дані, замовлення, адреси доставки, та ін.), за допомогою якого 
                Користувач має можливість здійснити покупку бажаного товару.
            </p>
            <p>
                <span className="font-bold">
                    Товар
                </span> - 
                матеріальний об'єкт, пропонований до продажу Продавцем, розміщений на сайті, щодо якого вказана ціна, назва, опис, 
                характеристики та зазначено статус його доступності.
            </p>
            <p>
                <span className="font-bold">
                    Угода
                </span> - 
                дана публічна оферта, включаючи всі її умови та додатки до неї.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold ml-10">
                Загальні положення
            </p>
            <p>
                1.1. Ця Угода регулює порядок доступу Користувача до інформації, що розміщується на Сайті, порядок 
                використання Сайту, а також можливість передачі товарів та інші умови.
            </p>
            <p>
                1.2. Сайт є платформою для розміщення пропозицій про продаж товарів Продавцем.
            </p>
            <p>
                1.3. Дана угода  відповідно до ст. ст. 633, 641 і гл. 63 Цивільного кодексу України є Публічним договором (офертою) 
                і адресовано невизначеному колу осіб не залежно від статусу (фізична особа, юридична особа, фізична особа - 
                підприємець), що бажають придбати товари, інформація про які міститься на Сайті. Оскільки ця Угода є публічною офертою, 
                то отримуючи доступ до матеріалів Сайту Користувач\Покупець вважається приєднався до цієї Угоди.
            </p>
            <p>
                1.4. Інформація про товар відображається на Сайті і є динамічною. Це означає, що інформація може бути оновлена, 
                змінена і доповнена Адміністрацією в будь-який момент часу без попереднього повідомлення про це Користувача. 
                Визначені зміни вступають в силу після їх публікації на Сайті та застосовуються до будь-якого замовлення, 
                зробленого після їх публікації.
            </p>
            <p>
                1.5. Інформація про товар Продавця, умови його придбання, ціни та будь-яка інша інформація Продавця точно 
                відображається на Сайті. Інформація на Сайті про Товар, Контент, Продавця та інші умови роботи Сайту та 
                правовідносин між сторонами цієї Угоди слугує лише в якості доповнення умов цієї Угоди. У разі суперечності 
                інформації на Сайті умовам цієї Угоди, умови Угоди мають перевагу та підлягають застосуванню.
            </p>
            <p>
                1.6. Ця Угода може бути укладена фізичною особою, яка досягла 18-річного віку, що володіє повною дієздатністю, 
                що використовує даний сайт і\або його окремі інструменти, яка погодилася з умовами Угоди та повністю приймає 
                на себе зобов'язання, що виникають в результаті використання Сайту і укладення цієї Угоди.
            </p>
            <p>
                1.7. Замовляючи товар на Сайті, Покупець погоджується з усіма умовами даної Угоди та її Додатків.
            </p>
            <p>
                1.8. Пропозиція на Сайті не є офертою. Однак, Покупець після ознайомлення з Пропозицією вправі зробити оферту 
                Продавцю шляхом обрання товару та заповнення форми у розділі «Оформлення замовлення». Заповнення визначеної 
                форми вважається офертою Покупця Продавцю на придбання відповідного товару на умовах, зазначених в Пропозиції. 
                Оферту Продавцю вправі зробити і незареєстрований  Користувач, при цьому він повинен коректно ввести всі 
                необхідні дані у форму «Оформлення замовлення» на Сайті.
            </p>
            <p>
                1.9. Оферта вважається прийнятою Продавцем (акцепт) якщо останній здійснив дії, які свідчать про прийняття 
                оферти Покупця, а саме: фактично відвантажив товар відповідно до умов, передбачених офертою Покупця або 
                надав доступ та можливість завантажити контент через Особистий кабінет Користувача.
            </p>
            <p>
                1.10. Після отримання оферти Покупця Продавець має право запропонувати придбати товар на інших умовах, 
                ніж було передбачено офертою Покупця. У цьому випадку така пропозиція вважається зустрічною офертою і 
                має бути прийнята Покупцем. Прийняттям зустрічної оферти вважається фактично оплата, отримання 
                Покупцем\Одержувачем товару на умовах, обумовлених зустрічною офертою. Продавець має право відкликати 
                таку зустрічну оферту до моменту оплати та видачі товару.
            </p>
            <p>
                1.11. У випадку помилковості відправленого акцепту Сторони мають право змінити умови тільки у випадку вчасного 
                повідомлення про таку помилковість одна одну.
            </p>
            <p>
                1.12. Достатнім доказом прийняття оферти Продавцем або зустрічної оферти (тобто узгодження Сторонами 
                всіх істотних умов продажу товару) є фактична його оплата, отримання  товару Покупцем\Одержувачем.
            </p>
            <p>
                1.13. Не вважається прийняттям Продавцем оферти Покупця направлення Продавцем\Адміністрацією засобами 
                електротехнічного (SMS-інформування, електронна пошта, телефон і т.п.) або іншого зв'язку повідомлення 
                Продавця/Адміністрації про одержання Замовлення Покупця або про терміни його отримання і/або про ціну 
                товару. Дане повідомлення є виключно повідомленням про отримання Продавцем оферти Покупця (але не про 
                її прийняття) і містить відтворення умов оферти, наданої  Покупцем.
            </p>
            <p>
                1.14. Інформація про Товар розміщена безпосередньо на Сайті, окрім цього при отриманні товару, 
                до моменту підписання документів, що підтверджують отримання товару, Покупець/Одержувач зобов'язаний 
                ознайомитися з інформацією про товар, що міститься на Товарі і/або упаковці та/або в товаросупровідних 
                документах. У разі необхідності отримання додаткової інформації про товар Покупець/Одержувач зобов'язаний 
                зв'язатися з Продавцем та отримати необхідну інформацію засобами дистанційного зв'язку до моменту прийняття 
                такого  товару.
            </p>
            <p>
                1.15. Знижки/акції не сумуються з іншими знижками/акціями і знижками за промокодом.  
            </p>
            <p>
                1.16. Знижка за промокодом не застосовується при купівлі подарункового сертифіката.  
            </p>
            <p>
                1.17. Подарунковим сертифікатом можна оплатити будь-який товар на сайті, крім подарункових сертифікатів.
            </p>
            <p>
                1.18. Подарунковий сертифікат можна використати лише один раз.
            </p>
            <p>
                1.19. Термін дії подарункового сертифіката становить 12 (дванадцять) календарних місяців.
            </p>
            <p>
                1.20. Якщо протягом строку дії подарункового сертифіката Покупцем не буде реалізоване право на придбання 
                овару, то сума, сплачена за сертифікат, поверненню не підлягає.
            </p>
            <p>
                1.21. Якщо сума чека перевищує номінал сертифіката – Покупцю буде необхідно доплатити різницю, 
                але якщо сума менша за номінал, залишок не повертається і подарунковий сертифікат буде вважатись 
                використаним.
            </p>
            <p>
                1.22. Розділити номінал подарункового сертифіката на декілька різних чеків неможливо.
            </p>
            <p>
                1.23. Кількість подарункових сертифікатів для оплати покупки необмежена, їх можна підсумувати.
            </p>
            <p>
                1.24. У разі втрати подарунковий сертифікат не підлягає поверненню чи відновленню. Подарунковий 
                сертифікат не підлягає обміну на грошові кошти.
            </p>
            <p>
                1.25. Власником прав інтелектуальної власності на поширення Контенту, представленого на Сайті, є 
                ТОВ «Якабу Рітейл», що зареєстроване за адресою Україна, 04073, м. Київ, вул. Кирилівська, 160, 
                літ. Ю. Використання текстових та фото/відео матеріалів Сайту можливо лише з дозволу Адміністрації.
            </p>
            <p>
                1.26. Даний сайт: https://www.yakaboo.ua може використовуватись іншими суб’єктами господарювання на 
                підставі відповідних договорів оренди та/або надання послуг та ін. У свою чергу зазначені суб’єкти 
                господарювання матимуть право здійснювати продаж товарів кінцевим споживачам, та нестимуть 
                відповідальність по даній продукції перед кінцевими споживачами.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold ml-10">
                Загальні положення
            </p>
            <p>
                2.1. Для отримання можливості здійснити покупку на сайті Користувач повинен зареєструватися на сайті. 
                Для цього він повинен натиснути кнопку «Вхід» та заповнити реєстраційну  форму. Адміністратор залишає за собою 
                право відхилити будь-яку заявку про реєстрацію   та/або припинити будь-чию реєстрацію  на Сайті.
            </p>
            <p>
                2.2. Також Користувач може здійснити Замовлення товару без відповідної реєстрації, але при цьому ним повинні 
                бути коректно заповнені обов'язкові поля у формі «Оформлення замовлення».
            </p>
            <p>
                2.3. Під час  реєстрації на Сайті, а саме заповнення реєстраційної форми та створення Особистого кабінету, 
                Користувач зобов'язується вказувати інформацію, позначену як обов'язкова, в повному обсязі, а також 
                Користувач несе відповідальність за достовірність, правильність і правдивість як обов'язкової, так і 
                іншої наданої інформації. У разі виявлення будь-якої недостовірності, неправильності або неправдивості 
                інформації, наданої Зареєстрованим Користувачем, Адміністрація Сайту безумовно залишає за собою право в 
                будь-який момент анулювати Обліковий запис такого Зареєстрованого Користувача без будь-яких компенсацій 
                чи відшкодувань.
            </p>
            <p>
                2.4. Внесення інформації у реєстраційну форму Сайту, а також оформивши Замовлення, Покупець підтверджує, що 
                ознайомлений з умовами даної Угоди, і всі дії, які їм будуть здійснені, не будуть суперечити умовам цієї Угоди.
            </p>
            <p>
                2.5. Замовлення вважається прийнятим до виконання, а Угода між Покупцем і Продавцем — 
                укладеною, після отримання Покупцем електронного повідомлення на адресу електронної пошти 
                від Продавця або шляхом здійснення телефонного дзвінка Продавцем на номер мобільного телефону, 
                що вказані при реєстрації Покупцем, з підтвердженням факту узгодження та приймання Замовлення.
            </p>
            <p>
                2.6. Продавець має право відхилити Замовлення в разі фактичної відсутності товару на складі, шляхом 
                надсилання електронного повідомлення чи здійснення телефонного дзвінка Покупцеві. У такому випадку 
                права і обов'язки Сторін, пов'язані з продажем, доставкою і передачею замовленого товару Покупцю і 
                оплатою його Продавцю передбачені даною Угодою, припиняються, а вартість товару, у випадку сплати 
                за нього, повертається Покупцю.
            </p>
            <p>
                2.7. У випадку відсутності можливості підтвердження Замовлення Продавцем у Покупця, з причин невірно 
                вказаної адреси електронної пошти чи\та номеру телефону, Продавець має право відмінити таке не підтверджене Замовлення.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold ml-10">
                Вартість та умови оплати товарів
            </p>
            <p>
                3.1. Ціна товару вказана на Сайті у відповідному розділі на момент оформлення Замовлення, і не включає вартість доставки.
            </p>
            <p>
                3.2. Продавець має право в односторонньому порядку без попередження змінити ціну на товар. Однак Продавець не 
                має права змінювати ціну замовленого товару після того, як Замовлення було прийнято Продавцем, а Покупець  
                oтримав електронне повідомлення або телефонний дзвінок, що підтверджує Замовлення або Покупець здійснив розрахунок за товар.
            </p>
            <p>
                3.3. Вартість товару сплачується в національній валюті України – гривні.
            </p>
            <p>
                3.4. Покупець може здійснити оплату замовленого Товару: банківською картою Visa або MasterCard на 
                Сайті в момент оформлення Замовлення; перерахувавши грошові кошти безпосередньо перед отриманням 
                Товару, на банківський рахунок Продавця; банківською картою Visa або MasterCard  в терміналах, 
                розміщених в відділеннях самовивозу Yakaboo.ua перед отриманням Замовлення; засобами Бонусного 
                рахунку з урахуванням умов і обмежень, визначених у розділі «Бонусна програма».
            </p>
            <p>
                3.5. Користувач/Покупець розуміє і погоджується з тим, що оператором з прийому і проведення платежів за товари, 
                представлені на Сайті, є, залежно від обставин, одна з компаній-екваєрів, підключена до Сайту і обрана 
                самостійно Користувачем/Покупцем у процесі здійснення оплати за товар.
            </p>
            <p>
                3.6. Товар до моменту його передачі Продавцем, повинен бути повністю оплачений Покупцем.
            </p>
            <p>
                3.7. У разі, якщо Замовлення анульоване Покупцем або відхилене Продавцем, сплачена вартість 
                Товару підлягає поверненню, а  вже витрачені кошти на  доставку, понесені до моменту 
                анулювання Замовлення Покупцем, поверненню не підлягають.
            </p>
            <p>
                3.7.1. У випадку, коли оплачене Покупцем Замовлення було відправлено до обраного Покупцем відділу служби доставки, 
                але Покупець відмовився від огляду та прийняття Замовлення, таке Замовлення вважається анульованим з 
                ініціативи Покупця відповідно до п. 3.7. цієї Угоди, а сплачені Покупцем кошти за Замовлення підлягають 
                поверненню за відрахуванням вартості послуг доставки Замовлення до відділу служби доставки
            </p>
            <p>
                3.7.2. У випадку відмови Покупця від отримання Замовлення у відділі служби доставки без 
                пред’явлення та оформлення претензії до служби доставки Покупцем відповідно до п. 3.9. 
                цієї Угоди, така відмова Покупця від отримання Замовлення вважається анулюванням Замовлення 
                з ініціативи Покупця відповідно до п. 3.7. цієї Угоди, а сплачені Покупцем кошти за 
                Замовлення підлягають поверненню за відрахуванням вартості послуг доставки Замовлення 
                до відділу служби доставки.
            </p>
            <p>
                3.8. Умови оплати Контенту
            </p>
            <p>
                3.8.1. Отримання доступу до перегляду каталогу Контенту, розміщеного на www.yakaboo.ua у відповідному розділі, є 
                безплатним для Користувачів Сайту, а плата стягується за отримання доступу до завантаження обраних 
                файлів Контенту у представлених на сайті форматах.
            </p>
            <p>
                3.8.2.  Оплата за платний Контент здійснюється банківською картою Visa або MasterCard на Сайті в момент оформлення Замовлення.
            </p>
        </div>
    </div>
        """
    },
    {
        "title": "Подарункові сертифікати",
        "slug": "podarunkovi-sertifikaty",
        "content": """
            <div className="w-[80%] bg-white rounded-md p-5 flex flex-col gap-4 mb-4">
        <p className="font-bold border-b border-gray-300 pb-3 text-[1.1rem]">
           Подарункові сертифікати Yakaboo.ua
        </p>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                Найкращий подарунок – це можливість вибору. Довірте вибір одержувачу подарунка.
            </p>
            <p>
                <Link href="#" className="text-blue-800 font-extrabold underline">
                    Подарунковий сертифікат Yakaboo.ua
                </Link> {" "}
                у вигляді пластикової карти або електронного сертифікату — це попередній платіж, який дає можливість купувати 
                будь-які товари магазину, на суму еквівалентну його номіналу.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                Переваги купівлі сертифікатів у нашому магазині
            </p>
            <p>
                Yakaboo.ua — найбільший в Україні книжковий інтернет-магазин, який налічує понад 600 000 книг 71 мовою, включаючи 
                найостанніші новинки і світові бестселери. Книги також доступні в електронному та аудіо форматах. Каталог товарів оновлюється щодня.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                Ідеальний подарунок для корпоративних клієнтів
            </p>
            <p>
                За допомогою сертифікатів Yakaboo.ua ви зможете зробити подарунки необмеженій кількості співробітників і 
                ділових партнерів, навіть за межами України.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                Цифровий подарунок без кордонів
            </p>
            <p>
                Немає можливості привітати особисто? Подаруйте електронний сертифікат — ми доставимо його в будь-яку точку світу за лічені секунди.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                Ексклюзивне дизайнерське рішення
            </p>
            <p>
                Для корпоративних клієнтів ми пропонуємо спеціальні умови співпраці. Ми можемо розробити унікальні 
                сертифікати, які будуть містити вашу корпоративну стилістику і будь-який бажаний номінал.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                Правила використання сертифікату
            </p>
            <ul className="flex flex-col gap-1 list-disc marker:text-pink-500 ml-4">
                <li>
                    Сертифікат не підлягає поверненню або грошовому обміну. 
                </li>
                <li>
                    Загублені сертифікати не підлягають відновленню.
                </li>
                <li>
                    Сертифікат має обмежений термін дії.
                </li>
                <li>
                    У разі перевищення номіналу за сумою покупки необхідно сплатити різницю.
                </li>
                <li>
                    Якщо вартість покупки менша, ніж номінал сертифікату, необхідно сплатити 1 грн., при цьому залишок коштів згорає, 
                    і його не можна перенести на накопичувальний бонусний рахунок.
                </li>
            </ul>
        </div>
    </div>
        """
    },
    {
        "title": "Питання по e-books",
        "slug": "faq",
        "content": """
            <div className="w-[80%] bg-white rounded-md p-5 flex flex-col gap-4 mb-4">
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                1. Що таке електронні книжки/аудіокниги?
            </p>
            <p>
                Електронна книга (англ. e-book) – версія книги в електронному (цифровому) форматі. Даний термін застосовується як для творів, 
                представлених у цифровій формі, так і по відношенню до пристроїв, що використовуються для їх читання. Аудіокнига 
                (від лат. Audio «слухати») – озвучений літературний твір, записаний на будь-який звуковий носій.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                2. Як придбати електронну книжку/аудіокнигу? 
            </p>
            <ul className="flex flex-col gap-2 list-disc marker:text-pink-500 ml-4">
                <li>
                    Зареєструватись на сайті;
                </li>
                <li>
                    Знайти потрібну книгу в потрібному форматі
                </li>
                <li>
                    Покласти її в кошик (можна додавати декілька книг);
                </li>
                <li>
                    Оформити замовлення;
                </li>
                <li>
                    Оплатити вміст кошику.
                </li>
            </ul>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                3. Де та як я можу отримати доступ до електронної книги/аудіокниги після оплати?
            </p>
            <p>
                Необхідно увійти в Особистий кабінет, натиснувши у верхньому правому куті сайту кнопку «Вхід», ввести логін 
                (номер телефону або e-mail), пароль та в розділі «Мої електронні книги» або «Мої аудіокнижки» завантажити придбану 
                книгу в потрібному форматі. Чи просто перейти в «Мої електронні книги» або «Мої аудіокнижки» свого Особистого кабінету, 
                якщо ви вже увійшли в свій обліковий запис на сайті раніше.
            </p>
        </div>
        <div className="flex flex-col gap-1">
            <p className="font-bold">
                4. Який формат книжки мені підійде?
            </p>
            <p>
                <span className="font-bold">
                    .txt 
                </span> - стандартний текстовий файл. Більша частина форматування буде втрачена, але книга відкриється будь-якою програмою.
            </p>
            <p>
                <span className="font-bold">
                    .rtf 
                </span> - текст із форматуванням, зручний для читання на комп’ютері чи для друку.
            </p>
            <p>
                <span className="font-bold">
                    .fb2
                </span> - відкритий формат на основі XML, напряму читається програмою Haali Reader та багатьма іншими. 
                Читалки та редактори існують практично для будь-якої ОС. Існує також програма конвертер FB2Any. 
                Рекомендований для пристрою PocketBook. Формат fb2 в карточках деяких товарів на сайті може надаватись покупцеві у вигляді fb2.zip.
            </p>
            <p>
                <span className="font-bold">
                    .pdf
                </span> - документ Adobe Acrobat. Підходить для читання на багатьох e-ink рідерах.
            </p>
            <p>
                <span className="font-bold">
                    .epub
                </span> - формат, що активно просувається фірмою Adobe, оснований на HTML. Підтримується багатьма сучасними програмами 
                та більшістю нових пристроїв. <br />Достатньо зручно його використовувати на iPhone.
            </p>
            <p>
                <span className="font-bold">
                    .mobi
                </span> - спеціалізований формат, створений спеціально для рідера  Amazon Kindle та, відповідно, підтримується лише цим рідером. 
                Ідентичний формат mobi.prс, на сайті позначено як mobi. У 2022 році Amazon оголосив про відмову від формату 
                <span className="font-bold">.mobi </span>на користь <span className="font-bold">epub.</span>
            </p>
            <p>
                <span className="font-bold">
                    .mp3
                </span> - формат для зберігання та прослуховування аудіо-інформації (аудіокнижок).
            </p>
            <p>
                <span className="font-bold">
                    .mp4
                </span> - формат для зберігання та прослуховування аудіо-інформації (аудіокниг), що зручно використовувати в мобільній версії.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                5. Як мені придбати потрібний формат?
            </p>
            <p>
                У нас діє принцип: одна покупка – всі формати. Після купівлі книги вам будуть доступні для завантаження всі 
                запропоновані формати в розділі «Мої електронні книги» або «Мої аудіокнижки».
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                6. Що можна робити з придбаною книгою?
            </p>
            <p>
                Використовувати в особистих цілях будь-яким способом. Читати або слухати, конвертувати, 
                зберігати резервну копію. Єдиний виняток – забороняється передавати придбану книгу іншим особам чи 
                розміщувати її в Інтернеті для загального користування.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                7. Скільки разів я можу завантажити придбану книжку?
            </p>
            <p>
                Загальна кількість завантажень необмежена. Придбавши книжку в нас, ви зможете отримати до неї доступ завжди – з будь-якого місця,
                з будь-якого комп’ютера. У деяких випадках кількість завантажень файлів Контенту, що придбані Покупцем від окремих Правовласників 
                (безпосередніх власників контенту) може бути обмежена. Інформація про обмеження кількості завантажень Контенту може бути надана 
                додатково. У разі перевищення допустимої кількості завантажень Покупцем Контенту доступ до придбаного файлу Контенту буде припинено. 
                Якщо перевищення допустимої кількості завантажень відбулося з технічних причин (наприклад, через нестабільне з'єднання або 
                проблеми з програмним забезпеченням зі сторони Покупця Контенту), Адміністрація сайту залишає за собою право, але не зобов'язана, 
                надати такому Покупцю контенту можливість здійснити одне додаткове завантаження.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                8. Що робити, якщо придбана книжка зникла з розділу «Мої електронні книги» або «Мої аудіокнижки» в Особистому кабінеті?
            </p>
            <p>
                Придбана книжка залишається доступною в розділі «Мої електронні книги» або «Мої аудіокнижки» назавжди. Але якщо ви виявили, 
                що книжка зникла, відразу повідомте про це співробітника call-center сайту. Ми зробимо все можливе, щоб у найкоротші 
                терміни книга знову була доступна вам.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                9. Як оплатити обрані книги?
            </p>
            <p>
                Оплата замовлення, в якому є електронні товари, можлива лише on-line (усіма доступними на сайті способами). 
                Також ви можете використати свої Бонуси для купівл
            </p>
        </div>
        <div className="flex flex-col gap-">
            <p className="font-bold">
                10. Що робити, якщо в кошику є паперові, електронні книжки та аудіокниги, а грошей на банківській картці 
                недостатньо (а доступна в такому випадку тільки оплата on-line)?
            </p>
            <p>
                Потрібно оформити два замовлення: одне тільки на електронні книжки/аудіокниги та оплатити on-line; друге – 
                на паперові книжки та оплатити будь-яким іншим доступним способом (наприклад, готівкою кур’єру при отриманні).
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                11. Замовлення на електронні книжки/аудіокниги оплачене, але в розділі Мої електронні книги/Мої аудіокнижки покупок немає.
            </p>
            <p>
                Трішки терпіння й ваші електронні книги/аудіокниги будуть доступні для вас. Інколи у випадку, якщо ви оплатили замовлення 
                Бонусами, покупки потрапляють в Мої електронні книги/Мої аудіокнижки з запізненням від декількох секунд до двох хвилин. 
                Також можете перезавантажити сторінку за допомогою комбінації клавіш Ctrl+F5. 
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                12. Не вдається відкрити придбану електронну книжку/аудіокнигу на iPhone, що робити?
            </p>
            <p>
                Потрібно відкрити браузер Safari (або перевірити чи використовуєте ви його). У ньому перейти на сайт  
                http://www.yakaboo.ua та відкрити розділ Мої електронні книги/Мої аудіокнижки. У ньому обрати куплену книгу та 
                натиснути Завантажити, далі обрати формат, в якому хочете читати книгу. Вам буде запропоновано відкрити книгу 
                за допомогою застосунку для читання iBooks (або будь-якого іншого, що є на вашому iPhone. Якщо ви використовуєте 
                інший браузер (не «рідний» для iPhone Safari), це може викликати проблеми з можливістю відкриття електронної книги/аудіокниги.
            </p>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                13. Як завантажити аудіокниги?
            </p>
            <p className="font-bold italic">
                Для Користувачів операційної системи Android:
            </p>
            <ul className="flex flex-col gap-1 list-disc marker:text-pink-500 ml-4">
                <li>
                    Перейти в Особистому кабінеті у вкладку «Мої аудіокнижки».
                </li>
                <li>
                    У вкладці «Мої аудіокнижки» вибрати книгу і натиснути кнопку «Завантажити».
                </li>
                <li>
                    Залежно від типу товару, книга може мати кілька форматів: MP3, MP4.
                </li>
                <li>
                    Вибрати потрібний формат, після чого відбудеться завантаження у папку, яка обрана на вашому комп'ютері для завантаження файлів із браузера.
                </li>
                <li>
                    Відтворити файл можна у будь-якому аудіоплеєрі, який підтримує формати MP3, MP4.
                </li>
            </ul>
            <p className="font-bold italic">
                Для Користувачів операційної системи IOS:
            </p>
            <ul className="flex flex-col gap-1 list-disc marker:text-pink-500 ml-4">
                <li>
                    Увага: для користувачів IOS скачування аудіокниги можливе тільки у браузері Safari.
                </li>
                <li>
                    Перейти в Особистому кабінеті у вкладку «Мої аудіокнижки».
                </li>
                <li>
                    У вкладці «Мої аудіокнижки» вибрати книгу і натиснути кнопку «Завантажити».
                </li>
                <li>
                    Залежно від типу товару, книга може мати кілька форматів: MP3, MP4.
                </li>
                <li>
                    Вибрати потрібний формат. Після підтвердження дії «Завантажити», скачування відбудеться в автоматичному режимі у 
                    папку «Завантаження», з якої файл можна відтворити як стандартним застосунком «Книги», так і будь-яким іншим 
                    застосунком, який підтримує формати MP3, MP4.
                </li>
            </ul>
            <p className="font-bold">
                Примітка:
            </p>
            <ul className="flex flex-col gap-1 list-disc marker:text-pink-500 ml-4">
                <li>
                    Швидкість завантаження залежить від розміру файлу, швидкості інтернету вашого провайдера і потужності самого пристрою.
                </li>
                <li>
                    Якщо аудіофайл містить розбивку на розділи (пункти), то їх сортування залежить від налаштувань у вашому аудіоплеєрі.
                </li>
                <li>
                    M4B – це файл аудіокниги, створений на основі MPEG-4 формату контейнера, зазвичай стиснутий кодеком AAC,
                     майже ідентичний файлу M4A, але призначений для аудіокниг, тому що підтримує «закладки».
                </li>
            </ul>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                14. Чому може не відкриватися книга?
            </p>
            <ul className="flex flex-col gap-1 list-disc marker:text-pink-500 ml-4">
                <li>
                    На пристрої не встановлений відповідний софт для відкриття файлів форматів MP3, MP4.
                </li>
                <li>
                    Файл завантажено не повністю, наприклад, стався обрив інтернет з'єднання.
                </li>
                <li>
                    Проблема з самим файлом. У такому випадку просимо звернутися до нашої служби підтримки. Ми зробимо все можливе, 
                    щоб у найкоротші терміни книга стала вам доступна.
                </li>
            </ul>
        </div>
        <div className="flex flex-col gap-2">
            <p className="font-bold">
                15. Я придбав не ту електронну книжку/не сподобалась електронна книжка/замість паперової книги купив електронну. Чи можу я повернути гроші?
            </p>
            <p>
                На жаль, за електронний контент адміністрація сайту не повертає грошові кошти 
                (див. <Link href="#" className="font-extrabold text-blue-500 underline">Умови використання сайту</Link>). 
                Електронні книжки та аудіокниги не підлягають поверненню чи обміну. 
            </p>
        </div>
    </div>
        """
    }
]

PROMO_CATEGORIES = [
    {
        "title": "Книги",
        "slug": "books",
    },
    {
        "title": "Електронні книги",
        "slug": "e-books"
    },
    {
        "title": "Аудіокниги",
        "slug": "audiobooks"
    },
    {
        "title": "Настільні ігри",
        "slug": "nastilni-igry"
    },
    {
        "title": "Подарунки",
        "slug": "podarunky"
    }
]

PROMOS = [
    {
        "title": "Видавництво тижня! До -35% на книжки від #книголав",
        "slug": "vydavnytstvo-tyzhnia-do-35-vid-knygolav",
        "image": "https://static.yakaboo.ua/media/promotions/image/830X299_1953221678.png",
        "main_description": """Замовляйте акційні книжки видавництва #книголав 
        зі знижками до -35% на Yakaboo.ua""",
        "short_description": """
            <p className="text-[0.9rem]">
                Замовляйте акційні книжки видавництва 
                <span className="font-bold">
                    #книголав зі знижками до -35%
                </span> на Yakaboo.ua
            </p>
        """,
        "end_date": datetime.datetime(2025, 5, 7),
        "active": True,
        "category_ids": [1]
    },
    {
        "title": "Кешбек 10% на навчальну літературу та книжки англійською мовою",
        "slug": "cashback-10-na-navchalnu-literaturu",
        "image": "https://static.yakaboo.ua/media/promotions/image/830X299_31540_.png",
        "main_description": """
            Замовляйте навчальну літературу на книжки англійською 
            мовою - та отримуйте 10% кешбеку
        """,
        "short_description": """
             <p className="text-[0.9rem]">
                Замовляйте навчальну літературу та книжки англійською мовою - 
                та отримуйте 
                <span className="font-bold">
                    10% кешбеку
                </span> на Yakaboo.ua
            </p>
        """,
        "end_date": datetime.datetime(2025, 5, 1),
        "active": True,
        "category_ids": [1]
    },
    {
        "title": "До -50% на книжки до Всесвітнього дня бажань",
        "slug": "do-50-na-knyzhky-do-dnya-bazhan",
        "image": "https://static.yakaboo.ua/media/promotions/image/830_299_1109_21042544.png",
        "main_description": """
            Замовляйте акційні книжки зі знижками до -50% до
            Всесвітнього дня бажань на Yakaboo.ua
        """,
        "short_description": """
            <p className="text-[0.9rem]">
                Замовляйте акційні книжки
                <span className="font-bold">
                    зі знижками до -50%
                </span> до Всесвітнього дня бажань на Yakaboo.ua
            </p>
        """,
        "end_date": datetime.datetime(2025, 5 , 10),
        "active": True,
        "category_ids": [1, 2, 3]
    },
    {
        "title": "Безплатна доставка Meest ПОШТА для замовлень від 349₴",
        "slug": "bezplatna-dostavka-meest-poshta-dlya-zamovlen-vid-349",
        "image": "https://static.yakaboo.ua/media/promotions/image/830_299_1446_2104_Meest.png",
        "main_description": """
            Замовляйте книжки - і користуйтесь безплатною доставкою 
            до відділення або поштомату Meest ПОШТА
        """,
        "short_description": """
             <p className="text-[0.9rem]">
                Замовляйте книжки на суму від 349 грн - 
                і користуйтесь 
                <span className="font-bold">
                    безплатною доставкою
                </span> 
                до відділення чи поштомату 
                <span className="font-bold">
                    Meest ПОШТА 
                </span> 
            </p>
        """,
        "end_date": None,
        "active": True,
        "active_ids": [1]
    }
]

PUBLISHING = [
    {
        "title": "А-ба-ба-га-ла-ма-га",
        "slug": "A_ba_ba_ga_la_ma_ga",
        "logo": "https://static.yakaboo.ua/media/entity/book_publisher/a/b/ababa.svg.png",
        "short_description": """
            «А-ба-ба-га-ла-ма-га» – це оригінальні подарункові книжки для 
            «малюків від 2 до 102», які відрізняються художньою і 
            поліграфічною якістю. Видавничий дім «А-ба-ба-га-ла-ма-га» 
            був заснований Іваном Малковичем в Україні у 1992 році. 
            Книжки видавництва виходять не лише в Україні, але й в 
            Америці, Швейцарії, Словаччині. Видавництво успішно продає 
            свої права провідним видавцям світу, серед яких гранд 
            «Alfred A. Knopf» (Нью-Йорк). Високий рівень роботи
            «А-ба-ба-га-ла-ма-га» підтверджується і тим, 
            що видавництво володіє ексклюзивними правами на 
            видання Джоан Роулінг «Гаррі Поттер» в Україні. 
            Віднедавна «А-ба-ба-га-ла-ма-га» публікує також переклади
        """,
        "long_description": """
            «А-ба-ба-га-ла-ма-га» – це оригінальні подарункові книжки для 
            «малюків від 2 до 102», які відрізняються художньою і 
            поліграфічною якістю. Видавничий дім «А-ба-ба-га-ла-ма-га»
            був заснований Іваном Малковичем в Україні у 1992 році. 
            Книжки видавництва виходять не лише в Україні, але й в 
            Америці, Швейцарії, Словаччині. Видавництво успішно продає 
            свої права провідним видавцям світу, серед яких гранд 
            «Alfred A. Knopf» (Нью-Йорк). Високий рівень роботи 
            «А-ба-ба-га-ла-ма-га» підтверджується і тим, що 
            видавництво володіє ексклюзивними правами на видання 
            Джоан Роулінг «Гаррі Поттер» в Україні. Віднедавна 
            «А-ба-ба-га-ла-ма-га» публікує також переклади власних 
            книжок іншими мовами, зокрема казки головного редактора 
            видавництва Малковича «Мед для мами» було видано в перекладі 
            англійською мовою, який Катерина Ющенко, подарувала дружинам 
            іноземних послів в Києві. Серед художників, які виконують 
            ілюстрації до книжок видавництва: Владислав Єрко, 
            Євгенія Гапчинська, Костянтин Лавро, Софія Усс, автори відомих ілюстрацій до казок «Снігова королева», «Казки Туманного Альбіону», «Ліза та її сни», «Ніч перед Різдвом», «Вовченятко, яке запливло далеко в море», «Різдвяна рукавичка» та інші.
        """
    },
    {
        "title": 'Книжковий клуб "Клуб Сімейного Дозвілля (КСД)"',
        "slug": "knyzhkovyi-klub-Klub-simejnogo-dozvillya",
        "logo": "https://static.yakaboo.ua/media/entity/book_publisher/l/o/logo-2023.jpg",
        "short_description": """
            Популярне харківське видавництво, з яким особисто знайома 
            чи не половина читачів нашої країни. Станом на 2016 рік 
            компанія випустила 150 мільйонів примірників друкованої 
            продукції. У каталозі книг «Книжкового клубу» представлені 
            твори українською, російською та іншими мовами. Щорічно 
            компанія презентує майже 700 ексклюзивних новинок, 
            у переліку яких можна знайти літературу абсолютно всіх 
            жанрів, стилів і напрямів. Купити книги КСД варто, якщо 
            ви любите сучасну та класичну художню літературу — саме 
            цих творів найбільше в каталозі видавця.
        """,
        "long_description": """
            Популярне харківське видавництво, з яким особисто знайома чи не половина читачів нашої країни. Станом на 2016 рік компанія випустила 150 мільйонів примірників друкованої продукції. У каталозі книг «Книжкового клубу» представлені твори українською, російською та іншими мовами. Щорічно компанія презентує майже 700 ексклюзивних новинок, у переліку яких можна знайти літературу абсолютно всіх жанрів, стилів і напрямів. Купити книги КСД варто, якщо ви любите сучасну та класичну художню літературу — саме цих творів найбільше в каталозі видавця.
            Асортимент і різноманітність літератури КСД

            Виробник зосередив роботу на тих літературних напрямах, які просто не можна обійти стороною, завдяки чому кожен рік справно видає цікаві й захопливі твори. Компанія має ексклюзивні права на публікацію головних бестселерів The New York Times. При цьому видавництво КСД пропонує шедеври світової літератури в найбільш повній та актуальній редакції.
            Окрему увагу компанія приділяє публікації робіт, які були відзначені престижними преміями або стали номінантами популярних конкурсів: Пулітцерівської, Гонкурівської, Нобелівської, Букерівської. Ці серії книг «Книжкового клубу» в Україні є дуже популярними серед читачів різних вікових категорій.
            Серед іншого, «Клуб сімейного дозвілля» є одним з небагатьох видавництв, які мають право публікувати твори Стівена Кінга українською мовою. На даний момент компанія випустила 27 романів і збірок оповідань авторства «короля жахів».
            Також «Клуб сімейного дозвілля» вважає невіддільною частиною своєї роботи публікацію творів відомих українських журналістів, істориків та громадських діячів. Завдяки цьому світ дізнався про роботи Івана Патриляк, Сергія Плохія, Володимира Галайчука й інших письменників, чиї твори визнані сьогодні національними та світовими шедеврами.
            Як купити книги КСД

            У каталозі нашого інтернет-магазину представлений широкий асортимент продукції популярного й важливого на ринку видавця. Ви можете купити твори «Клубу сімейного дозвілля» в Києві або з доставкою в інший регіон країни як через кошик, так і звернувшись до нашого контакт-центру. Зверніть увагу на регулярні знижки й безліч спеціальних пропозицій за дуже прийнятними цінами.
        """

    },
    {
        "title": "БІЗНЕС",
        "slug": "Business",
        "logo": "",
        "short_description": "",
        "long_description": ""
    },
    {
        "title": "Вівсянка",
        "slug": "Vivsjanka",
    },
    {
        "title": "ГДІП",
        "slug": "GDIP"
    },
    {
        "title": "Дніпро",
        "slug": "Dnipro",
    },
    {
        "title": "Егмонт Україна",
        "slug": "Egmont-Ukraine",
        "logo": "https://static.yakaboo.ua/media/entity/book_publisher/e/g/egmont_ukr_logo_1.jpg",
        "short_description": """
            Egmont Publishing - скандинавська медіа корпорація, заснована в далекому 1878 році, 
            сьогодні має філії в 30 країнах світу. З 2007 року «Егмонт» почав свою роботу і в Україні. 
            Девіз книжкової компанії говорить сам за себе: «Ми втілюємо казки в життя!»
            «Егмонт Україна» - це яскраві і захоплюючі дитячі книжки та журнали за мотивами популярних 
            мультфільмів, на сторінках яких оживає чарівний світ казки. Видавництво - один з лідерів 
            українського ринку дитячої періодики та книжкової продукції з потужною системою дистрибуції. 
            Асортимент видавництва складається з різних книжкових форматів: розмальовки, «розвивалки», 
            книжки-картонки, класичн...
        """,
        "long_description": """
            Egmont Publishing - скандинавська медіа корпорація, заснована в далекому 1878 році, 
            сьогодні має філії в 30 країнах світу. З 2007 року «Егмонт» почав свою роботу і в Україні. 
            Девіз книжкової компанії говорить сам за себе: «Ми втілюємо казки в життя!»
            «Егмонт Україна» - це яскраві і захоплюючі дитячі книжки та журнали за мотивами популярних 
            мультфільмів, на сторінках яких оживає чарівний світ казки. Видавництво - один з лідерів 
            українського ринку дитячої періодики та книжкової продукції з потужною системою дистрибуції. 
            Асортимент видавництва складається з різних книжкових форматів: розмальовки, «розвивалки», 
            книжки-картонки, класичні видання в твердій палітурці, книжки-іграшки тощо. Журнальне портфоліо - 
            це 16 видань для дітей різного віку та захоплень.
            Подорожуючи країною «Егмонт», під барвистими обкладинками Ваш малюк зустріне всесвітньо відомих 
            Блискавку Макквіна, Русалоньку, Лунтика, Машу і Ведмедя, Красуню і Чудовисько, учнів школи Монстер 
            Хай та багатьох інших казкових та мультиплікаційних героїв від Disney, Pixar, DreamWorks, інших студій. 
            Добре знайомі дітям персонажі навчать маленьких дружби, співчуття, поваги, допоможуть з дитинства 
            виховати у дитини любов до читання. А спільне читання в колі сім'ї завжди зміцнює емоційний зв'язок 
            між її членами, зближує та ріднить. На яскравих сторінках книжок «Егмонт» улюблені мультфільми та 
            казки стають ще ближче!
        """
    },
    {
        "title": "Євшан-зілля",
        "slug": "Evshan-zillja"
    },
    {
        "title": "Жорж",
        "slug": "Zhorzh"
    },
    {
        "title": "Зеніт",
        "slug": "Zenit"
    },
    {
        "title": "Іліон",
        "slug": "ilion"
    },
    {
        "title": "Йона Грей",
        "slug": "jona-grej"
    },
    {
        "title": "Лідер",
        "slug": "Lider-1"
    },
    {
        "title": "МАУП",
        "slug": "MAUP"
    },
    {
        "title": "Наука",
        "slug": "Nauka"
    },
    {
        "title": "Орієнтир",
        "slug": "Orientyr"
    },
    {
        "title": "Пегас",
        "slug": "Pegas"
    },
    {
        "title": "Ранок",
        "slug": "Ranok",
        "logo": "https://static.yakaboo.ua/media/entity/book_publisher/p/u/publishing_house_ranok_cover.jfif",
        "short_description": """
            Одне з провідних і найбільш популярних видавництв України. З його творами добре знайомі діти й 
            дорослі з понад 10 країн ближнього й далекого закордноння. У каталозі книг видавництва 
            «Ранок» представлено 18 000 примірників актуальної й ексклюзивної літератури, яка буде ц
            ікава як маленьким дітям, так і читачам постарше. На нашому сайті ви зможете вибрати і 
            купити книги видавництва «Ранок» для всієї родини.Одне з провідних і найбільш популярних 
            видавництв України. З його творами добре знайомі діти й дорослі з понад 10 країн ближнього й 
            далекого закордноння. У каталозі книг видавництва "...
        """,
        "long_description": """
            Одне з провідних і найбільш популярних видавництв України. З його творами добре знайомі діти й 
            дорослі з понад 10 країн ближнього й далекого закордноння. У каталозі книг видавництва «Ранок» 
            представлено 18 000 примірників актуальної й ексклюзивної літератури, яка буде цікава як маленьким 
            дітям, так і читачам постарше. На нашому сайті ви зможете вибрати і купити книги видавництва 
            «Ранок» для всієї родини.Одне з провідних і найбільш популярних видавництв України. З його 
            творами добре знайомі діти й дорослі з понад 10 країн ближнього й далекого закордноння. У 
            каталозі книг видавництва «Ранок» представлено 18 000 примірників актуальної й ексклюзивної 
            літератури, яка буде цікава як маленьким дітям, так і читачам постарше. На нашому сайті ви 
            зможете вибрати і купити книги видавництва «Ранок» для всієї родини.
            Видавництво та благодійний фонд

            Книжковий дім був заснований 1997 року в Харкові. Сьогодні видавництво має представництва
             в 27 містах України. Друкована продукція реалізується через фірмову мережу торгових 
             підприємств і дилерські мережі партнерів.

            Продукція «Ранок» випускається шістьма мовами: українською, англійською, румунською, 
            українською, німецькою та російською. Виробничі фонди зосереджені як в Україні, так і в інших країнах.

            Крім того, компанія є ще й одним із найбільших благодійних фондів. «Ранок» спонсорує й 
            підтримує дитячі інтернати, ДНЗ (дитячі навчальні заклади), сільські/міські бібліотеки, притулки. 
            З 2014 року видавничий дім очолює велику українську благодійну волонтерську організацію «Станція Харків».
            Книги видавництва «Ранок» в інтернет-магазині

            Книжковий дім спеціалізується на виробництві дитячої та навчально-підготовчої літератури. 
            В арсеналі видавництва є понад:

                4000 дитячих книг;
                6000 прикладних навчальних творів;
                8000 навчальних посібників.

            Тільки одного навчального матеріалу «Ранок» виробляє 12 млн примірників щорічно. 
            Уся продукція проходить ретельний контроль якості, завдяки чому не тільки цікава за змістом, 
            а й має приємний зовнішній вигляд.

            Серед дитячих книг представлені як розмальовки та ігри для дошкільнят, так і атласи з 
            енциклопедіями, які цікаво буде погортати школярам старших класів і навіть дорослим.

            Ознайомитися з цінами на продукцію можна в цьому каталозі. Тут же ви можете вибрати й 
            купити книги видавництва «Ранок» у Києві або замовити доставку в будь-який інший регіон країни. 
        """
    },
    {
        "title": "Світ",
        "slug": "Svit-1",
    },
    {
        "title": "Теза",
        "slug": "Teza"
    },
    {
        "title": "УПА",
        "slug": "UPA"
    },
    {
        "title": "Фоліо",
        "slug": "Folio",
        "logo": "https://static.yakaboo.ua/media/entity/book_publisher/5/4/541287ba-95f1-47b2-96b1-75e022bef73c-_logo_folio.jpg",
        "short_description": """
            «Видавництво Фоліо» — одне з найбільших видавництв в Україні. Існує на книжковому ринку більш як 
            30 років, видає класичну та сучасну українську та перекладну літературу українською, англійською, 
            німецькою, польською мовами.
            Розробили та підготували до друку понад 100 книжкових серій різних жанрів та тематик. Це твори 
            авторів України, США, Німеччини, Англії, Китаю, Португалії, Франції, Іспанії, Італії, Хорватії, 
            Норвегії, Швейцарії, Бельгії, Польщі, Туреччини, Словенії, Фінляндії, Японії та інших країн.
        """
    },
    {
        "title": "Хімджест",
        "slug": "Himdzhest"
    },
    {
        "title": "ЦНМП",
        "slug": "CNMP"
    },
    {
        "title": "Час",
        "slug": "Chas"
    },
    {
        "title": "Штучка",
        "slug": "Shtuchka"
    },
    {
        "title": "Ще одну сторінку",
        "slug": "Sche-odnu-storinku"
    },
    {
        "title": "Юніверс",
        "slug": "Junivers",
        "logo": "https://static.yakaboo.ua/media/entity/book_publisher/u/n/universe_logo_1_1.jpg",
        "short_description": """
            «Юніверс» - українське видавництво, засноване часописом «Всесвіт» в 1991 році. 
            Спеціалізується на виданні класичних творів світового письменства в українських перекладах. 
            Під знаком редакції друкуються й твори вітчизняних письменників та науковців. Головний 
            редактор організації - поет, перекладач Олег Жупанський.

            Активну діяльність на ринку книговидавництв компанія розпочала в 1996 році з приходом нового керівника 
            - Андрія Савчука. В цей час редакція започатковує та друкує перші книжкові серії - 
            «Філософська думка», «Світова поезія», «Австрійська бібліотека». Вперше українською було 
            видано цілий ряд визначних французьких письменн
        """,
        "long_description": """
            «Юніверс» - українське видавництво, засноване часописом «Всесвіт» в 1991 році. 
            Спеціалізується на виданні класичних творів світового письменства в українських перекладах. 
            Під знаком редакції друкуються й твори вітчизняних письменників та науковців. 
            Головний редактор організації - поет, перекладач Олег Жупанський.

            Активну діяльність на ринку книговидавництв компанія розпочала в 1996 році з 
            приходом нового керівника - Андрія Савчука. В цей час редакція започатковує та друкує 
            перші книжкові серії - «Філософська думка», «Світова поезія», «Австрійська бібліотека». 
            Вперше українською було видано цілий ряд визначних французьких письменників: Жозе-Маріа де Ередіа, 
            Поль Валері, Стефан Малларме, Луї Фердінанд Селін, Жан Жіоно, Анрі Мішо. Помітною подією в 
            історії видавництва була публікація першого перекладу українською мовою семитомного роману 
            Марселя Пруста «У пошуках втраченого часу».

            Одним із найбільш вдалих проектів видавництва «Юніверс» є книжкова серія «Лауреати 
            Нобелівської премії». Видавництво має намір опублікувати у цій серії по кілька томів кожного автора.

            Основні напрями діяльності видавництва на сьогодні - видання іноземної літератури 
            (художньої, наукової, навчальної тощо); видання творів українських письменників та 
            науковців; публікація перекладної дитячої літератури зі скандинавських мов.
        """
    },
    {
        "title": "Яблуко",
        "slug": "Jabluko",
    },
    {
        "title": "Аванта+",
        "slug": "Avanta"
    }
]

INTERESTING = [
    {
        "title": "Акції 🔥",
        "slug": "/promotions"
    },
    {
        "title": "Зимова єПідтримка ❄",
        "slug": "/promotion/zimova-epidtrymka"
    },
    {
        "title": "єКнига 📲",
        "slug": "/promotion/free-delivery"
    },
    {
        "title": "Комплекти до 1000₴ 🎁",
        "slug": "/knygy/komplekty-1000-grn"
    },
    {
        "title": "Комплекти єКнига 📚",
        "slug": "/knygy/dobirky-yakaboo/komplekty-eknyga"
    },
    {
        "title": 'Новинки квітня 🌼',
        "slug": "/promotion/novynky-kvitnia"
    },
    {
        "title": "Електронні новинки квітня",
        "slug": "/promotion/e-novynky-knitnia"
    },
    {
        "title": "Бажані знижки до -50%",
        "slug": "/promotion/do-50-na-knyzhky"
    },
    {
        "title": "Yakaboo Publishing ",
        "slug": "/book-publisher/yakaboo-publishing"
    }
]

FOOTERS = [
    {
        "title": "Про магазин",
        "link": "/about-us",
    },
    {
        "title": "Програма лояльності",
        "link": "/bonus"
    },
    {
        "title": "Вакансії",
        "link": "/vacancies"
    },
    {
        "title": "Контакти",
        "link": "/contact"
    },
    {
        "title": "Доставка та оплата",
        "link": "/delivery",
        "category": FooterCategory.INFO
    },
    {
        "title": "Подарункові сертифікати",
        "link": "/certificates",
        "category": FooterCategory.INFO
    },
    {
        "title": "Повернення товару",
        "link": "/returns",
        "category": FooterCategory.INFO
    },
    {
        "title": "Блог",
        "link": "/blog",
        "category": FooterCategory.INFO
    },
    {
        "title": "Часто шукають",
        "link": "/popular",
        "category": FooterCategory.INFO
    },
    {
        "title": "Серія книг",
        "link": "/book-series/view/all",
        "category": FooterCategory.INFO
    },
    {
        "title": "Автори",
        "link": "author/view/all",
        "category": FooterCategory.INFO
    }
]

BOARD_GAME_BRANDS = [
    {
        "title": "Winning Moves",
        "slug": "winning-moves",
    },
    {
        "title": "Djeco",
        "slug": "djeco",
        "image": 'https://static.yakaboo.ua/media/entity/children_brand/d/j/djeco.jpg',
        "description": """
            За понад півстоліття традиції і філософія цієї 
            компанії нітрохи не змінилися. Починаючи з 1954 року, 
            і до нині, Djeco виробляє кращу дитячу продукцію, 
            яка набагато випереджає свій час. Кращі матеріали 
            виробництва, новітні технології, високопрофесійна 
            поліграфія і креативний підхід дизайнерів 
            визначають роль цієї французької компанії, 
            як світового корифея, тренда, домінанти серед 
            подібних компаній. Djeco - це незвичайні набори 
            для творчості, дерев'яні іграшки і конструктори, 
            настільні ігри, пазли і багато іншого. Кожна іграшка - 
            оригінальний шедевр, продукт копіткої праці більше 30 
            дизайнерів, тестувальників, ілюстраторів, 
            психологів. Це не просто іграшки для безглуздої 
            забави, вони відіграють визначальну роль в розвитку 
            малюка - його креативності, творчих здібностей, 
            просторового мислення, розвитку почуття прекрасного. Розвивається логіка, пам'ять
            увага, стимулюється пізнавальна активність. Яскраві деталі привертають увагу дітей 
            і зацікавлюють у виконанні завдань. Розвиваючі іграшки Djeco знайомлять малюка з 
            його першими відчуттями, дитина пізнає кольори, форми, вчиться пізнавати предмети 
            на дотик, в процесі чого формується дрібна моторика і мовна діяльність.
        """
    },
    {
        "title": "Майстер",
        "slug": "maister",
    },
    {
        "title": "Ігромаг",
        "slug": "igromag",
    },
    {
        "title": "Geekach Games",
        "slug": "geekach-games",
    },
    {
        "title": "Strateg",
        "slug": "strateg",
    },
    {
        "title": "Magellan Entertainment",
        "slug": "magellan-entertainment",
    },
    {
        "title": "Ranok-Creative",
        "slug": "ranok-creative",
        "image": "https://static.yakaboo.ua/media/entity/children_brand/f/i/file_2.jpg",
        "description": """
            Нову торгову марку видавництва «Ранок», компанію «Ranok-Creative», 
            було створено в Україні у 2007 році. Основні напрямки її діяльності – 
            випуск продукції власних розробок, а також виробництво товарів під торговими марками партнерів з  
            Німеччини, Польщі й Чехії. Під власною маркою «Ранок» видає більше 650 одиниць ігрової продукції та 
            продукції для розвитку для дітей і дорослих у 8 серіях. Це серії настільних наукових, пізнавальних ігор, 
            ігор для розвитку, наборів для творчості й наочних посібників, книжок і різноманітних канцтоварів.
            Однією з найбільших серій є настільні ігри. Їх випускають в 5 основних групах: дитячі, для всієї родини, 
            дитячі ігри, ходилки, настільні ігри в дорогу та ігри, в яких суміщено гру з творчістю. На упаковці кожної 
            гри вказано для дитини якого віку вона призначена. Окрім того настільні ігри розділено за жанрами: 
            економічні, стратегічні, інтелектуальні, ігри для розваг. \n\n

            Дуже популярними зараз є наукові ігри, які представлено різноманітними наборами з хімічними компонентами 
            і біологічними матеріалами. До кожної гри додається детальний опис і рекомендації для проведення наукових 
            дослідів і експериментів, а до деяких навіть відео на DVD. Є комплекти, в яких зібрано декілька окремих 
            наборів для наукових ігор. Зручні й зрозумілі наочні посібники, які випускає компанія, можна застосовувати 
            у дитячому садочку й у школі, а також батькам вдома. Це демонстраційні матеріали, зошити з розвитку 
            мовлення, малювання, аплікації, календарі спостережень за природою, різноманітні стенди, плакати й 
            методичні посібники. Ігри для розвитку торгової марки було розроблено з врахуванням сучасних методик 
            раннього розвитку Монтессорі, Зайцева, Олени й Бориса Нікітіних і багатьох інших. Це різноманітні ігри на 
            магнітиках, трафарети, шнурівки, конструктори з натуральних матеріалів.\n

            Товари для творчості представлено значним асортиментом різних серій. Це набори для малювання,
             ліплення, роботи з бісером, створення віражних картинок, гравюр, свічок, мила, скриньок, прикрас. 
             Філіали і фірмові магазини компанії є в усіх регіонах нашої країни, а також – в Росії, 
             Молдові, Казахстані. Вся її продукція отримує чудові відгуки і є дуже популярною в усіх цих 
             країнах. Ознайомитись з асортиментом і подивитись фото товарів Ви можете на сторінці торгової 
             марки «Ranok-Creative». В інтернет-магазині Yakaboo Ви можете придбати цю продукцію або замовити її 
             з доставкою по Києву й інших містах країни.
        """
    },
    {
        "title": "Energy Plus",
        "slug": "energy-plus",
    },
    {
        "title": "Ранок",
        "slug": "ranok",
    }
]

GAME_SERIES = [
    {
        "title": "MemoBox",
        "slug": "memo-box",
    },
    {
        "title": "Weddingtons No.1",
        "slug": "weddingtons-no-1"
    },
    {
        "title": "Top Trumps Quiz",
        "slug": "top-trumps-quiz"
    },
    {
        "title": "FunBox",
        "slug": "fun-box"
    },
    {
        "title": "Guess Who",
        "slug": "guess-who",
    },
    {
        "title": "Розумні ігри",
        "slug": "rozumni-igry"
    },
    {
        "title": "Одягалка Fashion Look",
        "slug": "odyagalka-fasion-look"
    },
    {
        "title": "Розкажи історію",
        "slug": "rozkaxhy-istoriju"
    },
    {
        "title": "Warhammer 40,000",
        "slug": "warhammer-40000"
    },
    {
        "title": "Monopoly",
        "slug": "monopoly"
    },
    {
        "title": "Top Trumps Match",
        "slug": "top-trumps-match"
    },
    {
        "title": "Dixit",
        "slug": "dixit"
    },
    {
        "title": "Лото",
        "slug": "loto"
    },
    {
        "title": "Cluedo",
        "slug": "cluedo"
    },
    {
        "title": "Шакал",
        "slug": "shakal"
    },
    {
        "title": "Гралочка-розвивалочка",
        "slug": "hralochka-rozvyvalochka"
    },
    {
        "title": "IQ-клуб для малюків",
        "slug": "iq-club-dlya-malukiv"
    },
    {
        "title": "Ігри Парочки",
        "slug": "ihry-parochky"
    },
    {
        "title": "Еврика",
        "slug": "evryka"
    },
    {
        "title": "МЕМОгра",
        "slug": "memogra"
    },
    {
        "title": "City Line",
        "slug": "city-line"
    },
    {
        "title": "Я граюся з прищіпочками",
        "slug": "ya-hrajusya-z-pryshcipochkamy"
    },
    {
        "title": "Студія раннього розвитку",
        "slug": "studiya-ranyoho-rozvytku"
    },
    {
        "title": "Сідай і Грай",
        "slug": "siday-i-gray"
    },
    {
        "title": "Jenga",
        "slug": "jenga",
    },
]

BOARD_GAME_AGES = [
    {
        "age": "Підліткам",
        "slug": "pidlitkam"
    },
    {
        "age": "Від 9 до 12 років",
        "slug": "vid-9-do-12-rokiv"
    },
    {
        "age": "Від 6 до 8 років",
        "slug": "vid-6-do-8-rokiv"
    },
    {
        "age": "Від 3 до 5 років",
        "slug": "vid-3-do-5-rokiv"
    },
    {
        "age": "Батькам",
        "slug": "batkam"
    },
    {
        "age": "До 2-х років",
        "slug": "do-2-rokiv"
    }
]

CONTACTS = [
    {
        "social_title": "instagram",
        "link": "https://www.instagram.com/yakabooua/",
        "icon_title": "instagram.svg"
    },
    {
        "social_title": "youtube",
        "link": "https://www.youtube.com/channel/UC5w2HgI3yU_t3NtB-hAxVKw",
        "icon_title": "youtube.svg"
    },
    {
        "social_title": "facebook",
        "link": "https://www.facebook.com/yakabooua",
        "icon_title": "facebook.svg"
    },
    {
        "social_title": "telegram",
        "link": "https://t.me/yakabooua",
        "icon_title": "telegram.svg"
    }
]

COUNTRIES = [
    {
        "title": "Україна",
    },
    {
        "title": "Сполучені Штати"
    },
    {
        "title": "Канада"
    },
    {
        "title": "Австралія"
    },
    {
        "title": "Азербайджан"
    },
    {
        "title": "Албанія"
    },
    {
        "title": "Алжир"
    },
    {
        "title": "Бельгія"
    },
    {
        "title": "Болгарія"
    },
    {
        "title": "Боснія і Герцеговина"
    },
    {
        "title": "Бразилія"
    },
    {
        "title": "В'єтнам"
    },
    {
        "title": "Велика Британія"
    },
    {
        "title": "Венесуела"
    },
    {
        "title": "Вірменія"
    },
    {
        "title": "Гонконг"
    },
    {
        "title": "Гондурас"
    },
    {
        "title": "Греція"
    },
    {
        "title": "Грузія"
    },
    {
        "title": "Данія"
    },
    {
        "title": "Домініканська Республіка"
    },
    {
        "title": "Еквадор"
    },
    {
        "title": "Естонія"
    },
    {
        "title": "Єгипет"
    },
    {
        "title": "Ізраїль"
    },
    {
        "title": "Індія"
    },
    {
        "title": "Індонезія"
    },
    {
        "title": "Ірландія"
    },
    {
        "title": "Ісландія"
    },
    {
        "title": "Італія"
    },
    {
        "title": "Казахстан"
    },
    {
        "title": "Катар"
    },
    {
        "title": "Китай"
    },
    {
        "title": "Кіпр"
    },
    {
        "title": "Киргизстан"
    },
    {
        "title": "Коста-Ріка"
    },
    {
        "title": "Кувейт"
    },
    {
        "title": "Латвія"
    },
    {
        "title": "Литва"
    },
    {
        "title": "Ліван"
    },
    {
        "title": "Ліхтенштейн"
    },
    {
        "title": "Люксембург"
    },
    {
        "title": "Малайзія"
    },
    {
        "title": "Мальта"
    },
    {
        "title": "Марокко"
    },
    {
        "title": "Мексика"
    },
    {
        "title": "Монако"
    },
    {
        "title": "Нідерланди"
    },
    {
        "title": "Німеччина"
    },
    {
        "title": "Нова Зеландія"
    },
    {
        "title": "Норвегія"
    },
    {
        "title": "Об'єднані Арабські Емірати"
    },
    {
        "title": "Перу"
    },
    {
        "title": "Польща"
    },
    {
        "title": "Португалія"
    },
    {
        "title": "Румунія"
    },
    {
        "title": "Саудівська Аравія"
    },
    {
        "title": "Сербія"
    },
    {
        "title": "Словаччина"
    },
    {
        "title": "Словенія"
    },
    {
        "title": "Тайвань"
    },
    {
        "title": "Туреччина"
    },
    {
        "title": "Угорщина"
    },
    {
        "title": "Узбекистан"
    },
    {
        "title": "Фінляндія"
    },
    {
        "title": "Франція"
    },
    {
        "title": "Чехія"
    },
    {
        "title": "Хорватія"
    },
    {
        "title": "Швейцарія"
    },
    {
        "title": "Швеція"
    },
    {
        "title": "Шрі-Ланка"
    },
    {
        "title": "Японія"
    },
    {
        "title": "Молдова"
    },
    {
        "title": "Південна Корея"
    },
    {
        "title": "Аргентина"
    },
    {
        "title": "Намібія"
    }
]

CITIES = [
    {
        "title": "Вінниця",
        "region": "Вінницька",
        "country_id": 1
    },
    {
        "title": "Дніпро",
        "region": "Дніпропетровська",
        "country_id": 1
    },
    {
        "title": "Запоріжжя",
        "region": "Запорізька",
        "country_id": 1
    },
    {
        "title": "Івано-Франківськ",
        "region": "Івано-Франківська",
        "country_id": 1
    },
    {
        "title": "Київ",
        "region": "Київська",
        "country_id": 1
    },
    {
        "title": "Львів",
        "region": "Львівська",
        "country_id": 1
    },
    {
        "title": "Одеса",
        "region": "Одеська",
        "country_id": 1
    },
    {
        "title": "Полтава",
        "region": "Полтавська",
        "country_id": 1
    },
    {
        "title": "Тернопіль",
        "region": "Тернопільська",
        "country_id": 1
    },
    {
        "title": "Харків",
        "region": "Харківська",
        "country_id": 1
    }
]

DELIVERY_TERMS = [
    {
        "yakaboo_shop_price": 30,
        "new_post_office_price": 60,
        "new_post_department_price": 60,
        "new_post_courier_price": 95,
        "meest_post_price": 50,
        "ukrpost_department_price": 39,
        "ukrpost_courier_price": 75,
        "city_id": 5
    },
    {
        "new_post_office_price": 60,
        "new_post_department_price": 60,
        "new_post_courier_price": 95,
        "meest_post_price": 50,
        "ukrpost_department_price": 39,
        "ukrpost_courier_price": 75,
        "city_id": 1
    },
    {
        "new_post_office_price": 60,
        "new_post_department_price": 60,
        "new_post_courier_price": 95,
        "meest_post_price": 50,
        "ukrpost_department_price": 39,
        "ukrpost_courier_price": 75,
        "city_id": 2
    },
    {
        "new_post_office_price": 60,
        "new_post_department_price": 60,
        "new_post_courier_price": 95,
        "meest_post_price": 50,
        "ukrpost_department_price": 39,
        "ukrpost_courier_price": 75,
        "city_id": 3
    },
    {
        "new_post_office_price": 60,
        "new_post_department_price": 60,
        "new_post_courier_price": 95,
        "meest_post_price": 50,
        "ukrpost_department_price": 39,
        "ukrpost_courier_price": 75,
        "city_id": 4
    },
    {
        "new_post_office_price": 60,
        "new_post_department_price": 60,
        "new_post_courier_price": 95,
        "meest_post_price": 50,
        "ukrpost_department_price": 39,
        "ukrpost_courier_price": 75,
        "city_id": 6
    },
    {
        "new_post_office_price": 60,
        "new_post_department_price": 60,
        "new_post_courier_price": 95,
        "meest_post_price": 50,
        "ukrpost_department_price": 39,
        "ukrpost_courier_price": 75,
        "city_id": 7
    },
    {
        "new_post_office_price": 60,
        "new_post_department_price": 60,
        "new_post_courier_price": 95,
        "meest_post_price": 50,
        "ukrpost_department_price": 39,
        "ukrpost_courier_price": 75,
        "city_id": 8
    },
    {
        "new_post_office_price": 60,
        "new_post_department_price": 60,
        "new_post_courier_price": 95,
        "meest_post_price": 50,
        "ukrpost_department_price": 39,
        "ukrpost_courier_price": 75,
        "city_id": 9
    },
    {
        "new_post_office_price": 60,
        "new_post_department_price": 60,
        "new_post_courier_price": 95,
        "meest_post_price": 50,
        "ukrpost_department_price": 39,
        "ukrpost_courier_price": 75,
        "city_id": 10
    },
    {
        "new_post_courier_price": 1380,
        "country_id": 3
    }
]


AUTHOR_FACTS = [
    {
        'fact_text': "Книжкова Герміона Грейнджер, відмінниця і «нестерпна"
                     "всезнайка» практично повністю списана з самої Джоан Роулінг у віці одинадцяти років.",
        "author_id": 2
    }
]


BOOKS_INFO = [
    {
        'code': 100001,
        'rate': 4.5,
        'ISBN': '978-966-100001',
        'cover_type': 'Тверда',
        'pages_count': 660,
        'is_has_cashback': True,
        'format': 'Паперова',
        'language': 'Українська',
        'publishing_year': 2024,
        'first_publishing_at': 1991,
        'bonuses': 340,
        'description': "Опис книги 'Сяйво' Стівена Кінга."
    },
    {
        'code': 100002,
        'rate': 4.75,
        'ISBN': '978-966-100002',
        'cover_type': 'Тверда',
        'pages_count': 692,
        'is_has_cashback': True,
        'format': 'Паперова',
        'language': 'Українська',
        'publishing_year': 2024,
        'first_publishing_at': 1998,
        'bonuses': 300,
        'description': "Опис книги 'Керрі' Стівена Кінга."
    },
    {
        'code': 100003,
        'rate': 5,
        'ISBN': '978-966-100003',
        'cover_type': 'Тверда',
        'pages_count': 669,
        'is_has_cashback': True,
        'format': 'Паперова',
        'language': 'Українська',
        'publishing_year': 2024,
        'first_publishing_at': 2008,
        'bonuses': 150,
        'description': "Опис книги 'Мізері' Стівена Кінга."
    },
    {
        'code': 100004,
        'rate': 5,
        'ISBN': '978-966-100004',
        'cover_type': 'Тверда',
        'pages_count': 712,
        'is_has_cashback': True,
        'format': 'Паперова',
        'language': 'Українська',
        'publishing_year': 2024,
        'first_publishing_at': 1977,
        'bonuses': 300,
        'description': "Опис книги 'Кладовище домашніх тварин' Стівена Кінга."
    },
    {
        'code': 100005,
        'rate': 4.25,
        'ISBN': '978-966-100005',
        'cover_type': 'Тверда',
        'pages_count': 1300,
        'is_has_cashback': False,
        'format': 'Паперова',
        'language': 'Українська',
        'publishing_year': 2024,
        'first_publishing_at': 2004,
        'bonuses': 450,
        'description': "Опис книги 'Воно' Стівена Кінга."
    },
    {
        'code': 100006,
        'rate': 4.9,
        'ISBN': '978-966-100006',
        'cover_type': 'Тверда',
        'pages_count': 403,
        'is_has_cashback': False,
        'format': 'Паперова',
        'language': 'Українська',
        'publishing_year': 2024,
        'bonuses': 220,
        'first_publishing_at': 2001,
        'description': "Опис книги 'Темна вежа' Стівена Кінга."
    },
    {
        'code': 100007,
        'rate': 5,
        'ISBN': '978-966-100007',
        'cover_type': 'Тверда',
        'pages_count': 667,
        'is_has_cashback': False,
        'format': 'Паперова',
        'language': 'Українська',
        'publishing_year': 2024,
        'first_publishing_at': 2002,
        'bonuses': 300,
        'description': "Опис книги 'Доктор Сон' Стівена Кінга."
    }
]
BOOKS = [
    {
        'title': 'Сяйво',
        'slug': 'syaivo',
        'price': 420,
        'book_info_id': 2,
        'publishing_id': 5,
        'author_ids': [12],
        'images': [
            {'image_url': 'https://static.yakaboo.ua/media/catalog/product/2/6/26929_39860_10.jpg',
             'type': BookImageType.COVER}
        ]
    },
    {
        'title': 'Керрі',
        'slug': 'carry',
        'price': 357,
        'book_info_id': 3,
        'publishing_id': 5,
        'author_ids': [12],
        'images': [
            {'image_url': 'https://static.yakaboo.ua/media/cloudflare/product/webp/600x840/8/7/878683_1.jpg',
             'type': BookImageType.COVER}
        ]
    },
    {
        'title': 'Мізері',
        'slug': 'miseri',
        'price': 589,
        'book_info_id': 4,
        'publishing_id': 5,
        'author_ids': [12],
        'images': [
            {'image_url': 'https://static.yakaboo.ua/media/catalog/product/5/8/58388_115986_cr.jpg',
             'type': BookImageType.COVER},
            {'image_url': 'https://static.yakaboo.ua/media/catalog/product/i/m/image00016_36.jpg',
             'type': BookImageType.COVER},
            {'image_url': 'https://static.yakaboo.ua/media/mediagallery/image/0/2/02_8885.png',
             'type': BookImageType.PAGE},
            {'image_url': 'https://static.yakaboo.ua/media/mediagallery/image/0/3/03_8732.png',
             'type': BookImageType.PAGE},
        ]
    },
    {
        'title': 'Кладовище домашніх тварин',
        'slug': 'kladovyshche-domashnich-tvaryn',
        'price': 264,
        'book_info_id': 5,
        'publishing_id': 5,
        'author_ids': [12],
        'images': [
            {'image_url': 'https://static.yakaboo.ua/media/catalog/product/i/m/img567_95.jpg',
             'type': BookImageType.COVER},
            {'image_url': 'https://static.yakaboo.ua/media/catalog/product/i/m/img568_124.jpg',
             'type': BookImageType.COVER},
            {'image_url': 'https://static.yakaboo.ua/media/mediagallery/image/0/1/01_1256_10.jpg',
             'type': BookImageType.PAGE},
            {'image_url': 'https://static.yakaboo.ua/media/mediagallery/image/0/2/02_1284_10.jpg',
             'type': BookImageType.PAGE},
            {'image_url': 'https://static.yakaboo.ua/media/mediagallery/image/0/3/03_1229_10.jpg',
             'type': BookImageType.PAGE}
        ]
    },
    {
        'title': 'Воно',
        'slug': 'vono',
        'price': 650,
        'book_info_id': 6,
        'publishing_id': 5,
        'author_ids': [12],
        'images': [
            {'image_url': 'https://static.yakaboo.ua/media/catalog/product/i/m/img014_5_98.jpg',
             'type': BookImageType.COVER},
            {'image_url': 'https://static.yakaboo.ua/media/catalog/product/i/m/img015_3_131.jpg',
             'type': BookImageType.COVER},
            {'image_url': 'https://static.yakaboo.ua/media/mediagallery/image/0/1/01_8465.png',
             'type': BookImageType.PAGE},
            {'image_url': 'https://static.yakaboo.ua/media/mediagallery/image/0/2/02_8396.png',
             'type': BookImageType.PAGE}
        ]
    },
    {
        'title': 'Темна вежа I. Стрілець',
        'slug': 'temna-vezha',
        'price': 180,
        'book_info_id': 7,
        'publishing_id': 5,
        'author_ids': [12],
        'images': [
            {'image_url': 'https://static.yakaboo.ua/media/catalog/product/5/5/55871_107569.jpg',
             'type': BookImageType.COVER},
            {'image_url': 'https://static.yakaboo.ua/media/catalog/product/i/m/img392_1_63.jpg',
             'type': BookImageType.COVER},
            {'image_url': 'https://static.yakaboo.ua/media/mediagallery/image/0/1/01_1484.jpg',
             'type': BookImageType.PAGE},
            {'image_url': 'https://static.yakaboo.ua/media/mediagallery/image/0/2/02_1475.jpg',
             'type': BookImageType.PAGE}
        ]
    },
    {
        'title': 'Доктор Сон',
        'slug': 'doktor-son',
        'price': 372,
        'book_info_id': 8,
        'publishing_id': 5,
        'author_ids': [12],
        'images': [
            {'image_url': 'https://static.yakaboo.ua/media/catalog/product/1/9/19_7_3.jpg',
             'type': BookImageType.COVER},
            {'image_url': 'https://static.yakaboo.ua/media/catalog/product/1/9/19-2_25.jpg',
             'type': BookImageType.COVER},
            {'image_url': 'https://static.yakaboo.ua/media/mediagallery/image/1/_/1_oddbeqdiu0.jpg',
             'type': BookImageType.PAGE}
        ]
    }
]

TRANSLATORS = [
  {
    "first_name": "Світлана",
    "last_name": "Олійник",
    "slug": "svitlana-oliinyk",
  },
  {
    "first_name": "Владислав",
    "last_name": "Куліш",
    "slug": "vladyslav-kulish",
  },
  {
    "first_name": "Катерина",
    "last_name": "Матвійчук",
    "slug": "kateryna-matviichuk",
  },
  {
    "first_name": "Олександра",
    "last_name": "Музичук",
    "slug": "oleksandra-muzychuk",
  },
  {
    "first_name": "Ірина",
    "last_name": "Потапова",
    "slug": "iryna-potapova",
  },
  {
    "first_name": "Nathanaël",
    "last_name": "",
    "slug": "nathanael",
  },
  {
    "first_name": "Є.",
    "last_name": "Бахуров",
    "slug": "ie-bakhurov",
  },
  {
    "first_name": "Є.",
    "last_name": "Вінницька",
    "slug": "ie-vinnytska",
  },
  {
    "first_name": "Є.",
    "last_name": "Крижевич",
    "slug": "ie-kryzhevych",
  },
  {
    "first_name": "Є.",
    "last_name": "Миколаєва",
    "slug": "ie-mykolaieva",
  },
  {
    "first_name": "Є.",
    "last_name": "Стасюк",
    "slug": "ie-stasiuk",
  },
  {
    "first_name": "Єва",
    "last_name": "Ніколаєва",
    "slug": "yeva-nikolaieva",
  },
  {
    "first_name": "Зінаїда",
    "last_name": "Гулевич",
    "slug": "zinaida-hulevych",
  },
  {
    "first_name": "Зінаїда",
    "last_name": "Крижевич",
    "slug": "zinaida-kryzhevych",
  },
  {
    "first_name": "Анастасія",
    "last_name": "Кіржаєва",
    "slug": "anastasiia-kirzhaieva",
  },
  {
    "first_name": "Віктор",
    "last_name": "Сапіцький",
    "slug": "viktor-sapitskyi",
  },
  {
    "first_name": "Кирило",
    "last_name": "Болдирев",
    "slug": "kyrylo-boldyrev",
  },
  {
    "first_name": "Софія",
    "last_name": "Слаба",
    "slug": "sofiia-slaba",
  },
  {
    "first_name": "Lukas",
    "last_name": "",
    "slug": "lukas",
  },
  {
    "first_name": "Robin",
    "last_name": "Myers",
    "slug": "robin-myers",
  }
]
