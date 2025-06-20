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
    mentions = []
    channel_ids = []

    print(Fore.LIGHTCYAN_EX + "\n[+] TOKEN SETUP")
    mode = input(Fore.YELLOW + " > TOKEN MODE (SINGLE [s]/MULTI [m]): ").strip().lower()
    if mode == "s":
        token = input(Fore.YELLOW + " > ENTER TOKEN: ").strip()
        tokens.append(token)
    elif mode == "m":
        while True:
            token = input(Fore.YELLOW + " > ENTER TOKEN (type DONE to finish): ").strip()
            if token.lower() == "done":
                break
            tokens.append(token)

    print(Fore.LIGHTCYAN_EX + "\n[+] MENTION SETUP")
    mention_q = input(Fore.YELLOW + " > NEED TO MENTION SOMEONE? (Y/N): ").strip().lower()
    if mention_q == "y":
        mention_mode = input(Fore.YELLOW + " > MENTION MODE (SINGLE [s]/MULTI [m]): ").strip().lower()
        if mention_mode == "s":
            mention = input(Fore.YELLOW + " > ENTER USER ID TO MENTION: ").strip()
            mentions.append(mention)
        elif mention_mode == "m":
            while True:
                mention = input(Fore.YELLOW + " > ENTER USER ID (or type DONE to finish): ").strip()
                if mention.lower() == "done":
                    break
                mentions.append(mention)

    print(Fore.LIGHTCYAN_EX + "\n[+] CHANNEL SETUP")
    channel_mode = input(Fore.YELLOW + " > CHANNEL MODE (SINGLE [s]/MULTI [m]): ").strip().lower()
    if channel_mode == "s":
        channel = input(Fore.YELLOW + " > ENTER CHANNEL ID: ").strip()
        channel_ids.append(channel)
    elif channel_mode == "m":
        while True:
            channel = input(Fore.YELLOW + " > ENTER CHANNEL ID (or type DONE to finish): ").strip()
            if channel.lower() == "done":
                break
            channel_ids.append(channel)

    return tokens, mentions, channel_ids


def send_message(token, channel_id, message, mentions_text):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "content": f"# {mentions_text} *{message}*".strip()
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

    messages = load_clean_file("messages.txt")
    if not messages:
        print(Fore.RED + "[!] messages.txt is missing or empty. Exiting.")
        return

    if use_config == "y":
        tokens = load_clean_file("tokens.txt")
        mentions = load_clean_file("mentions.txt")
        channel_ids = []
        if os.path.exists("channel_id.txt"):
            channel_ids.append(open("channel_id.txt").read().strip())

        if not tokens or not channel_ids:
            print(Fore.RED + "[!] Required config files missing or empty.")
            return
    else:
        tokens, mentions, channel_ids = interactive_setup()
        if not tokens or not channel_ids:
            print(Fore.RED + "[!] Missing input. Exiting.")
            return

    mentions_text = " ".join([f"<@{m}>" for m in mentions]) if mentions else ""

    print(Fore.GREEN + "\n[+] Starting to send messages... (Press Ctrl+C to stop)")
    try:
        while True:
            for message in messages:
                for token in tokens:
                    for cid in channel_ids:
                        send_message(token, cid, message, mentions_text)

                        # تأخير ذكي متغير بين 0.3 ز 1.0 لا تبعبص بكسمه عشان الريت ليميت
                        sleep_time = random.uniform(0.3, 1.0)
                        print(Fore.CYAN + f"[DELAY] Sleeping {sleep_time:.2f}s before next...")
                        time.sleep(sleep_time)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[-] Stopped by user.")

if __name__ == "__main__":
    main()
