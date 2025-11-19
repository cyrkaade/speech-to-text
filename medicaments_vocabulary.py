# Medicament vocabulary for Kazakh and Russian speech recognition
# This list contains common pharmaceutical names used in Kazakhstan and Russia

MEDICAMENTS_RU = [
    # Cardiovascular medications
    "Аспирин", "Кардиомагнил", "Конкор", "Лозап", "Эналаприл",
    "Бисопролол", "Амлодипин", "Метопролол", "Нитроглицерин", "Престариум",
    "Лориста", "Валсартан", "Атенолол", "Каптоприл", "Дилтиазем",

    # Antibiotics
    "Амоксициллин", "Азитромицин", "Цефтриаксон", "Ципрофлоксацин", "Левофлоксацин",
    "Доксициклин", "Амоксиклав", "Сумамед", "Аугментин", "Супракс",
    "Флемоксин", "Цефалексин", "Кларитромицин", "Офлоксацин", "Метронидазол",

    # Analgesics and NSAIDs
    "Ибупрофен", "Парацетамол", "Нимесулид", "Диклофенак", "Кетопрофен",
    "Индометацин", "Мелоксикам", "Трамадол", "Кеторолак", "Нурофен",
    "Найз", "Кетанов", "Анальгин", "Баралгин", "Пенталгин",

    # Diabetes medications
    "Метформин", "Глюкофаж", "Сиофор", "Глибенкламид", "Гликлазид",
    "Инсулин", "Диабетон", "Галвус", "Янувия", "Форсига",

    # Gastrointestinal
    "Омепразол", "Мезим", "Панкреатин", "Эспумизан", "Смекта",
    "Линекс", "Хилак Форте", "Фестал", "Креон", "Ранитидин",
    "Де-Нол", "Мотилиум", "Энтеросгель", "Фосфалюгель", "Лактофильтрум",

    # Respiratory
    "Амброксол", "Бромгексин", "АЦЦ", "Синекод", "Эреспал",
    "Лазолван", "Флуимуцил", "Беродуал", "Пульмикорт", "Сальбутамол",

    # Antihistamines
    "Супрастин", "Цетиризин", "Лоратадин", "Зодак", "Кларитин",
    "Тавегил", "Зиртек", "Эриус", "Фенистил", "Телфаст",

    # Neurological
    "Глицин", "Фенибут", "Пирацетам", "Ноотропил", "Кавинтон",
    "Мексидол", "Актовегин", "Цитофлавин", "Мильгамма", "Нейромультивит",

    # Vitamins and supplements
    "Аскорбиновая кислота", "Рыбий жир", "Омега-3", "Кальций Д3", "Магний Б6",
    "Аевит", "Компливит", "Алфавит", "Витрум", "Мультитабс",

    # Antihypertensives
    "Нифедипин", "Верапамил", "Лизиноприл", "Периндоприл", "Индапамид",

    # Sedatives
    "Афобазол", "Феназепам", "Грандаксин", "Адаптол", "Персен",
    "Ново-Пассит", "Валериана", "Пустырник", "Корвалол", "Валокордин",

    # Anticoagulants
    "Варфарин", "Клопидогрел", "Плавикс", "Гепарин", "Ксарелто",
]

MEDICAMENTS_KK = [
    # Common Kazakh transliterations and local names
    "Аспирин", "Парацетамол", "Ибупрофен", "Амоксициллин", "Метформин",
    "Инсулин", "Омепразол", "Панкреатин", "Глицин", "Активированный уголь",

    # Kazakh-specific or locally used names
    "Кардиомагнил", "Конкор", "Лозап", "Эналаприл", "Сумамед",
    "Нурофен", "Найз", "Глюкофаж", "Мезим", "Линекс",
    "Лазолван", "Супрастин", "Цетиризин", "Фенибут", "Пирацетам",

    # Additional medications commonly used in Kazakhstan
    "Цитрамон", "Но-шпа", "Дротаверин", "Лоперамид", "Церукал",
    "Дексаметазон", "Преднизолон", "Гидрокортизон", "Димедрол", "Кеторол",
]

# Medical terms and phrases that might accompany medicaments
MEDICAL_TERMS_RU = [
    "таблетка", "капсула", "сироп", "инъекция", "мазь", "гель", "крем",
    "суспензия", "раствор", "порошок", "свечи", "капли", "спрей",
    "миллиграмм", "грамм", "миллилитр", "доза", "дозировка",
    "утром", "вечером", "до еды", "после еды", "три раза в день",
    "один раз в день", "два раза в день", "по необходимости",
    "артериальное давление", "сахар в крови", "головная боль",
    "температура", "кашель", "насморк", "аллергия",
]

MEDICAL_TERMS_KK = [
    "таблетка", "капсула", "сироп", "дәрі", "препарат",
    "доза", "дозировка", "күніне", "таңертең", "кешке",
    "тамақ алдында", "тамақтан кейін", "қан қысымы", "қант",
    "бас ауруы", "температура", "жөтел", "аллергия",
]

def get_all_medicaments():
    """Returns combined list of all medicaments (Russian and Kazakh)"""
    return list(set(MEDICAMENTS_RU + MEDICAMENTS_KK))

def get_all_medical_terms():
    """Returns combined list of all medical terms"""
    return list(set(MEDICAL_TERMS_RU + MEDICAL_TERMS_KK))

def get_speech_context_entries(boost_medicaments=20, boost_medical_terms=15):
    """
    Generate Soniox speech_context entries for medicament recognition.

    Args:
        boost_medicaments: Boost value for medicament names (default: 20)
        boost_medical_terms: Boost value for medical terms (default: 15)

    Returns:
        List of speech context entries in Soniox format
    """
    entries = []

    # Add medicament names with higher boost
    medicaments = get_all_medicaments()
    for med in medicaments:
        entries.append({
            "phrases": [med],
            "boost": boost_medicaments
        })

    # Add medical terms with moderate boost
    terms = get_all_medical_terms()
    for term in terms:
        entries.append({
            "phrases": [term],
            "boost": boost_medical_terms
        })

    return entries

def get_compact_speech_context(boost_medicaments=20, boost_medical_terms=15):
    """
    Generate compact speech_context by grouping all terms.
    This is more efficient for the API.

    Returns:
        Dictionary with speech_context structure
    """
    return {
        "entries": [
            {
                "phrases": get_all_medicaments(),
                "boost": boost_medicaments
            },
            {
                "phrases": get_all_medical_terms(),
                "boost": boost_medical_terms
            }
        ]
    }
