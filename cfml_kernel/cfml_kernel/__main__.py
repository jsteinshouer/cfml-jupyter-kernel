from ipykernel.kernelapp import IPKernelApp
from . import CFMLKernel

IPKernelApp.launch_instance(kernel_class=CFMLKernel)
