"""

A python based OSU beatmap file (.osu) parser

Usage: OSUFile("path/to/*.osu"[, dec_hit_objects: bool=False])
"""

import os
from typing import NoReturn, TextIO

DEFAULT_GENERAL = {"AudioLeadIn": 0, "PreviewTime": -1, "Countdown": 1,
                   "SampleSet": "Normal", "StackLeniency": 0.7, "Mode": 0,
                   "LetterboxInBreaks": 0, "StoryFireInFront": 1,
                   "UseSkinSprites": 0, "AlwaysShowPlayfield": 0,
                   "OverlayPosition": "NoChange", "EpilepsyWarning": 0,
                   "CountdownOffset": 0, "SpecialStyle": 0,
                   "WidescreenStoryboard": 0, "SamplesMatchPlaybackRate": 0}

OSU_HEADER = "osu file format "


class OSUFile:
    version: int = 14
    General: dict = DEFAULT_GENERAL
    Editor: dict = {}
    Metadata: dict = {}
    Difficulty: dict = {}
    Events: list = []
    TimingPoints: list = []
    HitObjects: list = []

    def __str__(self):
        return f"{self.Metadata['Title']} By {self.Metadata['Artist']} Mapper: {self.Metadata['Creator']} \
        BeatmapSet: {self.Metadata['BeatmapSetID']}/{self.Metadata['BeatmapID']}"

    def __init__(self, file: str = "", dec_hit: bool = False):
        if file is None:
            return

        try:
            if os.path.isfile(file):
                with open(file, "r") as f:
                    self.file_handler(f, dec_hit)
            else:
                raise ValueError("Input not a file.")
        except TypeError:
            raise TypeError("Input not a file path.")

    def file_handler(self, file: TextIO, dec_hit=False):
        if not self._is_osu_file(file):
            raise ValueError("Input file is not a OSU beatmap file.")

        tmp = []
        blocks = []

        ver = file.readlines()[0].lstrip(f"{OSU_HEADER}v").rstrip("\n")
        self.version = int(ver)

        file.seek(len(f"{OSU_HEADER}v{ver}\r\n\r\n"), 0)

        lines = file.readlines()
        for i, line in enumerate(lines):
            if line == "\n":
                if lines[i + 1].rstrip("\n") in self.OSU_PARSERS.keys():
                    blocks.append(tmp)
                    tmp = []

                continue

            tmp.append(line.rstrip("\n"))

        for block in blocks:
            self.OSU_PARSERS[block[0]](self, block)

        else:
            if dec_hit:
                self.hit_objects_decoder()

    @staticmethod
    def _key_value_handler(text: str) -> list:
        kvlist = []
        if ": " in text:
            kvlist = text.split(": ", 1)

        elif ":" in text:
            kvlist = text.split(":", 1)

        return kvlist

    @staticmethod
    def _is_osu_file(file) -> bool:
        file.seek(0, 0)
        # whether is a text file
        try:
            file.read()
        except UnicodeDecodeError:
            return False

        file.seek(0, 0)
        # whether contain OSU header
        try:
            if OSU_HEADER not in file.readlines()[0]:
                return False
        except Exception:
            return False

        file.seek(0, 0)
        return True

    def general_handler(self, text: list[str]) -> NoReturn:
        for line in text[1::]:
            kv = self._key_value_handler(line)
            if kv[1].isdigit():
                kv[1] = int(kv[1])

            elif "." in kv[1]:
                for digit in kv[1].split(".", 1):
                    if not digit.isdigit():
                        break

                else:
                    kv[1] = float(kv[1])

            elif kv[0] in ["LetterboxInBreaks", "StoryFireInFront", "UseSkinSprites", "AlwaysShowPlayfield",
                           "EpilepsyWarning", "SpecialStyle", "WidescreenStoryboard", "SamplesMatchPlaybackRate"]:
                kv[1] = bool(kv[1])

            self.General[kv[0]] = kv[1]

    def editor_handler(self, text: list[str]) -> NoReturn:
        for line in text[1::]:
            kv = self._key_value_handler(line)
            if kv[1].isdigit():
                kv[1] = int(kv[1])

            elif "." in kv[1]:
                for digit in kv[1].split(".", 1):
                    if not digit.isdigit():
                        break

                else:
                    kv[1] = float(kv[1])

            elif "," in kv[1]:
                kv[1] = kv[1].split(",")

            self.Editor[kv[0]] = kv[1]

    def metadata_handler(self, text: list[str]) -> NoReturn:
        for line in text[1::]:
            kv = self._key_value_handler(line)
            if kv[1].isdigit():
                kv[1] = int(kv[1])

            self.Metadata[kv[0]] = kv[1]

    def difficulty_handler(self, text: list[str]) -> NoReturn:
        for line in text[1::]:
            kv = self._key_value_handler(line)
            self.Difficulty[kv[0]] = float(kv[1])

    def events_handler(self, text: list[str]) -> NoReturn:
        for line in text[1::]:
            event_list = line.split(",")
            self.Events.append(event_list)

    def timing_points_handler(self, text: list[str]) -> NoReturn:
        for line in text[1::]:
            timing_point = line.split(",")
            for i, point in enumerate(timing_point):
                if point.isdigit():
                    timing_point[i] = int(timing_point[i])

                elif "." in point:
                    for digit in point.split(".", 1):
                        if not digit.isdigit():
                            break

                    else:
                        timing_point[i] = float(timing_point[i])

                if i == 6:
                    timing_point[i] = bool(timing_point[i])

            self.TimingPoints.append(timing_point)

    def hit_objects_handler(self, text: list[str]) -> NoReturn:
        for line in text[1::]:
            self.HitObjects.append(line)

    def hit_objects_decoder(self) -> NoReturn:
        pass

    OSU_PARSERS = {"[General]": general_handler, "[Editor]": editor_handler,
                   "[Metadata]": metadata_handler, "[Difficulty]": difficulty_handler,
                   "[Events]": events_handler, "[TimingPoints]": timing_points_handler,
                   "[HitObjects]": hit_objects_handler}
