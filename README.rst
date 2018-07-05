=========
RICOH Cloud SDK for Python
=========

Python client library for RICOH Cloud API.

------------
Installation
------------
::

  $ git clone https://github.com/ricohapi/ricoh-cloud-sdk-python.git
  $ cd ricoh-cloud-sdk-python
  $ pip install .

You can also download the SDK in a zip file from https://github.com/ricohapi/ricoh-cloud-sdk-python/releases and unzip it to ``<install_dir>``.

--------
SDK Usage
--------

Auth Constructor
--------------
To use any modules of the RICOH Cloud SDK, initialize ``AuthClient`` with your valid Client Credentials.

::

  from ricohcloudsdk.auth.client import AuthClient
  aclient = AuthClient('<your_client_id>', '<your_client_secret>')


Visual Recognition
------------------
Initialize ``VisualRecognition`` with an ``AuthClient`` object.

::

  from ricohcloudsdk.auth.client import AuthClient
  from ricohcloudsdk.vrs.client import VisualRecognition
  aclient = AuthClient('<your_client_id>', '<your_client_secret>')
  vr_client = VisualRecognition(aclient)

For ``detect_faces()`` and ``detect_humans()``, set either ``<image_uri>`` or ``<image_path>`` as an argument.

::

  vr_client.detect_faces('<image_uri> or <image_path>')
  vr_client.detect_humans('<image_uri> or <image_path>')

For ``compare_faces()``, set two arguments; one for source image location and the other for target image or face collection location.

Compare faces in two images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to make sure that those two arguments are a pair of URIs OR a pair of paths. You cannot set a URI and a path at the same time.

::

  vr_client.compare_faces('<source_image_uri> or <source_image_path>', '<target_image_uri> or <target_image_path>')


Compare faces to collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to make sure the source URI or path as the first argument and the second argument is collection_id.

::

  vr_client.compare_faces('<source_image_uri> or <source_image_path>', '<target_face_collection_id>')

``create_collection()``, ``list_collections()``, and ``delete_collection()`` handle face collections.

::

  vr_client.create_collection()
  vr_client.list_collections()
  vr_client.delete_collection('<face_collection_id>')


``add_face()``, ``list_faces()``, and ``remove_face()`` handle face.

::

  vr_client.add_face('<image_uri> or <image_path>', '<face_collection_id>')
  vr_client.list_faces('<face_collection_id>')
  vr_client.remove_face('<face_collection_id>', '<face_id>')



Image Processing
------------------
Initialize ``ImageProcessing`` with an ``AuthClient`` object.

::

  from ricohcloudsdk.auth.client import AuthClient
  from ricohcloudsdk.ips.client import ImageProcessing
  aclient = AuthClient('<your_client_id>', '<your_client_secret>')
  ip_client = ImageProcessing(aclient)

For ``filter()``, set two arguments; one for source image location and the other for parameters.

::

  parameters = {
    'locations': [
      {'left': 226, 'top': 227, 'right': 387, 'bottom': 387}
    ],
    'type': 'gaussian',
    'options': {
      'locations': {
        'shape': 'min_enclosing_circle',
        'edge': 'blur'
      },
      'ksize_width': 3,
      'ksize_height': 3,
      'sigma_x': 0,
      'sigma_y': 0
    }
  }
  ip_client.filter('<source_image_uri> or <source_image_path>', parameters)

For more information about parameters, see `RICOH Cloud API Developer Guide <https://api.ricoh/docs/ricoh-cloud-api/image-processing/>`_.

--------
Sample Codes
--------

- `Visual Recognition Sample Code <./samples/visual-recognition/>`_
- `Image Processing Sample Code <./samples/image-processing/>`_

--------
See Also
--------

- `RICOH Cloud API Developer Guide <https://api.ricoh/docs/ricoh-cloud-api/>`_
