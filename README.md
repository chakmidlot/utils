# utils
Small util scripts


## slicer-mixer.py 
python 3.6

Slices a movie into pices, mixes them and joins back to one file.
```
slicer-mixer.py [-h] -i INPUT_VIDEO [-w WORKDIR] [-t PART_SIZE]

  -i INPUT_VIDEO, --input_video INPUT_VIDEO
                        path to input video
  -w WORKDIR, --workdir WORKDIR
                        directory for saving movie parts and result video
  -t PART_SIZE, --part-size PART_SIZE
                        size of video parts in seconds
```
`ffmpeg` and `ffprobe` are required
