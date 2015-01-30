ffmpeg -ss 00:12:00 -i student.mp4 -s 480x270 -c:v libx264 -crf 20 -maxrate 300K -bufsize 500K -acodec copy  -t 00:10:00 s.mp4
