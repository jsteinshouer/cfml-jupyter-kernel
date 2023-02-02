# Jupyter Kernel for CFML

This is an attempt at creating a Jupyter Kernel for CFML powered by the [CommandBox REPL](https://commandbox.ortusbooks.com/usage/repl). 

It is based on the concept of a [Python wrapper kernel](https://jupyter-client.readthedocs.io/en/latest/wrapperkernels.html). I do not have a lot of experience working in Python so there are probably a lot of things that can be improved here.
## Run on mybinder.org

You can try it out and create CFML notebooks using this link:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jsteinshouer/cfml-jupyter-kernel/main?urlpath=/tree)

## Github Codespaces / Dev Container

You can fork this repo and run it with Github Codespaces or clone the repo and run it locally with the VS Code Dev Containers extension.
## Running with Docker

```bash
docker compose -f ./docker/docker-compose.yml up
```

Go to http://127.0.0.1:8888/lab?token=x to access the Jupyter Lab application.

### Resources

- [echo_kernel](https://github.com/jupyter/echo_kernel)