#!/bin/bash
ffmpeg -re -stream_loop -1 -i /root/video-flag.mp4 -vcodec libx264 -preset:v ultrafast -acodec aac -f flv rtmp://localhost:1935/coucou/toi
