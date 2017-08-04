# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

""" face detection sample """
import os
import json
import argparse
from PIL import Image, ImageDraw
from ricohcloudsdk.auth.client import AuthClient
from ricohcloudsdk.vrs.client import VisualRecognition


class FaceDetectionSample(object):
    """ face detection sample """

    def __init__(self):
        """ read config file and initialize auth client """
        with open('./config.json', 'r') as settings:
            config = json.load(settings)
            client_id = config['CLIENT_ID']
            client_secret = config['CLIENT_SECRET']

        self.auth_client = AuthClient(client_id, client_secret)
        self.vrs_client = VisualRecognition(self.auth_client)

    def show_result(self, pil_img, img_path):
        """ call face detection API and show the processed image """
        draw = ImageDraw.Draw(pil_img)
        res = self.vrs_client.detect_faces(img_path)
        faces_list = res["faces"]
        for face in faces_list:
            top = face['location']['top']
            left = face['location']['left']
            right = face['location']['right']
            bottom = face['location']['bottom']
            draw.rectangle(((left, top), (right, bottom)),
                           outline=(255, 0, 0), fill=None)
        if not os.path.exists('./results'):
            os.mkdir('./results')
        pil_img.save('./results/face_detection.jpg', quality=90)

    def main(self):
        """ main """
        parser = argparse.ArgumentParser(description='Face detection sample')
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
    FaceDetectionSample().main()
