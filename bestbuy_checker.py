import time
import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from config import DISCORD_CART_WEBHOOK_URL, PRICE_THRESHOLD, RTX_5080_THRESHOLD, human_delay
from bestbuy_checkout import checkout_bestbuy
from discord_notifier import send_stock_notification

# ✅ **Best Buy - Get Price**
def get_bestbuy_price(driver):
    try:
        time.sleep(human_delay())
        price_container = driver.find_element(By.CSS_SELECTOR, 'span[data-automation="product-price"]')
        price_element = price_container.find_element(By.TAG_NAME, "div")
        return float(price_element.text.replace("$", "").replace(",", "").strip())
    except:
        return None

# ✅ **Best Buy - Check Stock & Notify**
def check_bestbuy_stock(driver, product_url):
    print(f"🔍 Checking stock at Best Buy: {product_url}")
    driver.get(product_url)
    time.sleep(human_delay())

    product_name = driver.title.split(" - Best Buy")[0]
    price_threshold = RTX_5080_THRESHOLD if "5080" in product_name else PRICE_THRESHOLD

    try:
        container = driver.find_element(By.CLASS_NAME, "addToCartButtonContainer_3kNch")
        add_to_cart_btn = container.find_element(By.CLASS_NAME, "addToCartButton_3HRhU")

        if add_to_cart_btn.is_enabled():
            gpu_price = get_bestbuy_price(driver)

            if gpu_price is not None:
                print(f"🟢 In stock at Best Buy! Price: ${gpu_price}")
                send_stock_notification("Best Buy", product_name, product_url, gpu_price)

                if gpu_price <= price_threshold:
                    print(f"✅ Price within budget (${gpu_price} ≤ ${price_threshold}). Proceeding to checkout...")
                    checkout_bestbuy(driver, product_url, product_name)
                else:
                    print(f"❌ Price too high (${gpu_price} > ${price_threshold}). Skipping purchase.")
    except:
        print(f"🔴 Out of stock at Best Buy: {product_url}")
