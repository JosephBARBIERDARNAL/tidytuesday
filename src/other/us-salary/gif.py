from gifing import GIF

path = [f"src/other/us-salary/temp/{x}.png" for x in range(1, 115 + 1)]

gif = GIF(path, frame_duration=125, n_repeat_last_frame=80)
gif.set_size((1200, 800), scale=2)
gif.make("src/other/us-salary/gifing.gif")
