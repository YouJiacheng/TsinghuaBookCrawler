import struct

def parsejpg(filename):
    # Extract info from a JPEG file
    f = None
    try:
        with open(filename, 'rb') as f:
            while True:
                markerHigh, markerLow = struct.unpack('BB', f.read(2))
                if markerHigh != 0xFF or markerLow < 0xC0:
                    raise SyntaxError('No JPEG marker found')
                elif markerLow == 0xDA: # SOS
                    raise SyntaxError('No JPEG SOF marker found')
                elif (markerLow == 0xC8 or # JPG
                        (markerLow >= 0xD0 and markerLow <= 0xD9) or # RSTx
                        (markerLow >= 0xF0 and markerLow <= 0xFD)): # JPGx
                    pass
                else:
                    dataSize, = struct.unpack('>H', f.read(2))
                    data = f.read(dataSize - 2) if dataSize > 2 else ''
                    if ((markerLow >= 0xC0 and markerLow <= 0xC3) or # SOF0 - SOF3
                        (markerLow >= 0xC5 and markerLow <= 0xC7) or # SOF4 - SOF7
                        (markerLow >= 0xC9 and markerLow <= 0xCB) or # SOF9 - SOF11
                        (markerLow >= 0xCD and markerLow <= 0xCF)): # SOF13 - SOF15
                        bpc, height, width, layers = struct.unpack_from('>BHHB', data)
                        colspace = 'DeviceRGB' if layers == 3 else ('DeviceCMYK' if layers == 4 else 'DeviceGray')
                    break
    except Exception as e:
        if f:
            f.close()
        print(f'Missing or incorrect image file: {filename}. error: {e}')

    with f:
        # Read whole file from the start
        f.seek(0)
        data = f.read()
    return {'w':width,'h':height,'cs':colspace,'bpc':bpc,'f':'DCTDecode','data':data}