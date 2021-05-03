from UE4Parse.BinaryReader import BinaryStream
from .EBulkDataFlags import EBulkDataFlags


class FByteBulkDataHeader:
    BulkDataFlags: int
    ElementCount: int
    SizeOnDisk: int
    OffsetInFile: int

    def __init__(self, reader: BinaryStream, bulkOffset: int) -> None:
        self.BulkDataFlags = reader.readInt32()
        if (self.BulkDataFlags & EBulkDataFlags.BULKDATA_Size64Bit) != 0:
            self.ElementCount = reader.readInt64()
            self.SizeOnDisk = reader.readInt64()
        else:
            self.ElementCount = reader.readInt32()
            self.SizeOnDisk = reader.readInt32()

        self.OffsetInFile = reader.readInt64()
        if not (self.BulkDataFlags & EBulkDataFlags.BULKDATA_NoOffsetFixUp):  # UE4.26 flag
            self.OffsetInFile += bulkOffset

        if (self.BulkDataFlags & EBulkDataFlags.BULKDATA_BadDataVersion) != 0:
            reader.seek(2)


class FByteBulkData:
    Header: FByteBulkDataHeader
    Data: bytes

    def __init__(
        self, reader: BinaryStream, ubulk: BinaryStream, bulkOffset: int
    ) -> None:
        self.Header = FByteBulkDataHeader(reader, bulkOffset)
        bulkDataFlags = self.Header.BulkDataFlags

        if self.Header.ElementCount == 0:
            self.Data = None
        elif (bulkDataFlags & EBulkDataFlags.BULKDATA_Unused) != 0:
            self.Data = None
        elif (bulkDataFlags & EBulkDataFlags.BULKDATA_OptionalPayload) != 0:
            self.Data = None
        elif (bulkDataFlags & EBulkDataFlags.BULKDATA_ForceInlinePayload) != 0:
            self.Data = reader.readBytes(self.Header.ElementCount)
        elif (bulkDataFlags & EBulkDataFlags.BULKDATA_PayloadInSeperateFile) != 0:  # ubulk
            ubulk.seek(self.Header.OffsetInFile, 0)
            self.Data = ubulk.readBytes(self.Header.ElementCount)
        elif (bulkDataFlags & EBulkDataFlags.BULKDATA_PayloadAtEndOfFile) != 0:
            pos = reader.base_stream.tell()
            if self.Header.OffsetInFile + self.Header.ElementCount <= reader.size:
                reader.seek(self.Header.OffsetInFile, 0)
                self.Data = reader.readBytes(self.Header.ElementCount)
            else:
                self.Data = None
            reader.seek(pos, 0)
