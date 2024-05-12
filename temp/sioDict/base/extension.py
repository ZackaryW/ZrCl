
from functools import cache, cached_property
import typing
from sioDict.base.dicta_interface import SioInterface


class SioExtension:
    hooks : typing.List[str] = []
    hasCallback : bool = False

    def onBind(self, bindTarget : SioInterface, host : 'SioExtensionHost', **kwargs):
        self._bindTarget = bindTarget
        self._host = host

    def onHook(self, hookkey : str, hookTarget : object = None):
        pass

    def onCallback(self, *args, **kwargs):
        pass

    def onDiffer(self):
        pass


class SioExtensionHost:
    def __init__(self, ref):
        self.__ref = ref
        self.extensions : typing.Dict[str, typing.Union[SioExtension, dict]] = {}

    def onHook(self, hookkey : str, hookTarget : object = None, runType : typing.Literal["only1", "all"] = "all"):
        for ext in self.extensions.values():
            if not isinstance(ext, SioExtension):
                continue

            ext : SioExtension
            if hookkey not in ext.hooks:
                continue
            
            if hookTarget is None:
                hookTarget = self

            hookRes = ext.onHook(hookkey, hookTarget)
            
            if hookRes is not None:
                hookTarget = hookRes

            if runType == "only1":
                break

        return hookTarget

    def onDiffer(self):
        for ext in self.extensions.values():
            if isinstance(ext, SioExtension):
                onDiffer = ext.onDiffer
            elif isinstance(ext, dict) and "onDiffer" in ext:
                onDiffer = ext["onDiffer"]
            else:
                continue

            onDiffer()

    def onCallback(self, *args, **kwargs):
        for ext in self.extensions.values():
            if isinstance(ext, SioExtension) and ext.hasCallback:
                onCallback = ext.onCallback
            elif isinstance(ext, dict) and "onCallback" in ext:
                onCallback = ext["onCallback"]
            else:
                continue

            onCallback(*args, **kwargs)

    def registerExtension(self, extension : SioExtension | dict | typing.Type[SioExtension], regName : str = None):
        if isinstance(extension, SioExtension):
            if regName is None:
                regName = extension.__class__.__name__

            if regName in self.extensions:
                raise ValueError(f"Extension {regName} already registered")

            self.extensions[regName] = extension
            extension.onBind(self.__ref, self)
        
        elif isinstance(extension, dict):
            if regName is None:
                raise ValueError("Extension name not specified")
            
            self.extensions[regName] = extension
            if "onBind" in extension:
                extension["onBind"](self)
        elif isinstance(extension, typing.Type) and issubclass(extension, SioExtension):
            self.registerExtension(extension(), regName=regName)
        
        else:
            raise ValueError("Unknown extension type")
        
        self._reset_cache()

    def _reset_cache(self):
        if "hasCallback" in self.__dict__:
            del self.__dict__["hasCallback"]
        
        self.hasHook.cache_clear()

    @cache
    def hasHook(self, hookkey : str):
        for ext in self.extensions.values():
            if not isinstance(ext, SioExtension):
                continue

            ext : SioExtension
            if hookkey in ext.hooks:
                return True
        return False
    
    @cached_property
    def hasCallback(self):
        for ext in self.extensions.values():
            if not isinstance(ext, SioExtension):
                continue

            ext : SioExtension
            if ext.hasCallback:
                return True
        return False