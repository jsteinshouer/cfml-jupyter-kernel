import subprocess, os, logging

class CommandBoxWrapper():

    PROMPT_STRINGS = ["CFSCRIPT-REPL: ",".............: ","CFML-REPL: ","CommandBox> ",u"\u276F "]
    CF_REPL_TYPE = "cfscript"

    def __init__(self,repl_type = "cfscript", **kwargs):
        # logging.basicConfig(filename='box_wrapper_debug.log',
        #                     encoding='utf-8', level=LOG_LEVEL)
        self.CF_REPL_TYPE = repl_type
        # New version of commandbox (5.9.0) uses a prompt with the current working directory in it
        self.PROMPT_STRINGS.append("CommandBox:" + os.getcwd().split(os.sep)[-1] + ">");
        self.box_shell = self._create_process()
        self._search_for_output()
        self._start_repl()

    def do_execute(self, code):

        if (code[:8] == "$install" or code[:8] == "%install"):
            # stop the repl
            self._stop_repl()

            #Run the install command
            output = self._box_install(code)

            #start the repl
            self._start_repl()

            return output
        elif (code[:8] == "$loadjar" or code[:8] == "%loadjar"):
            #Load jar
            output = self._load_jar(code)

            return output
        else:
            code_lines = code.splitlines()

            response = [];
            for line in code_lines:  
                self.box_shell.stdin.write( bytes( f"{line.strip()}\n".encode("utf-8") ) )
                self.box_shell.stdin.flush()
                output = self._search_for_output()
                
                for string in self.PROMPT_STRINGS:
                    output = output.replace(string,"")

                if (output.__contains__("[EMPTY STRING]") == False):
                    response.append(output.strip())
                    # response.append("\n")

            return "\n".join(response).strip()
    
    def _box_install(self,code):
        self.box_shell.stdin.write(bytes(f"install {code.replace('$install','').replace('%install','')}\n".encode("utf-8")))
        self.box_shell.stdin.flush()
        output = self._search_for_output()
        for string in self.PROMPT_STRINGS:
            output = output.replace(string,"")
        return output
    
    def _load_jar(self,code):

        loadjar_expression = "loadJar = (path) => { \
            filePath = getDirectoryFromPath( getCurrentTemplatePath() ) & path; \
            new commandbox.system.util.FileSystem().classLoad( filePath ); \
            return 'Loaded ' & filePath; \
        }"
        self.box_shell.stdin.write(bytes(f"{loadjar_expression}\n".encode("utf-8")))
        self.box_shell.stdin.flush()
        self._search_for_output()
        self.box_shell.stdin.write(bytes(f"loadJar('{code.replace('$loadjar','').replace('%loadjar','').strip()}');\n".encode("utf-8")))
        self.box_shell.stdin.flush()
        output = self._search_for_output()
        for string in self.PROMPT_STRINGS:
            output = output.replace(string,"")

        return output

    def _start_repl(self):
        if (self.CF_REPL_TYPE == "cfml"):
            cmd = "repl script=false\n"
        else:
            cmd = "repl\n"
        self.box_shell.stdin.write(bytes(cmd.encode("utf-8")))
        self.box_shell.stdin.flush()
        self._search_for_output()

    def _stop_repl(self):
        self.box_shell.stdin.write(bytes("q\n".encode("utf-8")))
        self.box_shell.stdin.flush()
        self.box_shell.stdin.write(bytes("reload\n".encode("utf-8")))
        self.box_shell.stdin.flush()
        self._search_for_output()

    def _create_process(self):
        my_env = os.environ.copy()
        my_env["box_config_nonInteractiveMode"] = "false"
        my_env["box_config_colorInDumbTerminal"] = "true"
        # The bullet train module prompt uses this character
        #  https://www.compart.com/en/unicode/U+276F
        # I am new to python and could not figure out how to match that so am disabling 
        # it for now
        my_env["box_config_ModulesExclude"] = "[\"commandbox-bullet-train\"]"
        box_shell = subprocess.Popen(
            [
                "box"
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            env=my_env
        )
        
        return box_shell
    
    def _search_for_output(self):
        buffer = u""
        logging.debug("_search_for_output: \n\n")
        while not any(string in buffer for string in self.PROMPT_STRINGS):
            try:
                buffer = buffer + self.box_shell.stdout.read1(1).decode("utf-8")
            except:
                try:
                    buffer = buffer + self.box_shell.stdout.read1(1).decode("utf-16", "ignore")
                except:    
                    buffer = buffer + "?"
                    logging.error("Error occured decoding output")
            logging.debug("buffer: \n\n" + buffer)
        return buffer
