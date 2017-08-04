# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

""" face detection sample """
from __future__ import print_function

import os
import json
import argparse
from PIL import Image, ImageDraw
from ricohcloudsdk.auth.client import AuthClient
from ricohcloudsdk.vrs.client import VisualRecognition


class FaceRecognitionSample(object):
    """ face recognition sample """

    def __init__(self):
        """ read config file and initialize auth client """
        with open('./config.json', 'r') as settings:
            config = json.load(settings)
            client_id = config['CLIENT_ID']
            client_secret = config['CLIENT_SECRET']

        self.auth_client = AuthClient(client_id, client_secret)
        self.vrs_client = VisualRecognition(self.auth_client)

    @staticmethod
    def __draw_rect(face, draw):
        top = face['location']['top']
        left = face['location']['left']
        right = face['location']['right']
        bottom = face['location']['bottom']
        draw.rectangle(((left, top), (right, bottom)),
                       outline=(255, 0, 0), fill=None)

    def show_result(self, src_img, tar_img, source_path, target_path):
        """ call face recognition API and show the processed image """
        resp = self.vrs_client.compare_faces(source_path, target_path)
        src_draw = ImageDraw.Draw(src_img)
        FaceRecognitionSample.__draw_rect(resp['source'], src_draw)
        tar_draw = ImageDraw.Draw(tar_img)
        FaceRecognitionSample.__draw_rect(resp['target'], tar_draw)
        if not os.path.exists('./results'):
            os.mkdir('./results')
        src_img.save('./results/face_recognition_source.jpg', quality=90)
        tar_img.save('./results/face_recognition_target.jpg', quality=90)
        print('score: {0}'.format(resp['score']))

    def main(self):
        """ main """
        parser = argparse.ArgumentParser(description='face recognition sample')
        parser.add_argument('-s', '--source', type=str, dest='source_path',
                            help='specify image file (JPEG or PNG) to process')
        parser.add_argument('-t', '--target', type=str, dest='target_path',
                            help='specify image file (JPEG or PNG) to process')

        args = parser.parse_args()
        if args.source_path is None or args.target_path is None:
            parser.print_help()
            return
        try:
            src_img = Image.open(args.source_path)
            tar_img = Image.open(args.target_path)
        except IOError:
            raise

        self.show_result(src_img, tar_img, args.source_path, args.target_path)


if __name__ == '__main__':
    FaceRecognitionSample().main()
