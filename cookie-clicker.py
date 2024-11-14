import time
from selenium import webdriver
from selenium.webdriver.common.by import By
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://orteil.dashnet.org/experiments/cookie/')
cookie = driver.find_element(By.CSS_SELECTOR, '#cookie')
items = driver.find_elements(By.CSS_SELECTOR, value='#store div ')
item_ids = [item.get_attribute('id') for item in items]
print(item_ids)

timeout = time.time() + 5
two_min = time.time() + 60 * 2

while True:
    cookie.click()
    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, value='#store b')
        item_prices = []
        for price in all_prices:
            if price.text != '':
                cost = int(price.text.split('-')[1].strip().replace(',', ''))
                item_prices.append(cost)
        # Get current cookie count
        money_text = driver.find_element(By.ID, value='money').text
        if ',' in money_text:
            money_text = money_text.replace(',', '')
        cookie_count = int(money_text)
        # A dictionary of prices and ids
        cookie_upgrade = {}
        for i in range(len(item_prices)):
            cookie_upgrade[item_prices[i]] = item_ids[i]
        # Finding upgrades we can afford
        affordable_upgrade = {}
        for cost, id in cookie_upgrade.items():
            if cookie_count >= cost:
                affordable_upgrade[cost] = id
        # Purchasing the most expensive upgrades
        most_expensive_upgrade = max(affordable_upgrade)
        purchase_id = affordable_upgrade[most_expensive_upgrade]

        driver.find_element(By.ID, value=purchase_id).click()

        timeout = time.time() + 5

    if time.time() > two_min:
        cookie_per_s = driver.find_element(By.ID, value='cps')
        print(cookie_per_s.text)
        break






