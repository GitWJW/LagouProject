# coding=utf-8
__author__ = "WJW"

import urllib
import urllib2
import json
import xlsxwriter
import math

# 得到当前页的json内容,url为爬取的链接，page_num是爬取网站的第几页，keyword是需要爬取的关键字
def get_page(url,page_num,keyword):

    page_hearders = {      # 模拟浏览器，封装头部hearder信息
                'Accept':'application/json, text/javascript, */*; q=0.01',
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'Host':'www.lagou.com',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                'Connection':'keep-alive',
                'X-Requested-With':'XMLHttpRequest'
                }

    if page_num==1:
        flag = 'true'
    else:
        flag = 'false'

    data = {        # Post请求的三个参数
        'first':flag,
        'kd':keyword,
        'pn':page_num
    }


    page_data = urllib.urlencode(data)
    request = urllib2.Request(url,headers=page_hearders)
    file = urllib2.urlopen(request,data=page_data.encode('utf-8'))
    page_contents = file.read().decode('utf-8')
    file.close()
    return page_contents


# 得到当前页相应标签的内容,page_content是爬取的网站内容，tag是需要爬取的标签
def get_real_info(page_content,tag):

    data = json.loads(page_content)
    jdata = data['content']['positionResult']['result']
    ls = []         # 把我们需要的数据处理到list里,list里面封装的是字典类型数据
    for jd in jdata:
        company = {}
        for t in tag:
            if 'companyLabelList' == t:
                if jd[t]:
                    company[t] = ','.join(jd[t])
                else:
                    company[t] = 'no label'
            elif 'positionAdvantage' == t:
                if jd[t]:
                    company[t] = jd[t]
                else:
                    company[t] = 'no advantage'
            else:
                company[t] = jd[t]
        ls.append(company)
    return ls


# 保存所有数据的信息到Excel中,all_info是我们需要保存的数据,file_name是需要保存的文件名
def save_in_excel(all_info,file_name):

    # 这里我们默认保存到桌面
    book = xlsxwriter.Workbook(r'C:\Users\Administrator\Desktop\%s.xls' % file_name)
    worksheet = book.add_worksheet()
    row_num = len(all_info)
    for i in xrange(1,row_num+2):
        if i==1:
            tag_pos = 'A1'
            worksheet.write_row(tag_pos,all_info[0].keys())
        else:
            con_pos = 'A%s'%i
            content = all_info[i-2].values()
            worksheet.write_row(con_pos,content)
    book.close()

# 得到总共多少页
def get_totalPages(page):
    data = json.loads(page)
    totalCount = data['content']['positionResult']['totalCount']
    totalPage = math.ceil(totalCount/15.0)
    return totalPage


if __name__ == '__main__':
    url = 'http://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&city=全国'
    tag = ['companyFullName', 'city', 'companySize', 'education', 'financeStage', 'industryField',
           'jobNature','positionAdvantage','positionName','salary','workYear','positionId','companyLabelList']
    totalPages = get_totalPages(get_page(url,1,'数据挖掘'))
    allinfo = []

    for x in xrange(1,totalPages):
        pageinfo = get_page(url,x,'数据挖掘')
        info = get_real_info(pageinfo,tag)
        allinfo.extend(info)
        print '爬取成功第%s页'%x

    save_in_excel(allinfo,'lagouInfo')

    print '抓取完毕'