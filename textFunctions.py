###################
# rightJustifyText
# This contains the text justifier code from HW3
###################
import string

def replaceWhiteSpace(text):
    #replace white space in text with normal spaces
    #inspired by recitation 3 video
    inWhiteSpace=False
    result=''
    for c in text:
        if not inWhiteSpace and c.isspace():
            inWhiteSpace=True
        elif inWhiteSpace and not c.isspace():
            inWhiteSpace=False
            result+=' '+c
        elif not inWhiteSpace and not c.isspace():
            result+=c
    return result

def breakLines(text, width):
    #break into lines of required width
    newText=''
    lineLen=0
    for word in text.split(' '):
        if lineLen+len(word) > width:
            newText+='\n'+word+' '
            lineLen=len(word)+1
        else:
            newText+=word+' '
            lineLen+=len(word)+1
    return newText

def removeTrailingSpaces(text):
    #remove trailing white space in each line
    newText=''
    for line in text.splitlines():
        newText+=line.strip()+'\n'
    return newText

def createNewText(text, width):
    #return clean lines of required width with above functions
    text=text.strip()
    text=replaceWhiteSpace(text)
    text=breakLines(text, width)
    text=removeTrailingSpaces(text)
    return text

def rightJustifyText(text, width):
    #return right-justified text
    text=createNewText(text, width)
    newText=''
    #add white space before text to align right
    for line in text.splitlines():
        newText+=' '*(width-len(line))+line+'\n'
    #remove '\n' at end
    newText=newText[:-1]
    return newText