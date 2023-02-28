from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import re

def test_shopping(driver):
    product = 'samsung galaxy s22'
    amazon_price = 0.0
    bestbuy_price = 0.0

    driver.get("https://www.amazon.com")

    search_form_input = driver.find_element(By.XPATH,  "//input[@name='field-keywords']")
    search_form_input.send_keys(product)
    search_form_input.send_keys(Keys.RETURN)

    search_results = driver.page_source
    soup = BeautifulSoup(search_results, 'html.parser')

    all_products = soup.find_all('div', {'data-component-type': 's-search-result'})

    max_reviews = 0
    for prodct in all_products:
        reviews = prodct.find('span', {'class': 'a-size-base s-underline-text'})
        if reviews is not None:
            count_number = re.sub('[^0-9]','', reviews.text)
            if count_number.isdigit() and int(count_number) > max_reviews:
                max_reviews = int(count_number)
                price = prodct.find('span', {'class': 'a-price-whole'})
                if price is not None:
                    amazon_price = float(price.text.replace(',', ''))
               

    driver.get("https://www.bestbuy.com/")
    country_button = driver.find_element(By.XPATH, "//a[@class='us-link']")
    country_button.click()

    search_bar = driver.find_element(By.XPATH, "//input[@id='gh-search-input']")
    search_bar.send_keys(product)
    search_bar.send_keys(Keys.RETURN)

    search_results = driver.page_source
    soup = BeautifulSoup(search_results, 'html.parser')
    all_products = soup.find_all('div', {'class': 'list-item lv'})

    max_reviews = 0
    for prodct in all_products:
        reviews = prodct.find('span', {'class': 'c-reviews'})
        if reviews is not None:
            count_number = re.sub('[^0-9]','', reviews.text)
            if count_number.isdigit() and int(count_number) > max_reviews:
                max_reviews = int(count_number)
                price = prodct.find('div', {'class': 'priceView-hero-price priceView-customer-price'})
                if price is not None:
                    bestbuy_price = re.search(r'\d+.\d+\.\d+', price.text).group(0)
                    bestbuy_price = float(bestbuy_price.replace(',', ''))


    # pass
    # once script completed the line below should be uncommented.
    assert amazon_price > bestbuy_price

