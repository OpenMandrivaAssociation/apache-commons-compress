Name:		apache-commons-compress
Version:	1.28.0
Release:	1
Summary:	Library for tar, zip, and other archive formats
Group:		Development/Java
License:	ASL 2.0
URL:		https://commons.apache.org/proper/commons-compress/
Source0:	https://archive.apache.org/dist/commons/compress/source/commons-compress-%{version}-src.tar.gz

BuildArch:	noarch
BuildRequires:	mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:	mvn(commons-io:commons-io)
BuildRequires:	mvn(org.apache.commons:commons-lang3)
BuildRequires:	mvn(commons-codec:commons-codec)
BuildRequires:	mvn(org.tukaani:xz)
BuildRequires:	python
BuildSystem:	maven
BuildOption(install):	--file-name commons-compress --link %{name} --alias commons-compress:commons-compress

%description
Apache Commons Compress reads and writes tar, zip, 7z, and other archive
formats. Zstandard and Brotli are left out: zstd-jni is a prebuilt native
library, and Pack200 needs a bundled ASM that this package does not ship.
XZ and LZMA come from the system xz-java package.

%prep
%setup -q -n commons-compress-%{version}-src
python - <<'PY'
import re
import shutil
from pathlib import Path

pom = Path("pom.xml")
text = pom.read_text()
patterns = [
    r"\s*<dependency>\s*<groupId>com\.github\.luben</groupId>\s*<artifactId>zstd-jni</artifactId>.*?</dependency>",
    r"\s*<dependency>\s*<groupId>org\.brotli</groupId>\s*<artifactId>dec</artifactId>.*?</dependency>",
    r"\s*<!-- Pack200 -->\s*<dependency>\s*<groupId>org\.ow2\.asm</groupId>\s*<artifactId>asm</artifactId>.*?</dependency>",
]
for pattern in patterns:
    text, count = re.subn(pattern, "\n", text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"pom edit missed {pattern}")
pom.write_text(text)

for relative in (
    "src/main/java/org/apache/commons/compress/compressors/brotli",
    "src/main/java/org/apache/commons/compress/compressors/zstandard",
    "src/main/java/org/apache/commons/compress/compressors/pack200",
    "src/main/java/org/apache/commons/compress/harmony",
    "src/main/java/org/apache/commons/compress/java",
):
    shutil.rmtree(relative)

def sub(path, old, new):
    file = Path(path)
    text = file.read_text()
    if old not in text:
        raise SystemExit(f"missing snippet in {path}: {old[:80]!r}")
    file.write_text(text.replace(old, new, 1))

factory = "src/main/java/org/apache/commons/compress/compressors/CompressorStreamFactory.java"
for line in (
    "import org.apache.commons.compress.compressors.brotli.BrotliCompressorInputStream;\n",
    "import org.apache.commons.compress.compressors.brotli.BrotliUtils;\n",
    "import org.apache.commons.compress.compressors.pack200.Pack200CompressorInputStream;\n",
    "import org.apache.commons.compress.compressors.pack200.Pack200CompressorOutputStream;\n",
    "import org.apache.commons.compress.compressors.zstandard.ZstdCompressorInputStream;\n",
    "import org.apache.commons.compress.compressors.zstandard.ZstdCompressorOutputStream;\n",
    "import org.apache.commons.compress.compressors.zstandard.ZstdUtils;\n",
):
    sub(factory, line, "")
sub(
    factory,
    """        if (compressorNames.contains(PACK200) && Pack200CompressorInputStream.matches(signature, signatureLength)) {
            return PACK200;
        }
""",
    "",
)
sub(
    factory,
    """        if (compressorNames.contains(ZSTANDARD) && ZstdUtils.matches(signature, signatureLength)) {
            return ZSTANDARD;
        }
""",
    "",
)
sub(
    factory,
    """            if (BROTLI.equalsIgnoreCase(name)) {
                if (!BrotliUtils.isBrotliCompressionAvailable()) {
                    throw new CompressorException("Brotli compression is not available." + YOU_NEED_BROTLI_DEC);
                }
                return new BrotliCompressorInputStream(in);
            }
""",
    """            if (BROTLI.equalsIgnoreCase(name)) {
                throw new CompressorException("Brotli compression is not available." + YOU_NEED_BROTLI_DEC);
            }
""",
)
sub(
    factory,
    """            if (ZSTANDARD.equalsIgnoreCase(name)) {
                if (!ZstdUtils.isZstdCompressionAvailable()) {
                    throw new CompressorException("Zstandard compression is not available." + YOU_NEED_ZSTD_JNI);
                }
                return new ZstdCompressorInputStream(in);
            }
""",
    """            if (ZSTANDARD.equalsIgnoreCase(name)) {
                throw new CompressorException("Zstandard compression is not available." + YOU_NEED_ZSTD_JNI);
            }
""",
)
sub(
    factory,
    """            if (PACK200.equalsIgnoreCase(name)) {
                return new Pack200CompressorInputStream(in);
            }
""",
    """            if (PACK200.equalsIgnoreCase(name)) {
                throw new CompressorException("Pack200 compression is not available.");
            }
""",
)
sub(
    factory,
    """            if (PACK200.equalsIgnoreCase(name)) {
                return new Pack200CompressorOutputStream(out);
            }
""",
    """            if (PACK200.equalsIgnoreCase(name)) {
                throw new CompressorException("Pack200 compression is not available.");
            }
""",
)
sub(
    factory,
    """            if (ZSTANDARD.equalsIgnoreCase(name)) {
                return new ZstdCompressorOutputStream(out);
            }
""",
    """            if (ZSTANDARD.equalsIgnoreCase(name)) {
                throw new CompressorException("Zstandard compression is not available." + YOU_NEED_ZSTD_JNI);
            }
""",
)

zip_in = "src/main/java/org/apache/commons/compress/archivers/zip/ZipArchiveInputStream.java"
sub(zip_in, "import org.apache.commons.compress.compressors.zstandard.ZstdCompressorInputStream;\n", "")
sub(
    zip_in,
    """    protected InputStream createZstdInputStream(final InputStream in) throws IOException {
        return new ZstdCompressorInputStream(in);
    }
""",
    """    protected InputStream createZstdInputStream(final InputStream in) throws IOException {
        if (in == null) {
            throw new IOException("Zstandard compression is not available.");
        }
        throw new IOException("Zstandard compression is not available.");
    }
""",
)

zip_file = "src/main/java/org/apache/commons/compress/archivers/zip/ZipFile.java"
sub(zip_file, "import org.apache.commons.compress.compressors.zstandard.ZstdCompressorInputStream;\n", "")
sub(
    zip_file,
    """        return zstdInputStreamFactory != null ? zstdInputStreamFactory.apply(in) : new ZstdCompressorInputStream(in);
""",
    """        if (zstdInputStreamFactory != null) {
            return zstdInputStreamFactory.apply(in);
        }
        throw new IOException("Zstandard compression is not available.");
""",
)
PY

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
