morphot = DAL("sqlite://storage.sqlite")

morphot.define_table('pos',
                    Field('author'),
                    Field('title'),
                    Field('year'),
                    Field('groups'),
                    Field('noun'),
                    Field('verb'),
                    Field('infn'),
                    Field('adjf'),
                    Field('adjs'),
                    Field('prep'),
                    Field('conj'),
                    Field('prcl'),
                    Field('sluzh'))

morphot.define_table('verb',
                    Field('author'),
                    Field('title'),
                    Field('year'),
                    Field('verbs', 'list:string'))