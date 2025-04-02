# Running in Docker (Development mode)

You can find a Docker example under the `example` directory.

Check the included `example/Dockerfile` and `example/docker-compose.yml` for more information.

Here's how to start the `example` project via Docker:

1. Navigate to the `example` directory:

   ```bash
   cd example
   ```

2. Build the containers using `docker-compose`:

   ```bash
   docker-compose build
   ```

3. Start the containers:

   ```bash
   docker-compose up
   ```

4. Open `http://localhost:8000` in a browser. You should see the main page.
