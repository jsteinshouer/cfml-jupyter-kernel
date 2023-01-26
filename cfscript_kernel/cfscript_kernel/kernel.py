from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF
import subprocess
import re
import base64
import pexpect

PEXPECT_PROMPT = u'CFSCRIPT-REPL: '
PEXPECT_CONTINUATION_PROMPT = u'.............:'

class CFScriptKernel(Kernel):
    implementation = 'CFScript'
    implementation_version = '1.0'
    language = 'CFML'
    language_version = '0.1'
    language_info = {
        'name': 'CFScript',
        'mimetype': 'text/x-javascript',
        'file_extension': '.cfm'
    }
    banner = "CFScript kernel"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.repl = self._create_repl()

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:

            resp = self.repl.run_command(code.strip())
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
        cfscript_repl = pexpect.spawn("box", args=['repl'], echo=False,encoding='utf-8')
        
        # Test to see if this could work on Windows - https://pexpect.readthedocs.io/en/stable/overview.html#pexpect-on-windows
        #cfscript_repl = pexpect.popen_spawn.PopenSpawn("box repl",encoding='utf-8')

        orig_prompt =  u'CFSCRIPT-REPL: '
        cfscript_repl_wrapper = replwrap.REPLWrapper(cfscript_repl, orig_prompt = orig_prompt,
                                    prompt_change=None,
                                    extra_init_cmd="PROMPT_COMMAND=''")

        return cfscript_repl_wrapper

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=CFScriptKernel)