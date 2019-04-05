import snap7.client as c
from snap7.util import *
from snap7.snap7types import *


def ReadMemory(plc, byte, bit, datatype):
    result = plc.read_area(areas['MK'], 0, byte, datatype)
    if datatype == S7WLBit:
        return get_bool(result, 0, 1)
    elif datatype == S7WLByte or datatype == S7WLWord:
        return get_int(result, 0)
    elif datatype == S7WLReal:
        return get_real(result, 0)
    elif datatype == S7WLDWord:
        return get_dword(result, 0)
    else:
        return None


def WriteMemory(plc, byte, bit, datatype, value):
    result = plc.read_area(areas['MK'], 0, byte, datatype)
    if datatype == S7WLBit:
        set_bool(result, 0, bit, value)
    elif datatype == S7WLByte or datatype == S7WLWord:
        set_int(result, 0, value)
    elif datatype == S7WLReal:
        set_real(result, 0, value)
    elif datatype == S7WLDWord:
        set_dword(result, 0, value)
    plc.write_area(areas["MK"], 0, byte, result)


def WriteOutput(dev, byte, bit, cmd):
    data = dev.read_area(0x82, 0, byte, 1)
    set_bool(data, byte, bit, cmd)
    dev.write_area(0x82, 0, byte, data)
    pass


def ReadOutput(dev, byte, bit):
    data = dev.read_area(0x82, 0, byte, 1)
    status = get_bool(data, byte, bit)
    return status


if __name__ == "__main__":
    plc = c.Client()
    #plc.connect('192.168.31.222', 0, 1)
    # print ReadMemory(plc, 420, 0, S7WLReal)
    # print ReadMemory(plc, 100, 0, S7WLWord)
