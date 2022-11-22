import requests
from bs4 import BeautifulSoup
from datetime import date

def is_valid_date(datestr):
    try:
        date.fromisoformat(datestr)
    except:
        return False
    else:
        year, month, day = datestr.split("-")
        return date.today() >= date(int(year), int(month), int(day))

def get_exchange_rate(input_date):
    html = f"https://rate.bot.com.tw/xrt/all/{input_date}"
    response = requests.get(html)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find_all("tr")
    table = table[2:]
    rate_title = ["本行現金買入", "本行現金賣出", "本行即期買入", "本行即期賣出"]
    exchange_rate_dict = {}
    for col in table:
        rates_dict = {}
        currency = col.find("div", class_="visible-phone")
        if currency == None:
            break
        currency = currency.text.strip()
        name_zhtw, name_en = currency.split(" ")
        name_en = name_en[1:4]
        rates_dict.setdefault("幣別", name_en)
        rates = col.find_all("td")[1:5]
        for index, text in enumerate(rates):
            rate = None if "-" == text.text.strip() else float(text.text.strip())
            rates_dict.setdefault(rate_title[index], rate)
        exchange_rate_dict.setdefault(name_zhtw, rates_dict)
    return exchange_rate_dict

def main():
    input_date = input("輸入想查詢的日期，請以'-'作為分隔，若為個位數日期須補齊2位數 e.g.2022-01-05\n \
              若不符格式則跳出查詢\n")
    input_date = input_date if is_valid_date(input_date) else None
    if input_date == None:
        print("錯誤日期格式或未來期別")
        return
    print(f'查詢日期為{input_date}')
    exchange_rate_dict = get_exchange_rate(input_date=input_date)
    if not(exchange_rate_dict):
        print("選擇日期為假日")
        return
    input_currency = input("輸入幣別:")
    input_exchange_type = input("輸入兌換方式:")
    rate = exchange_rate_dict.get(input_currency).get(input_exchange_type)
    print(rate)

if __name__ == '__main__':
    main()