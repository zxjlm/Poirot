"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2021-03-24 14:32:51
@description: None
"""
from fontTools.ttLib import TTFont, deprecateArgument, BytesIO, SFNTReader


class MyTTFont(TTFont):
    """The main font object. It manages file input and output, and offers
    a convenient way of accessing tables.
    Tables will be only decompiled when necessary, ie. when they're actually
    accessed. This means that simple operations can be extremely fast.
    """

    def __init__(self, file=None, res_name_or_index=None,
                 sfntVersion="\000\001\000\000", flavor=None, checkChecksums=0,
                 verbose=None, recalcBBoxes=True, allowVID=False, ignoreDecompileErrors=False,
                 recalcTimestamp=True, fontNumber=-1, lazy=None, quiet=None,
                 _tableCache=None):

        for name in ("verbose", "quiet"):
            val = locals().get(name)
            if val is not None:
                deprecateArgument(name, "configure logging instead")
            setattr(self, name, val)

        self.lazy = lazy
        self.recalcBBoxes = recalcBBoxes
        self.recalcTimestamp = recalcTimestamp
        self.tables = {}
        self.reader = None

        # Permit the user to reference glyphs that are not int the font.
        self.last_vid = 0xFFFE  # Can't make it be 0xFFFF, as the world is full unsigned short integer
        # counters that get incremented after the last seen GID value.
        self.reverseVIDDict = {}
        self.VIDDict = {}
        self.allowVID = allowVID
        self.ignoreDecompileErrors = ignoreDecompileErrors

        self._tableCache = _tableCache
        self.reader = SFNTReader(file, checkChecksums, fontNumber=fontNumber)
        self.sfntVersion = self.reader.sfntVersion
        self.flavor = self.reader.flavor
        self.flavorData = self.reader.flavorData
