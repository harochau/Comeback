# -*- coding: utf-8 -*-
"""My first portfolio project
Author: harochau@gmail.com

This module will be able to request data form onliner_baraholka, kufar and yandex_market, parse it and store in/load form local files
"""

#-----constants--------
a = 2/3
REGEX_DIGITS = '[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)'
YAN_MAR_SHOP_NAME = 'data-autotest-currency="б.p."><span>'
YAN_MAR_SHOP_NAME_LEN = len(YAN_MAR_SHOP_NAME)
ONLINER_BAR_PRICE = '<div class="price-primary">'
ONLINER_BAR_PRICE_LEN = len(ONLINER_BAR_PRICE)
KUF_MORETEXT_FIND = '<div class="k-PFvs-32e68">'
#-----constants--------

CODENAMES = {
    'g70':'NV47',
    }
PROCESSES = {
    'g70':'110nm'
}
MANUFACTURERS ={
    'g70':'TSMC'
}
SKU_TO_GPU ={
    '7800 GT':'g70'
}



def take_link_screenshot(link):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
    driver.set_window_size(S('Width'), S(
        'Height'))  # May need manual adjustment
    driver.find_element_by_tag_name('body').screenshot(link.split('/')[-1] + '.png')
    driver.quit()
class SKU:
    def __init__(self,name):
        self.name = name
        self.set_gpu()
        self.gpu_perf_index = 0.0
    def set_gpu(self):
        if self.name in SKU_TO_GPU.keys():
            tempgpu = GPU(SKU_TO_GPU[self.name])
            if tempgpu.is_good():
                self.gpu = tempgpu
            else:
                print('Missing data')
class GPU:
    def __init__(self,name):
        self.good = 1
        self.name = name
        if name in CODENAMES:
            self.codename = CODENAMES[name]
        else:
            self.good = 0
            print(f'No such name {name} in CODENAMES database')

        if name in PROCESSES:
            self.process = PROCESSES[name]

        else:
            self.good = 0
            print(f'No such name {name} in PROCESSES database')
        if name in MANUFACTURERS:
            self.manufacturer = MANUFACTURERS[name]

        else:
            self.good = 0
            print(f'No such name {name} in MANUFACTURERS database')
    def is_good(self):
        return self.good
class ONLINER_BAR_ITEM:
    def __init__(self, time_up, time_created, price,
                 author,city, text, moretext,
                 link, currency, buy_sell_type, shipping,author_link,
                 time_now,is_duplicate):
        self.time_up = time_up
        self.time_created = time_created
        self.price = price
        self.currency = currency
        self.author= author
        self.city = city
        self.text = text
        self.moretext = moretext
        self.link = link
        self.buy_sell_type = buy_sell_type
        self.shipping = shipping
        self.author_link = author_link
        self.time_now = time_now
        self.duplicate = is_duplicate
    def __eq__(self,other):
        return self.link == other.link
    def set_duplicate(self):
        self.duplicate = 'DUPLICATE'
    def print_to_console(self,looking_for = ''):
        if looking_for == '' or looking_for in self.text:
            print(self.link)
            print(self.text)
            print(self.moretext)
            print(self.city)
            print(self.shipping)
            print(self.author_link)
            print(self.author)
            print(self.price)
            print(self.time_created)
            print(self.time_up)
            print(self.buy_sell_type)
            print(self.time_now.strftime("%Y/%m/%d, %H:%M:%S"))
            #print(self.duplicate)
            print()

    def print_sell_to_console(self,looking_for = ''):
        if self.buy_sell_type == 'Sell' or self.buy_sell_type == 'Продажа':
            self.print_to_console(looking_for)

    def print_buy_to_console(self, looking_for = ''):
        if self.buy_sell_type == 'Buy':
            self.print_to_console(looking_for)


















g70= GPU('g70')
#print(g70.process)
card = SKU('7800 GT')
#print(card.gpu.codename)
YANDEX_BACKUP_STARTPATH = 'C:/backup_yandex_market'
FILE_FOR_FILE_AD = 'file://'
import pickle
import os, sys
import requests, pprint
from bs4 import BeautifulSoup
import re, time
from requests_file import FileAdapter #works as 16.12.2020
import datetime as dt, base64
from urllib.request import urlopen
from requests_html import HTMLSession #replacement for requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
def yandex_url_to_language(url):
    return url.split('/')[3]

time_now = dt.datetime.now()
time_now_filename = f'{time_now.year}_{time_now.month}_{time_now.day}_{time_now.hour}_{time_now.minute}'
URL = 'https://www.overclockers.ua/video/gpu/amd/radeon-rx-6900-xt/'
URL_3600 = 'https://market.yandex.by/product--protsessor-amd-ryzen-5-3600/508275153/offers?how=aprice&grhow=shop&onstock=1&local-offers-first=0'
URL_4650G = 'https://market.yandex.by/product--protsessor-amd-ryzen-5-pro-4650g/727392004/offers?grhow=shop&onstock=1&how=aprice&local-offers-first=0'
URL_3500X = 'https://market.yandex.by/product--protsessor-amd-ryzen-5-3500x/624160127/offers?grhow=shop&onstock=1&how=aprice&local-offers-first=0'
URL_5600X = 'https://market.yandex.by/product--protsessor-amd-ryzen-5-5600x/717093016/offers?track=tabs&onstock=1&grhow=shop&local-offers-first=0'

URL_LIST = []
URL_LIST.append(URL_3600)
URL_LIST.append(URL_4650G)
URL_LIST.append(URL_3500X)
URL_LIST.append(URL_5600X)

TYPE_SELL = 'ba-label-2'
TYPE_BUY = 'ba-label-3'
TYPE_EXCHANGE = 'ba-label-4'
TYPE_SERVICE = 'ba-label-5'
TYPE_RENT = 'ba-label-6'
TYPE_CLOSED = 'ba-label-7'
class Yandex_market_request:

    def __init__(self,url):
        self.url = url
        self.url_lang = yandex_url_to_language(url)

        self.page = requests.get(url)
        self.yandex_backup_path = YANDEX_BACKUP_STARTPATH + self.url_lang + '.txt'
        if 'Content-Length' in self.page.headers:  # only if error is returned
            print('Your IP is banned')
            global sleep_time_yandex
            sleep_time_yandex = 0
            yandex_backup_path = YANDEX_BACKUP_STARTPATH + self.url_lang + '.txt'

            if os.path.isfile(yandex_backup_path):
                s = requests.Session()
                s.mount(FILE_FOR_FILE_AD, FileAdapter())
                # absolute
                self.page = s.get(FILE_FOR_FILE_AD + '/' + self.yandex_backup_path)
                print('Backing up data from local file')
            else:
                print('No backup file exists!')

                raise SystemExit(1)



        else:
            print('New data recived')
            f = open(self.yandex_backup_path, 'wb')
            f.write(self.page.content)
            f.close()
    def parse_price(self):
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.split_soup = re.split('б.p.В', self.soup.text)
        for price_string in self.split_soup[:-1]:
            price = re.findall(REGEX_DIGITS, price_string[-10:])

            if len(price) > 1:
                print(f'{price[0]} б.р {price[1]} коп.')
            else:
                print(f'{price[0]} б.р 00 коп.')
    def parse_price_and_name(self):
        source_code_str = self.page.text
        shop_index = source_code_str.find('reviews-count"><a href=')
        source_code_str = source_code_str[shop_index:]
        shop_index = 0
        print(self.url_lang)
        while shop_index > -1:
            shop = source_code_str[shop_index:shop_index + 100]
            shop = shop.split('/')[1]

            price_index = source_code_str.find(YAN_MAR_SHOP_NAME, shop_index)
            price_string = source_code_str[price_index + YAN_MAR_SHOP_NAME_LEN:price_index + YAN_MAR_SHOP_NAME_LEN + 30]

            price_string = price_string.replace('</span>', ' ')
            price_string = price_string.replace('<span>', ' ')
            price_string = price_string.replace('<', ' ')

            price, currency = price_string.split()[0:2]

            print(f'{shop} {price} {currency}')
            shop_index = source_code_str.find('reviews-count"><a href=', shop_index + 1)
onliner_bar_gpu = 'https://baraholka.onliner.by/viewforum.php?f=286&start=0'
onliner_bar_сpu = 'https://baraholka.onliner.by/viewforum.php?f=285&start=0'
onliner_bar_pc = 'https://baraholka.onliner.by/viewforum.php?f=180&start=0'
kufar_gpu = 'https://www.kufar.by/listings?cat=16010&cct=11&rgn=7&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MX0%3D'

obi_list = []
class Onliner_baraholka_request:


    def __init__(self,url):
        self.url = url
        self.not_end = 1
        if self.url == onliner_bar_gpu:
            self.lang = 'Барахолка: Видеокарты'
        if self.url == onliner_bar_сpu:
            self.lang = 'Барахолка: Процессоры и материнские платы'
        if self.url == onliner_bar_pc:
            self.lang = 'Барахолка: Компьютеры и серверы'
        self.page = requests.get(url)
        self.page_counter = int(self.url.split('=')[2])
        self.link_paid_adv = self.page.text.split('<span class="img-va"><a href="')[1][1:56].split('"')[0]  # first adv on page
        print(self.link_paid_adv)
        self.recurring_count = 0
    def gpu_parse(self):
        source_code_str = self.page.text
        if '<span class="img-va"><a href="' in source_code_str:
            source_code_after_split = source_code_str.split('<span class="img-va"><a href="')
        else:
            print('Could not find advertisement')
            return 0


        for source_code_str_item in source_code_after_split[1:]:#split every advertisement
            #print(source_code_str_item)
            if True:#(TYPE_SELL in source_code_str_item): #if it is a "sell" adv
                #print(source_code_str_item)



                split_human =  source_code_str_item.split('>')
                #print(split_human)
                link = 'https://baraholka.onliner.by' + split_human[0][1:-1]
                if link == self.link_paid_adv: #check for recurring adv
                    #print(self.link_paid_adv+'Paid adv'+'\n'+link+'\n')

                    continue

                text = split_human[split_human.index('\n                                <h2 class="wraptxt"')+2][:-3]

                moretext = split_human[split_human.index('\n                                <h2 class="wraptxt"')+5][:-3]
                if moretext == '<':
                    moretext = '!NO_DESCRIPTION_VISIBLE!'
                city = split_human[split_human.index('\n                                                                            <strong')+1][:-8]



                if '\n                                                                                                            ' \
                   '<span class="baraholka-list__delivery"' in split_human:


                    shipping = split_human[split_human.index('\n                                                                                                            '
                                                     '<span class="baraholka-list__delivery"')+1].split('\n')[1].strip()
                else:
                    shipping = '!NO_SHIPPING_AVALIABLE!'
                start = source_code_str_item.find('https://profile.onliner.by/user/')
                end = source_code_str_item.find('</',start)

                author_link = source_code_str_item[start:end].split(">")[0][:-1]
                author = source_code_str_item[start:end].split(">")[1]

                if '\n                            <div class="price-primary"' in split_human:
                    price = split_human[split_human.index('\n                            <div class="price-primary"')+1].split('<')[0]
                else:
                    price = '!NO_PRICE_INFO!'
                time_created = split_human[split_human.index('\n                <div class="ba-topic-last-post-data" style="display:none"')+2].split('<')[0]
                time_up = split_human[split_human.index('<small class="tot-up"')+2].split('<')[0][1:]

                if TYPE_SELL in source_code_str_item:
                    if 'куплю' in text.lower() or 'куплю' in moretext.lower():
                        buy_sell_type = 'Buy'
                    else:
                        buy_sell_type = 'Sell'
                elif TYPE_BUY in source_code_str_item:
                    buy_sell_type = 'Buy'
                elif TYPE_EXCHANGE in source_code_str_item:

                    buy_sell_type = 'Exchange'
                elif TYPE_SERVICE in source_code_str_item:

                    buy_sell_type = 'Service'
                elif TYPE_RENT in source_code_str_item:
                    buy_sell_type = 'Rent'
                elif TYPE_CLOSED in source_code_str_item:
                    buy_sell_type = 'Closed'
                else:
                    print('Why ' + text)
                    print(source_code_str_item)
                    buy_sell_type = 'Sell'
                    time.sleep(5)




                # if 'куплю 'in text or 'куплю ' in moretext or 'Куплю ' in text or 'Куплю ' in moretext:
                #     buy_sell_type = 'Buy'
                # else:
                #     buy_sell_type = 'Sell'


                    #buy_sell_type = split_human[split_human.index('\n                            <div class="txt-i"')+1].split('"')[1]




                # print(link)
                # print(text)
                # print(moretext)
                # print(city)
                # print(shipping)
                # print(author_link)
                # print(author)
                # print(price)
                # print(time_created)
                # print(time_up)
                # print()

                obi_i = ONLINER_BAR_ITEM(time_up,time_created,price,author,city,text,moretext,link,'BYN',buy_sell_type, shipping, author_link, dt.datetime.now())
                obi_list.append(obi_i)
                #print(str(len(obi_list)))
                if self.page_counter - len(obi_list) > 5:
                    print('Last page reached\n')
                    return 0
                        #obi.print_sell_to_console()
                #obi_i.print_sell_to_console()
            else:
                print('Skipping buy ad')



        return 1
    def gpu_parse_all(self):
        while True:

            self.page_counter+=50

            self.next_url = self.url.split('=')[0]+'='+self.url.split('=')[1]+'='+str(self.page_counter)
            print(f'Processing next page, url is {self.next_url} (page {int(self.page_counter/50+1)})')



            self.page = requests.get(self.next_url)


            self.not_end = self.gpu_parse()
            if self.not_end == 0:
                break

class Kufar_request:
    def __init__(self,url):
        self.url = url
        self.next_url = url
        self.session = HTMLSession()
        #self.page = requests.get(self.url)
        #self.page_text = self.page.text
        b = (self.url.split('=')[-1])
        bb = str(b)
        bbb = bb[:-3]+'3'
        bc = base64.b64encode(b'{"t":"abs","f":true,"p":1}7')
        dec = base64.b64decode(bc)
        dec2 = str(base64.b64decode(bbb))
        #print(dec)
        #print(dec2)
        self.page_counter = int(dec2.split('"')[-1][1:-3])
        #self.page_counter = self.url.split('=')[-1].decode('UTF8')


    def parse(self):

        r = self.session.get(self.next_url)
        self.page_text = r.content.decode('utf-8')
        page_text = self.page_text

        if not '?rule=line_thumbs"},"title":"' in page_text:
            print('ERROR')
            print(len(page_text))
            return 1
        #print(len(page_text))
        text_split = page_text.split('?rule=line_thumbs"},"title":"')[1:]
        for ad_item in text_split:
            ad_item_split = ad_item.split('"')
            text = ad_item_split[0]
            price = ad_item_split[6]
            position = ad_item_split.index('updateDate')
            updated_last_time = ad_item_split[position+2]
            position = ad_item_split.index('address')
            city = ad_item_split[position+2]
            position = ad_item_split.index('name')
            author = ad_item_split[position + 4]
            position = ad_item_split.index('ad_link')
            ad_link = ad_item_split[position + 2]
            position = ad_item_split.index('Тип сделки')
            ad_type = ad_item_split[position + 4]
            position = ad_item_split.index('list_time')
            created_time = ad_item_split[position + 2]
            #r2 = self.session.get(ad_link)
            #ad_text = r2.content.decode('utf-8')


            moretext = self.moretext_reconnect(ad_link)
            if moretext == '="ru">':
                interval = 3
                print(ad_link +f' ERROR3: probably server timeout, trying to reconnect in {interval} seconds')
                #take_link_screenshot(ad_link)
                while moretext == '="ru">':
                    time.sleep(interval)
                    moretext = self.moretext_reconnect(ad_link)
                print('Reconnected')




            shipping = 'NO_SHIPPING_INFO'
            position = ad_item_split.index('account_id')

            author_link = 'https://www.kufar.by/user/'+ad_item_split[position + 1][1:-1]
            kr_obi_i = ONLINER_BAR_ITEM(updated_last_time,created_time,price,author,city,text,moretext,ad_link,'BYN',ad_type, shipping, author_link, dt.datetime.now(),'unique')

            if kr_obi_i in obi_list:
                #print('DUPLICATE')
                kr_obi_i.set_duplicate() #do not add ads that are already in the list
            else:
                obi_list.append(kr_obi_i)
    def parse_2_to_9(self):
        for page_counter_i in range(2,10):
            self.page_counter = page_counter_i
            t = f'{{"t":"abs","f":true,"p":{self.page_counter}}}7'

            t = bytes(t,'utf-8')

            self.url_add = str(base64.b64encode(t))


            self.next_url = self.url[:self.url.rfind('=')]+'='+ self.url_add[2:-3]+'0%3D'
            print(f'{self.next_url} page number {self.page_counter}')
            #self.page = requests.get(self.next_url)
            #self.page_text = self.page.text
            self.parse()
    def parse_last_9(self):
        for page_counter_i in range(9,0,-1):
            self.page_counter = page_counter_i
            t = f'{{"t":"abs","f":false,"p":{self.page_counter}}}'
            t = bytes(t, 'utf-8')
            self.url_add = str(base64.b64encode(t))
            self.next_url = self.url[:self.url.rfind('=')] + '=' + self.url_add[2:-1]
            print(f'{self.next_url} page number {self.page_counter} form last')
            #self.page = requests.get(self.next_url)
            #self.page = requests.get('https://www.kufar.by/listings?cat=16010&cct=11&rgn=7&cursor=eyJ0IjoicmVsIiwiYyI6W3sibiI6Imxpc3RfdGltZSIsInYiOjE2MDgxMjYxOTcwMDB9LHsibiI6ImFkX2lkIiwidiI6MTE1MzE4NzAxfV0sImYiOnRydWV9')

            #r = self.session.get(self.next_url)
            #print(r.content.decode('utf-8'))
            #self.page_text = r.content.decode('utf-8')
            #self.page = r.content
            #p = urlopen(self.next_url)
            #html_bytes = p.read()
            #h = html_bytes.decode("utf-8")
            #print(h)
            #time.sleep(2)
            #print(self.page)
            #time.sleep(2)
            self.parse()
    def parse_url(self, next_url):
        self.next_url = next_url

    def moretext_reconnect(link):
        ad_text = requests.get(link).text
        start_pos = ad_text.find(KUF_MORETEXT_FIND)
        end_pos = ad_text.find('<', start_pos + len(KUF_MORETEXT_FIND))
        moretext = ad_text[start_pos + len(KUF_MORETEXT_FIND):end_pos]
        return moretext








onliner_bar_link = onliner_bar_gpu
kufar_link = kufar_gpu
def launch_kufar_parse(kufar_link):
    kr1 = Kufar_request(kufar_link)
    kr1.parse()
    #kr1.parse_2_to_9()
    #kr1.parse_last_9()
    print(len(obi_list))
    file = open(time_now_filename + kufar_link.split('?')[-1] + '.txt', 'wb')
    static_file = open('lastfile.txt', 'w')
    static_file.write(time_now_filename + kufar_link.split('?')[-1] + '.txt')
    static_file.close()
    pickle.dump(obi_list, file)
    file.close()
launch_kufar_parse(kufar_link)

def launch_onliner_bar_parse(onliner_bar_link):

    cbr1 = Onliner_baraholka_request(onliner_bar_link)
    cbr1.gpu_parse()
    cbr1.gpu_parse_all()
    print(len(obi_list))
    file = open(time_now_filename + onliner_bar_link.split('?')[-1] + '.txt', 'wb')
    static_file = open('lastfile.txt','w')
    static_file.write(time_now_filename + onliner_bar_link.split('?')[-1] + '.txt')
    static_file.close()
    pickle.dump(obi_list, file)
    file.close()
#launch_onliner_bar_parse(onliner_bar_link)

def load_onliner_bar_from_file():
    static_file = open('lastfile.txt','r')
    last_file_path = static_file.read()


    file2 = open(last_file_path,'rb')
    obi_list_2 = pickle.load(file2)
    for obi_i in obi_list_2:

        obi_i.print_sell_to_console('')
load_onliner_bar_from_file()





sleep_time_yandex = 60
# ymr3 = Yandex_market_request(URL_3500X)
# ymr3.parse_price_and_name()
# print(f'\nSleeping for {sleep_time_yandex} seconds')
# time.sleep(sleep_time_yandex)
# ymr1 = Yandex_market_request(URL_3600)
# ymr1.parse_price_and_name()
# print(f'\nSleeping for {sleep_time_yandex} seconds')
# time.sleep(sleep_time_yandex)
# ymr2 = Yandex_market_request(URL_4650G)
# ymr2.parse_price_and_name()
# print(f'\nSleeping for {sleep_time_yandex} seconds')
# time.sleep(sleep_time_yandex)
count = 0

# while True:
#
#     ymr_inf = Yandex_market_request(URL_LIST[count])
#
#     ymr_inf.parse_price_and_name()
#     print(f'\nSleeping for {sleep_time_yandex} seconds')
#     time.sleep(sleep_time_yandex)
#     count+=1


session = HTMLSession()
#r = session.get('https://catalog.onliner.by/cpu/amd/rzn55600x/prices')
page_minus_9 = 'https://www.kufar.by/listings?cat=16010&cct=11&rgn=7&cursor=eyJ0IjoiYWJzIiwiZiI6ZmFsc2UsInAiOjl9'
r = session.get(page_minus_9)

#r2 = session.get('https://www.kufar.by/listings?cat=16010&cct=11&rgn=7&cursor=eyJ0IjoiYWJzIiwiZiI6ZmFsc2UsInAiOjh9')
#r.html.find
'''
if not '?rule=line_thumbs"},"title":"' in r.content.decode('utf-8'):
    print('ERROR2')
else:
    qr1 = Kufar_request(kufar_gpu)
    reverse_urls =[]
    for page_counter_i in range(9, 0, -1):

        t = f'{{"t":"abs","f":false,"p":{page_counter_i}}}'
        t = bytes(t, 'utf-8')
        url_add = str(base64.b64encode(t))
        next_url = kufar_gpu[:kufar_gpu.rfind('=')] + '=' + url_add[2:-1du]
        print(f'{next_url} page number {page_counter_i} form last')
        reverse_urls.append(next_url)
    qr1.parse_url(next_url)
    qr1.parse()
'''

#print(r2.content.decode('utf-8'))
#r.html.render()


#table = r.html.find('table', first=True)
#from IPython.core.display import display_html
#display_html(table.html, raw=True)
#print(r.html.search('1445,49 р.'))









print('\n')


