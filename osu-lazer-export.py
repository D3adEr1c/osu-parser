import os
import json
import subprocess

import osu

# set your osu-lazer/files folder
PARENT_DIR = os.path.abspath("../")
DOWNLOAD_DIR = os.path.abspath("../../Songs")
osu_beatmaps = {}


def get_files(path):
    for item in os.listdir(path):
        sub = os.path.join(path, f"{item}")
        if os.path.isdir(sub):
            get_files(sub)
        else:
            file_handler(sub)


def file_handler(file_path):
    print(f"Handling {file_path}")
    try:
        beatmap = osu.OSUFile(file_path)

    except ValueError:
        print("Not a beatmap.")
        return
    except UnicodeDecodeError:
        print("Not a text file.")
        return
    else:
        if beatmap.Metadata["BeatmapSetID"] in osu_beatmaps.keys():
            osu_beatmaps[beatmap.Metadata["BeatmapSetID"]].append(beatmap.Metadata["BeatmapID"])
        else:
            osu_beatmaps[beatmap.Metadata["BeatmapSetID"]] = [beatmap.Metadata["BeatmapID"]]
            subprocess.run(
                ["wget", "-O", f"{DOWNLOAD_DIR}/{beatmap.Metadata["BeatmapSetID"]}.osz",
                 f"https://txy1.sayobot.cn/beatmaps/download/full/{beatmap.Metadata["BeatmapSetID"]}?server=auto"],
                stdout=subprocess.PIPE)


get_files(PARENT_DIR)
with open("beatmaps", "w") as f:
    json.dump(osu_beatmaps, f)
