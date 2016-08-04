# coding=utf-8
__author__ = "WJW"

import re
import xlsxwriter

skill_count = {}

def getSkillContents():

    fs = open('./bb.txt','r')
    contents = fs.read()
    fs.close()
    return contents

def search_skill(contents):
    if contents:
        rule = re.compile(r'[a-zA-z]+')
        skills = rule.findall(contents)
        return skills
    else:
        return None

def save_excel(skills,file_name):
    book = xlsxwriter.Workbook(r'./%s.xls' % file_name)
    worksheet = book.add_worksheet()
    row_num = len(skills)
    for i in xrange(0, row_num ):
        pos = 'A%s' %(i+1)
        worksheet.write_row(pos,skills[i])
    book.close()


skillContents = getSkillContents()
skills = search_skill(skillContents)
for s in skills:
    s = s.lower()
    pre_count = skill_count.get(s,0)
    skill_count[s] = pre_count+1
skill_count = sorted(skill_count.iteritems(),key=lambda d:d[1],reverse=True)
# print skill_count
save_excel(skill_count,'countSkill')
print 'success'
