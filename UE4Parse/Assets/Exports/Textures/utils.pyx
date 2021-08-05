from math import floor

# from ueviewer
def build_blue_channel(bytearray data, int size_x, int size_y):
    """note modifies data inplace"""
    cdef int offset = 0
    cdef int i = 0
    cdef float uf, vf, t
    while i < size_x*size_y:
        i += 1
        u = data[offset]
        v = data[offset + 1]
        uf = u / 255.0 * 2 - 1
        vf = v / 255.0 * 2 - 1
        t = t  = 1.0 - uf * uf - vf * vf
        if t >= 0:
            data[offset+2] = floor((t + 1.0) * 127.5)
        else:
            data[offset+2] = 255
        offset += 4
