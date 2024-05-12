from sioDict.base.extension import SioExtension
import json
import pickle
import re

default_serializer_hook = "<serialized_object>"

class Serializer(json.JSONEncoder):
    def __init__(self, serializer_hook, **kwargs):
        super(Serializer, self).__init__(**kwargs)
        self.serializer_hook = serializer_hook
    
    def default(self, obj):
        try:
            return {self.serializer_hook: pickle.dumps(obj).decode('latin-1')}
        except pickle.PickleError:
            return super().default(obj)


class SerializerExt(SioExtension):
    hooks = [
        "CUSTOM_DESERIALIZE_STR",
        "CUSTOM_SERIALIZE_STR"
    ]

    def __init__(
        self, 
        binary : bool = False,
        serializer_hook : str = default_serializer_hook
    ):
        self.binary = binary
        self.serializer_hook = serializer_hook

    def __deserialize__(self, obj):
        if isinstance(obj, dict):
            for key, val in obj.items():
                if isinstance(val, dict) or isinstance(val, list) or isinstance(val, tuple):
                    obj[key] = self.__deserialize__(val)
                if isinstance(val, dict) and self.serializer_hook in val:
                    obj[key] = pickle.loads(val[self.serializer_hook].encode('latin-1'))
        if isinstance(obj, list) or isinstance(obj, tuple):
            for i in range(len(obj)):
                if isinstance(obj[i], dict) or isinstance(obj[i], list) or isinstance(obj[i], tuple):
                    obj[i] = self.__deserialize__(obj[i])
        return obj
    
    def __serialize__(self):
        if self.binary:
            dict_str = Serializer(self.serializer_hook).encode(self.dictify())
        else:
            dict_str = json.dumps(self._bindTarget.dictify())
        return dict_str
    
    def onHook(self, hookkey: str, hookTarget: object = None):
        if hookkey == "CUSTOM_DESERIALIZE_STR":
            return self.__deserialize__(hookTarget)
        elif hookkey == "CUSTOM_SERIALIZE_STR":
            return self.__serialize__()

    def stringify(self, return_binaries=False):
        '''Returns a string representation of the data in SioDict. Use return_binaries=True, if you want to return binary data also. Default is False'''
        dict_str = self.__serialize__()
        if not return_binaries and self.serializer_hook in dict_str:
            hook_positions = [m.start() for m in re.finditer(self.serializer_hook, dict_str)]
            open_bracket_positions = [m.start() for m in re.finditer("{", dict_str)]
            closed_bracket_positions = [m.start() for m in re.finditer("}", dict_str)]
            closed_bracket_positions.reverse()
            for hook_position in hook_positions:
                hook_begin = None
                for open_bracket in open_bracket_positions:
                    if open_bracket < hook_position:
                        hook_begin = open_bracket
                hook_end = None
                for closed_bracket in closed_bracket_positions:
                    if closed_bracket > hook_position:
                        hook_end = closed_bracket
            dict_str = dict_str.replace(dict_str[hook_begin:hook_end], self.serializer_hook)
        return dict_str