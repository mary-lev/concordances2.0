test = DAL("sqlite://storage.sqlite")

test.define_table('image',
   Field('title', unique=True),
   Field('file', 'upload'),
   format = '%(title)s',
   migrate=False,fake_migrate=True)

test.define_table('author',
                  Field('name'),
                  Field('surname'),
                  Field('family'),
                  Field('year_birth'),
                  Field('year_death'),
                  migrate=False,fake_migrate=True)

test.define_table('text',
                  Field('author', test.author),
                  Field('title'),
                  Field('year'),
                  Field('body'),
                  Field('book'),
                  migrate=False,fake_migrate=True)

test.define_table('text2',
                  Field('title', unique=True),
                  Field('author'),
                  Field('body', 'text'),
                  Field('year'),
                  Field('book'),
                  format='%(title)s',
                  migrate=False,fake_migrate=True)

test.define_table('tokens',
                  Field('title'),
                  Field('author', test.author),
                  Field('tokens', 'list:string'),
                  format='%(title)s',
                  migrate=False,fake_migrate=True)

test.define_table('morpho',
                  Field('title'),
                  Field('author'),
                  Field('year'),
                  Field('form'),
                  Field('groups'),
                  Field('sr_ar'),
                  Field('number'),
                  Field('slovoforma'),
                  Field('slovar'),
                  Field('sentences'),
                  Field('dlina_predl'),
                  Field('stop'),
                  Field('udel_stop'),
                  format='%(title)s',
                  migrate=False,fake_migrate=True)

test.define_table('new_form',
                  Field('omonim', 'string'),
                  Field('sentences', 'string'),
                  Field('meaning', 'string'),
                  Field('forms', 'list:string'),
                  Field('one_form', 'string'),
                  migrate=False,fake_migrate=True)

test.define_table('url',
                  Field('urladres'),
                  Field('text', 'text'),
                  Field('author'),
                  Field('title'),
                  Field('year'),
                  Field('wordfile'),
                  migrate=False,fake_migrate=True)

test.define_table('slovar',
                  Field('author'),
                  Field('title'),
                  Field('year'),
                  Field('form'),
                  Field('tokens'),
                  Field('lemmas', 'list:string'),
                  Field('verbs_lemmas', 'list:string'),
                  format='%(title)s',
                  migrate=False,fake_migrate=True)

test.define_table('comment',
   Field('image_id', test.image),
   Field('author'),
   Field('email'),
   Field('body', 'text'),
   migrate=False,fake_migrate=True)

test.image.title.requires = IS_NOT_IN_DB(test, test.image.title)
test.text2.body.requires = IS_NOT_EMPTY()
test.comment.image_id.requires = IS_IN_DB(test, test.image.id, '%(title)s')
test.comment.author.requires = IS_NOT_EMPTY()
test.comment.email.requires = IS_EMAIL()
test.comment.body.requires = IS_NOT_EMPTY()

test.comment.image_id.writable = test.comment.image_id.readable = False
