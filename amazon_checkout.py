import time
from selenium.webdriver.common.by import By
from config import human_delay
from discord_notifier import send_cart_notification, send_purchase_notification

# ✅ **Amazon - Checkout Process**
def checkout_amazon(driver, product_url, product_name):
    print(f"🛒 Adding to cart on Amazon: {product_url}")
    driver.get(product_url)
    time.sleep(human_delay())

    try:
        add_to_cart_btn = driver.find_element(By.ID, "add-to-cart-button")
        add_to_cart_btn.click()
        print("✅ Item added to cart at Amazon!")
        send_cart_notification("Amazon", product_name, product_url)

        driver.get("https://www.amazon.ca/gp/cart/view.html")
        time.sleep(human_delay())

        proceed_to_checkout_btn = driver.find_element(By.NAME, "proceedToRetailCheckout")
        proceed_to_checkout_btn.click()
        print("✅ Proceeding to checkout...")

        time.sleep(human_delay())

        place_order_btn = driver.find_element(By.ID, "placeOrder")
        driver.execute_script("arguments[0].click();", place_order_btn)
        print("✅ Order Placed Successfully at Amazon!")
        send_purchase_notification("Amazon", product_name, product_url)

    except Exception as e:
        print(f"❌ Error during Amazon checkout: {e}")
