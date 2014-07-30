# coding: utf-8

from ctypes import CDLL, cast, c_char_p, c_int, c_size_t, c_void_p
from ctypes.util import find_library

__all__ = ['CONFIGS', 'convert']


def load_library():
    libc = CDLL(find_library('libc'), use_errno=True)
    libopencc = CDLL(find_library('libopencc'), use_errno=True)
    return libc, libopencc

libc, libopencc = load_library()

libc.free.argtypes = [c_void_p]

libopencc.opencc_open.restype = c_void_p
libopencc.opencc_convert_utf8.argtypes = [c_void_p, c_char_p, c_size_t]
libopencc.opencc_convert_utf8.restype = c_void_p
libopencc.opencc_close.argtypes = [c_void_p]
libopencc.opencc_perror.argtypes = [c_char_p]
libopencc.opencc_dict_load.argtypes = [c_void_p, c_char_p, c_int]

CONFIGS = [
    'zhs2zhtw_p.ini', 'zhs2zhtw_v.ini', 'zhs2zhtw_vp.ini',
    'zht2zhtw_p.ini', 'zht2zhtw_v.ini', 'zht2zhtw_vp.ini',
    'zhtw2zhs.ini', 'zhtw2zht.ini', 'zhtw2zhcn_s.ini', 'zhtw2zhcn_t.ini',
    'zhs2zht.ini', 'zht2zhs.ini',
]


def convert(text, config='zht2zhs.ini'):
    assert config in CONFIGS

    od = libopencc.opencc_open(c_char_p(config))
    retv_i = libopencc.opencc_convert_utf8(od, text, len(text))
    if retv_i == -1:
        raise Exception('OpenCC Convert Error')
    retv_c = cast(retv_i, c_char_p)
    value = retv_c.value
    libc.free(retv_c)
    libopencc.opencc_close(od)
    return value
