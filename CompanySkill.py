#coding='utf-8'

import urllib2
from bs4 import BeautifulSoup
import re


fs = open('/home/wjw/pythonProject/lagouProject/CompanyId.txt','r')
contents = fs.read()
fs.close()

ls = contents.splitlines()
addr = ['http://www.lagou.com/jobs/%s.html' %l for l in ls]

# 得到相应链接下的页面信息
def get_page(url):

    page_hearders = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Host':'www.lagou.com',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                'Connection':'keep-alive'
                }

        
    request = urllib2.Request(url,headers=page_hearders)
    file = urllib2.urlopen(request)
    page_contents = file.read().decode('utf-8')
    file.close()
    return page_contents

# 提取页面信息里面的岗位信息
def get_realinfo(pageContent):
    
    if pageContent:
        soup = BeautifulSoup(pageContent, 'lxml')
        job_description = soup.select('dd[class="job_bt"]')
        job_description = str(job_description[0])
        rule = re.compile(r'<[^>]+>')
        result = rule.sub('', job_description)
        return result
    else:
        return None

# 找到所有的技能信息		
def search_skill(realinfo):
    if realinfo:
        rule = re.compile(r'[a-zA-z]+')
        skills = rule.findall(realinfo)
        return skills    
    else:
        return None

# 将统计后的技能信息保存在Excel
def save_in_txt(all_info,file_name):
    
    fs = open(r'/home/wjw/%s.txt' %file_name,'w')
    for info in all_info:
        fs.write(str(info)+'\n')
    fs.close()


for a in xrange(0,len(addr)):
    print addr[a]
    try:
        pageContent = get_page(addr[a])
    except Exception as e:
        pageContent = None
        print 'fail %s' %addr[a]
        continue
    realinfo = get_realinfo(pageContent)
    skills = search_skill(realinfo)  
    for s in skills:
        s = s.lower()
        pre_count = skill_dict.get(s,0)
        skill_dict[s] = pre_count+1 
skill_dict = sorted(skill_dict.iteritems(),key=lambda d:d[1],reverse=True)
print skill_dict
save_in_txt(skill_dict,'skills')
print 'success'




