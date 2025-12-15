import random
import time

FULL_NAME = {'s': 'Snake', 'w': 'Water', 'g': 'Gun'}
WIN_RULES = {
    ('s', 'w'): "Snake drinks Water",
    ('w', 'g'): "Water damages Gun",
    ('g', 's'): "Gun kills Snake"
}

def decide(p, c):
    if p == c:
        return "draw", "Same choice"
    if (p, c) in WIN_RULES:
        return "player", WIN_RULES[(p, c)]
    else:
        return "computer", WIN_RULES[(c, p)]

def type_text(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def countdown(n=3):
    for i in range(n, 0, -1):
        print(f"Revealing in {i}...", end='\r')
        time.sleep(0.5)
    print(" " * 30, end='\r')

def thinking_animation(duration=1.5):
    dots = ['.  ', '.. ', '...']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"Computer is thinking{dots[i % len(dots)]}", end='\r')
        time.sleep(0.4)
        i += 1
    print(" " * 30, end='\r')

def get_computer_choice(difficulty="normal"):
    opts = ['s', 'w', 'g']
    if difficulty == "easy":
        return random.choice(['w', 'g', 'w', 'g', 's'])
    elif difficulty == "hard":
        return random.choice(['g', 'g', 'g', 's', 'w'])
    else:
        return random.choice(opts)

def play_game(rounds=5, difficulty="normal"):
    player_score = comp_score = draws = 0

    type_text("=== Welcome to Snake · Water · Gun ===", 0.07)
    print("Rules: Snake>Water, Water>Gun, Gun>Snake.")
    print("Enter: s (Snake), w (Water), g (Gun). Type q to quit early.\n")

    for r in range(1, rounds + 1):
        while True:
            user = input(f"Round {r}/{rounds} - Your choice (s/w/g, q to quit): ").lower().strip()
            if user == 'q':
                print("You ended the game early.")
                return player_score, comp_score, draws
            if user in FULL_NAME:
                break
            print("Invalid input. Try again.")

        comp = get_computer_choice(difficulty)

        print("You locked your choice.")
        thinking_animation()
        countdown(3)

        print(f"You: {FULL_NAME[user]} | Computer: {FULL_NAME[comp]}")
        winner, reason = decide(user, comp)

        if winner == "draw":
            draws += 1
            print(f"Result: Draw ({reason}).")
        elif winner == "player":
            player_score += 1
            print(f"You WIN! ({reason})")
        else:
            comp_score += 1
            print(f"Computer WINS! ({reason})")

        print(f"Score => You: {player_score} | Computer: {comp_score} | Draws: {draws}\n")

    return player_score, comp_score, draws

if __name__ == "__main__":
    try:
        total_rounds = int(input("How many rounds do you want to play? (default 5): ") or "5")
        if total_rounds <= 0:
            total_rounds = 5
    except ValueError:
        total_rounds = 5

    difficulty = input("Difficulty (easy / normal / hard) [default normal]: ").strip().lower() or "normal"
    if difficulty not in ("easy", "normal", "hard"):
        difficulty = "normal"

    p, c, d = play_game(total_rounds, difficulty)

    type_text("=== Final Result ===", 0.07)
    print(f"You: {p} | Computer: {c} | Draws: {d}")
    if p > c:
        print("Overall: You WON the match! 🎉")
    elif c > p:
        print("Overall: Computer WON the match. Try again!")
    else:
        print("Overall: Match Drawn.")
        
