"""User defined functions for Spark."""

import pefile
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

from ns_app.enum.metadata import ArchEnum, FileType

SchemaFields = [
    StructField("file_type", StringType(), nullable=True),
    StructField("arch", StringType(), nullable=True),
    StructField("numer_of_imports", IntegerType(), nullable=True),
    StructField("number_of_exports", IntegerType(), nullable=True),
]


@udf(returnType=StructType(SchemaFields))
def get_file_metadata(
    bfile: bytes,
) -> tuple[str | None, str | None, int | None, int | None]:
    """User defined function to get PE file metadata."""
    file_type = arch = numer_of_imports = number_of_exports = None

    try:
        pfile = pefile.PE(data=bytes(bfile), fast_load=True)
    except pefile.PEFormatError:
        pass
    else:
        if pfile.is_exe():
            file_type = FileType.exe.value
        if pfile.is_dll():
            file_type = FileType.dll.value

        machine = pfile.FILE_HEADER.Machine
        if machine == pefile.MACHINE_TYPE["IMAGE_FILE_MACHINE_I386"]:
            arch = ArchEnum.x32.value
        elif machine == pefile.MACHINE_TYPE["IMAGE_FILE_MACHINE_AMD64"]:
            arch = ArchEnum.x64.value

        if hasattr(pfile, "DIRECTORY_ENTRY_IMPORT"):
            numer_of_imports = len(pfile.DIRECTORY_ENTRY_IMPORT)

        if hasattr(pfile, "DIRECTORY_ENTRY_EXPORT"):
            number_of_exports = len(pfile.DIRECTORY_ENTRY_EXPORT)
    return file_type, arch, numer_of_imports, number_of_exports
