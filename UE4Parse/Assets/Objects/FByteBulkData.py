from UE4Parse.Logger import get_logger
from UE4Parse.BinaryReader import BinaryStream
from .EBulkDataFlags import EBulkDataFlags
from contextlib import suppress

from ...Versions.EUEVersion import Versions

logger = get_logger(__name__)

class FByteBulkDataHeader:
    BulkDataFlags: int
    ElementCount: int
    SizeOnDisk: int
    OffsetInFile: int

    def __init__(self, reader: BinaryStream, bulkOffset: int) -> None:
        self.BulkDataFlags = reader.readUInt32()
        with suppress(ValueError):
            self.BulkDataFlags = self.BulkDataFlags

        if (self.BulkDataFlags & EBulkDataFlags.BULKDATA_Size64Bit) != 0:  # todo is this correct?
            self.ElementCount = reader.readInt64()
            self.SizeOnDisk = reader.readInt64()
        else:
            self.ElementCount = reader.readInt32()
            self.SizeOnDisk = reader.readUInt32()

        self.OffsetInFile = reader.readInt64() if reader.version >= Versions.VER_UE4_BULKDATA_AT_LARGE_OFFSETS \
                                               else reader.readInt32()

        if not (self.BulkDataFlags & EBulkDataFlags.BULKDATA_NoOffsetFixUp):  # UE4.26 flag
            self.OffsetInFile += bulkOffset

        if (self.BulkDataFlags & EBulkDataFlags.BULKDATA_BadDataVersion) != 0:
            reader.seek(2)
            self.BulkDataFlags &= EBulkDataFlags.BULKDATA_BadDataVersion


class FByteBulkData:
    Header: FByteBulkDataHeader
    Data: bytes

    def __init__(
            self, reader: BinaryStream, ubulk: BinaryStream, bulkOffset: int
    ) -> None:
        self.Header = FByteBulkDataHeader(reader, bulkOffset)
        bulkDataFlags = self.Header.BulkDataFlags
        with suppress(ValueError):
            bulkDataFlags = EBulkDataFlags(self.Header.BulkDataFlags)

        if self.Header.ElementCount == 0:
            self.Data = None
        elif (bulkDataFlags & EBulkDataFlags.BULKDATA_Unused) != 0:
            self.Header.BulkDataFlags = EBulkDataFlags.BULKDATA_Unused
            self.Data = None
        elif (bulkDataFlags & EBulkDataFlags.BULKDATA_OptionalPayload) != 0:
            self.Header.BulkDataFlags = EBulkDataFlags.BULKDATA_OptionalPayload
            self.Data = None
        elif (bulkDataFlags & EBulkDataFlags.BULKDATA_ForceInlinePayload) != 0:  # broken?
            self.Header.BulkDataFlags = EBulkDataFlags.BULKDATA_ForceInlinePayload
            pos = reader.tell()
            self.Data = reader.readBytes(self.Header.ElementCount)
            if reader.position != pos + self.Header.ElementCount:
                logger.warn("Incorrect number of bytes read")
                reader.seek(pos + self.Header.ElementCount, 0)
        elif (bulkDataFlags & EBulkDataFlags.BULKDATA_PayloadInSeperateFile) != 0:  # ubulk
            self.Header.BulkDataFlags = EBulkDataFlags.BULKDATA_PayloadInSeperateFile
            if ubulk is None:
                self.Data = None
                logger.warn("BulkDataFlags.BULKDATA_PayloadInSeperateFile but no ubulk")
            ubulk.seek(self.Header.OffsetInFile, 0)
            self.Data = ubulk.readBytes(self.Header.ElementCount)
        elif (bulkDataFlags & EBulkDataFlags.BULKDATA_PayloadAtEndOfFile) != 0:
            self.Header.BulkDataFlags = EBulkDataFlags.BULKDATA_PayloadAtEndOfFile
            pos = reader.base_stream.tell()
            if self.Header.OffsetInFile + self.Header.ElementCount <= reader.size:
                reader.seek(self.Header.OffsetInFile, 0)
                self.Data = reader.readBytes(self.Header.ElementCount)
            else:
                self.Data = None
            reader.seek(pos, 0)
