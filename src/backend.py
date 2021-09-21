# Dependencies
import json
import requests as req
import re
import os
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
        # episode_name: str, episode_link: str
        return f"Episode {download_link.split('+')[-1]}", link.a.get("href")

    def episodes_to_json(self, episodes):
        episodes_json = {
            "Title": self.title,
            "Quality": self.episode_quality,
            "Episodes": episodes,
        }
        json_file = os.path.join(self.folder, f"{self.name}-episodes.json")
        with open(json_file, "w") as file:
            json.dump(episodes_json, file, ensure_ascii=False, indent=4)
        return f"File saved in {self.name}-episodes.json"


@dataclass(init=True)
class CustomError(Exception):
    """Custom exception that will accept message as a parameter and it will print it on the console."""

    message: str

    def print_error(self) -> str:
        print(self.message)
