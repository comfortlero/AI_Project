
'''
        Extract Data as script:

            run this scirpt by usage:
                python3 ./extract_data.py [OPTIONS]

                OPTIONS:

                    --video_path='../your/path/to/file/' this must end with a /

                    --image_resize=size this must be a int with only a single value **defaults to 416**

                    --dataframe_path='../path/to/dataframe.pkl' this must also end with either \\ or / **defaults to current directory**

                    --use_video=True allow for extraction via video files **defaults to True, use False if you cant do mp4 videos or avi**

        File Naming Convention:

            You MUST include the class feature within the video/image. if there are multiple in the same frame or video, besure to use the following formats:

                USAGE:

                    EACH file descriptor WILL be underscore '_' serarated or this script will fail you.

                    Single class per image/video:

                        className.mp4

                            --className non space seperated all anycase string the will match to the class features list we have exactly.

                    Multi-class per image/video:

                        N_ClassName1_className2_classNameN.mp4

                            --N will be the number of classes represented in the video/picture
                            --classNameN will be an exact naming convention of a class feature


        Notes:

            Please make sure you have your videos saved in .mp4 or .avi formats...unsure if other formats will work.

            If you cannot record in .avi or .mp4 formats please save images in the following formats:

                Windows bitmaps - *. bmp, *. dib (always supported)
                JPEG files - *. jpeg, *. ...
                JPEG 2000 files - *. jp2 (see the Notes section)
                Portable Network Graphics - *. png (see the Notes section)
                Portable image format - *. pbm, *. ...
                Sun rasters - *. sr, *. ...
                TIFF files - *. tiff, *.

    '''
import subprocess
import os
import sys
def install_requirements(file_path):
    '''
        predefined subprocess that will install required files for the program to run
    '''
    subprocess.call(['sudo','apt-get','install','software-properties-common'])
    subprocess.call(['sudo','apt-add-repository','universe'])
    subprocess.call(['sudo','apt-get','update'])
    subprocess.call(['sudo', 'apt-get','install', 'python3-pip'])
    subprocess.call(['sudo','apt-get','install','python-pip'])
    subprocess.call(['sudo','apt-get','install','python3-opencv'])
    subprocess.call(['sudo','apt-get','update'])
    subprocess.call(['pip3', 'install', '-r', file_path+'requirements.txt'])
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--video_path', dest='video_path', type=str, default=None, help='provide a path to directory (folder) with the raw videos')
parser.add_argument('--image_resize', dest='image_resize', type=int, default=416, help='provide a tupe (height, width) for the image resize')
parser.add_argument('--dataframe_path', dest='dataframe_path', type=str, default='', help='provide a path to directory (folder) that has the pickled dataframe')
parser.add_argument('--use_video', dest='use_video', type=bool, default=True, help='will extract video frames else it will process images saved in directory')
parser.add_argument('--requirements_path', dest='requirements_path', type=str, default='', help='this will be a path to requirements.txt file, will intall needed packages')
args = parser.parse_args()
if not os.path.exists(args.requirements_path+'requirements.txt'):
    print('Requirements.txt file is missing')
    sys.exit(1)
install_requirements(args.requirements_path)
#######################################################################################################################################################################################
#
#                                                               POST REQUIREMENTS INSTALL SECTION
#
########################################################################################################################################################################################
from utils.Config import *
import cv2
import pandas as pd
import tqdm
from tqdm import trange

def extract_video(config):
    '''
        This will be the primary function to handle the frame extractions.

        Params:

            --config this will be the config utility object created on initial run, it will handle loading and saving

        Return:

            str() a string object for the use of displaying to stdout the completion of this function/program

        Notes:
            I added a tqdm process monitor for visuals during the extraction process
            and it will be sending that progress to stdout

            I have this setup to only capture and save every 10th frame, can change later if we need more data.

    '''
    total = len(config.list_of_files)
    for video_idx in trange(total, file=sys.stdout, desc='Videos Processed'):
        video = config.list_of_files[video_idx]
        video_name = config.get_video_name(video)
        capture = cv2.VideoCapture(video)
        frame_num = 0
        while capture.isOpened():
            ret, frame = capture.read()
            if not ret:
                break
            if frame_num % 10 == 0:
                config.save_frame(video_idx, video_name, frame, frame_num)
            frame_num += 1
        capture.release()
        cv2.destroyAllWindows()
    return '\n\n\tCompleted processing all '+str(total)+' videos successfully!\n'

def extract_pictures(config):
    return str()

if __name__ == '__main__':
    config = Config(parser, args)
    if args.use_video:
        output = extract_video(config)
    else:
        output = extract_pictures(config)
    config.save_data()
    print(output)
