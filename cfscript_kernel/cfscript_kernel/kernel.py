from ipykernel.kernelbase import Kernel
import subprocess, os

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

    PROMPT_STRINGS = ["CFSCRIPT-REPL: ", ".............: "]

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.repl = self._create_repl()

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:

            code_lines = code.splitlines()

            response = [];
            for line in code_lines:  
                self.repl.stdin.write( bytes( f"{line.strip()}\n".encode("utf-8") ) )
                self.repl.stdin.flush()
                output = self._search_for_output(repl=self.repl)
                
                for string in self.PROMPT_STRINGS:
                    output = output.replace(string,"")
                response.append(output)
            

            stream_content = {'name': 'stdout', 'text': "".join(response)}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

    def _create_repl(self):
        my_env = os.environ.copy()
        my_env["box_config_nonInteractiveMode"] = "false"
        my_env["box_config_colorInDumbTerminal"] = "true"
        cfscript_repl = subprocess.Popen(
            [
                "box",
                "repl"
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            env=my_env
        )
        self._search_for_output(repl=cfscript_repl)

        return cfscript_repl
    
    def _search_for_output(self,repl):
        buffer = ""
        while not any(string in buffer for string in self.PROMPT_STRINGS):
            buffer = buffer + repl.stdout.read1(1).decode("utf-8")
        return buffer

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=CFScriptKernel)