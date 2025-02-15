import requests
from config import DISCORD_PURCHASE_WEBHOOK_URL, DISCORD_CART_WEBHOOK_URL, DISCORD_INSTOCK_WEBHOOK_URL

# ✅ **Send In-Stock Notification**
def send_stock_notification(store, product_name, product_url, price):
    data = {
        "content": f"@everyone 🟢 **In Stock!**\n\n**Product:** {product_name}\n**Price:** ${price} CAD\n**Store:** {store}\n🔗 [View Product]({product_url})"
    }
    requests.post(DISCORD_INSTOCK_WEBHOOK_URL, json=data)

# ✅ **Send Add to Cart Notification**
def send_cart_notification(store, product_name, product_url):
    data = {
        "content": f"@everyone 🛒 **Added to Cart!**\n\n**Product:** {product_name}\n**Store:** {store}\n🔗 [View Product]({product_url})"
    }     
    requests.post(DISCORD_CART_WEBHOOK_URL, json=data)

# ✅ **Send Purchase Notification**
def send_purchase_notification(store, product_name, product_url):
    data = {
        "content": f"@everyone ✅ **Purchased!**\n\n**Product:** {product_name}\n**Store:** {store}\n🔗 [View Product]({product_url})"
    }
    requests.post(DISCORD_PURCHASE_WEBHOOK_URL, json=data)
