import re
import os
import glob

rawHtmlFolder           = os.getcwd() + '/corpus/'
docId2DocNumFile        = 'DocumentIndexMapping_CACM.txt'

pTagRegex               = '<pre>.*?</pre>'
ulTagRegex              = '<ul>.*?</ul>'
textExtractingRegex     = r'<[^>]+>|[^<]+'
titleRegex              = '<title>(.+?)</title>'

numericRegex            = r'(\d{1,3},\d{3}(,\d{3})*)(\.\d*)?|\d+\.?\d*'
alphanumericRegex       = '.*\\d+.*'

def getParagraphs(body):
    pattern = re.compile(pTagRegex)
    return re.findall(pattern, body)

def getBullets(body):
    pattern = re.compile(ulTagRegex)
    return re.findall(pattern, body)

def getText(paragraph):
    pattern = re.compile(textExtractingRegex)
    return " ".join([t.strip() for t in
              re.findall(pattern, paragraph)
                     if not '<' in t])

def getTitle(htmlText):
    pattern = re.compile(titleRegex)
    return re.findall(pattern, htmlText)


def removePunctuation(text):
    pattern = re.compile(numericRegex)
    #if re.match(pattern, text):
        #return text
    if hasNumber(text):
       text = preservePunctuation(text)
    else:
        if ',' in text:
            text = text.replace(',',' ')
        if '.' in text:
            text = text.replace('.',' ')

    if '/' in text:
        text = text.replace('/',' ')
    if '?' in text:
        text = text.replace('?',' ')
    if '!' in text:
        text = text.replace('!',' ')
    if '"' in text:
        text = text.replace('"',' ')
    if '~' in text:
        text = text.replace('~',' ')
    if '@' in text:
        text = text.replace('@',' ')
    if '#' in text:
        text = text.replace('#',' ')
    if '(' in text:
        text = text.replace('(',' ')
    if ')' in text:
        text = text.replace(')',' ')
    if '^' in text:
        text = text.replace('^',' ')
    if '[' in text:
        text = text.replace('[',' ')
    if ']' in text:
        text = text.replace(']',' ')
    if ':' in text:
        text = text.replace(':',' ')
    if ';' in text:
        text = text.replace(';',' ')
    if '&amp' in text:
        text = text.replace('&amp',' ')
    if '&nbsp' in text:
        text = text.replace('&nbsp',' ')

    if text != '' and (text[-1] == '.' or text[-1] == ','):
        return text[:-1]
    
    return text

def hasNumber(text):
    pattern = re.compile(alphanumericRegex)
    if re.match(pattern, text):
        return True

    return False

def preservePunctuation(text):
    n = len(text)
    i = 0
    while i < n-1:
        if i>0 and (text[i] == ',' or text[i] == '.'):
            if not (re.match('[0-9]', text[i - 1]) and re.match('[0-9]', text[i + 1])):
                text = text[:i] + text[(i+1):]
                n-=1
        i+=1
        
    return text
                            
def indexableText(paragraph):
    newParagraph = ''
    for text in paragraph.split(' '):
        if '-' in text:
            for hyphenated in text.split('-'):
                newParagraph += removePunctuation(hyphenated.lower()) + '-'
            newParagraph = newParagraph[:-1]
        else:
            newParagraph += removePunctuation(text.lower())
            
        newParagraph += ' '

    return newParagraph[:-1]

def parseHtml(rawHtml):
    extractedText = ''
    title = getTitle(rawHtml)
    if len(title) > 0:
        extractedText += title[0].lower() + '\n'
    paragraphs    = getParagraphs(rawHtml)
    for paragraph in paragraphs:
        extractedText += indexableText(getText(paragraph)).replace('   ',' ').replace('   ',' ').replace('  ', ' ') + '\n'
    bullets = getBullets(rawHtml)
    for bullet in bullets:
        extractedText += indexableText(getText(bullet)).replace('   ',' ').replace('   ',' ').replace('  ', ' ') + '\n'

    return extractedText.replace('    ',' ').replace('   ',' ').replace('  ', ' ')


docCounter = 1
with open (os.getcwd() + '\\' + docId2DocNumFile, 'w') as dictFile:
    dictFile.write('DocId, PlainTextFile, RawHtmlFile\n')
    for root, dirs, files in os.walk(rawHtmlFolder):
        for document in files:
            print docCounter
            with open (rawHtmlFolder + document, 'r') as htmlFile:
                extractedText = parseHtml(htmlFile.read().replace('\n',' ').replace('\t',' ').replace('   ',' ').replace('  ', ' '))
                docId = document.replace('_','').replace('-','').replace(',','').replace('(','').replace(')','').replace('.','').replace('txt','') + '%d' % (docCounter)
                
                with open (os.getcwd() + '\\PlainText\\' + docId + '.txt', 'w') as plainTextFile:
                    plainTextFile.write(extractedText)
                    
            dictFile.write('%d, %s, %s\n' % (docCounter, docId, document))
            docCounter += 1

            
