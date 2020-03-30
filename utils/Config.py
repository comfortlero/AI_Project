import argparse
import pandas as pd
import numpy as np
import pickle
import sys
import os
import cv2

class Config:

    def __init__(self, parser, args):
        '''
            The config class will be used as a helper class object

            Params:

                --parser a argparser.ArgumentParser() object from extract_data.py main
                --args parsed arguments from parser object that were extracted from command line stdin


            Notes:
                This helper object will be to handle all data/saves/loads/updates/errors
        '''
        self.args = args
        self.video_path = args.video_path
        self.image_resize = (args.image_resize, args.image_resize)
        self.dataframe_path = args.dataframe_path
        self.df = pickle.load(open(self.dataframe_path+'dataframe.pkl', 'rb'))
        self.uid = self.df.size+1
        self.use_video = args.use_video
        if not self.is_argument_integrity_valid():
            parser.print_usage()
            sys.exit(1)
        print(os.listdir(self.video_path))
        self.list_of_files = [self.video_path+video_name for video_name in os.listdir(self.video_path)]

    def save_data(self):
        with open(self.dataframe_path+'dataframe.pkl', 'wb') as f:
            pickle.dump(self.df, f)

    def get_video_name(self, video_name):
        if '\\' in video_name:
            return (video_name.split('\\')[-1]).spit('.')[0]
        else:
            return (video_name.split('/')[-1]).split('.')[0]
    
    def save_frame(self, video_num, video_name, frame, frame_num):
        resized_frame = cv2.resize(frame, self.image_resize)
        flattened = resized_frame.flatten()
        data = {'pixel_'+str(idx) : [flattened[idx]] for idx in range(416*416*3)}
        data['id'] = [video_num + self.uid + frame_num]
        self.df = pd.concat([self.df, pd.DataFrame(data)])
        self.uid += 1

    def is_argument_integrity_valid(self):
        '''
            Ensuring that the command line arguments followed the proper pattern was followed
                or it will spit out the argparser usage message and terminate the program
        '''
        if self.video_path is None:
            print(0)
            return False
        elif self.video_path[-1] is not '/':
            print(1)
            return False
        else:
            return True
    
