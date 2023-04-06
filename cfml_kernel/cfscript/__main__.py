from ipykernel.kernelapp import IPKernelApp
from . import CFScriptKernel

IPKernelApp.launch_instance(kernel_class=CFScriptKernel)
