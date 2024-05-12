"""
this is an implementation that restores all dicta functionalities
"""
from sioDict.base.dicta_modified import SioDict
from sioDict.extensions.syncFile import SyncFileExt
from sioDict.extensions.callback import CallbackExt
from sioDict.extensions.serializer import SerializerExt
import os

import orjson

class DictAWrapper:
    def __init__(self, *args, **kwargs):
        self.dicta = SioDict(*args, **kwargs)
        self.__syncfilebinded = False
        self.__syncFileExt = None
        self.__serializerExt =None

    def syncFile(self, path, reset=False):
        if self.__syncfilebinded:
            return
        self.__syncFileExt = SyncFileExt(path, reset=reset)
        self.dicta.bind(self.__syncFileExt, name="syncFile")
        self.__syncfilebinded = True

    def importFile(self, path : str):
        if os.path.exists(path):
            with open(path, "rb") as f:
                if self.dicta.extensionHost.hasHook("CUSTOM_DESERIALIZE_STR"):
                    data = self.dicta.extensionHost.onHook("CUSTOM_DESERIALIZE_STR", runType="only1", hookTarget=f.read())
                else:
                    data = orjson.loads(f.read())
                
            self.dicta.update(**data)
        else:
            raise FileNotFoundError(path)

    def clearFile(self, path):
        if not self.__syncFileExt:
            raise Exception("No syncFile extension binded")
        
        self.__syncFileExt.clearFile(path)

    def bind(self, callback, response=None, *args, **kwargs):
        '''Set the callback function'''
        self.__callbackExt = CallbackExt(callback)
        self.dicta.bind(self.__callbackExt, name="callback")
        self.__callbackExt.callbackArgs = args
        self.__callbackExt.callbackKwargs = kwargs
        if response:
            self.dicta.debug = True

    def enable_serializer(self):
        self.__serializerExt = SerializerExt()
        self.dicta.bind(self.__serializerExt, name="serializer")

    def setBinarySerializer(self, toggle):
        if self.__serializerExt is None:
            raise Exception("No serializer extension binded")
        
        self.__serializerExt.binary = toggle

