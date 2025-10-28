# Contributing

You're welcome to contribute to this project!

## Bugs and suggestions

If you have found a bug, please use the [issue tracker on GitHub][issues].

[issues]: https://github.com/timonweb/django-tailwind/issues

## Tests

You need UV and Node.js installed to run the tests.

```console
python -m pip install uv
uv sync
```

Install Node.js using nvm (as recommended by the official npm documentation [https://docs.npmjs.com/downloading-and-installing-node-js-and-npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)).
```console
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
source ~/.bashrc   # or ~/.zshrc or ~/.profile depending on your shell
nvm install node
```

```console
uv run pytest
```
