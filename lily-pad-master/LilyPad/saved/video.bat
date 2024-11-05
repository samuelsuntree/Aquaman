ffmpeg -framerate 30 -i frame-%04d.png -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4
