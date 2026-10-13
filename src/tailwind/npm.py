import subprocess

from tailwind import get_config


class NPMException(Exception):
    def __init__(self, message, returncode=1):
        super().__init__(message)
        self.returncode = returncode


class NPM:
    cwd = None
    npm_bin_path = None

    def __init__(self, cwd=None, npm_bin_path=None):
        self.npm_bin_path = npm_bin_path if npm_bin_path else get_config("NPM_BIN_PATH")
        self.cwd = cwd

    def cd(self, cwd):
        self.cwd = cwd

    def command(self, *args):
        try:
            subprocess.run([self.npm_bin_path, *args], cwd=self.cwd, check=True)
        except subprocess.CalledProcessError as err:
            raise NPMException(
                f"'npm {' '.join(args)}' failed with exit code {err.returncode}.",
                # A process killed by a signal reports a negative code; still exit non-zero.
                returncode=max(err.returncode, 1),
            ) from err
        except OSError as err:
            raise NPMException(
                "\nIt looks like node.js and/or npm is not installed or cannot be found.\n\n"
                "Visit https://nodejs.org to download and install node.js for your system.\n\n"
                "If you have npm installed and still getting this error message, "
                "set NPM_BIN_PATH variable in settings.py to match path of NPM executable in your system.\n\n"
                ""
                "Example:\n"
                'NPM_BIN_PATH = "/usr/local/bin/npm"'
            ) from err
