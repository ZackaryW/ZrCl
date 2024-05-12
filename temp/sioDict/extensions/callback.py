
from sioDict.base.extension import SioExtension

class CallbackExt(SioExtension):
    hasCallback = True

    def __init__(self, callback):
        self.callback = callback
        self.callbackArgs = []
        self.callbackKwargs = {}

    def onCallback(self, *args, **kwargs):
        return self.callback(*args,*self.callbackArgs ,**kwargs, **self.callbackKwargs)    
    