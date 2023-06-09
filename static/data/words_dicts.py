from models.models_db import Question
from config.app_config import db, app

easy = {
    'hello': 'привет',
    'goodbye': 'до свидания',
    'thank you': 'спасибо',
    'yes': 'да',
    'no': 'нет',
    'please': 'пожалуйста',
    'sorry': 'извините',
    'excuse me': 'извините',
    'help': 'помощь',
    'time': 'время',
    'day': 'день',
    'night': 'ночь',
    'morning': 'утро',
    'afternoon': 'день',
    'evening': 'вечер',
    'today': 'сегодня',
    'tomorrow': 'завтра',
    'yesterday': 'вчера',
    'week': 'неделя',
    'month': 'месяц',
    'year': 'год',
    'number': 'число',
    'one': 'один',
    'two': 'два',
    'three': 'три',
    'four': 'четыре',
    'five': 'пять',
    'six': 'шесть',
    'seven': 'семь',
    'eight': 'восемь',
    'nine': 'девять',
    'ten': 'десять',
    'red': 'красный',
    'blue': 'синий',
    'green': 'зеленый',
    'yellow': 'желтый',
    'black': 'черный',
    'white': 'белый',
    'big': 'большой',
    'small': 'маленький',
    'hot': 'горячий',
    'cold': 'холодный',
    'happy': 'счастливый',
    'sad': 'грустный',
    'angry': 'сердитый',
    'tired': 'уставший',
    'hungry': 'голодный',
    'thirsty': 'жаждущий',
    'beautiful': 'красивый',
    'ugly': 'уродливый',
    'fast': 'быстрый',
    'slow': 'медленный',
    'easy': 'легкий',
    'difficult': 'сложный',
    'old': 'старый',
    'new': 'новый',
    'good': 'хороший',
    'bad': 'плохой',
    'interesting': 'интересный',
    'boring': 'скучный',
    'exciting': 'захватывающий',
    'funny': 'смешной',
    'serious': 'серьезный',
    'surprised': 'удивленный',
    'afraid': 'испуганный',
    'brave': 'храбрый',
    'strong': 'сильный',
    'weak': 'слабый',
    'healthy': 'здоровый',
    'sick': 'больной',
    "apple": "яблоко",
    "banana": "банан",
    "cat": "кошка",
    "dog": "собака",
    "elephant": "слон",
    "fish": "рыба",
    "giraffe": "жираф",
    "house": "дом",
    "island": "остров",
    "jungle": "джунгли",
    "kangaroo": "кенгуру",
    "lion": "лев",
    "monkey": "обезьяна",
    "nest": "гнездо",
    "ocean": "океан",
    "parrot": "попугай",
    "queen": "королева",
    "rabbit": "кролик",
    "snake": "змея",
    "tiger": "тигр",
    "umbrella": "зонтик",
    "village": "деревня",
    "whale": "кит",
    "xylophone": "ксилофон",
    "yacht": "яхта",
    "zebra": "зебра",
    "airport": "аэропорт",
    "beach": "пляж",
    "car": "автомобиль",
    "doctor": "доктор",
    "engineer": "инженер",
    "fire": "огонь",
    "guitar": "гитара",
    "hotel": "отель",
    "jacket": "куртка",
    "king": "король",
    "lamp": "лампа",
    "mountain": "гора",
    "notebook": "тетрадь",
    "orange": "апельсин",
    "pencil": "карандаш",
    "river": "река",
    "ship": "корабль",
    "table": "стол",
    "violin": "скрипка",
    "window": "окно",
    "yogurt": "йогурт",
    "zeppelin": "дирижабль"
}

medium = {
    "abandon": "оставлять",
    "benevolent": "благожелательный",
    "candid": "откровенный",
    "deft": "ловкий",
    "elusive": "неуловимый",
    "fathom": "понять",
    "gullible": "доверчивый",
    "harmony": "гармония",
    "impeccable": "безупречный",
    "jovial": "жизнерадостный",
    "keen": "острый",
    "lucid": "понятный",
    "meticulous": "дотошный",
    "novice": "новичок",
    "oblivion": "забвение",
    "pristine": "нетронутый",
    "quell": "подавлять",
    "reverence": "почтение",
    "scrutinize": "тщательно исследовать",
    "tedious": "утомительный",
    "unanimous": "единодушный",
    "vibrant": "яркий",
    "wary": "осторожный",
    "zealous": "ревностный",
    "accomplish": "достигать",
    "bewilder": "смущать",
    "conscientious": "добросовестный",
    "diligent": "прилежный",
    "eloquent": "красноречивый",
    "facetious": "шутливый",
    "gregarious": "общительный",
    "humble": "скромный",
    "impartial": "беспристрастный",
    "juxtapose": "помещать рядом",
    "kindle": "разжигать",
    "lament": "оплакивать",
    "mediocre": "посредственный",
    "nurture": "воспитывать",
    "ominous": "зловещий",
    "perceptive": "проницательный",
    "quench": "утолять",
    "resilient": "стойкий",
    "serene": "безмятежный",
    "tangible": "осязаемый",
    "unprecedented": "безпрецедентный",
    "venerate": "почитать",
    "wistful": "тоскующий",
    "yearn": "тосковать",
    "zeal": "рвение",
    "abate": "уменьшать",
    "beguile": "обманывать",
    "concur": "соглашаться",
    "dubious": "сомнительный",
    "elaborate": "разрабатывать",
    "fabricate": "выдумывать",
    "gluttony": "обжорство",
    "hinder": "препятствовать"
}

hard = {
    "aberrant": "отклоняющийся от нормы",
    "acerbic": "язвительный",
    "ambivalent": "амбивалентный, двойственный",
    "antediluvian": "доклиноводный, устаревший",
    "apocryphal": "недостоверный, вымышленный",
    "avaricious": "жадный",
    "bellicose": "воинственный",
    "bucolic": "деревенский, пасторальный",
    "capricious": "капризный",
    "chicanery": "хитрость, мошенничество",
    "conundrum": "загадка, сложная задача",
    "debacle": "крах, провал",
    "decadent": "декадентский, разложение",
    "delineate": "описывать, очерчивать",
    "diatribe": "диатриба, резкая критика",
    "dichotomy": "дихотомия, разделение на две противоположности",
    "disparate": "различный, несовместимый",
    "ebullient": "живой, пылкий",
    "egregious": "вопиющий, явный",
    "enigmatic": "загадочный",
    "ephemeral": "эфемерный, недолговечный",
    "exacerbate": "обострять",
    "exorbitant": "чрезмерный, завышенный",
    "extricate": "высвобождать, освобождать",
    "farcical": "фарсовый, смехотворный",
    "furtive": "тайный, украдкой",
    "garrulous": "болтливый, разговорчивый",
    "gratuitous": "неоправданный, бесплатный",
    "gregarious": "общительный, стадный",
    "hackneyed": "избитый, банальный",
    "heretical": "еретический, отступнический",
    "iconoclast": "иконоборец, бунтарь",
    "idiosyncratic": "идиосинкратический, своеобразный",
    "impetuous": "импульсивный, порывистый",
    "incongruous": "несоответствующий, несовместимый",
    "indomitable": "непокорный, непреклонный",
    "insidious": "коварный, подлый",
    "insolent": "дерзкий, наглый",
    "intransigent": "непреклонный",
}

words_base = {
    1: easy,
    2: medium,
    3: hard
}


# Загрузка слов в базу данных
def load_words_to_database():
    with app.app_context():
        for level, words in words_base.items():
            for word, translate in words.items():
                question = Question(level=level, question=word, answer=translate.split(',')[0])
                db.session.add(question)

        db.session.commit()


if __name__ == '__main__':
    load_words_to_database()
