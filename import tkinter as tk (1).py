import tkinter as tk
from tkinter import messagebox
import random

# --- Player Class ---
class Player:
    def __init__(self, id, money):
        self.id = id
        self.money = money
        self.original_money = money
        self.won_items = []

    def win_item(self, item_id, price):
        self.won_items.append(item_id)
        self.money -= price

# --- Khởi tạo dữ liệu ---
players = [Player(i, random.randint(70,120)) for i in range(3)]
items = [f"Món hàng {i}" for i in range(5)]
min_prices = [random.randint(15,30) for _ in range(5)]

user = None
user_target_items = []
current_item = 0
user_skipped_last_round = False

user_interest_score = {i: 0 for i in range(5)}  # AI theo dõi hành vi người chơi
INTEREST_THRESHOLD = 2  # Ngưỡng nghi ngờ người chơi cần món này

# --- Giao diện ---
root = tk.Tk()
root.title("🎮 Trò chơi Đấu giá - Lý thuyết Trò chơi")
root.geometry("560x420")

main_frame = tk.Frame(root)
main_frame.pack(pady=20)

# --- Chọn người chơi ---
def choose_player(player_id):
    global user, user_target_items
    user = players[player_id]
    user_target_items = random.sample(range(5), 2)
    show_auction_screen()

# --- Đấu giá ---
def submit_bid():
    global current_item, user_skipped_last_round
    try:
        bid = int(bid_entry.get())
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập một số hợp lệ.")
        return

    item_price = min_prices[current_item]
    if bid < item_price:
        messagebox.showwarning("❌ Giá thấp quá", f"Giá sàn là {item_price}.")
        return
    if bid > user.money:
        messagebox.showwarning("❌ Thiếu tiền", "Bạn không đủ tiền.")
        return

    # AI học hành vi người chơi
    if bid - item_price > 5:
        user_interest_score[current_item] += 1

    # AI đấu giá
    opponents = [p for p in players if p != user]
    opponent_bids = []
    for p in opponents:
        if p.money >= item_price:
            # Logic AI
            if user_skipped_last_round:
                lower = item_price + 10
                upper = item_price + 40
            else:
                lower = item_price
                upper = item_price + 30

            # Nếu nghi ngờ bạn cần món này -> AI đặt giá cao hơn để gây nhiễu
            if user_interest_score.get(current_item, 0) >= INTEREST_THRESHOLD:
                lower += 10
                upper += 10

            opp_bid = random.randint(lower, min(p.money, upper))
        else:
            opp_bid = 0
        opponent_bids.append(opp_bid)

    all_bids = [bid] + opponent_bids
    winner_index = all_bids.index(max(all_bids))
    price_paid = all_bids[winner_index]

    if winner_index == 0:
        user.win_item(current_item, bid)
        messagebox.showinfo("✅ Kết quả", f"Bạn đã thắng {items[current_item]} với giá {bid}")
    else:
        opponents[winner_index - 1].win_item(current_item, price_paid)
        messagebox.showinfo("❌ Kết quả", f"Bạn đã thua. Đối thủ thắng {items[current_item]} với giá {price_paid}")

    user_skipped_last_round = False
    next_item()

def skip_bid():
    global user_skipped_last_round
    user_skipped_last_round = True
    next_item()

def next_item():
    global current_item
    current_item += 1
    if current_item < len(items):
        show_auction_screen()
    else:
        show_result()

def restart_game():
    global players, user, user_target_items, current_item, user_skipped_last_round, user_interest_score
    players = [Player(i, random.randint(70, 120)) for i in range(3)]
    user = None
    user_target_items = []
    current_item = 0
    user_skipped_last_round = False
    user_interest_score = {i: 0 for i in range(5)}
    show_player_selection()

# --- Khởi động ---
show_player_selection()
root.mainloop()
