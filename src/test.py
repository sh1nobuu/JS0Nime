import json


# def create():
#     pass


# episodes_json = {
#     "title": "anime name",
#     "episodes": {
#         "episode name": "episode link",
#         "episode name": "episode link",
#         "episode name": "episode link",
#         "episode name": "episode link",
#         "episode name": "episode link",
#     },
# }


class Create:
    def __init__(self, title):
        self.title = title
        self.episodes_json = {"title": self.title}

    def get_episodes_json(self):
        return self.episodes_json

    def add_to_dict(self, obj):
        self.episodes_json.update({"episodes":obj})
        return self.episodes_json


c = Create("tokyo ghoul")

d = {f"episode-{i}": f"episode-{i}-link" for i in range(1, 10)}

c_json = c.add_to_dict(d)
print(c_json)
