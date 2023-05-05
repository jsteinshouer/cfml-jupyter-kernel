from ipykernel.kernelbase import Kernel
from cfml_kernel.box_wrapper import CommandBoxWrapper

class CFMLKernel(Kernel):
    implementation = 'CFML'
    implementation_version = '1.0'
    language = 'CFML'
    language_version = '1.0'
    language_info = {
        'name': 'CFML',
        'mimetype': 'text/x-html',
        'file_extension': '.cfm'
    }
    banner = "CFML kernel"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.box_wrapper = CommandBoxWrapper(repl_type="cfml")

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:

            responses = self.box_wrapper.do_execute(code)

            for content in responses:
                if isinstance( content, str ):
                    stream_content = {'name': 'stdout', 'text': content}
                    self.send_response(self.iopub_socket, 'stream', stream_content)
                else:
                    self.send_response(self.iopub_socket, 'display_data', content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=CFMLKernel)
