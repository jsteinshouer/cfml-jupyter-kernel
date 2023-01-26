# Jupyter Kernel for CFML

This is a proof-of-concept for creating a Jupyter Kernel powered by the [CommandBox REPL](https://commandbox.ortusbooks.com/usage/repl). 

It is based on the concept of a [Python wrapper kernel](https://jupyter-client.readthedocs.io/en/latest/wrapperkernels.html). It is a work in progress. It has known issues and has not been battle tested.

## Running with Docker

```bash
docker compose up
```

Go to http://127.0.0.1:8888/lab?token=x to access the Jupyter Lab application.

### Resources

- [echo_kernel](https://github.com/jupyter/echo_kernel)