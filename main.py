import requests
from lxml import etree  # xpath
from download import Download, jdt  # 下载模块，用的是以前造的轮子
import re  # 正则
import os
from log1 import l  # 日志模块，可无视


def FindPageUrl(gpdm):
    '''
    获取主页面
    :param gpdm: 股票代码
    :return:主页面链接
    '''
    response = mySession.get(searchURL + gpdm)

    html = etree.HTML(response.content.decode("GBK"))

    result = html.xpath('//a[@target="_blank"]')

    pageUrl = ""
    for data in result:
        if data.text == "明细":
            pageUrl = data.attrib['href']
            break
    return pageUrl


def FindExcelUrl(pageUrl):
    '''
    获取excel文件的下载链接
    :param pageUrl:
    :return: None
    '''
    response = mySession.get(pageUrl)
    html = etree.HTML(response.content.decode("GBK"))
    result = html.xpath('//a')
    companyName = html.xpath('//*[@id="toolbar"]/div[1]/h1/a')[0].text
    if not os.path.isdir(f'./{companyName}'):
        os.makedirs(f'./{companyName}')
    for data in result:
        if data.text == "资产负债表":
            zcfzbUrl = data.attrib['href']
            zcfzStockid = re.findall("stockid/(.*?)/ctrl", zcfzbUrl)[0]
            stockId = zcfzStockid
            continue
        # if data.text == "现金流量表":
        #     xjllbUrl = data.attrib['href']
        #     xjllStockid=re.findall("stockid/(.*?)/ctrl")[0]
        #     continue
        # if data.text == "利润表":
        #     lrbUrl = data.attrib['href']
        #     lrStockid=re.findall("stockid/(.*?)/ctrl")[0]
        #     continue
    downloadList[
        f"./{companyName}/资产负债表.xls"] = f"http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/{stockId}/ctrl/all.phtml"
    downloadList[
        f"./{companyName}/利润表.xls"] = f"http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/{stockId}/ctrl/all.phtml"
    downloadList[
        f"./{companyName}/现金流量表.xls"] = f"http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/{stockId}/ctrl/all.phtml"

    # print(zcfzbUrl)


def DownLoadAll():
    '''
    下载所有文件
    :return:
    '''
    total = len(downloadList)
    current = 0
    failed = 0
    l.info(f"正在下载共计{total}个文件。。。")
    for name, url in downloadList.items():
        try:
            Download(url, name)
            current = current + 1
        except Exception:
            failed = failed + 1
            l.warn(f"文件{name}下载失败！！！")
        jdt(current, total)


if __name__ == '__main__':
    # cookie = 'UOR=,finance.sina.com.cn,; SINAGLOBAL=112.53.136.40_1624621190.590834; Apache=112.53.136.40_1624621190.590835; MONEY-FINANCE-SINA-COM-CN-WEB5=; ULV=1624621383616:2:2:2:112.53.136.40_1624621190.590835:1624621190743; SUB=_2A25N0aQzDeRhGeFP41MV8C_FyjiIHXVuppL7rDV_PUNbm9ANLVqmkW9NQRJrjHroL2gsPHbuM70iPFYJTuMacKy1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWhZeU8jK9qVj5keqA1_Yba5JpX5KzhUgL.FoMp1h2Xeh24eKB2dJLoI7DKUcHXwHvhdNiL; ALF=1656162275; _s_upa=20'
    # gpdms = ['sz002594']
    a = input("请输入股票代码，多个请用','分割:\n")
    gpdms = a.split(',')
    l.info(f"共{len(gpdms)}个公司")
    searchURL = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/scbhz/index.phtml?symbol="

    mySession = requests.session()
    mySession.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
        # , 'cookie': cookie
    }
    downloadList = {}
    num = 0
    l.info("初始化完成！")
    for gpdm in gpdms:
        num += 1
        l.info(f"正在处理第{num}个。。。")
        pageUrl = FindPageUrl(gpdm)
        print(pageUrl)
        FindExcelUrl(pageUrl)
    DownLoadAll()
    # print(pageUrl)
    l.info("程序执行完毕。")
