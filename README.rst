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

For ``compare_faces()``, set two arguments; one for source image location and the other for target image location.

You need to make sure that those two arguments are a pair of URIs OR a pair of paths. You cannot set a URI and a path at the same time.

::

  vr_client.compare_faces('<source_image_uri> or <source_image_path>', '<target_image_uri> or <target_image_path>')

--------
Sample Codes
--------

- `Visual Recognition Sample Code <./samples/visual-recognition/>`_

--------
See Also
--------

- `RICOH Cloud API Developer Guide <https://api.ricoh/docs/ricoh-cloud-api/>`_
