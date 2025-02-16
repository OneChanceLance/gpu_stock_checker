import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from config import human_delay
from discord_notifier import send_cart_notification, send_purchase_notification

# ✅ **Best Buy - Checkout Process**
def checkout_bestbuy(driver, product_url, product_name):
    driver.get(product_url)

    try:
        add_to_cart_btn = driver.find_element(By.XPATH, "//button[@data-automation='addToCartButton']")
        add_to_cart_btn.click()
        print("✅ Added to cart at Best Buy!")
        send_cart_notification("Best Buy", product_name, product_url)

        driver.get("https://www.bestbuy.ca/en-ca/basket")
        time.sleep(human_delay())

        proceed_to_checkout_btn = driver.find_element(By.XPATH, "//a[@data-automation='continue-to-checkout']")
        proceed_to_checkout_btn.click()
        print("✅ Proceeding to checkout...")

        time.sleep(human_delay())

        place_order_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Place Order')]")
        driver.execute_script("arguments[0].click();", place_order_btn)
        print("✅ Order Placed Successfully!")
        send_purchase_notification("Best Buy", product_name, product_url)

    except Exception as e:
        print(f"❌ Error during Best Buy checkout: {e}")
