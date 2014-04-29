
import subprocess

__download_tools = {}

default_config = {
    "aria2": {
        "extra_opts": ("-s10", "-x10")
    }
}


def get_download_tool(name):
    return __download_tools.get(name, None)

def download_tool(name):
    def register(cls):
        config = default_config.get(name, None)
        assert isinstance(config, dict)
        if config:
            __download_tools[name] = cls(**config)
        else:
            __download_tools[name] = cls()
        return cls
    return register


class DownloadTool(object):
    """
    Interface definition for all download tools
    """
    def download(self, uri='', resume=True, path="", headers=""):
        pass

@download_tool("aria2")
class Aria2(DownloadTool):
    def __init__(self, default_header="", extra_opts=None):
        self.__default_headers = default_header
        self.__extra_opts = None
        if isinstance(extra_opts, str):
            self.__extra_opts = extra_opts.split()
        elif type(extra_opts) in (list, tuple):
            self.__extra_opts = extra_opts
        else:
            self.__extra_opts = str(extra_opts)

    def download(self, uri='', resume=True, path="", headers=""):
        aria2_opts = ['aria2c', '--header=' + headers, uri, '--out', path, '--file-allocation=none']
        if resume:
            aria2_opts.append('-c')
        if self.__extra_opts:
            aria2_opts.extend(self.__extra_opts)
        exit_code = subprocess.call(aria2_opts)
        if exit_code != 0:
            raise Exception('aria2c exited abnormally')