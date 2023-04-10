# Jupyter Kernel for CFML

This a Jupyter Kernel for CFML powered by the [CommandBox REPL](https://commandbox.ortusbooks.com/usage/repl). It should work on Window, Linux, and MacOS but I have not done extensive testing on them. You can also try it out on [mybinder.org](https://mybinder.org/v2/gh/jsteinshouer/cfml-jupyter-kernel/main?urlpath=/tree).

It is based on the concept of a [Python wrapper kernel](https://jupyter-client.readthedocs.io/en/latest/wrapperkernels.html). It is a work it progress so likley has some functionality missing that other Kernels may provide. I am new to Python so there are probably a lot of things that can be improved here.

## Requirements

### Python

If you want to run it locally you will need to have [Python](https://wiki.python.org/moin/BeginnersGuide/Download) installed. I installed it on Windows using the [Chocolatey package manager](https://chocolatey.org/).

```bash
choco install python
```

### CommandBox

You will also need to make sure [CommandBox](https://commandbox.ortusbooks.com/setup/download) is installed and in the system `path`.

### Jupyter

You will need to have [Jupyter](https://jupyter.org/install) installed or you can also use the [VS Code Jupyter notebook extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter).

### Docker

You can also run it with Docker if you do not want to mess around with installing dependencies. There is a docker image associated with the repository that can be utilized for running it was well. See the other options below.

## Clone the repo

```bash
git clone https://github.com/jsteinshouer/cfml-jupyter-kernel.git
```

## Install Kernel

```bash
pip install ./cfml-jupyter-kernel
python -m cfml_kernel.cfscript.install
python -m cfml_kernel.cfml.install
```

If you want to develop on the Kernel you can add the `-e` flag to make it editable.

```bash
pip install -e ./cfml-jupyter-kernel
python -m cfml_kernel.cfscript.install
python -m cfml_kernel.cfml.install
```

## Run it

I prefer to use the [VS Code Jupyter notebook extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) to run my notebooks but if you installed `Jupyter` to can run it using this command:

```
jupyter notebook
```

## Run on mybinder.org

You can try it out and create CFML notebooks using this link:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jsteinshouer/cfml-jupyter-kernel/main?urlpath=/tree)

## Github Codespaces / Dev Container

You can fork this repo and run it with Github Codespaces or clone the repo and run it locally with the VS Code Dev Containers extension.
## Running locally with Docker

If you have cloned the repo you can just use `docker compose` to run it.

```bash
docker compose up
```

Go to http://127.0.0.1:8888/lab?token=123 to access the Jupyter Lab application.

However there is a pre-built image you can use instead. This will run the Jupyter lab application using the pre-built image.

```
docker run -v ${PWD}:/home/jovyan/work -p 8888:8888 -e JUPYTER_TOKEN=123 ghcr.io/jsteinshouer/cfml-jupyter:latest
```

