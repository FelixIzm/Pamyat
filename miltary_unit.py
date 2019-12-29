import requests, hashlib, base64, json, pprint
import urllib.parse 
from string import Template

cookies = {}
headers={}

str_00 = 'bda88568a54f922fcdfc6dbf940e5d00'
str_0b = '56105c9ab348522591eea18fbe4d080b'
str_PNSESSIONID = 'PNSESSIONID'
#military_unit = ''

#pprint.pprint(json.loads(data_))
#exit(0)

#####################################        
def parse_file (name_file):
    dict_ = {}
    f = open(name_file, 'r')
    s = f.read()
    dict_={}
    list_ = s.splitlines()
    for item in list_:
        items = item.split(":")
        dict_[items[0]] = items[1].lstrip() 
    return dict_
#####################################        
def parse_json_file(json_file):
    with open(json_file) as json_file:
        return json.load(json_file)
#####################################        
def make_str_cookie(cookies):
    str_cook = ''
    for key, value in cookies.items():
        str_cook += '{0}={1};'.format(key,value)
    return str_cook
#####################################        


headers = parse_file('mu_header1.txt')
cookies = parse_file('mu_cookie1.txt')
url = 'https://pamyat-naroda.ru/'
##############################################
#    Первый запрос - получаем 307 статус     #
##############################################
res1 = requests.get(url, allow_redirects=False)
if(res1.status_code==307):
    print('*********************')
    print(res1.status_code)
    #for item in res.cookies.items():
    #    print(item)
    print(res1.cookies[str_00])
    # Получили переменные из кук
    cookie_PNSESSIONID = res1.cookies['PNSESSIONID']
    cookie_00 = res1.cookies[str_00]
    cookie_0b = res1.cookies[str_0b]
    #####################################################
    # готовим 2-й запрос, посылаем с получанными куками #
    #####################################################
    cookies = {}
    cookies[str_00]=cookie_00
    cookies[str_0b]=cookie_0b
    cookies[str_PNSESSIONID] = cookie_PNSESSIONID
    cookies['BITRIX_PN_DATALINE_LNG'] = 'ru'
    str_cook = ''
    #for key, value in cookies.items():
    #    str_cook += '{0}={1};'.format(key,value)
    print(str_cook)

    headers = parse_file('mu_header2.txt')
    headers['Cookie'] = str_cook
    ############## 2-й запрос #############
    res2 = requests.get(url,cookies=cookies,headers=headers, allow_redirects=True)
    #######################################
    if(res2.status_code==200):
        print('*********  2  **********')
        print(res2.status_code)
        print(res2.cookies[str_00])
        #pprint.pprint(res1.cookies)
        #for item in res2.cookies.items():
        #    print(item)
        
        cookies = parse_json_file('mu_cookie3.txt')
        cookies[str_00] = res2.cookies[str_00]
        cookies[str_0b] = res1.cookies[str_0b]
        cookies[str_PNSESSIONID] = res1.cookies[str_PNSESSIONID]
        cookies['r'] = res1.cookies[str_0b]
        
        headers = parse_file('mu_header3.txt')
        headers['Cookie'] = make_str_cookie(cookies)
        headers['Content-Type'] = 'application/json'
        
        ############## 3-й запрос #############
        url3 = 'https://pamyat-naroda.ru/documents/'
        res3 = requests.get(url3,headers=headers,cookies=cookies)
        print("*********  3  **********")
        print(res3.status_code)
        print(res3.cookies[str_00])
        #for item in res3.cookies.items():
        #    print(item)
        ############## 4-й запрос #############
        headers=parse_file('mu_header4.txt')

        bs = res3.cookies[str_00]
        bs += "=" * ((4 - len(res3.cookies[str_00]) % 4) % 4)
        bs = base64.b64decode(bs).decode()
        a_bs = bs.split('XXXXXX')[0]
        b_bs = bs.split('XXXXXX')[1].split('YYYYYY')[0]
        print(a_bs)
        print(b_bs)
        print('*********  4  ************')
        para1 = urllib.parse.quote('Боевые донесения, оперсводки')
        para2 = urllib.parse.quote('Боевые приказы и распоряжения')
        para3 = urllib.parse.quote('Отчеты о боевых действиях')
        para4 = urllib.parse.quote('Переговоры')
        para5 = urllib.parse.quote('Журналы боевых действий')
        para6 = urllib.parse.quote('Директивы и указания')
        para7 = urllib.parse.quote('Приказы')
        para8 = urllib.parse.quote('Постановления')
        para9 = urllib.parse.quote('Доклады')
        para10 = urllib.parse.quote('Рапорты')
        para11 = urllib.parse.quote('Разведывательные бюллетени и донесения')
        para12 = urllib.parse.quote('Сведения')
        para13 = urllib.parse.quote('Планы')
        para14 = urllib.parse.quote('Планы операций')
        para15 = urllib.parse.quote('Карты')
        para16 = urllib.parse.quote('Схемы')
        para17 = urllib.parse.quote('Справки')
        para18 = urllib.parse.quote('Прочие документы')
        data_ = Template('{"query":{"bool":{"should":[{"bool":{"should":[{"match_phrase":{"document_type":"${para1}"}},{"match_phrase":{"document_type":"${para2}"}},{"match_phrase":{"document_type":"${para3}"}},        {"match_phrase":{"document_type":"${para4}"}},{"match_phrase":{"document_type":"${para5}"}},{"match_phrase":{"document_type":"${para6}"}},{"match_phrase":        {"document_type":"${para7}"}},{"match_phrase":{"document_type":"${para8}"}},{"match_phrase":{"document_type":"${para9}"}},{"match_phrase":        {"document_type":"${para10}"}},{"match_phrase":{"document_type":"${para11}"}},{"match_phrase":{"document_type":"${para12}"}},        {"match_phrase":{"document_type":"${para13}"}},{"match_phrase":{"document_type":"${para14}"}},        {"match_phrase":{"document_type":"${para15}"}},{"match_phrase":{"document_type":"${para16}"}},{"match_phrase":{"document_type":"${para17}"}},        {"match_phrase":{"document_type":"${para18}"}}]}},{"bool":{"should":[{"bool":{"must":[{"range":{"date_from":{"lte":"${finish_date}"}}},{"range":{"date_to":{"gte":"${start_date}"}}}],"boost":3}},{"bool":{"must":[{"range":{"document_date_b":{"lte":"${finish_date}"}}},{"range":{"document_date_f":{"gte":"${start_date}"}}}],"boost":7}}]}},{"bool":{"should":[{"match_phrase":{"authors_list.keyword":{"query":"${military_unit}","boost":50}}},{"match":{"document_name":{"query":"${military_unit}","type":"phrase","boost":30}}},{"match":{"authors":{"query":"${military_unit}","type":"phrase","boost":20}}},{"match":{"army_unit_label.division":{"query":"${military_unit}","type":"phrase","boost":10}}},{"nested":{"path":"page_magazine","query":{"bool":{"must":[{"match":{"page_magazine.podrs":{"query":"${military_unit}","type":"phrase"}}},{"range":{"page_magazine.date_from":{"lte":"${finish_date}"}}},{"range":{"page_magazine.date_to":{"gte":"${start_date}"}}}]}},"boost":4}}]}}],"minimum_should_match":3}},"_source":["id","document_type","document_number","document_date_b","document_date_f","document_name","archive","fond","opis","delo","date_from","date_to","authors","geo_names","operation_name","secr","image_path","delo_id","deal_type","operation_name"],"size":10,"from":0}')
        data_ = data_.safe_substitute(para1 = para1,para2 = para2,para3 = para3,para4 = para4,para5 = para5,para6 = para6,para7 = para7,para8 = para8,para9 = para9,para10 = para10,para11 = para11,para12 = para12,para13 = para13,para14 = para14,para15 = para15,para16 = para16,para17 = para17,para18 = para18,start_date='1945-1-1',finish_date='1945-5-31', military_unit=urllib.parse.quote('147 сд'))
        #data_ = urllib.parse.quote(data_)
        #print(data_)

        url4 = 'https://cdn.pamyat-naroda.ru/data/'+a_bs+'/'+b_bs+'/pamyat/document,map,magazine/_search'
        print(url4)
        res4 = requests.post(url4,data=json.dumps(data_),headers=headers)
        print(res4.text)

        exit(0)



