from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF
import pexpect

PEXPECT_PROMPT = u'CFML-REPL:'
PEXPECT_CONTINUATION_PROMPT = u'.............:'

class CFMLKernel(Kernel):
    implementation = 'CFML'
    implementation_version = '1.0'
    language = 'CFML'
    language_version = '0.1'
    language_info = {
        'name': 'CFML',
        'mimetype': 'text/x-html',
        'file_extension': '.cfm'
    }
    banner = "CFML kernel"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.repl = self._create_repl()

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:

            resp = self.repl.run_command(code.strip(), timeout=5)
            code_lines = code.splitlines()
            resp_lines = resp.strip().splitlines()
            new_resp = [];
            for line in resp_lines:
                if not any(line.strip() == x.strip() for x in code_lines):
                    new_resp.append(line)

            stream_content = {'name': 'stdout', 'text': "\n".join(new_resp).strip()}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

    def _create_repl(self):
        child = pexpect.spawn("box", args=['repl','script=false'], timeout=30, echo=False,
                encoding='utf-8', codec_errors='replace')

        orig_prompt =  'CFML-REPL:'

        repl = replwrap.REPLWrapper(child, orig_prompt = orig_prompt,
                                    prompt_change=None,
                                    extra_init_cmd="PROMPT_COMMAND=''")

        return repl

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=CFMLKernel)