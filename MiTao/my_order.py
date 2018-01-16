#coding:utf-8
import urllib
import urllib2
import cookielib
import re
import webbrowser
import sys
import os
import time
import json
# import tool
import mongodb_api
# from selenium import webdriver

# browser = webdriver.Chrome()
# wait = WebDriverWait(browser, 10)

# f = open(r'.\article4.txt','w')
reload(sys)
sys.setdefaultencoding('utf-8')
class TaoBao:

    def __init__(self):
        self.loginURL = "https://login.taobao.com/member/login.jhtml"
        self.proxyURL = "http://120.193.146.97:843"
        # 通过st实现登录的URL
        self.st_url = 'https://login.taobao.com/member/vst.htm?st={st}'
        #我的已买宝贝
        self.bought_url = 'https://trade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a1z09.2.1997525045.2.34c9604098yr5t'
        self.loginHeaders =  {
            'Host':'login.taobao.com',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Referer' : 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection' : 'Keep-Alive'
        }
        self.username = u'筱陌时光被荒废'

        self.ua = '106#+YoBcBBEB1tBGQKaBBBBBpZb54Efo05u94/ZyTpcGUzudiGY949YDCpYk4PUoCKs9u8VyTog7VEfdiBPGUNYs05R9ULu/JkKBBgbylZwUUu0D8SKBB5byltqmNC/BCBEylmi4gO0ylmbyl6v3p0b1lmbyxzz0q4wylmUPgO0yqebyl6v3pVY12LKBlYh6Dm51E2XtQDc7hcUPZpzAm9s2qAepuO93Uy/SdbeqOZYkNcUPZpzAm9a63a4AjDo9fCxH2L09fGYm4uhQQ+UKfKUd8uSDhpmtC5Tr+ToBQphGhHajYTHpuOM2cAtDhpmtC9EFxzAdDYg7URYTO1YWXbOncUdAet0vjiIyJ97vZGO7URYTOTSBjba63a4AjDpdfi1cyi4+ZLutPXINpOICudzv8avZV+97NJhckD0nZdUdBuAaeiopm2NqvapKjB57mZ1FxQm5TBj+feuOZGbBTtfm6lnBP9AdW0UaJQuoLZYtQ8HjDGYkotuGHmopuQDdf1Mc527lLZYtQ8qBCBFSkhg4Qs3IDqHUFzE5VSketb6uVpg9DtFwyMM6N0Eqms1v5xpXCgHUy81aXGA3S71ZcM8ZCb2lub1l7kKBB7byIDv3pD+BCBoBBmWOesKBBfBQCBBnboBK2XKopXOBCBDtcmi4SjeKCCmYzK/Vfvnfo/+ajwOBCBDtRmi4SjmKCCmYz0cfU7GUzb+ajwOBCBDtcmi4Rx9KCCmYz0cfU7GUzb+ajwOBCBDtRmi4Ri9KCCmYz0cfU7GUzb+ajwOBCBDtcmi4Ri2KCCmYz0cfU7GUzb+ajwOBCBDtRmi4Ri2QSqoe5dRDf4omDQGP4h5BCB5tcmi4gjLKCDoBFxMWf7kRtMkLDo++DgkRmsKBBfBQCBBNCoBAVlb1ZzzxUDpKB3a7TLNRkung+pKXf02Rkb1BCBoQ2oBB+LKBKTRylDv369YKCCmaNJ5+SRGUzUZCCLTfkRklCoBK2XKBBX5BCB5tcmi4gjO1bDoBFxMWf7kRtMkLDo++DgkR+LKBKTRylDv36oKKCCmaNJ5+SRGUzUZCCLTfkRkNCoBAVlb1ZzzEWspKB3a7TLNRkung+pKXf02RkU5BCB5tcmi4gjQrCDoBFxMWf7kRtMkLDo++DgkR+LKBKTRylDv36k7KCCmaNJ5+SRGUzUZCCLTfkRkNCoBAVlb1ZzzELkpKB3a7TLNRkung+pKXf02RkU5BCB5tcmi4gj/BbDoBFxMWf7kRtMkLDo++DgkR+LKBKTRylDv36RuKCCmaNJ5+SRGUzUZCCLTfkRkNCoBAVlb1ZzzrRLpKB3a7TLNRkung+pKXf02RkU5BCB5tcmi4gjMGbDoBFxMWf7kRtMkLDo++DgkR+LKBKTRylDv36z/KCCmaNJ5+SRGUzUZCCLTfkRkrboBKlBb1ZziBCB+ylAa4yp0knmAGCoBmuoYHKcQ0eXbiz6aWptPfRDKBB1YkvbqF0Dby7fXaTOV+sSiBCBVtR4S4ci0kl4pQaxGeednfQuoQV1klkQiBCBVtR4S4z+0klpvQaxGeednfQuoQV1klkQJBCB8tR4S4zp0ylBbkvLvtQroe9OnPAxr2DQGfSQ1BCBoQ2oBBB=='
        self.password2 = '05ced684113878097fcfa1f22ed00e8c1f6cb38e802fea8f9427a40fcf43b88efa4fd8aa442fb900c13028d5e3b3a05fd9e73d93aeacccd8d3ec6039eb8c0dd796e5a6c912293f63d1e392cbcae50bce8ae756d82ceb79bc9bfa26ff0f8b659951b6b23455dbc4ffd90375c2915d3d2c6f61bbd2a7f164b4ededdcc4af09732c'
        self.post = post = {
            'TPL_username':self.username.encode('gbk'),
            'TPL_password':'',
            'ncoSig':'',
            'ncoSessionid':'',
            'ncoToken':'babd645923d4e681e169e84f859d5bbf67366fbf',
            'slideCodeShow':'false',
            'useMobile':'false',
            'lang':'zh_CN',
            'loginsite':'0',
            'newlogin':'0',
            'TPL_redirect_url':'https://www.taobao.com/',
            'from':'tb',
            'fc':'default',
            'style':'default',
            'css_style':'',
            'keyLogin':'false',
            'qrLogin':'true',
            'newMini':'false',
            'newMini2':'false',
            'tid':'',
            'loginType':'3',
            'minititle':'',
            'minipara':'',
            'pstrong':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'sub_jump':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':'68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D613231626F2E323031372E3735343839343433372E362E36623963386165344D586F4B796226663D746F70266F75743D7472756526726564697265637455524C3D68747470732533412532462532467777772E74616F62616F2E636F6D253246',
            'from_encoding':'',
            'sub':'',
            'TPL_password_2':self.password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh-CN',
            'sr':'1920*1080',
            'osVer':'windows|6.1',
            'naviVer':'chrome|61.031631',
            'osACN':'Mozilla',
            'osAV':'5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'osPF':'Win32',
            'miserHardInfo':'',
            'appkey':'',
            'nickLoginLink':'',
            'mobileLoginLink':'https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/&useMobile=true',
            'showAssistantLink':'',
            'um_token':'HV01PAAZ0b8bda7ada6b37fc5a5b0027003b1068',
            'ua':self.ua,
        }
        self.postData = urllib.urlencode(self.post)
        self.proxy = urllib2.ProxyHandler({'http':self.proxyURL}) 
        self.cookie = cookielib.LWPCookieJar()
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        #设置登录时用到的opener，它的open方法相当于urllib2.urlopen
        self.opener = urllib2.build_opener(self.cookieHandler,self.proxy,urllib2.HTTPHandler)
        self.newCookie = cookielib.CookieJar()
        self.newOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.newCookie))
        # self.tool = tool.Tool()

        #得到是否需要输入验证码，这次请求的相应有时会不同，有时需要验证有时不需要
    def needIdenCode(self):
        #第一次登录获取验证码尝试，构建request
        request = urllib2.Request(self.loginURL,self.postData,self.loginHeaders)
        #得到第一次登录尝试的相应
        response = self.opener.open(request)
        #获取其中的内容
        content = response.read().decode('gbk')
        # f.writelines(u'内容:%s%s\n'%(str(content),os.linesep))
        #获取状态吗
        status = response.getcode()
        #状态码为200，获取成功
        if status == 200:
            print u"获取请求成功"
            #\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801这六个字是请输入验证码的utf-8编码
            pattern = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801',re.S)
            result = re.search(pattern,content)

            pattern = re.compile('<script src=\"(.*)\"><\/script>')
            match = pattern.findall(content)
            print match
            #如果找到该字符，代表需要输入验证码
            if result:
                print u"此次安全验证异常，您需要输入验证码"
                return content
            #否则不需要
            elif match:
                print 'coming match'
                request = urllib2.Request(match[0])
                response = self.opener.open(request)
                content = response.read().decode('gbk')
                
                pattern = re.compile('{"st":"(.*?)"}')
                match = pattern.findall(content)
                # f.writelines(u'内容:%s%s\n'%(str(match),os.linesep))
                print match
                self.login_by_st(match[0])
                return False
            else:
                print u"此次安全验证通过，您这次不需要输入验证码"
                # print content
                return False
        else:
            print u"获取请求失败"


    #得到验证码图片
    def getIdenCode(self,page):
        #得到验证码的图片
        pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"',re.S)
        #匹配的结果
        matchResult = re.search(pattern,page)
        #已经匹配得到内容，并且验证码图片链接不为空
        if matchResult and matchResult.group(1):
            print matchResult.group(1)
            return matchResult.group(1)
        else:
            print u"没有找到验证码内容"
            return False

    #获得已买到的宝贝页面
    # def getGoodsPage(self):
    #     goodsURL = 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm'
    #     response = self.newOpener.open(goodsURL)
    #     page =  response.read().decode('gbk')
    #     # f.writelines(u'内容:%s%s\n'%(str(page),os.linesep))

    #     return page


    # 区别是并不需要传递user_name字段，只需要st就可以了
    def login_by_st(self, st):
        st_url = self.st_url.format(st=st)
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Host':'login.taobao.com',
            'Connection' : 'Keep-Alive'
        }
        request = urllib2.Request(st_url, headers=self.loginHeaders)
        response = self.newOpener.open(request)
        content =  response.read().decode('gbk')

        #检测结果，看是否登录成功
        pattern = re.compile('top.location.href = "(.*?)"', re.S)
        match = re.search(pattern, content)
        match = pattern.findall(content)
        # f.writelines(u'内容:%s%s\n'%(str(content),os.linesep))

        if match:
            
            url = match[0].split('?')[0]
            # url = re.sub(pattern, repl, string)
            print(u'登录网址成功',match[0],url)
            self.init_goods(url)
            return True
        else:
            print(u'登录失败')
            return False

    #获得已买到的宝贝页面
    def init_goods(self,url):
        orderAPI = mongodb_api.orderAPI()
        orderAPI.remove_all_order()
        # request = urllib2.Request(url, headers=self.loginHeaders)
        print self.bought_url
        response = self.newOpener.open(self.bought_url)
        content =  response.read().decode('gbk').decode('raw_unicode_escape')
        # pattern = re.compile(r'<table.*?class="bought-table-mod__table___mnLl_ bought-wrapper-mod__table___3xFFM".*?<div class="ml-mod__container___dVhLg production-mod__production___2ucc4 suborder-mod__production___3WebF".*?<a.*?class="production-mod__pic___fLXn7".*?<img src="(.*?)".*?</a>.*?</div>.*?</table>',re.S)
        content = content.replace('\\','')
        pattern = re.compile(r'var data = JSON.parse(.*?)</script>',re.S)
        items = re.findall(pattern,content)
        # print 'items',items
        nowTimes = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) 
        # f.write('时间:{}\n\n'.format(content),);
        i = items[0]
        i.encode('utf-8')
        i = i[2:-4]
        i = json.loads(i)
        i = i['mainOrders']
        for item in i:
            i = json.dumps(i)
            # print item
            for index in range(len(item['subOrders'])):
                title = item['subOrders'][index]['itemInfo']['title']
                # print index,len(item['subOrders']),item['subOrders'][index]['itemInfo']['title']
                flag = orderAPI.is_exist(title)
                if flag:
                    orderAPI.update_order_info(title,flag)
                if item['subOrders'][index]['itemInfo']['title'] == u'保险服务':
                    continue
                data = dict(buyDate=item['orderInfo']['createDay'],seller=item['seller'],itemInfo=item['subOrders'][index]['itemInfo'],title=title,priceInfo=item['subOrders'][index]['priceInfo'],bought_count = 1)
                orderAPI.add_order_info(data)
                # f.writelines('%s%s\n'%(str(data).decode('gbk').decode('raw_unicode_escape').replace('u',''),os.linesep))
        # f.close()



    #程序运行主干
    def main(self):
        #是否需要验证码，是则得到页面内容，不是则返回False
        needResult = self.needIdenCode()
        if not needResult == False:
            print u"您需要手动输入验证码"
            idenCode = self.getIdenCode(needResult)
            #得到了验证码的链接
            if not idenCode == False:
                print u"验证码获取成功"
                print u"请在浏览器中输入您看到的验证码"
                webbrowser.open_new_tab(idenCode)
            #验证码链接为空，无效验证码
            else:
                print u"验证码获取失败，请重试"
        else:
            # data = self.getGoodsPage()
            print u"不需要输入验证码"
            
            # f.writelines(u'内容:%s%s\n'%(str(data),os.linesep))
            # print data



taobao = TaoBao()
taobao.main()
