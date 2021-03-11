"""
Created on 03/01/2021

file:           mrz_parser.py
description:

@author: Almoutaz
"""
class cardType():
    nocard = -1
    card_0 = 0
    card_1 = 1
    card_2 = 2
    card_3 = 3
    card_4 = 4

def sub_string(line, start, end):
    sub_line = line[start: end]
    sub_line = sub_line.replace('<', '')
    return sub_line

def sub_string_with_space_replace(line, start, end):
    sub_line = line[start: end]
    sub_line = sub_line.replace('<', ' ')
    return sub_line

def sub_string_without_replace(line, start, end):
    sub_line = line[start: end]
    return sub_line

class mrzParser():
    def __init__(self, lines):
        self.lines = lines

        self.passportType = ""
        self.countryCode = ""
        self.surname = ""
        self.givenname = ""
        self.passportNumber = ""
        self.passportChecksum = ""
        self.nationality = ""
        self.birthday = ""
        self.birthdayChecksum = ""
        self.sex = ""
        self.expirationDate = ""
        self.expirationChecksum = ""
        self.personalNumber = ""
        self.personalNumberChecksum = ""
        self.secondRowChecksum = ""
        self.optionalData = ""
        self.optionalData2 = ""

        self.hash1 = ""
        self.hash2 = ""
        self.hash3 = ""
        self.hash4 = ""
        self.final_hash = ""

    def getCardType(self):
        type = cardType.nocard
        separated = self.lines.split('\r\n')
        linecount = len(separated)
        ch_num = len(separated[0])
        first_ch = separated[0][0]

        if linecount == 3 and ch_num == 30:
            type = cardType.card_0
        elif linecount == 2 and ch_num == 36:
            if first_ch == "V" :
                type == cardType.card_4
            else:
                type = cardType.card_1
        elif linecount == 2 and ch_num == 44:
            if first_ch == "V":
                type = cardType.card_3
            else:
                type = cardType.card_2
        return type

    def analysisMRZ_0(self):
        separated_lines = self.lines.split('\r\n')

        # line 1
        line_tmp = separated_lines[0]

        # document type
        self.passportType = sub_string(line_tmp, 0, 2)
        # country
        self.countryCode = sub_string(line_tmp, 2, 5)
        # document num
        self.passportNumber = sub_string(line_tmp, 5, 14)
        # hash1
        self.hash1 = sub_string(line_tmp, 14, 15)
        # optional data
        self.optionalData = sub_string(line_tmp, 15, 30)

        # line 2
        line_tmp = separated_lines[1]

        # date of birth
        self.birthday = sub_string(line_tmp, 0, 2) + '/' + sub_string(line_tmp, 2, 4) + '/' + sub_string(line_tmp, 4, 6)
        # hash2
        self.hash2 = sub_string(line_tmp, 6, 7)
        # gender
        self.sex = sub_string(line_tmp, 7, 8)
        # expire date
        self.expirationDate = sub_string(line_tmp, 8, 10) + '/' + sub_string(line_tmp, 10, 12) + '/' + sub_string( line_tmp, 12, 14)
        # hash3
        self.hash3 = sub_string(line_tmp, 14, 15)
        # nationality
        self.nationality = sub_string(line_tmp, 15, 18)
        # optional data 2
        self.optionalData2 = sub_string(line_tmp, 18, 29)
        # final hash
        self.final_hash = sub_string(line_tmp, 29, 30)

        # line 3
        line_tmp = separated_lines[2]

        sept_names = line_tmp.split('<<')
        if len(sept_names) >= 2:
            # last name
            self.surname = sub_string_with_space_replace(sept_names[0], 0, len(sept_names[0]))
            # given name
            self.givenname = sub_string_with_space_replace(sept_names[1], 0, len(sept_names[1]))
        else:
            # last name
            self.surname = ""
            # given name
            self.givenname = sub_string(line_tmp, 0, 30)
        return

    def analysisMRZ_1(self):
        separated_lines = self.lines.split('\r\n')

        # line 1
        line_tmp = separated_lines[0]

        # document type
        self.passportType = sub_string(line_tmp, 0, 2)
        # country
        self.countryCode = sub_string(line_tmp, 2, 5)

        name_line = sub_string_without_replace(line_tmp, 5, 36)
        sept_names = name_line.split('<<')
        if len(sept_names) >= 2:
            # last name
            self.surname = sub_string_with_space_replace(sept_names[0], 0, len(sept_names[0]))
            # given name
            self.givenname = sub_string_with_space_replace(sept_names[1], 0, len(sept_names[1]))
        else:
            # last name
            self.surname = ""
            # given name
            self.givenname = sub_string(line_tmp, 5, 36)

        # line 2
        line_tmp = separated_lines[1]
        # document num
        self.passportNumber = sub_string(line_tmp, 0, 9)
        # hash1
        self.hash1 = sub_string(line_tmp, 9, 10)
        # nationality
        self.nationality = sub_string(line_tmp, 10, 13)
        # date of birth
        self.birthday = sub_string(line_tmp, 13, 15) + '/' + sub_string(line_tmp, 15, 17) + '/' + sub_string(line_tmp,
                                                                                                             17, 19)
        # hash2
        self.hash2 = sub_string(line_tmp, 19, 20)
        # gender
        self.sex = sub_string(line_tmp, 20, 21)
        # expire date
        self.expirationDate = sub_string(line_tmp, 21, 23) + '/' + sub_string(line_tmp, 23, 25) + '/' + sub_string(
            line_tmp, 25, 27)
        # hash3
        self.hash3 = sub_string(line_tmp, 27, 28)
        # optional data
        self.optionalData = sub_string(line_tmp, 28, 35)
        # final hash
        self.final_hash = sub_string(line_tmp, 35, 36)
        return

    def analysisMRZ_2(self):
        separated_lines = self.lines.split('\r\n')

        # line 1
        line_tmp = separated_lines[0]

        # document type
        self.passportType = sub_string(line_tmp, 0, 2)
        # country
        self.countryCode = sub_string(line_tmp, 2, 5)

        name_line = sub_string_without_replace(line_tmp, 5, 44)
        sept_names = name_line.split('<<')
        if len(sept_names) >= 2:
            # last name
            self.surname = sub_string_with_space_replace(sept_names[0], 0, len(sept_names[0]))
            # given name
            self.givenname = sub_string_with_space_replace(sept_names[1], 0, len(sept_names[1]))
        else:
            # last name
            self.surname = ""
            # given name
            self.givenname = sub_string(line_tmp, 5, 44)

        # line 2
        line_tmp = separated_lines[1]
        # document num
        self.passportNumber = sub_string(line_tmp, 0, 9)
        # hash1
        self.hash1 = sub_string(line_tmp, 9, 10)
        # nationality
        self.nationality = sub_string(line_tmp, 10, 13)
        # date of birth
        self.birthday = sub_string(line_tmp, 13, 15) + '/' + sub_string(line_tmp, 15, 17) + '/' + sub_string(line_tmp, 17, 19)
        # hash2
        self.hash2 = sub_string(line_tmp, 19, 20)
        # gender
        self.sex = sub_string(line_tmp, 20, 21)
        # expire date
        self.expirationDate = sub_string(line_tmp, 21, 23) + '/' + sub_string(line_tmp, 23, 25) + '/' + sub_string(line_tmp, 25, 27)
        # hash3
        self.hash3 = sub_string(line_tmp, 27, 28)
        # personal number
        self.personalNumber = sub_string(line_tmp, 28, 42)
        # hash4
        self.hash4 = sub_string(line_tmp, 42, 43)
        # final hash
        self.final_hash = sub_string(line_tmp, 43, 44)
        return

    def analysisMRZ_3(self):
        separated_lines = self.lines.split('\r\n')

        # line 1
        line_tmp = separated_lines[0]

        # document type
        self.passportType = sub_string(line_tmp, 0, 2)
        # country
        self.countryCode = sub_string(line_tmp, 2, 5)

        name_line = sub_string_without_replace(line_tmp, 5, 44)
        sept_names = name_line.split('<<')
        if len(sept_names) >= 2:
            # last name
            self.surname = sub_string_with_space_replace(sept_names[0], 0, len(sept_names[0]))
            # given name
            self.givenname = sub_string_with_space_replace(sept_names[1], 0, len(sept_names[1]))
        else:
            # last name
            self.surname = ""
            # given name
            self.givenname = sub_string(line_tmp, 5, 44)

        # line 2
        line_tmp = separated_lines[1]

        # document num
        self.passportNumber = sub_string(line_tmp, 0, 9)
        # hash1
        self.hash1 = sub_string(line_tmp, 9, 10)
        # nationality
        self.nationality = sub_string(line_tmp, 10, 13)
        # date of birth
        self.birthday = sub_string(line_tmp, 13, 15) + '/' + sub_string(line_tmp, 15, 17) + '/' + sub_string(line_tmp,
                                                                                                             17, 19)
        # hash2
        self.hash2 = sub_string(line_tmp, 19, 20)
        # gender
        self.sex = sub_string(line_tmp, 20, 21)
        # expire date
        self.expirationDate = sub_string(line_tmp, 21, 23) + '/' + sub_string(line_tmp, 23, 25) + '/' + sub_string(
            line_tmp, 25, 27)
        # hash3
        self.hash3 = sub_string(line_tmp, 27, 28)
        # optional data
        self.optionalData = sub_string(line_tmp, 28, 44)
        return

    def analysisMRZ_4(self):
        separated_lines = self.lines.split('\r\n')

        # line 1
        line_tmp = separated_lines[0]

        # document type
        self.passportType = sub_string(line_tmp, 0, 2)
        # country
        self.countryCode = sub_string(line_tmp, 2, 5)

        name_line = sub_string_without_replace(line_tmp, 5, 36)
        sept_names = name_line.split('<<')
        if len(sept_names) >= 2:
            # last name
            self.surname = sub_string_with_space_replace(sept_names[0], 0, len(sept_names[0]))
            # given name
            self.givenname = sub_string_with_space_replace(sept_names[1], 0, len(sept_names[1]))
        else:
            # last name
            self.surname = ""
            # given name
            self.givenname = sub_string(line_tmp, 5, 36)

        # line 2
        line_tmp = separated_lines[1]
        # document num
        self.passportNumber = sub_string(line_tmp, 0, 9)
        # hash1
        self.hash1 = sub_string(line_tmp, 9, 10)
        # nationality
        self.nationality = sub_string(line_tmp, 10, 13)
        # date of birth
        self.birthday = sub_string(line_tmp, 13, 15) + '/' + sub_string(line_tmp, 15, 17) + '/' + sub_string(line_tmp,
                                                                                                             17, 19)
        # hash2
        self.hash2 = sub_string(line_tmp, 19, 20)
        # gender
        self.sex = sub_string(line_tmp, 20, 21)
        # expire date
        self.expirationDate = sub_string(line_tmp, 21, 23) + '/' + sub_string(line_tmp, 23, 25) + '/' + sub_string(
            line_tmp, 25, 27)
        # hash3
        self.hash3 = sub_string(line_tmp, 27, 28)
        # optional data
        self.optionalData = sub_string(line_tmp, 28, 36)
        return

    def process(self):
        type = self.getCardType()
        if type == cardType.card_0:
            self.analysisMRZ_0()
        elif type == cardType.card_1:
            self.analysisMRZ_1()
        elif type == cardType.card_2:
            self.analysisMRZ_2()
        elif type == cardType.card_3:
            self.analysisMRZ_3()
        elif type == cardType.card_4:
            self.analysisMRZ_4()
        else:
            return "error"