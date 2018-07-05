# Image Processing Sample Code

Study sample code to learn how to use Image Processing API via RICOH Cloud SDK for Python.

## How to Use

### Setup

Install required libraries.

```sh
$ pip install .
```

Rename `template.config.json` to `config.json` and set your valid Client Credentials to the file.

### Gaussian Filter

```sh
$ python gaussian_filter.py -f <FILE_PATH> \
                            -t <LOCATION_TOP> \
                            -r <LOCATION_RIGHT> \
                            -b <LOCATION_BOTTOM> \
                            -l <LOCATION_LEFT> \
                            --ksize_width <KSIZE_WIDTH> \
                            --ksize_height <KSIZE_HEIGHT> \
                            --sigma_x <SIGMA_X> \
                            --sigma_y <SIGMA_Y>
```

### Human Detection and Blur Filter

```sh
$ python human_detection_and_blur_filter.py -f <FILE_PATH> \
                                            --ksize_width <KSIZE_WIDTH> \
                                            --ksize_height <KSIZE_HEIGHT>
```


### Human Detection and Face Detection and Gaussian Filter

```sh
$ python human_detection_and_face_detection_and_gaussian_filter.py -f <FILE_PATH> \
                                                                   --ksize_width <KSIZE_WIDTH> \
                                                                   --ksize_height <KSIZE_HEIGHT> \
                                                                   --sigma_x <SIGMA_X> \
                                                                   --sigma_y <SIGMA_Y>
```

See [Image Processing API Developer Guide](https://api.ricoh/docs/ricoh-cloud-api/image-processing/) for more information.
