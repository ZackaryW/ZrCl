
from sioDict.base.dicta_interface import SioInterface
from sioDict.base.extension import SioExtension, SioExtensionHost
import os
import orjson

class SyncFileExt(SioExtension):
    
    """
    Supported Hooks: 
        CUSTOM_SERIALIZE_STR (1)
        CUSTOM_DESERIALIZE_STR (1)
    
    """
    def __init__(
        self, 
        path : str, 
        reset : bool = False,
        orjson_opts = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2
    ):
        self.path = path
        self.reset = reset
        self.orjson_opts = orjson_opts

    def onBind(self, reference: SioInterface, host : SioExtensionHost, **kwargs):
        super().onBind(reference, host, **kwargs)
        if self.reset:
            self.clearFile(self.path)

        try:
            self.importFile(self.path)
        except FileNotFoundError:
            pass

    def onDiffer(self):
        self.exportFile(self.path, reset=False)

    def removeFile(self, path):
        '''Delete a file. Use with care'''
        if os.path.exists(path):
            os.remove(path)
        else:
            print("removeFile: File '{}' does not exist.".format(path))

    def clearFile(self, path):
        '''Clear a file. Use with care'''
        if isinstance(self._bindTarget, dict):
            defaultString = "{}"
        elif isinstance(self._bindTarget, list):
            defaultString = "[]"
        else:
            raise Exception("clearFile: target is not a dict or list")

        with open(path, 'w') as f:
            f.write(defaultString)
            f.close()

    def exportFile(self, path, reset=True):
        '''Export data to a file. Set reset=True if you want to reset the data in the file at first. Default is True'''
        if reset:
            self.clearFile(path)
        if not self._host.hasHook("CUSTOM_SERIALIZE_STR"):
            with open(path, 'wb') as f:
                f.write(orjson.dumps(self._bindTarget, option=self.orjson_opts))
        else:
            dict_str = self._host.onHook("CUSTOM_SERIALIZE_STR", runType="only1")
            with open(path, 'w') as f:
                f.write(dict_str)
        
    def importFile(self, path):
        '''Insert/Import data from a file.'''
        if os.path.exists(path):
            with open(path, "rb") as f:
                if self._host.hasHook("CUSTOM_DESERIALIZE_STR"):
                    data = self._host.onHook("CUSTOM_DESERIALIZE_STR", runType="only1", hookTarget=f.read())
                else:
                    data = orjson.loads(f.read())
                
            if isinstance(self._bindTarget, dict):
                self._bindTarget.update(**data)
            elif isinstance(self._bindTarget, list):
                self._bindTarget.clear()
                self._bindTarget.extend(data)
        else:
            raise FileNotFoundError(path)