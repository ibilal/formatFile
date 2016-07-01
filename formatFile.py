import re
import sys


#To run program:

# ./formatFile.py file course_number m(midterm)/f(final)
#
# [REQUIRED] midterm/final (m/f) argument for CS 162 input files
# [OPTIONAL] midterm/final (m/f) argument for CS 163, CS 202 input files
#
#
# Example run:
#   ./formatFile.py input1.txt 162 m
#   ./formatFile.py input2.txt 163
#   ./formatFile.py input3.txt 202 f



#Constant values for command line argument length as well as
#filename, exam, course argument indicies
MAX_ARG_COUNT = 4
MIN_ARG_COUNT = 3
COURSE = 2
FILENAME = 1
EXAM = 3



#Regex for detecting questions, additional instructions, and function prototypes
INSTRUC_REGX = r'[a-zA-Z-_0-9\s!@#$%^&*()+=|\{}[]'""'.,/?><~`]+[^;]'  #all characters expect for semi colon
PROTOTYPE_REGX = r'([a-zA-Z-_0-9\s()*&]+[;])'   #function characters ending in semi colon
#Two variations of question format
QUESTION = 'Write a C++'
QUESTION2 = 'Write a'
PROTOTYPE_KEYWORD = 'Prototype'
PUBLIC_KEYWORD = 'Public Prototype'
PRIVATE_KEYWORD = 'Private Prototype'



#Function to parse CS202 midterm/final questions to required format
#with the specified exam as optional:
def format202(filename, exam, lines):
    print('some to come')


#Function to parse CS163 midterm/final and CS162 final questions to required format
    # REQUIRED: exam for CS 162 Final Files
    # OPTIONAL: exam for CS 163 Midterm/Final Files
def format163(filename, exam, lines):
    question_array = []
    question = False
    prototype = False

    question_text = ''
    prototype_text = ''

    for line in lines:
       # print(line)
        if QUESTION in line or QUESTION2 in line:
            if (question == True):
                if(prototype == True):
                    question_array.append(question_text + '\n' + prototype_text + '\n')
                    question = False
                    question_text = ''
                    prototype_text = ''
                    prototype = False
                else:
                    print('Sorry, file is formatted; question exists without prototype')
                    exit()
            question_text += line
            question = True
        elif re.search(PROTOTYPE_KEYWORD, line, 0):
            continue
        elif re.search(PROTOTYPE_REGX, line, 0):
            prototype_text = line
            prototype = True
        else:
            question_text += line
    if question_text != '' and prototype_text != '' and question == True and prototype == True:
        question_array.append(question_text + '\n' + prototype_text + '\n')

    results = ''
    for element in question_array:
        results += element
    if(exam == ''):
        outputFile = filename + '[FORMATTED].txt'
    else:
        outputFile = filename + '[FORMATTED-' + exam + '].txt'
    output = open(outputFile, 'a')
    output.write(results)


#Function takes a filename and an exam session to parse a CS 162 input textfile
#   into the appropriate exam format (midterm or final)
def format162(filename, exam, lines):

    #if user specifies file is for CS 162
    if exam in ['M', 'm']:
        input = filename.split('.')
        results = ''
        for line in lines:
            results += line + '\n'
        outputFile = filename + '[FORMATTED-" + exam + "].txt'
        output = open(outputFile, 'a')
        output.write(results)


    #else user has specified final for CS 162; in which case will be handled
    # same as CS 163 midterm/final files
    else:
        format163(filename, exam, lines)





### Entry Point ###


#Check argument length for given course:

arg_count = len(sys.argv)

#Too many arguments; throw error
if(arg_count > MAX_ARG_COUNT):
    print('Sorry, too many arguments to format file')
    exit()


#Too few arguments; throw error
if(arg_count < MIN_ARG_COUNT):
    print('Sorry, too few arguments to format file')
    exit()


#Store filename and exam session as well as course
course = sys.argv[COURSE]
filename = sys.argv[FILENAME]
if(arg_count == MAX_ARG_COUNT):
    exam = sys.argv[EXAM]
else:
    exam = ''


#open filename and parse all new lines out of input to be passed to format functions
file = open(filename, 'r')
filename = filename.split('.')
filename = filename[0]
lines = file.readlines()
parsed_lines = []
for line in lines:
    line = line.replace('\n', '')
    line = line.replace('\r', '')
    line = line.replace('\t', '')
    if '\n' not in line:
        parsed_lines.append(line)


#If course selected is 162: format according to midterm/final exam argument
if course == '162':
    if arg_count < MAX_ARG_COUNT:
        print('Sorry, too few arguments to format file')
        print('\n(Try: ./formatFile ' + filename + ' ' + course + ' m/f')

    elif exam not in ['M', 'm', 'F', 'f']:
        print('Sorry, please specify whether the file expected is Midterm (m) or Final (f)')
        print('\n(Try: ./formatFile ' + filename + ' ' + course + ' m/f')

    else:
        format162(filename, exam, parsed_lines)


#Else if course selected is 163: format according to the only format; exam argument is optional - not required
elif course == '163':
    format163(filename, exam, parsed_lines)


#Else if course selected is 202: format according to the only format; exam argument is optional - not required
elif course == '202':
    format202(filename, exam, parsed_lines)

