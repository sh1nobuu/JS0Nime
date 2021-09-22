# Dependencies
import json
import requests as req
import re
import os
from colorama import Fore
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass(init=True)
class Generate:
    name: str
    title: str
    episode_quality: str
    folder: str
    all_episodes: int
    episode_start: int
    episode_end: int
    printed: bool = False

    def get_links(self, source=None) -> list[str]:
        if source is not None:
            source_ep = f"https://gogoanime.pe/{self.name}-episode-"
            episode_links = [
                f"{source_ep}{i}"
                for i in range(self.episode_start, self.episode_end + 1)
            ]
            episode_links.insert(0, source)
        else:
            source_ep = f"https://gogoanime.pe/{self.name}-episode-"
            episode_links = [
                f"{source_ep}{i}"
                for i in range(self.episode_start, self.episode_end + 1)
            ]
        return episode_links

    def get_download_links(self, episode_link) -> list[str]:
        with req.get(episode_link) as res:
            soup = BeautifulSoup(res.content, "html.parser")
            exist = soup.find("h1", {"class": "entry-title"})
            if exist is None:
                # Episode link == 200
                episode_link = soup.find("li", {"class": "dowloads"})
                return episode_link.a.get("href")
            else:
                # Episode link == 404
                episode_link = f"{episode_link}-"
                with req.get(episode_link) as res:
                    soup = BeautifulSoup(res.content, "html.parser")
                    exist = soup.find("h1", {"class": "entry-title"})
                    if exist is None:
                        episode_link = soup.find("li", {"class": "dowloads"})
                        return episode_link.a.get("href")
                    else:
                        return None

    def get_download_urls(self, download_link) -> list[str]:
        with req.get(download_link) as res:
            soup = BeautifulSoup(res.content, "html.parser")
            link = soup.find("div", {"class": "mirror_link"}).find(
                "div",
                text=re.compile(fr"\b{self.episode_quality}\b"),
                attrs={"class": "dowload"},
            )
            if link is None:
                link = soup.find("div", {"class": "mirror_link"}).find(
                    "div", {"class": "dowload"}
                )
                if not self.printed:
                    CustomMessage(None, self.episode_quality).qual_not_found()
                    self.episode_quality = link.text.split()[1][1:]
                    CustomMessage(None, self.episode_quality).use_default_qual()
                    self.printed = True
        return f"Episode {download_link.split('+')[-1]}", link.a.get(
            "href"
        )  # episode_name: str, episode_link: str

    def episodes_to_json(self, episodes):
        episodes_json = {
            "Title": self.title,
            "Quality": self.episode_quality,
            "Episodes": episodes,
        }
        json_file = os.path.join(self.folder, f"{self.name}-episodes.json")
        with open(json_file, "w") as file:
            json.dump(episodes_json, file, ensure_ascii=False, indent=4)
        return f"[{Fore.GREEN}+{Fore.RESET}] File saved in {Fore.LIGHTCYAN_EX}{self.name}-episodes.json{Fore.RESET}"


@dataclass(init=True)
class CustomMessage(Exception):
    """Custom message that will accept message as a parameter and it will print it on the console."""

    message: str = None
    episode_quality: str = None

    def print_error(self) -> str:
        print(self.message)

    def qual_not_found(self) -> str:
        print(
            f"[{Fore.RED}-{Fore.RESET}] {Fore.LIGHTCYAN_EX}{self.episode_quality}{Fore.RESET} quality not found."
        )

    def use_default_qual(self) -> str:
        print(
            f"[{Fore.GREEN}+{Fore.RESET}] Using {Fore.LIGHTCYAN_EX}{self.episode_quality}{Fore.RESET} as a default quality."
        )
