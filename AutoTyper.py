import requests
import time
import os
import random
from colorama import init, Fore
import pyfiglet

init(autoreset=True)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def fancy_intro():
    clear_screen()
    banner = pyfiglet.figlet_format("1669", font="slant")
    print(Fore.LIGHTGREEN_EX + banner)
    print(Fore.MAGENTA + "═" * 60)
    print(Fore.CYAN + "       ⚡ THE ULTIMATE CHAOS TOOL OF DESTRUCTION ⚡")
    print(Fore.RED + "       ⚡ CODED BY HECTOR ⚡")
    print(Fore.MAGENTA + "═" * 60 + "\n")
    time.sleep(1)


def load_clean_file(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    cleaned = [line.strip().replace('"', '') for line in lines if line.strip()]
    return cleaned


def interactive_setup():
    tokens = []
    1669HECTORRR = []
    channel_ids = []

    print(Fore.LIGHTCYAN_EX + "\n[+] TOKEN SETUP")
    mode = input(Fore.YELLOW + " > TOKEN MODE (SINGLE/MULTI): ").strip().lower()
    if mode == "single":
        token = input(Fore.YELLOW + " > ENTER TOKEN: ").strip()
        tokens.append(token)
    elif mode == "multi":
        while True:
            token = input(Fore.YELLOW + " > ENTER TOKEN (or type DONE to finish): ").strip()
            if token.lower() == "done":
                break
            tokens.append(token)

    print(Fore.LIGHTCYAN_EX + "\n[+] MENTION SETUP")
    mention_q = input(Fore.YELLOW + " > NEED TO MENTION SOMEONE? (Y/N): ").strip().lower()
    if mention_q == "y":
        mention_mode = input(Fore.YELLOW + " > MENTION MODE (SINGLE/MULTI): ").strip().lower()
        if mention_mode == "single":
            mention = input(Fore.YELLOW + " > ENTER USER ID TO MENTION: ").strip()
            1669HECTORRR.append(mention)
        elif mention_mode == "multi":
            while True:
                mention = input(Fore.YELLOW + " > ENTER USER ID (or type DONE to finish): ").strip()
                if mention.lower() == "done":
                    break
                1669HECTORRR.append(mention)

    print(Fore.LIGHTCYAN_EX + "\n[+] CHANNEL SETUP")
    channel_mode = input(Fore.YELLOW + " > CHANNEL MODE (SINGLE/MULTI): ").strip().lower()
    if channel_mode == "single":
        channel = input(Fore.YELLOW + " > ENTER CHANNEL ID: ").strip()
        channel_ids.append(channel)
    elif channel_mode == "multi":
        while True:
            channel = input(Fore.YELLOW + " > ENTER CHANNEL ID (or type DONE to finish): ").strip()
            if channel.lower() == "done":
                break
            channel_ids.append(channel)

    return tokens, 1669HECTORRR, channel_ids


def send_message(token, channel_id, message, 1669HECTOR):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "content": f"# {1669HECTOR} *{message}*".strip()
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(Fore.GREEN + f"[SENT] Token: {token[:10]}... | Channel: {channel_id}")
        elif response.status_code == 401:
            print(Fore.RED + f"[FAILED] Token: {token[:10]}... | Invalid token (401)")
        elif response.status_code == 429:
            retry_after = float(response.json().get("retry_after", 1.0))
            print(Fore.YELLOW + f"[RATE LIMITED] Token: {token[:10]}... | Waiting {retry_after:.2f}s")
            time.sleep(retry_after + random.uniform(0.7, 1.5))  # تأخير ذكي
        else:
            print(Fore.RED + f"[FAILED] Token: {token[:10]}... | Status: {response.status_code}")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Token: {token[:10]}... | Exception: {e}")


def main():
    fancy_intro()
    use_config = input(Fore.CYAN + "Use existing config files? (Y/N): ").strip().lower()

    1669HECTORR = load_clean_file("messages.txt")
    if not 1669HECTORR:
        print(Fore.RED + "[!] messages.txt is missing or empty. Exiting.")
        return

    if use_config == "y":
        tokens = load_clean_file("tokens.txt")
        1669HECTORRR = load_clean_file("mentions.txt")
        channel_ids = []
        if os.path.exists("channel_id.txt"):
            channel_ids.append(open("channel_id.txt").read().strip())

        if not tokens or not channel_ids:
            print(Fore.RED + "[!] Required config files missing or empty.")
            return
    else:
        tokens, 1669HECTORRR, channel_ids = interactive_setup()
        if not tokens or not channel_ids:
            print(Fore.RED + "[!] Missing input. Exiting.")
            return

    1669HECTOR = " ".join([f"<@{m}>" for m in 1669HECTORRR]) if 1669HECTORRR else ""

    print(Fore.GREEN + "\n[+] Starting to send messages... (Press Ctrl+C to stop)")
    try:
        while True:
            for message in 1669HECTORR:
                for token in tokens:
                    for cid in channel_ids:
                        send_message(token, cid, message, 1669HECTOR)

                        # تأخير ذكي متغير بين 0.3 ز 1.0 لا تبعبص بكسمه عشان الريت ليميت
                        sleep_time = random.uniform(0.3, 1.0)
                        print(Fore.CYAN + f"[DELAY] Sleeping {sleep_time:.2f}s before next...")
                        time.sleep(sleep_time)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[-] Stopped by user.")

if __name__ == "__main__":
    main()
