from enum import IntEnum


class EPackageFlags(IntEnum):
    PKG_None = 0x00000000
    PKG_NewlyCreated = 0x00000001
    PKG_ClientOptional = 0x00000002
    PKG_ServerSideOnly = 0x00000004
    PKG_CompiledIn = 0x00000010
    PKG_ForDiffing = 0x00000020
    PKG_EditorOnly = 0x00000040
    PKG_Developer = 0x00000080

    PKG_ContainsMapData = 0x00004000
    PKG_Need = 0x00008000
    PKG_Compiling = 0x00010000
    PKG_ContainsMap = 0x00020000
    PKG_RequiresLocalizationGather = 0x00040000
    PKG_DisallowLazyLoading = 0x00080000
    PKG_PlayInEditor = 0x00100000
    PKG_ContainsScript = 0x00200000
    PKG_DisallowExport = 0x00400000
    PKG_ReloadingForCooker = 0x40000000
    PKG_FilterEditorOnly = 0x80000000
