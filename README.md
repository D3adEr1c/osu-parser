# osu-parser
A python based .osu file parser, writen with python 3.12

# Usage

Download the `osu.py`
```python
import osu

file = osu.OSUFile("/path/to/.osu/file")
```

# Example
```python

# get BeatmapSetID
file.Metadata["BeatmapSetID"]

```
See [osu official wiki](https://osu.ppy.sh/wiki/en/Client/File_formats/osu_%28file_format%29) for more information
Or see `osu-lazer-export.py` - a script to get imported .osz beatmapfile from Internet


# TODO
Add support for hit objects decoding
Add support for events decoding
More method ( `get_info()`)
Edit .osu file
