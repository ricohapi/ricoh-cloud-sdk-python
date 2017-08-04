# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

""" face detection sample """
import os
import json
import argparse
from PIL import Image, ImageDraw
from ricohcloudsdk.auth.client import AuthClient
from ricohcloudsdk.vrs.client import VisualRecognition


class HumanDetectionSample(object):
    """ human detection sample """

    def __init__(self):
        """ read config file and initialize auth client """
        with open('./config.json', 'r') as settings:
            config = json.load(settings)
            client_id = config['CLIENT_ID']
            client_secret = config['CLIENT_SECRET']

        self.auth_client = AuthClient(client_id, client_secret)
        self.vrs_client = VisualRecognition(self.auth_client)

    def show_result(self, pil_img, file_path):
        """ call human detection API and show the processed image """
        draw = ImageDraw.Draw(pil_img)
        res = self.vrs_client.detect_humans(file_path)
        humans_list = res["humans"]
        for human in humans_list:
            top = human['location']['top']
            left = human['location']['left']
            right = human['location']['right']
            bottom = human['location']['bottom']
            draw.rectangle(((left, top), (right, bottom)),
                           outline=(255, 0, 0), fill=None)
        if not os.path.exists('./results'):
            os.mkdir('./results')
        pil_img.save('./results/human_detection.jpg', quality=90)

    def main(self):
        """ main """
        parser = argparse.ArgumentParser(description='Human detection sample')
        parser.add_argument('-f', '--file', type=str, dest='file_path',
                            help='specify image file (JPEG or PNG) to process')
        args = parser.parse_args()
        if args.file_path is None:
            parser.print_help()
            return
        try:
            pil_img = Image.open(args.file_path)
        except IOError:
            raise

        self.show_result(pil_img, args.file_path)


if __name__ == '__main__':
    HumanDetectionSample().main()
