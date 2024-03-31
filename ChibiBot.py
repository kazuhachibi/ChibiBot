import requests
from telegram.ext import Updater, CommandHandler

# Hàm lấy giá của token từ CoinGecko
def get_token_price(token):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    if token in data:
        return data[token]['usd']
    else:   
        return None

# Hàm xử lý lệnh convert
def convert_to_usdt(update, context):
    try:
        args = context.args
        if len(args) != 2:
            update.message.reply_text("Usage: /value <amount> <token>")
            return

        amount = float(args[0])
        token = args[1].lower()

        price = get_token_price(token)
        if price:
            usdt_amount = amount * price
            update.message.reply_text(f"{amount} {token.upper()} is equal to {usdt_amount} USDT")
        else:
            update.message.reply_text("Unable to fetch data for the token")
    except ValueError:
        update.message.reply_text("Invalid amount. Please enter a valid number.")

# Hàm chính
def main():
    # Khởi tạo updater và dispatcher
    updater = Updater("7051129500:AAEMv83sPLY5qq2cPxdm2FykFX6fFc7Aosc", use_context=True)
    dp = updater.dispatcher

    # Đăng ký handler cho lệnh convert
    dp.add_handler(CommandHandler("value", convert_to_usdt))

    # Bắt đầu polling để lắng nghe các tin nhắn mới
    updater.start_polling()

    # Dừng chương trình khi nhận phím tắt Ctrl+C
    updater.idle()

# Kiểm tra nếu file được thực thi trực tiếp
if __name__ == '__main__':
    main()