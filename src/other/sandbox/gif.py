import os
from gifing import GIF

dir_path = "src/other/sandbox/temp/"
files = sorted(os.listdir(dir_path), key=lambda x: int(x.split(".")[0]))
files = [os.path.join(dir_path, f) for f in files]
gif = GIF(file_path=files, frame_duration=150, n_repeat_last_frame=30)
gif.set_size((1500, 1600))
gif.set_background_color("#f4f4f9")
gif.make("src/other/sandbox/consumer.gif")
