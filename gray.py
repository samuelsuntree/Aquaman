import moviepy.editor as mp

# Load the video
video_path = "input.mp4"  # 替换为你的输入视频文件路径
video = mp.VideoFileClip(video_path)

# Convert to grayscale
gray_video = video.fx(mp.vfx.blackwhite)

# Save the result
output_path = "20240112_f57_crop1.mp4"  # 替换为你希望保存的输出文件路径
gray_video.write_videofile(output_path, codec='libx264')
