#!/usr/bin/env python
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
def format202(filename, lines):
    question_array = []
    public_prototype_flag = False
    private_prototype_flag = False

    question_text = ''
    public_prototype_text = ''
    private_prototype_text = ''

    for line in lines:
        if QUESTION in line or QUESTION2 in line:
            if question_text != '' and public_prototype_text != '' and private_prototype_text != '':
                question_array.append(question_text + '\n' + public_prototype_text + ':' + private_prototype_text + '\n')
                question_text = line
                private_prototype_text = ''
                public_prototype_text = ''
                public_prototype_flag = False
                private_prototype_flag = False
            else:
                question_text = line

        elif PUBLIC_KEYWORD in line or PRIVATE_KEYWORD in line:
            continue
        elif re.search(PROTOTYPE_REGX, line, 0):
            if public_prototype_flag == False:
                public_prototype_text += line;
                public_prototype_flag = True
            elif private_prototype_flag == False:
                private_prototype_text += line;
                private_prototype_flag = True
            else:
                print('Sorry, too many prototypes for [' + question_text + ']. Please reformat file.' )
                sys.exit()
        else:
            question_text += ' ' + line
    if question_text != '' and private_prototype_text != '' and public_prototype_text != '' and public_prototype_flag == True and private_prototype_flag == True:
        if question_array.__len__() > 0:
            question_array.append('\n')
        question_array.append(question_text + '\n' + public_prototype_text + ':' + private_prototype_text + '\n')

    results = ''
    for element in question_array:
        results += element
    outputFile = filename + 'FORMATTED.txt'
    output = open(outputFile, 'w')
    output.writelines(results)


#Function to parse CS163 midterm/final and CS162 final questions to required format
    # REQUIRED: exam for CS 162 Final Files
    # OPTIONAL: exam for CS 163 Midterm/Final Files
def format163(filename, lines):
    question_array = []
    prototype_received_flag = False

    question_text = ''
    prototype_text = ''

    for line in lines:
        if QUESTION in line or QUESTION2 in line:
            if prototype_text != '':
                question_array.append(question_text + '\n' + prototype_text + '\n')
                question_text = ''
                prototype_text = ''
                prototype_received_flag = False

            elif question_array.__len__() > 0:
                print('Sorry, file is not formatted correctly for this course; question exists without prototype')
                sys.exit()
            question_text += ' ' + line
        elif re.search(PROTOTYPE_KEYWORD, line, 0):
            continue
        elif re.search(PROTOTYPE_REGX, line, 0):
            prototype_text = line
            prototype_received_flag = True
        else:
            question_text += ' ' + line
    if question_text != '' and prototype_text != '' and prototype_received_flag == True:
        question_array.append(question_text + '\n' + prototype_text + '\n')

    results = ''
    for element in question_array:
        results += element
    outputFile = filename + 'FORMATTED.txt'
    output = open(outputFile, 'w')
    output.writelines(results)


#Function takes a filename and an exam session to parse a CS 162 input textfile
#   into the appropriate exam format (midterm or final)
def format162(filename, exam, lines):

    #if user specifies file is for CS 162
    if exam in ['M', 'm']:
        input = filename.split('.')
        results = ''
        for line in lines:
            if results != '':
                results += '\n'
            results += line.replace('\n', '')
        outputFile = filename + 'FORMATTED.txt'
        output = open(outputFile, 'w')
        output.writelines(results)


    #else user has specified final for CS 162; in which case will be handled
    # same as CS 163 midterm/final files
    else:
        format163(filename, lines)





### Entry Point ###




#Check argument length for given course:

arg_count = len(sys.argv)

#Too many arguments; throw error
if(arg_count > MAX_ARG_COUNT):
    print('Sorry, too many arguments to format file. At most, there can only be three arguments after ./formatFile.py')
    exit()


#Too few arguments; throw error
if(arg_count < MIN_ARG_COUNT):
    print('Sorry, too few arguments to format file. There needs to be at least two arguments after ./formatFile.py')
    exit()


#Store filename and exam session as well as course
course = sys.argv[COURSE]
filename = sys.argv[FILENAME]
if(arg_count == MAX_ARG_COUNT):
    exam = sys.argv[EXAM]
else:
    exam = ''

if exam != '' and exam not in ['M', 'm', 'F', 'f']:
    print('Sorry, exam must be either midterm (M or m) or final (F or f)')
    print('Example: \nTry:   ./formatFile.py input1.txt 162 m')
    sys.exit()


#open filename and parse all new lines out of input to be passed to format functions
try:
    file = open(filename, 'r')
    lines = file.readlines()
except IOError as e:
    print('Sorry, file ' + filename + ' does not exist. Please try again.')
    exit()
except:
    print('Unexpected error: ' +  sys.exec_info()[0])
    exit()

filename = filename.split('.')
filename = filename[0]


if lines.__len__() <= 0:
    print('Input file to format was empty.')
    sys.exit()

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
        print('\n(Try: ./formatFile.py ' + filename + ' ' + course + ' m/f')
        sys.exit()

    elif exam not in ['M', 'm', 'F', 'f']:
        print('Sorry, please specify whether the file expected is Midterm (m) or Final (f)')
        print('\n(Try: ./formatFile.py ' + filename + ' ' + course + ' m/f')
        sys.exit()

    else:
        exam = exam.lower()
        format162(filename, exam, parsed_lines)


#Else if course selected is 163: format according to the only format; exam argument is optional - not required
elif course == '163':
    format163(filename, parsed_lines)


#Else if course selected is 202: format according to the only format; exam argument is optional - not required
elif course == '202':
    format202(filename, parsed_lines)

else:
    print('Sorry, course is not 162, 163, or 202. The input files must be for one of these courses')
    print('Example: \nTry:   ./formatFile.py input1.txt 162 m')
    sys.exit()

