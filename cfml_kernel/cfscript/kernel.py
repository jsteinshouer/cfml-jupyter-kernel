from ipykernel.kernelbase import Kernel
from cfml_kernel.box_wrapper import CommandBoxWrapper

class CFScriptKernel(Kernel):
    implementation = 'CFScript'
    implementation_version = '1.0'
    language = 'CFML'
    language_version = '1.0'
    language_info = {
        'name': 'CFScript',
        'mimetype': 'text/x-javascript',
        'file_extension': '.cfm'
    }
    banner = "CFScript kernel"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.box_wrapper = CommandBoxWrapper(repl_type="cfscript")

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:

            output = self.box_wrapper.do_execute(code);
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=CFScriptKernel)
    