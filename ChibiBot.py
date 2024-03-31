import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Ánh xạ tên token từ người dùng sang tên token được CoinGecko hiểu
TOKEN_MAPPING = {
    'sol': 'solana',
    'bnb': 'binancecoin',
    'eth': 'ethereum',
    'matic': 'polygon',
    'avax': 'avalanche',
    'btc': 'bitcoin',
    # Thêm các ánh xạ khác nếu cần thiết
}


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

    # Chuyển đổi tên token nếu cần thiết
    if token in TOKEN_MAPPING:
      token = TOKEN_MAPPING[token]

    price = get_token_price(token)
    if price:
      usdt_amount = amount * price
      update.message.reply_text(
          f"{amount} {token.upper()} = {usdt_amount} USDT"
      )
    else:
      update.message.reply_text("Unable to fetch data for the token")
  except ValueError:
    update.message.reply_text("Invalid amount. Please enter a valid number.")


# Hàm xử lý tin nhắn văn bản không chứa lệnh cụ thể
def handle_text_message(update, context):
  text = update.message.text.lower()
  if text.startswith("value"):
    # Loại bỏ từ "value" từ tin nhắn và chạy hàm convert_to_usdt
    args = text.split()[1:]
    context.args = args
    convert_to_usdt(update, context)


def chibi(update, context):
  # Lấy tên người dùng từ đối tượng update
  user_name = update.message.from_user.first_name
  # Tạo thông báo chào hỏi cùng với tên người dùng
  message = f"Gì mậy khứa {user_name}! Muốn gì mậy?"
  # Gửi thông báo phản hồi
  update.message.reply_text(message)


# Hàm chính
def main():
  # Khởi tạo updater và dispatcher
  updater = Updater("7051129500:AAEMv83sPLY5qq2cPxdm2FykFX6fFc7Aosc",
                    use_context=True)
  dp = updater.dispatcher

  # Đăng ký handler cho lệnh convert
  dp.add_handler(CommandHandler("value", convert_to_usdt))

  # Đăng ký handler cho tin nhắn văn bản không chứa lệnh cụ thể
  dp.add_handler(
      MessageHandler(Filters.text & (~Filters.command), handle_text_message))

  # Thêm handler cho lệnh /chibi
  dp.add_handler(CommandHandler("chibi", chibi))

  # Bắt đầu polling để lắng nghe các tin nhắn mới
  updater.start_polling()

  # Dừng chương trình khi nhận phím tắt Ctrl+C
  updater.idle()


# Kiểm tra nếu file được thực thi trực tiếp
if __name__ == '__main__':
  main()
