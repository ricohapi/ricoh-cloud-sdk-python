# Visual Recognition Sample Code

Study sample code to learn how to use Visual Recognition API via RICOH Cloud SDK for Python.

## How to Use

### Setup

Install required libraries.

```sh
$ pip install pillow
```

Rename `template.config.json` to `config.json` and set your valid Client Credentials to the file.

### Face Detection and Human Detection

Face Detection sample and Human Detection sample detect faces or people in specified images and generate new images in the `results` folder. Face Detection sample generates a new image with a mark to show where in specified image it has detected faces. Human Detection sample generates one to show where it has detected people.

Run the following commands specifying your local image path to `<image>`. You cannot use URIs to locate images for these code samples. The image formats supported by Visual Recognition API are JPEG and PNG.

```sh
# Face Detection sample
$ python face_detection.py -f <image>

# Human Detection sample
$ python human_detection.py -f <image>
```

### Face Recognition

Face Recognition sample compares two faces in specified images to return the similarity score to standard output. At the same time, it also creates new images with marks to show which part of the images it has used for comparison.

Run the following commands specifying your local image paths to `<source_image>` and `<target_image>`. You cannot use URIs to locate images for this code sample. The supported image formats are same as above.

```sh
$ python face_recognition.py -s <source_image> \
                             -t <target_image>
```

#### Using face collection

You can add face in face collection and compare face using face collection.

This sample detects the face from the specified image and adds it to the face collection. If no face collection has been created, it will be created automatically. When the face is successfully added to the face collection, generates a new image with marks to show which part of the image it has detected face.

Run the following commands specifying your local image path to `<image>`. You cannot use URIs to locate images for this code sample. The supported image formats are the same as above.

```sh
$ python add_face_to_collection.py -f <image>
```

This sample compares the face to the face collection to return the similarity score to standard output. At the same time, it also creates new images with marks to show which part of the images it has used for comparison.

Run the following commands specifying your local image path to `<image>`. You cannot use URIs to locate images for this code sample. The supported image formats are the same as above.

```sh
$ python compare_face_to_collection.py -f <image>
```

To remove the face from the face collection, use the following sample. Run the following commands specifying ID of the face to `<face_id>`. Images stored locally will also be deleted.

```sh
$ python remove_face_from_collection.py --face_id <face_id>
```

To delete the face collection, use the following sample. Run the following commands. Images stored locally will also be deleted.

```sh
$ python delete_collection.py
```

See [Visual Recognition API Developer Guide](https://api.ricoh/docs/ricoh-cloud-api/visual-recognition/) for more information.
