import os
import tempfile

from tailwind.utils import extract_host_and_port
from tailwind.utils import extract_protocol_from_command
from tailwind.utils import extract_server_url_from_procfile


def test_extract_protocol_from_command():
    """
    GIVEN various commands with and without SSL flags
    WHEN extract_protocol_from_command is called
    THEN it should return the appropriate protocol
    """
    assert extract_protocol_from_command("python manage.py runserver") == "http"
    assert extract_protocol_from_command("python manage.py runserver --ssl") == "https"
    assert extract_protocol_from_command("python manage.py runserver --secure") == "https"
    assert extract_protocol_from_command("python manage.py runserver --https") == "https"
    assert extract_protocol_from_command("python manage.py runserver --cert cert.pem") == "https"
    assert (
        extract_protocol_from_command("python manage.py runserver --ssl --cert cert.pem") == "https"
    )
    assert extract_protocol_from_command("") == "http"
    assert (
        extract_protocol_from_command("python manage.py runserver --settings=ssl_settings.py")
        == "http"
    )


def test_extract_host_and_port():
    """
    GIVEN various commands with different host and port configurations
    WHEN extract_host_and_port is called
    THEN it should return the appropriate host and port
    """
    assert extract_host_and_port("python manage.py runserver") == ("127.0.0.1", "8000")
    assert extract_host_and_port("python manage.py runserver 55555") == ("127.0.0.1", "55555")
    assert extract_host_and_port("python manage.py runserver 192.168.1.1:3000") == (
        "192.168.1.1",
        "3000",
    )
    assert extract_host_and_port("python manage.py runserver localhost:9000") == (
        "localhost",
        "9000",
    )
    assert extract_host_and_port("python manage.py runserver [::1]:8080") == ("::1", "8080")
    assert extract_host_and_port("python manage.py runserver 0.0.0.0:8000") == ("0.0.0.0", "8000")
    assert extract_host_and_port("python manage.py runserver 127.0.0.1:8000 --noreload") == (
        "127.0.0.1",
        "8000",
    )
    assert extract_host_and_port(
        "python manage.py runserver --settings=app.settings:dev 127.0.0.1:8000"
    ) == (
        "127.0.0.1",
        "8000",
    )
    assert extract_host_and_port("") == ("127.0.0.1", "8000")


def test_extract_server_url_from_procfile():
    """
    GIVEN various Procfile contents
    WHEN extract_server_url_from_procfile is called
    THEN it should return the appropriate server URL or None
    """
    # Happy path: django and tailwind processes
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("django: python manage.py runserver 127.0.0.1:8000\ntailwind: npm run dev\n")
        f.flush()
        assert extract_server_url_from_procfile(f.name) == "http://127.0.0.1:8000/"
        os.unlink(f.name)

    # No django process present
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("tailwind: npm run dev\nworker: python worker.py\n")
        f.flush()
        assert extract_server_url_from_procfile(f.name) is None
        os.unlink(f.name)
