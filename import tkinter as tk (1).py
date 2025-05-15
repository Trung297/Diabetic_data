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

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# --- Chọn người chơi ---
def choose_player(player_id):
    global user, user_target_items
    user = players[player_id]
    user_target_items = random.sample(range(5), 2)
    show_auction_screen()

def show_player_selection():
    clear_frame(main_frame)
    tk.Label(main_frame, text="🧍 Chọn người chơi của bạn", font=("Arial", 14)).pack(pady=10)
    for i in range(3):
        tk.Button(main_frame, text=f"Player {i}", font=("Arial", 12),
                  command=lambda i=i: choose_player(i)).pack(pady=5)

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

# --- Màn hình đấu giá ---
def show_auction_screen():
    clear_frame(main_frame)
    tk.Label(main_frame, text=f"🎯 Mục tiêu: thắng món {user_target_items[0]} và {user_target_items[1]}",
             font=("Arial", 12), fg="blue").pack(pady=5)
    tk.Label(main_frame, text=f"🧍 Bạn là Player {user.id} | 💰 Tiền: {user.money}", font=("Arial", 11)).pack(pady=5)

    tk.Label(main_frame, text=f"💎 Đang đấu giá: {items[current_item]}", font=("Arial", 13, "bold")).pack(pady=10)
    tk.Label(main_frame, text=f"💵 Giá sàn: {min_prices[current_item]}", font=("Arial", 11)).pack()

    global bid_entry
    bid_entry = tk.Entry(main_frame, font=("Arial", 12))
    bid_entry.pack(pady=10)

    tk.Button(main_frame, text="💰 Đặt giá", command=submit_bid).pack(pady=5)
    tk.Button(main_frame, text="⏭️ Bỏ qua", command=skip_bid).pack(pady=5)

# --- Kết quả ---
def show_result():
    clear_frame(main_frame)
    win_items = set(user.won_items)
    goal_items = set(user_target_items)
    matched = win_items & goal_items

    tk.Label(main_frame, text="📊 KẾT QUẢ", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(main_frame, text=f"Bạn đã thắng các món: {sorted(user.won_items)}", font=("Arial", 12)).pack()
    tk.Label(main_frame, text=f"Mục tiêu cần: {sorted(user_target_items)}", font=("Arial", 12)).pack()
    tk.Label(main_frame, text=f"Số món mục tiêu đã thắng: {len(matched)}", font=("Arial", 12)).pack()

    if len(matched) >= 2:
        tk.Label(main_frame, text="🏆 CHÚC MỪNG! BẠN ĐÃ THẮNG!", font=("Arial", 14), fg="green").pack(pady=10)
    else:
        tk.Label(main_frame, text="❌ BẠN ĐÃ THUA! HẸN GẶP LẠI.", font=("Arial", 14), fg="red").pack(pady=10)

    tk.Button(main_frame, text="🔁 Chơi lại", command=restart_game).pack(pady=10)

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