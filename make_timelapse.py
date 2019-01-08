#!/usr/bin/python
from datetime import date, timedelta
import cv2
import os
import shutil
import sys
import cli_utils
import numpy as np

def make(today, output_fps):

    # Check arguments for custom date
    custom_date = cli_utils.get_cli_arg("--date")
    if custom_date is None and today:
        custom_date = date.today().strftime("%Y-%m-%d")

    if custom_date is None:
        # Get yesterday's snapshots
        yesterday = date.today() - timedelta(1)
        source_date = yesterday.strftime("%Y-%m-%d")
    else:
        # Get snapshots for specified date
        source_date = custom_date

    # Determine source directory
    absolute_script_dir = os.path.dirname(os.path.realpath(__file__))
    source_dir = absolute_script_dir + '/snapshots/' + source_date

    if not os.path.exists(source_dir):
        print("Error: Source directory does not exist: {}".format(source_dir))
        sys.exit(1)

    # Determine save location for timelapse video
    save_dir = absolute_script_dir + '/timelapses'
    save_path = save_dir + '/' + source_date + '.mp4'

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Delete any empty image files that were created in error
    for imageFile in os.listdir(source_dir):
        if os.path.getsize(source_dir + "/" + imageFile) == 0:
            os.remove(source_dir + "/" + imageFile)

    # Create timelapse and save
    images = [img for img in os.listdir(source_dir) if not img.startswith('.') ]
    images.sort()
    frame = cv2.imread(source_dir+ "/"+images[0])
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(save_path, fourcc, output_fps, (width, height ))

    for image in images:
        img = cv2.imread(os.path.join(source_dir, image))

        # Shape of image in terms of pixels.
        # (rows, cols) = img.shape[:2]
        # M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -90, 1)
        # res = imutils.rotate(img, -90)
        # res = cv2.warpAffine(img, M, (cols, rows))
        # src = cv2.transpose(cv2.imread(os.path.join(source_dir, image)))
        # src = cv2.flip(src,flipCode=0)
        video.write(img)

    video.release()

    # Ensure timelapse was generated successfully
    if not os.path.exists(save_path):
        print("Error: Failed to generate timelapse video file.")
        sys.exit(2)

    # Delete source images if desired
    if cli_utils.has_cli_arg("--cleanup"):
        shutil.rmtree(source_dir)
    print(save_path)
    return save_path
def main():
    print(make(today=cli_utils.has_cli_arg("--today"), output_fps = float(cli_utils.get_cli_arg_with_default("--fps", 5.0))))


if __name__ == "__main__":
    main()
