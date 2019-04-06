# -*- coding: utf-8 -*-


from .file_download import FileDownloadHandler


__all__ = ['urls']


urls = [
    # 文件下载
    (r'file_download', FileDownloadHandler),
]

