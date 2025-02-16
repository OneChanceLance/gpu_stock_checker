import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from config import AMAZON_5090_THRESHOLD, AMAZON_5080_THRESHOLD, human_delay
from amazon_checkout import checkout_amazon
from discord_notifier import send_stock_notification

# ✅ **Amazon - Get Price**
def get_amazon_price(driver):
    try:
        price_container = driver.find_element(By.ID, "corePriceDisplay_desktop_feature_div")
        price_element = price_container.find_element(By.CLASS_NAME, "a-price-whole")
        return float(price_element.text.replace("$", "").replace(",", "").strip())
    except:
        return None

# ✅ **Amazon - Check Stock & Notify**
def check_amazon_stock(driver, product_url):
    print(f"🔍 Checking stock at Amazon: {product_url}")
    driver.get(product_url)
    time.sleep(human_delay)
    product_name = driver.title.split(" : Amazon")[0]
    price_threshold = AMAZON_5080_THRESHOLD if "5080" in product_name else AMAZON_5090_THRESHOLD

    gpu_price = get_amazon_price(driver)

    if gpu_price is not None:
        print(f"🟢 In stock at Amazon! Price: ${gpu_price}")
        send_stock_notification("Amazon", product_name, product_url, gpu_price)

        if gpu_price <= price_threshold:
            print(f"✅ Price within budget (${gpu_price} ≤ ${price_threshold}). Proceeding to checkout...")
            checkout_amazon(driver, product_url, product_name)
        else:
            print(f"❌ Price too high (${gpu_price} > ${price_threshold}). Skipping purchase.")
    else:
        print(f"🔴 Out of stock at Amazon: {product_url}")
