# Running in Docker

You can find Docker example under `example` directory.

Check included `example/Dockerfile` and `example/docker-compose.yml` for more information.

Here's how to start `example` project via Docker:

1. Go into `example` directory;

    ```bash
    cd example
    ```

2. Build containers via `docker-compose`:

    ```bash
    docker-compose build
    ```

3. Start containers:

    ```bash
    docker-compose up
    ```

4. Open `http://localhost:8000` in a browser. You should see the main page.   
