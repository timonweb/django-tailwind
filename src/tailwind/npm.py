import subprocess
import sys


class NPMException(Exception):
    pass


class NPM:
    cwd = None
    npm_bin_path = None

    def __init__(self, cwd=None, npm_bin_path=None):
        self.npm_bin_path = npm_bin_path
        self.cwd = cwd

    def cd(self, cwd):
        self.cwd = cwd

    def command(self, *args):
        try:
            npm_bin = [self.npm_bin_path] if self.npm_bin_path else [sys.executable, "-m", "nodejs.npm"]
            subprocess.run(npm_bin + list(args), cwd=self.cwd)
            return True
        except OSError:
            raise NPMException(
                "\nIt looks like node.js and/or npm is not installed or cannot be found.\n\n"
                "Visit https://nodejs.org to download and install node.js for your system.\n\n"
                "If you have npm installed and still getting this error message, "
                "set NPM_BIN_PATH variable in settings.py to match path of NPM executable in your system.\n\n"
                ""
                "Example:\n"
                'NPM_BIN_PATH = "/usr/local/bin/npm"'
            )
