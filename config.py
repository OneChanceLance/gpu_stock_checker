import random

# ✅ Discord Webhooks
DISCORD_PURCHASE_WEBHOOK_URL = "https://discord.com/api/webhooks/1338578389480505414/1hCOS03gIr-cKcL8d6amO9oAS4VQB4cIDGfCzrwl8tgk5dJK08RkuNAEOAfdsghTf2Q6"
DISCORD_CART_WEBHOOK_URL = "https://discord.com/api/webhooks/1338875358350540850/iL8zpFlwvPn2pt1zD0zrTTjwwQLDOTR07l6qpKtItf4SOBETLrJ8vgTaJtUvE5JcSLxQ"
DISCORD_INSTOCK_WEBHOOK_URL = "https://discord.com/api/webhooks/1338875358350540850/iL8zpFlwvPn2pt1zD0zrTTjwwQLDOTR07l6qpKtItf4SOBETLrJ8vgTaJtUvE5JcSLxQ"

# ✅ Price Thresholds
PRICE_THRESHOLD = 4500  # Default for all GPUs
RTX_5080_THRESHOLD = 2150  # Special threshold for RTX 5080 GPUs

AMAZON_5090_THRESHOLD = 4500
AMAZON_5080_THRESHOLD = 2150

NEWEGG_5090_THRESHOLD = 4500
NEWEGG_5080_THRESHOLD = 2150

BESTBUY_5090_THRESHOLD = 4500
BESTBUY_5080_THRESHOLD = 2150

# ✅ **Randomized Human-Like Delays**
def human_delay():
    return random.randint(1, 2)  # Random delay between 2.5s - 7.5s

# ✅ **Stock Check Interval (Varies Each Run)**
def stock_check_interval():
    return random.randint(3, 4)  # Waits between 1-3 minutes before checking stock

# ✅ **User-Agent Rotator**
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)