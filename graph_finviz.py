from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pandas as pd
import numpy as np
import data_finviz


def get_graph(ticker,n):
    url = 'https://finviz.com/quote.ashx?t=' + ticker

    options = webdriver.ChromeOptions()
    options.add_extension('drivers/AdBlock.crx')
    browser = webdriver.Chrome(executable_path='drivers/chromedriver.exe', options=options)
    browser.set_window_size(1200, 1000)

    try:
        browser.get(url=url)
        browser.switch_to.window(browser.window_handles[0])
        html_source = browser.page_source
        a = data_finviz.parse_html(html_source,n,ticker)
        if a==False:
            browser.close()
            browser.quit()
            return False
        browser.get_screenshot_as_file('screenshots/' + ticker + '.png')
        parse_image(ticker)
    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()


def parse_image(ticker):
    im = Image.open(r'screenshots/' + ticker + '.png')
    # crop for my computer
    # rewrire using width and height
    left = 115
    top = 285
    right = 1350
    bottom = 875
    im1 = im.crop((left, top, right, bottom))
    im1.save('screenshots/'+ticker+".png","PNG")
