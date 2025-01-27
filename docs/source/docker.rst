====================================
Running in Docker (Development mode)
====================================

You can find a Docker example under the ``example`` directory.

Check the included ``example/Dockerfile`` and ``example/docker-compose.yml`` for more information.

Here’s how to start the ``example`` project via Docker:

#. Go into the ``example`` directory;

   .. code-block:: bash

      cd example

#. Build containers via ``docker-compose``:

   .. code-block:: bash

      docker-compose build

#. Start containers:

   .. code-block:: bash

      docker-compose up -d

#. Open `http://localhost:8000 <http://localhost:8000>`_ in a browser. You should see the main page.
