import requests as req
import ctypes
import os
import colorama
import concurrent.futures
from backend import Generate, CustomError
from bs4 import BeautifulSoup
from colorama import Fore

colorama.init(autoreset=True)
PLUS = f"[{Fore.GREEN}+{Fore.RESET}] "
MINUS = f"[{Fore.RED}-{Fore.RESET}] {Fore.LIGHTRED_EX}"
try:
    ctypes.windll.kernel32.SetConsoleTitleW("BitAnime")
except (AttributeError):
    pass


def js0nime():
    while True:
        print(
            f""" {Fore.LIGHTBLUE_EX}
                         _  _____  ___  _   _ _                
                        | |/ ____|/ _ \| \ | (_)               
                        | | (___ | | | |  \| |_ _ __ ___   ___ 
                    _   | |\___ \| | | | . ` | | '_ ` _ \ / _ \\
                   | |__| |____) | |_| | |\  | | | | | | |  __/
                    \____/|_____/ \___/|_| \_|_|_| |_| |_|\___|
                              {Fore.LIGHTYELLOW_EX}
                                  By: sh1nobu
                  Github: https://github.com/sh1nobuu/JS0Nime
    """
        )
        while True:
            name = input(f"{PLUS}Enter anime name > ").lower()
            if "-" in name:
                title = name.replace("-", " ").title().strip()
            else:
                title = name.title().strip()
            source = f"https://gogoanime.pe/category/{name}"
            with req.get(source) as res:
                if res.status_code == 200:
                    soup = BeautifulSoup(res.content, "html.parser")
                    all_episodes = soup.find("ul", {"id": "episode_page"})
                    all_episodes = int(all_episodes.get_text().split("-")[-1].strip())
                    break
                else:
                    print(f"{MINUS}Error 404: Anime not found. Please try again.")
        while True:
            quality = input(
                f"{PLUS}Enter episode quality (1.SD/360P|2.HD/720P|3.FULLHD/1080P) > "
            )
            if quality == "1" or quality == "":
                episode_quality = "SDP"
                break
            elif quality == "2":
                episode_quality = "HDP"
                break
            elif quality == "3":
                episode_quality = "FullHDP"
                break
            else:
                print(f"{MINUS}Invalid input. Please try again.")
        print(f"{PLUS}Title: {Fore.LIGHTCYAN_EX}{title}")
        print(f"{PLUS}Episode/s: {Fore.LIGHTCYAN_EX}{all_episodes}")
        print(f"{PLUS}Quality: {Fore.LIGHTCYAN_EX}{episode_quality}")
        print(f"{PLUS}Link: {Fore.LIGHTCYAN_EX}{source}")
        folder = os.path.join(os.getcwd(), title)
        if not os.path.exists(folder):
            os.mkdir(folder)

        choice = "y"

        if all_episodes != 1:
            while True:
                choice = input(
                    f"{PLUS}Do you want to generate all episode? (y/n) > "
                ).lower()
                if choice in ["y", "n"]:
                    break
                else:
                    print(f"{MINUS}Invalid input. Please try again.")

        episode_start = None
        episode_end = None

        if choice == "n":
            while True:
                try:
                    episode_start = int(input(f"{PLUS}Episode start > "))
                    episode_end = int(input(f"{PLUS}Episode end > "))
                    if episode_start <= 0 or episode_end <= 0:
                        CustomError(
                            f"{MINUS}episode_start or episode_end cannot be less than or equal to 0"
                        ).print_error()
                    elif episode_start >= all_episodes or episode_end > all_episodes:
                        CustomError(
                            f"{MINUS}episode_start or episode_end cannot be more than {all_episodes}"
                        ).print_error()
                    elif episode_end <= episode_start:
                        CustomError(
                            f"{MINUS}episode_end cannot be less than or equal to episode_start"
                        ).print_error()
                    else:
                        break
                except ValueError:
                    print(f"{MINUS}Invalid input. Please try again.")

        episode_start = episode_start if episode_start is not None else 1
        episode_end = episode_end if episode_end is not None else all_episodes

        download = Generate(
            name,
            title,
            episode_quality,
            folder,
            all_episodes,
            episode_start,
            episode_end,
        )

        source = f"https://gogoanime.pe/{name}"
        with req.get(source) as res:
            soup = BeautifulSoup(res.content, "html.parser")
            episode_zero = soup.find("h1", {"class": "entry-title"})  # 404

        if choice == "n" or episode_zero is not None:
            source = None

        episode_links = download.get_links(source)
        with concurrent.futures.ThreadPoolExecutor() as exec:
            download_links = list(exec.map(download.get_download_links, episode_links))
            download_urls = dict(exec.map(download.get_download_urls, download_links))
        print(
            f"{PLUS}Generating {Fore.LIGHTCYAN_EX}{len(download_urls)}{Fore.RESET} episode/s"
        )

        print(download.episodes_to_json(download_urls))

        try:
            os.startfile(folder)
        except (AttributeError):
            import sys, subprocess

            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, folder])
        use_again = input(f"{PLUS}Do you want to use the app again? (y|n) > ").lower()
        if use_again == "y":
            os.system("cls")
        else:
            break


if __name__ == "__main__":
    js0nime()
