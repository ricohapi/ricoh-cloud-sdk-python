# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ricoh Co., Ltd. All Rights Reserved.

"""Delete collection sample."""
import os
import shutil
from vr_utils import create_vrs_client, get_collection_id, ClientError


def delete_collection():
    """Delete collection and local images."""
    vrs_client = create_vrs_client()
    collection_id = get_collection_id(vrs_client)
    vrs_client.delete_collection(collection_id)
    save_dir = './results/{0}'.format(collection_id)
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)


def main():
    try:
        delete_collection()
    except ClientError as error:
        print(error.message)


if __name__ == '__main__':
    main()
