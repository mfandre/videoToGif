import imageio.v3 as iio # pip install imageio | pip install imageio[ffmpeg] | pip install imageio[pyav]
import numpy as np

#######################################################
# The example below only was tested using MP4 videos  #
#######################################################

# make sure it will be the best for your scenario.,.. maybe you will need to improve it!
def get_total_frames(file:str) -> int:
    props = iio.improps(file, plugin="pyav")

    # Make sure the codec knows the number of frames
    assert props.shape[0] != -1

    return props.shape[0]

def extract_Nseconds_into_frames(file:str, n_seconds:int) -> np.ndarray:
    # default is to have 30 frames per second to have a good feel... but change as you wish
    totalframes = get_total_frames(file)
    print(f"Total frames: {totalframes}")

    fps = iio.immeta(file, plugin="pyav")["fps"]
    print(f"Video FPS: {fps}")

    step = int(totalframes / (n_seconds*fps))
    print(f"Step to achieve number of seconds: {step}")

    if step <= 1:
        raise Exception("Your video file dont have frames enough to be extract in desire FPS")

    frames_to_be_extracted = []
    for idx in range(0, totalframes, step):
        frames_to_be_extracted.append(idx)

    print(f"Selected frames (total): {len(frames_to_be_extracted)}")

    img_list = []
    for idx in frames_to_be_extracted:
        img_list.append(iio.imread("imageio:cockatoo.mp4", index=idx))

    print(f"Stacking frames")
    frames = np.stack(img_list, axis=0)

    return frames, fps

def frames_to_gif(gif_path:str, frames:np.ndarray, fps:int):
    print(f"Converting frames into GIF")
    iio.imwrite(gif_path, frames, duration=1/fps/1000)

frames, fps = extract_Nseconds_into_frames("imageio:cockatoo.mp4", 3)
frames_to_gif("cockatoo.gif", frames, fps)


