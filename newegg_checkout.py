import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from config import human_delay
from discord_notifier import send_cart_notification, send_purchase_notification
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException

# ✅ **Newegg - Checkout Process**
def checkout_newegg(driver, product_url, product_name, cvv_code):
    driver.get(product_url)

    try:
        add_to_cart_btn = driver.find_element(By.CLASS_NAME, "btn-primary")
        add_to_cart_btn.click()
        print("✅ Added to cart at Newegg!")
        send_cart_notification("Newegg Canada", product_name, product_url)

        driver.get("https://secure.newegg.ca/shop/cart")


        proceed_to_checkout_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary"))
        )
        proceed_to_checkout_btn.click()
        print("✅ Proceeding to checkout...")

        try:
            cvv_input = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.NAME, "cvvNumber"))
            )
            cvv_input.click()
            cvv_input.clear()
            cvv_input.send_keys(cvv_code)
            print(f"✅ Entered CVV code.")
        except NoSuchElementException:
            print("❌ Could not find CVV input field.")

        try:
            use_payment_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Use This Payment Method')]")
            use_payment_btn.click()
            print("✅ Selected payment method.")
            time.sleep(1)
        except NoSuchElementException:
            print("ℹ️ No 'Use This Payment Method' button found. Skipping to order placement...")

        place_order_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Place Order')]")
        driver.execute_script("arguments[0].click();", place_order_btn)
        print("✅ Order Placed Successfully!")
        send_purchase_notification("Newegg Canada", product_name, product_url)
    
        time.sleep(10)

    except Exception as e:
        print(f"❌ Error during Newegg checkout: {e}")
