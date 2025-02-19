import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from config import human_delay
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from discord_notifier import send_cart_notification, send_purchase_notification

# ✅ **Amazon - Checkout Process**
def checkout_amazon(driver, product_url, product_name):
    print(f"🛒 Adding to cart on Amazon: {product_url}")
    #driver.get(product_url)
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
            driver.execute_script("arguments[0].click();", place_order_btn)
            print("✅ Order Placed Successfully at Amazon CA!")
            send_purchase_notification("Amazon", product_name, product_url)

        except Exception as e:
            print(f"❌ Error during Amazon checkout: {e}")
    elif "amazon.com" in product_url:
        try:
            buy_now_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "buy-now-button"))
            )
            buy_now_button.click()
            print("🛒 Buying now...")
            try:
                # ✅ **Wait for iframe & switch into it**
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "turbo-checkout-iframe"))
                )
                iframe = driver.find_element(By.ID, "turbo-checkout-iframe")
                driver.switch_to.frame(iframe)  # Switch to checkout iframe
                print("✅ Switched to Turbo Checkout iframe.")
                # ✅ **Find the Parent Container**

                try:
                    place_order_form = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.ID, "place-order-form"))
                    )
                    print("✅ Found 'place-order-form' inside iframe.")
                except TimeoutException:
                    print("❌ 'place-order-form' NOT found inside iframe.")
                    driver.switch_to.default_content()  # Exit iframe

                try:
                    # ✅ **Wait for the Free Shipping button to appear (if available)**
                    free_shipping_btn = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, "//span[@class='a-color-base' and contains(text(), 'FREE Shipping')]"))
                    )
                    
                    # ✅ **Scroll to the button to make sure it's visible**
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", free_shipping_btn)
                    
                    # ✅ **Find the parent <button> element to click it**
                    shipping_button = free_shipping_btn.find_element(By.XPATH, "./ancestor::button")

                    # ✅ **Click the "Free Shipping" button**
                    shipping_button.click()
                    print("✅ Selected FREE Shipping successfully!")

                except TimeoutException:
                    print("ℹ️ No Free Shipping option available. Skipping.")

                except NoSuchElementException:
                    print("❌ Could not find Free Shipping option.")

                except Exception as e:
                    print(f"❌ Error selecting Free Shipping: {e}")

                order_place_btn = WebDriverWait(place_order_form, 5).until(
                    EC.element_to_be_clickable((By.XPATH, ".//input[@type='submit' and @class='a-button-input']"))
                )


                # ✅ **Find the Button as a Descendant of the Correct Parent**

                # 🔹 **Click Using JavaScript (Bypasses Bot Protection)**
                driver.execute_script("arguments[0].click();", order_place_btn)
                print("✅ Clicked 'Place Your Order' button successfully!")
                send_purchase_notification("Amazon", product_name, product_url)
                time.sleep(5)
                return  # Success, exit function

            except StaleElementReferenceException:
                print(f"⚠️ Stale element error detected.")

            except Exception as e:
                print(f"❌ Failed to click 'Place Your Order': {e}")
            
        except Exception as e:
            print(f"❌ Error during Amazon checkout: {e}")