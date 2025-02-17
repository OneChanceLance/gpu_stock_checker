import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from config import human_delay
from selenium.webdriver.support import expected_conditions as EC
from discord_notifier import send_cart_notification, send_purchase_notification

# ✅ **Amazon - Checkout Process**
def checkout_amazon(driver, product_url, product_name):
    print(f"🛒 Adding to cart on Amazon: {product_url}")
    driver.get(product_url)
    time.sleep(human_delay())
    if "amazon.ca" in product_url:
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
            #driver.execute_script("arguments[0].click();", place_order_btn)
            print("✅ Order Placed Successfully at Amazon CA!")
            send_purchase_notification("Amazon", product_name, product_url)

        except Exception as e:
            print(f"❌ Error during Amazon checkout: {e}")
    elif "amazon.com" in product_url:
        try:
            add_to_cart_btn = driver.find_element(By.ID, "add-to-cart-button")
            add_to_cart_btn.click()
            print("✅ Item added to cart at Amazon!")
            send_cart_notification("Amazon", product_name, product_url)

            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "attach-desktop-sideSheet"))
                )

                # ✅ Locate the actual input button
                no_thanks_button = driver.find_element(By.XPATH, "//input[@aria-labelledby='attachSiNoCoverage-announce']")

                # ✅ Scroll into view
                driver.execute_script("arguments[0].scrollIntoView();", no_thanks_button)

                if no_thanks_button.is_displayed():
                    print("⚠️ Protection plan popup detected! Clicking 'No Thanks'...")
                    no_thanks_button.click()
                    print("✅ Closed protection plan popup successfully!")
                    WebDriverWait(driver, 5).until(EC.invisibility_of_element(no_thanks_button))
                    print("✅ Protection plan popup closed!")
            except NoSuchElementException:
                print("ℹ️ No protection plan popup detected. Continuing checkout...")

            driver.get("https://www.amazon.com/gp/cart/view.html")

            proceed_to_checkout_btn = driver.find_element(By.NAME, "proceedToRetailCheckout")
            proceed_to_checkout_btn.click()
            print("✅ Proceeding to checkout...")

            try:
                # ✅ Locate "No Thanks" button by its unique ID
                no_thanks_button = driver.find_element(By.ID, "prime-updp-decline-cta")

                if no_thanks_button.is_displayed():
                    print("⚠️ Amazon Prime trial popup detected! Clicking 'No Thanks'...")
                    no_thanks_button.click()
                    time.sleep(2)  # Allow transition to complete
                    print("✅ Closed Prime trial popup successfully!")

            except NoSuchElementException:
                print("ℹ️ No Prime trial popup detected. Continuing checkout...")

            place_order_btn = driver.find_element(By.ID, "placeOrder")
            #driver.execute_script("arguments[0].click();", place_order_btn)
            print("✅ Order Placed Successfully at Amazon US!")
            send_purchase_notification("Amazon", product_name, product_url)

        except Exception as e:
            print(f"❌ Error during Amazon checkout: {e}")
