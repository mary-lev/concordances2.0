trymysql = DAL('mysql://concordance:sosnora@concordance.mysql.pythonanywhere-services.com/concordance$new')

trymysql.define_table('author',
                  Field('name', label="Имя"),
                  Field('surname', label="Отчество"),
                  Field('family', label="Фамилия"),
                  Field('real_name', label="Настоящее имя"),
                  Field('year_birth', label="Год рождения"),
                  Field('year_death', label="Год смерти"),
                  Field('gender', label="Пол"),
                  Field('birth_location', label="Место рождения"),
                  Field('death_location', label="Место смерти"),
                  migrate=False,fake_migrate=True)

trymysql.define_table('group_text',
                  Field('title', label="Название"),
                  Field('author', trymysql.author),
                  Field('v', label="Объем текста"),
                  Field('genre', label="Жанр"),
                  Field('dedication', label = 'Посвящение'),
                  Field('epigraph', label="Эпиграф"),
                  Field('epigraph_text_name', label="Источник эпиграфа"),
                  Field('year', label="Год написания"),
                  Field('superpgroup', label="Группа текстов"),
                  migrate=False,fake_migrate=True)

trymysql.define_table('text1',
                  Field('title', label="Название"),
                  Field('first_string', label="Первая строка"),
                  Field('body', 'text', label="Текст"),
                  Field('filename', 'string'),
                  Field('year_writing', label="Год написания"),
                  Field('month_writing', label="Месяц написания"),
                  Field('day_writing', label="День написания"),
                  Field('dyear_writing', label="Неточный год написания"),
                  Field('dmonth_writing', label="Неточный месяц написания"),
                  Field('season_writing', label="Сезон"),
                  Field('dday_writing', label="Неточный день написания"),
                  Field('writing_location', label="Место написания"),
                  Field('year_publishing', label="Год первой публикации"),
                  Field('genre', label="Жанр"),
                  Field('under_title', label="Подзаголовок"),
                  Field('dedication', label="Посвящение"),
                  Field('epigraph', 'text', label="Текст эпиграфа"),
                  Field('epigraph_author', label="Автор эпиграфа"),
                  Field('epigraph_text_name', label="Источник эпиграфа"),
                  Field('v', label="Объем текста"),
                  Field('book', label="Источник текста"),
                  Field('group_text', trymysql.group_text, label="Принадлежность к группе текстов"),
                  Field('n_in_group', label="Порядковый номер в группе текстов"),
                  Field('author', trymysql.author, label="Номер автора"),
                  migrate=False,fake_migrate=True)

trymysql.define_table('stih',
                      Field('title', trymysql.text1, label="Текст"),
                      Field('author', trymysql.author, label="Автор"),
                      Field('strofa', label="Строфа"),
                      Field('kol_strok', label = "Количество строф"),
                      Field('type_s', label = "Тип строфы"),
                      Field('rhymes', 'text', label = "Рифмы"),
                      Field('trhymes', 'text', label="ТРифмы"),
                      Field('type_r', label = "Схема рифмовки"),
                      migrate=False,fake_migrate=True)

trymysql.define_table('allword',
                  Field('word', label="Слово"),
                  Field('lemma'),
                  Field('title', trymysql.text1, label="Текст"),
                  Field('partos', label="Часть речи"),
                  Field('anim', label="Одушевленность"),
                  Field('gendr', label="Род"),
                  Field('number', label="Число"),
                  Field('cas', label="Падеж"),
                  Field('tense', label="Время"),
                  Field('aspect', label="Вид"),
                  Field('person', label="Лицо"),
                  Field('transitivity', label="Переходность"),
                  Field('mood', label="Наклонение"),
                  Field('involvment', label="Совместность"),
                  Field('voice', label="Залог"),
                  Field('sobstv', label="Имя собственное"),
                  Field('style', label="Стиль"),
                  Field('other', label="Другое"),
                  Field('text_location', label="Место в тексте"),
                  Field('string_number', label="Номер строки"),
                  Field('lexical_group', label="Лексическая группа"),
                  Field('concordance_number',  label="Номер в конкордансе"),
                  Field('warning', label = "Warning"),
                  Field('author', label="Автор"),
                  migrate=False,fake_migrate=True)

trymysql.define_table('slovar',
                      Field('word', label='Основа'),
                      Field('pro', label='Производные'))

trymysql.define_table('slovar1',
                      Field('word', label='Основа'),
                      Field('pro', label='Производные'))

trymysql.define_table('concordances',
                  Field('word', label="Слово"),
                  Field('partos', label="Часть речи"),
                  Field('lexical', label="Лексическая группа"),
                  migrate=False,fake_migrate=True)

trymysql.define_table('color',
                  Field('word', label="Слово"),
                  Field('partos', label="Часть речи"),
                  Field('lexical', label="Лексическая группа"),
                  migrate=False,fake_migrate=True)

trymysql.define_table('comments',
                      Field('title', trymysql.text1, label = "Номер текста"),
                      Field('stanza', label = "Номер строфы в тексте"),
                      Field('line', label = "Номер строки в тексте"),
                      Field('word_first', trymysql.allword, label="Номер первого слова"),
                      Field('word_last', trymysql.allword, label="Номер последнего слова"),
                      Field('comment_text', 'text', label = "Комментарий"),
                      Field('comment_book', label = "Источник"),
                      Field('comment_year', label="Год публикации комментария"),
                      migrate=False,fake_migrate=True)

trymysql.define_table('variants',
                      Field('title', trymysql.text1, label = "Номер текста"),
                      Field('stanza', label = "Номер строфы в тексте"),
                      Field('line', label = "Номер строки в тексте"),
                      Field('word_first', trymysql.allword, label="Номер первого слова"),
                      Field('word_last', trymysql.allword, label="Номер последнего слова"),
                      Field('comment_text', 'text', label = "Вариант"),
                      Field('comment_book', label = "Издание"),
                      Field('comment_year', label="Год публикации комментария"),
                      migrate=False,fake_migrate=True)

trymysql.define_table('data',
                  Field('author', trymysql.author),
                  Field('book', trymysql.group_text),
                  Field('year', label="Год"),
                  Field('alltexts', label="Количество текстов"),
                  Field('allwords', label="Количество слов"),
                  Field('all_nouns', label="Количество существительных"),
                  Field('all_verbs', label="Количество глаголов"),
                  Field('all_infn', label="Количество инфинитивов"),
                  Field('all_adjf', label="Количество полных прилагательных"),
                  Field('all_adjs', label="Количество кратких прилагательных"),
                  Field('all_grnd', label="Количество деепричастий"),
                  Field('all_prtf', label="Количество полных причастий"),
                  Field('all_prts', label="Количество кратких причастий"),
                  Field('all_advb', label="Количество наречий"),
                  Field('all_prep', label="Количество предлогов"),
                  Field('all_conj', label="Количество союзов"),
                  Field('all_prcl', label="Количество частиц"),
                  Field('all_npro', label="Количество местоимений"),
                  Field('all_point', label="Количество точек"),
                  Field('all_exclam', label="Количество восклицательных знаков"),
                  Field('all_comma', label="Количество запятых"),
                  Field('all_question', label="Количество вопросительных знаков"),
                  Field('length_sentence', label="Средняя длина предложения"),
                  Field('length_words', label="Средняя длина слова"),
                  Field('words_range', label="Насыщенность словаря"),
                  migrate = False, fake_migrate=True)

trymysql.define_table('grammar',
                  Field('author', trymysql.author),
                  Field('book', trymysql.group_text),
                  Field('year', label="Год"),
                  Field('masc', label="Мужской род"),
                  Field('femn', label="Женский род"),
                  Field('inan', label="Неодушевленные"),
                  Field('anim', label="Одушевленные"),
                  Field('past', label="Прошедшее время"),
                  Field('pres', label="Настоящее время"),
                  Field('futr', label="Будущее время"),
                  Field('name', label="Имен собственных"),
                  Field('len_text', label="Средняя длина текста, строк"),
                  Field('len_line', label="Средняя длина строки, слова"),
                  Field('len_line_w', label="Средняя длина строки, буквы"),
                  migrate=False, fake_migrate=False)

trymysql.define_table('biblio',
                      Field('title', label='Название'),
                      Field('author', trymysql.author),
                      Field('city', label='Город'),
                      Field('editor', label='Издательство'),
                      Field('year', label='Год'),
                      Field('part', label='Том'),
                      Field('short', label = 'Сокращенно'),
                      migrate = False, fake_migrate=True)

trymysql.define_table('drafts',
                      Field('author', trymysql.author),
                      Field('text', trymysql.text1),
                      Field('title', label="Название"),
                      Field('filename', 'string'),
                      Field('epi', 'text', label="Эпиграф"),
                      Field('epi_author', label="Автор эпиграфа"),
                      Field('epi_book', label="Источник эпиграфа"),
                      Field('dedication', 'string', label='Посвящение'),
                      Field('day', label=''),
                      Field('month', label=''),
                      Field('year', label='Год'),
                      Field('date', label='Неточная дата'),
                      Field('book', trymysql.biblio),
                      Field('book_page', label='Страница'))

trymysql.define_table('page',
                       Field('book', trymysql.biblio),
                       Field('number', label="Страница"),
                       Field('filename', label="Файл"),
                       Field('text', trymysql.text1),
                       Field('variant', trymysql.drafts),
                       Field('old_text', label='В старой орфографии'))

trymysql.define_table('old',
                      Field('author', trymysql.author),
                      Field('text', trymysql.text1),
                      Field('title', label="Название"),
                      Field('first_string', label="Первая строка"),
                      Field('filename', 'string'),
                      Field('epi', 'text', label="Эпиграф"),
                      Field('epi_author', label="Автор эпиграфа"),
                      Field('epi_book', label="Источник эпиграфа"),
                      Field('dedication', 'string', label='Посвящение'),
                      Field('day', label=''),
                      Field('month', label=''),
                      Field('year', label='Год'),
                      Field('date', label='Неточная дата'),
                      Field('book', trymysql.biblio),
                      Field('book_page', label='Страница'))

trymysql.define_table('epi',
                       Field('text', trymysql.text1),
                       Field('epi_text', 'text', label='Текст'),
                       Field('epi_author', label='Автор'),
                       Field('epi_author_id', trymysql.author, requires=None),
                       Field('epi_book', label='Книга'),
                       Field('epi_text_id', trymysql.text1, requires=None),
                       Field('epi_filename', label='Файл'))

trymysql.define_table('mystem',
               Field('word', label="Слово"),
               Field('lemma', label='Словоформа'),
               Field('title', trymysql.text1, label="Текст"),
               Field('partos', label="Часть речи"),
               Field('anim', label="Одушевленность"),
               Field('gender', label="Род"),
               Field('forma', label = "Форма"),
               Field('comp', label = "Сравнит"),
               Field('number', label="Число"),
               Field('cas', label="Падеж"),
               Field('tense', label="Время"),
               Field('aspect', label="Вид"),
               Field('person', label="Лицо"),
               Field('trans', label="Переходность"),
               Field('verb', label="Форма глагола"),
               Field('voice', label="Залог"),
               Field('other', label="Другое"),
               Field('lexical_group', label="Лексическая группа"),
               Field('location', label='Номер в тексте'),
               Field('concordance_number',  label="Номер в конкордансе"),
               Field('author', trymysql.author, label="Автор") )

#purchased = (trymysql.author.name==trymysql.text1.author)&(trymysql.author.id==trymysql.words.author)
#n2ew = (trymysql.text1.title==trymysql.words.title)&(trymysql.text1.id==trymysql.words.title)
b = (trymysql.variants.comment_book==trymysql.biblio.id)
