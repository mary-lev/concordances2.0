# coding: utf8
# попробовать что-либо вида
from lxml import etree
from tokenize1 import *

def index(): return dict(message="hello from xml.py")

def create_xml():
    n = 1
    author_texts = [all.id for all in trymysql(trymysql.text1.author==n).select()]
    author_id = trymysql(trymysql.author.id==n).select().first()
    page = etree.Element('all') # create xml tree
    doc = etree.ElementTree(page)
    author = etree.SubElement(page, 'author')
    family = etree.SubElement(author, 'family').text=author_id.family.decode('utf-8')
    name = etree.SubElement(author, 'family').text=author_id.name.decode('utf-8')
    for x in author_texts[1:]:
        texts = trymysql(trymysql.text1.id==int(x)).select()[0] # select one poem
        words_from_base = trymysql(trymysql.allword.title==int(x)).select() # select the poem's words from allword base
        f = open(texts.filename, 'rb')
        content = f.readlines()
        f.close()
        text = etree.SubElement(page, 'text')
        info = etree.SubElement(text, 'info')
        one = etree.SubElement(info, 'title').text = texts.title.decode('utf-8')
        if isinstance(texts.under_title, str):
            subtitle = etree.SubElement(info, 'subtitle').text=texts.under_title.decode('utf-8')
        if isinstance(texts.group_text.title, str):
            group = etree.SubElement(info, 'group').text=texts.group_text.title.decode('utf-8')
        if len(texts.dedication)>0:
            dedication = etree.SubElement(info, 'dedication').text = texts.dedication.decode('utf-8')
        try:
            year = etree.SubElement(info, 'year').text = texts.year_writing
            month = etree.SubElement(info, 'month').text = texts.month_writing
            day = etree.SubElement(info, 'day').text = texts.day_writing
        except:
            pass
        poem = etree.SubElement(text, 'poem')
        count_stanza = 1                                             # count stanzas
        line_count = 1                   # get first word's id from allword base
        word_count = 0
        word_number = words_from_base[0].id
        stanza = etree.SubElement(poem,  'stanza', number = str(count_stanza))
        for lines in content:
            if lines in ['\n', '\r\n']:
                count_stanza += 1
                stanza = etree.SubElement(poem, 'stanza', number = str(count_stanza))
            else:
                string = etree.SubElement(stanza, 'line', number=str(line_count))
                right_line = tokenize2(lines.decode('utf-8'))
                line_count +=1
                for word in right_line:
                    if len(words_from_base)>0:
                        if words_from_base[word_count].id != word_number:
                            slovo=etree.SubElement(string, 'werd')
                            word_number+=1
                        else:
                            slovo = etree.SubElement(string, 'word', number=str(words_from_base[word_count].id), pos = words_from_base[word_count].partos).text=words_from_base[word_count].lemma.decode('utf-8')
                            word_count +=1
                            word_number +=1
                    else:
                        slovo=etree.SubElement(string, 'wurd')
                        word_number +=1
                        word_count += 1
    path = "applications/test/uploads/xml/"
    new_name=path + str(n) + ".xml"
    outFile = open(new_name, 'w')
    doc.write(outFile, pretty_print=True, xml_declaration=True, encoding='utf-16')
    outFile.close()

def create_xml_unique(): # create one xml for one text
    author_texts = [all.id for all in trymysql(trymysql.text1.author==13).select()] # 9458, 10188, 10261 for author 8, 8236 for author 9
    for x in author_texts:
        page = etree.Element('results') # create xml tree
        doc = etree.ElementTree(page)
        texts = trymysql(trymysql.text1.id==int(x)).select().first() # select one poem
        words_from_base = trymysql(trymysql.allword.title==int(x)).select().first().id # select the poem's words from allword base
        title = texts.title
        author = texts.author
        f = open(texts.filename, 'rb')
        content = f.readlines()
        f.close()
        text = etree.SubElement(page, 'text')
        info = etree.SubElement(text, 'info')
        one = etree.SubElement(info, 'title').text = title.decode('utf-8')
        two = etree.SubElement(info, 'name').text = author.name.decode('utf-8')
        three = etree.SubElement(info, 'author').text = author.family.decode('utf-8')
        poem = etree.SubElement(text, 'poem')
        count_stanza = 1                                             # count stanzas
        line_count = 1
        word_number = words_from_base                       # get first word's id from allword base
        stanza = etree.SubElement(poem,  'stanza', number = str(count_stanza))
        for lines in content:
            if lines in ['\n', '\r\n']:
                count_stanza += 1
                stanza = etree.SubElement(poem, 'stanza', number = str(count_stanza))
            else:
                string = etree.SubElement(stanza, 'line', number=str(line_count))
                right_line = tokenize2(lines.decode('utf-8'))
                line_count +=1
                for word in right_line:
                    if trymysql(trymysql.allword.id==word_number).select().first() is None:
                        slovo = etree.SubElement(string, 'werd', number = str(word_number))
                    else:
                        if trymysql(trymysql.allword.id==word_number).select().first().id in [all.id for all in trymysql(trymysql.allword.title==x).select()]:
                            slovo_from_base = trymysql(trymysql.allword.id==word_number).select().first()
                            if slovo_from_base.id in [all.word_first for all in trymysql(trymysql.variants.id>0).select()]: #write variant of word if any
                                slovo = etree.SubElement(string, 'word', number=str(slovo_from_base.id), variant = trymysql(trymysql.variants.word_first==slovo_from_base.id).select().first()['comment_text'].decode('utf-8'), pos = slovo_from_base.partos).text=slovo_from_base.lemma.decode('utf-8')
                            else:
                                slovo = etree.SubElement(string, 'word', number=str(slovo_from_base.id), pos = slovo_from_base.partos).text=slovo_from_base.lemma.decode('utf-8')
                    word_number+=1 # update word's id
        path = "applications/test/uploads/xml/13/"
        new_name=path+str(x) + ".xml"
        DECLARATION = """<?xml version="1.0" encoding="utf-8"?>
        <?xml-stylesheet type="text/xsl" href="style.xslt"?>\n"""
        with open(new_name, 'w') as output: # would be better to write to temp file and rename
            output.write(DECLARATION)
            doc.write(output, xml_declaration=False, pretty_print=True, encoding='utf-8')
            output.close()

def table_as_xml(): #no view yet, for view: {{=TAG(r)}}
    words = trymysql(trymysql.allword.title==15).select()
    r = words.xml()
    return dict(r=r)

types = [None, 'monostich', 'couplet', 'tercet', 'quatrain', 'quintain', 'sestain', 'septet', 'octave', 'nonnet', '10', '11', '12', '13', '14', '15', '16']

def for_tei():
    n = str(request.args(0))
    path = "applications/test/uploads/xml/"
    author_texts = [all.id for all in trymysql(trymysql.text1.author==request.args(0)).select()]
    author_id = trymysql(trymysql.author.id==request.args(0)).select().first()
    page = etree.Element('teiCorpus', xmlns="http://www.tei-c.org/ns/1.0") # create xml tree
    doc = etree.ElementTree(page)
    main_header = etree.SubElement(page, 'teiHeader')
    main_info = etree.SubElement(main_header, 'fileDesc')
    main_titleStmt = etree.SubElement(main_info, 'titleStmt')
    zag = str(author_id.name) + " " + str(author_id.family) + " в tei"
    main_title = etree.SubElement(main_titleStmt, 'title').text=zag.decode('utf-8')
    main_publication = etree.SubElement(main_info, 'publicationStmt')
    main_publisher = etree.SubElement(main_publication, 'publisher').text="ConcorDances.Ru"
    main_source = etree.SubElement(main_info, 'sourceDesc')
    ab = etree.SubElement(main_source, 'ab').text = 'http://concordances.ru'
    for x in author_texts:
        texts = trymysql(trymysql.text1.id==int(x)).select()[0] # select one poem
        f = open(texts.filename, 'rb')
        content = f.readlines()
        f.close()
        tei = etree.SubElement(page, 'TEI')
        header = etree.SubElement(tei, 'teiHeader')
        info = etree.SubElement(header, 'fileDesc')
        titleStmt = etree.SubElement(info, 'titleStmt')
        aut = texts.author.name + ' ' + texts.author.family
        one = etree.SubElement(titleStmt, 'title').text = texts.title.decode('utf-8')
        teiauthor = etree.SubElement(titleStmt, 'author').text=aut.decode('utf-8')

        publication = etree.SubElement(info, 'publicationStmt')
        publisher = etree.SubElement(publication, 'publisher').text="ConcorDances.Ru"
        profileDesc = etree.SubElement(header, 'profileDesc')

        if texts.book:
            sourceDesc = etree.SubElement(info, 'sourceDesc')
            p = etree.SubElement(sourceDesc, 'p').text=texts.book.decode('utf-8')
        if texts.group_text:
            group = etree.SubElement(info, 'group').text=texts.group_text.title.decode('utf-8')

        creation = ''
        if texts.year_writing:
            creation += str(texts.year_writing)
        if texts.month_writing:
            creation = creation + '-' + str(texts.month_writing)
        if texts.day_writing:
            creation = creation + '-' + str(texts.day_writing)
        creation_tei = etree.SubElement(profileDesc, 'creation')
        if creation:
            tei_date = etree.SubElement(creation_tei, 'date', when = creation).text= creation.decode('utf-8')
        if texts.writing_location:
            place = etree.SubElement(creation_tei, 'rs').text=texts.writing_location.decode('utf-8')
        back = count_lines(content)
        text = etree.SubElement(tei, 'text', lines = str(sum(back)), stanzas = str(len(back)), id = str(texts.id))
        if len(texts.dedication) > 0 or texts.epigraph:
            front = etree.SubElement(text, 'front')
        if len(texts.dedication)>0:
            dedication = etree.SubElement(front, 'div', type = 'dedication')
            ded = etree.SubElement(dedication, 'p').text=texts.dedication.decode('utf-8')
        if texts.epigraph:
            epigraph = etree.SubElement(front, "epigraph")
            epis = trymysql(trymysql.epi.text== texts.id).select()
            for e in epis:
                cit = etree.SubElement(epigraph, 'cit')
                quote = etree.SubElement(cit, "quote").text = e.epi_text.decode('utf-8')
                if e.epi_author or e.epi_book:
                    bibl = etree.SubElement(cit, 'bibl')
                if e.epi_author:
                    author_bibl = etree.SubElement(bibl, 'author').text = e.epi_author.decode('utf-8')
                if e.epi_book:
                    title_bibl = etree.SubElement(bibl, 'title').text = e.epi_book.decode('utf-8')
        body = etree.SubElement(text, 'body')
        count_stanza = 1                 # count stanzas
        line_count = 1                   # get first word's id from allword base
        stanza = etree.SubElement(body, 'lg', n = str(count_stanza), type = str(back.pop(0)))
        for lines in content:
            if lines in ['\n', '\r\n', '|'] or '|' in lines:
                count_stanza += 1
                stanza = etree.SubElement(body, 'lg', n = str(count_stanza), type = str(back.pop(0)))
            else:
                string = etree.SubElement(stanza, 'l', n = str(line_count)).text = lines.decode('utf-8')
                line_count +=1
    new_name=str(str(n)) + ".xml"
    DECLARATION = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml"  schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml"
	schematypens="http://purl.oclc.org/dsdl/schematron"?>"""
    #outFile = open(new_name, 'w')
    #doc.write(outFile, pretty_print=True, xml_declaration=True, encoding='utf-16')
    #outFile.close()
    with open(new_name, 'w') as output: # would be better to write to temp file and rename
            output.write(DECLARATION)
            doc.write(output, xml_declaration=False, pretty_print=True, encoding='utf-8')
            output.close()

def type_stanza(count):
    types = [None, 'monostich', 'couplet', 'tercet', 'quatrain', 'quintain', 'sestain', 'septet', 'octave', 'nonnet', '10', '11', '12', '13', '14', '15', '16']
    try:
        a = types[count]
    except:
        a = str(count)
    return a

def count_lines(content):
    back = []
    line_count = 0                   # get first word's id from allword base
    for lines in content:
        if lines in ['\n', '\r\n', '|'] or '|' in lines:
            back.append(line_count)
            line_count = 0
        else:
            line_count +=1
    back.append(line_count)
    return back
