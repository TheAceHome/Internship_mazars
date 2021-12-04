import pandas as pd
from finvizfinance.quote import finvizfinance
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import numpy as np


def parse_html(html_source,n,ticker):
    try:
        df = pd.read_html(html_source)
        company_type = df[6][0].values[-1].split(' ')[0].lower()
        print(company_type)
        df[8].to_csv('data.csv', index=False)
        get_comp_mean(n, company_type,ticker)
    except:
        print('wrong company')
        return False


def get_comp_mean(n,company_type,ticker):
    try:
        i=1
        competitors=[]
        while n>=i:
            url = 'https://finviz.com/screener.ashx?v=111&f=sec_'+company_type+'&o=-marketcap&r='+str(i)
            options = webdriver.ChromeOptions()
            options.add_extension('drivers/AdBlock.crx')
            browser = webdriver.Chrome(executable_path='drivers/chromedriver.exe', options=options)
            browser.set_window_size(1200, 1000)
            browser.get(url=url)
            browser.switch_to.window(browser.window_handles[0])
            html_source2 = browser.page_source
            competitors.extend(pd.read_html(html_source2)[17][1].values[1:])
            i+=20
        browser.close()
        browser.quit()

        df = pd.DataFrame()
        for i in competitors[:n]:
            df = df.append(finvizfinance(i).TickerFundament(), ignore_index=True)
        df = df.drop(['Earnings'], axis=1)
        for i in df.columns[5:]:
            l = []
            for j in df[i]:
                if j == '-':
                    j = np.nan
                try:
                    j = j.replace('%', '')
                except:
                    pass
                try:
                    j = float(j)
                    l.append(j)
                except:
                    pass
                try:
                    if j.find('B'):
                        j = j.replace('B', '')
                        j = float(j)
                        j = j * 1000000
                        l.append(j)
                except:
                    pass
                try:
                    if j.find('M'):
                        j = j.replace('M', '')
                        j = float(j)
                        j = j * 1000
                        l.append(j)
                except:
                    pass
                try:
                    if j.find('K'):
                        j = j.replace('K', '')
                        j = float(j)
                        j = j * 1000
                        l.append(j)
                except:
                    pass

                if j == 'Yes':
                    l.append(j)
                if j == 'No':
                    l.append(j)
                try:
                    s = ''
                    for p in j.split(','):
                        s = s + p
                    l.append(int(s))
                except:
                    pass

            df[i] = l
        df_mean = pd.DataFrame(data={'Mean':df.mean()}).sort_index()
        main_tick = finvizfinance(ticker).TickerFundament()
        main_tick = pd.DataFrame(data={ticker: main_tick}).drop(
            ['Earnings', 'Company', 'Country', 'Index', 'Industry', 'Optionable', 'Sector', 'Shortable'])
        main_tick["mean"] = df_mean
        main_tick.to_csv('data_with_mean.csv')
    except:
        print("Error in get_comp_mean")

