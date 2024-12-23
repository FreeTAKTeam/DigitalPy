import os
import urllib.parse

""" * FileUtil provides basic support for file functionality
"""


class FileController:
    """
    * Copy an uploaded file to a given destination (only if the mime type matches the given one).
    * @param $mediaFile An associative array with the following keys: 'name', 'type', 'tmp_name' (typically a $_FILES entry)
    * @param $destName The destination file name
    * @param $mimeTypes An array holding the allowed mime types, null if arbitrary (default: _null_)
    * @param $override Boolean whether an existing file should be overridden, if false an unique id will be placed in the filename to prevent overriding (default: _true_)
    * @return The filename of the uploaded file
    """

    # TODO: move to separate conf file
    MIME_TYPE_MAP = {
        "ai": "application/postscript",
        "aif": "audio/x-aiff",
        "aifc": "audio/x-aiff",
        "aiff": "audio/x-aiff",
        "asc": "text/plain",
        "asf": "video/x-ms-asf",
        "asx": "video/x-ms-asf",
        "au": "audio/basic",
        "avi": "video/x-msvideo",
        "bcpio": "application/x-bcpio",
        "bin": "application/octet-stream",
        "bmp": "image/bmp",
        "cdf": "application/x-netcdf",
        "class": "application/octet-stream",
        "cpio": "application/x-cpio",
        "cpt": "application/mac-compactpro",
        "csh": "application/x-csh",
        "css": "text/css",
        "dcr": "application/x-director",
        "dir": "application/x-director",
        "djv": "image/vnd.djvu",
        "djvu": "image/vnd.djvu",
        "dll": "application/octet-stream",
        "dms": "application/octet-stream",
        "doc": "application/msword",
        "dvi": "application/x-dvi",
        "dxr": "application/x-director",
        "eps": "application/postscript",
        "etx": "text/x-setext",
        "exe": "application/octet-stream",
        "ez": "application/andrew-inset",
        "gif": "image/gif",
        "gtar": "application/x-gtar",
        "hdf": "application/x-hdf",
        "hqx": "application/mac-binhex40",
        "htm": "text/html",
        "html": "text/html",
        "ice": "x-conference/x-cooltalk",
        "ief": "image/ief",
        "txt": "text/plain",
        "html": "text/html",
        "htm": "text/html",
        "php": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "json": "application/json",
        "xml": "application/xml",
        "swf": "application/x-shockwave-flash",
        "flv": "video/x-flv",
        "txt": "text/plain",
        "php": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "json": "application/json",
        "xml": "application/xml",
        "swf": "application/x-shockwave-flash",
        "flv": "video/x-flv",
        "zip": "application/zip",
        "rar": "application/x-rar-compressed",
        "exe": "application/x-msdownload",
        "msi": "application/x-msdownload",
        "cab": "application/vnd.ms-cab-compressed",
        "pdf": "application/pdf",
        "doc": "application/msword",
        "rtf": "application/rtf",
        "xls": "application/vnd.ms-excel",
        "ppt": "application/vnd.ms-powerpoint",
        "odt": "application/vnd.oasis.opendocument.text",
        "ods": "application/vnd.oasis.opendocument.spreadsheet",
        # images
        "png": "image/png",
        "jpe": "image/jpeg",
        "jpeg": "image/jpeg",
        "jpg": "image/jpeg",
        "gif": "image/gif",
        "bmp": "image/bmp",
        "ico": "image/vnd.microsoft.icon",
        "tiff": "image/tiff",
        "tif": "image/tiff",
        "svg": "image/svg+xml",
        "svgz": "image/svg+xml",
        # audio/video
        "mp3": "audio/mpeg",
        "qt": "video/quicktime",
        "mov": "video/quicktime",
    }

    @staticmethod
    def upload_file(media_file, dest_name, mime_types=None, override=True):
        message = ObjectFactory.get_instance("message")

        # check if the file was uploaded
        if not os.path.isfile(media_file["tmp_name"]):
            msg = message.get_text(
                "Possible file upload attack: filename %0%.", [media_file["name"]]
            )
            raise IOException(msg)

        # check mime type
        if mime_types is not None and media_file["type"] not in mime_types:
            raise IOException(
                message.get_text(
                    "File '%0%' has wrong mime type: %1%. Allowed types: %2%.",
                    [media_file["name"], media_file["type"], ", ".join(mime_types)],
                )
            )

        # check if we need a new name
        if not override and os.path.exists(dest_name):
            pieces = os.path.splitext(os.path.basename(dest_name))
            extension = pieces[1]
            name = pieces[0]
            dest_name = (
                os.path.dirname(dest_name)
                + "/"
                + name
                + str(os.urandom(6).hex())
                + extension
            )

        result = os.rename(media_file["tmp_name"], dest_name)
        if result is False:
            raise IOException(
                message.get_text(
                    "Failed to move %0% to %1%.", [media_file["tmp_name"], dest_name]
                )
            )

        return os.path.basename(dest_name)

    @staticmethod
    def get_mime_type(file):
        """
        * Get the mime type of the given file
        * @param $file The file
        * @return String
        """
        defaultType = "application/octet-stream"

        # try to determine from file content, if the file exists
        if fileExists(file):
            if class_exists("\FileInfo"):
                # use FileInfo extension
                fileInfo = finfo(FILEINFO_MIME)
                fileType = fileInfo.file(file_get_contents(file))
            else:
                # try detect image mime type
                imageInfo = getimagesize(file)
                fileType = imageInfo["mime"] if "mime" in imageInfo else ""
            return fileType if isinstance(fileType, str) and fileType else defaultType

        # fall back to file extension
        pieces = re.split(r"\.", basename(file))
        extension = str.lower(pieces.pop())
        return MIME_TYPE_MAP[extension] if extension in MIME_TYPE_MAP else defaultType

    @staticmethod
    def fputs_unicode(fp, str):
        """
        * Write unicode to file.
        * @param $fp File Handle
        * @param $str String to write
        """
        fp.write(str.encode("utf8"))

    @staticmethod
    def get_files(directory, pattern="/./", prependDirectoryName=False, recursive=False):
        """
        * Get the files in a directory that match a pattern
        * @param $directory The directory to search in
        * @param $pattern The pattern (regexp) to match (default: _/./_)
        * @param $prependDirectoryName Boolean whether to prepend the directory name to each file (default: _false_)
        * @param $recursive Boolean whether to recurse into subdirectories (default: _false_)
        * @return An array containing the filenames sorted by modification date
        """
        if directory[-1] != "/":
            directory += "/"
        if not os.path.isdir(directory):
            raise ValueError(f"The directory '{directory}' does not exist.")
        result = []
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.name != "." and entry.name != "..":
                    if recursive and entry.is_dir():
                        files = getFiles(
                            directory + entry.name,
                            pattern,
                            prependDirectoryName,
                            recursive,
                        )
                        result.extend(files)
                    elif entry.is_file() and re.match(pattern, entry.name):
                        sortkey = (entry.stat().st_ctime,)
                        if prependDirectoryName:
                            file = directory + entry.name
                        sortkey += file
                        result[sortkey] = file
        result = sorted(result, reverse=True)
        return list(result.values())

    @staticmethod
    def get_directories(
        directory, pattern="/./", prependDirectoryName=False, recursive=False
    ):
        """/*
        * Get the directories in a directory that match a pattern
        * @param $directory The directory to search in
        * @param $pattern The pattern (regexp) to match (default: _/./_)
        * @param $prependDirectoryName Boolean whether to prepend the directory name to each directory (default: _false_)
        * @param $recursive Boolean whether to recurse into subdirectories (default: _false_)
        * @return An array containing the directory names
        */
        """
        if strrpos(directory, "/") != len(directory) - 1:
            directory += "/"
        if not os.path.isdir(directory):
            message = ObjectFactory.getInstance("message")
            raise IllegalArgumentException(
                message.getText("The directory '%0%' does not exist.", [directory])
            )

        result = []
        d = os.scandir(directory)
        # iterate over all files
        for file in d:
            # exclude this and parent directory
            if file.name != "." and file.name != "..":
                # include directories only
                if file.is_dir():
                    # recurse
                    if recursive:
                        dirs = getDirectories(
                            directory + file.name,
                            pattern,
                            prependDirectoryName,
                            recursive,
                        )
                        result = result + dirs
                    if re.match(pattern, file.name):
                        if prependDirectoryName:
                            file = directory + file.name
                        result.append(file)
        d.close()
        return result

    @staticmethod
    def copy_rec(source, dest):
        """
        Recursive copy for files AND directories.

        Args:
            source (str): The name of the source directory/file.
            dest (str): The name of the destination directory/file.
        """
        if os.path.isfile(source):
            perms = os.stat(source).st_mode
            return shutil.copy(source, dest) and os.chmod(dest, perms)
        if not os.path.isdir(source):
            message = ObjectFactory.get_instance("message")
            raise IllegalArgumentException(
                message.get_text(
                    "Cannot copy %0% (it's neither a file nor a directory).", [source]
                )
            )
        FileController.copy_rec_dir(source, dest)

    @staticmethod
    def copy_rec_dir(source, dest):
        """
        Recursive copy for directories.

        Args:
            source (str): The name of the source directory.
            dest (str): The name of the destination directory.
        """
        if not os.path.isdir(dest):
            FileController.mkdir_rec(dest)
        with os.scandir(source) as entries:
            for entry in entries:
                if entry.name == "." or entry.name == "..":
                    continue
                FileController.copy_rec(
                    f"{source}/{entry.name}", f"{dest}/{entry.name}"
                )

    @staticmethod
    def mkdir_rec(dirname, perm=0o775):
        """
        Recursive directory creation.

        Args:
            dirname (str): The name of the directory.
            perm (int, optional): The permission for the new directories (default: 0o775).
        """
        if not os.path.isdir(dirname):
            os.makedirs(dirname, perm)

    @staticmethod
    def empty_dir(dirname):
        """
        Empty a directory.

        Args:
            dirname (str): The name of the directory.
        """
        if os.path.isdir(dirname):
            files = [os.path.join(dirname, f) for f in os.listdir(dirname)]
            for file in files:
                if os.path.isfile(file):
                    os.unlink(file)
                elif os.path.isdir(file):
                    FileController.empty_dir(file)
                    os.rmdir(file)

    @staticmethod
    def realpath(path):
        """
        Realpath function that also works for non-existing paths.

        Args:
            path (str): The path.

        Returns:
            str: The canonical path.
        """
        if os.path.exists(path):
            return os.path.realpath(path).replace("\\", "/")

        path = path.replace("\\", "/")
        parts = [p for p in path.split("/") if p]
        absolutes = []
        for part in parts:
            if part == ".":
                continue
            elif part == "..":
                absolutes.pop()
            else:
                absolutes.append(part)
        result = "/".join(absolutes)
        if os.name != "nt":
            result = "/" + result
        return result

    @staticmethod
    def sanitizeFilename(file: str) -> str:
        """
        * Get a sanitized filename
        * code from: http://stackoverflow.com/questions/2021624/string-sanitizer-for-filename#2021729
        * @param $file
        * @return String
        """
        file = re.sub(r"([^\w\s\d\-_~,;:\[\]\(\).])", "", file)
        file = re.sub(r"([\.]{2,})", "", file)
        return file

    @staticmethod
    def fix_filename(file: str) -> Union[str, None]:
        """
        * Fix the name of an existing file to be used with php file functions
        * @param $file
        * @return String or null, if the file does not exist
        """
        if os.path.exists(file):
            return file
        else:
            file = file.encode("utf-8").decode("cp1252")
            if os.path.exists(file):
                return file
        return None

    @staticmethod
    def urlencode_filename(file: str) -> str:
        """
        * Url encode a file path
        * @param $file
        * @return String
        """
        parts = file.split("/")
        result = []
        for part in parts:
            result.append(urllib.parse.quote(part))
        return "/".join(result)

    @staticmethod
    def file_exists(file: str) -> bool:
        """
        * Check if the given file exists
        * @param $file
        * @return Boolean
        """
        try:
            with open(file, "r"):
                return True
        except FileNotFoundError:
            return False

    @staticmethod
    def basename(file):
        """
        * Get the trailing name component of a path (locale independent)
        * @param $file
        * @return String
        """
        parts = file.split("/")
        return parts[-1]
