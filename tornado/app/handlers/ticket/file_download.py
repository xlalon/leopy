# -*- coding: utf-8 -*-

from ..base.base_handler import BaseHandler
from io import StringIO


class FileDownloadHandler(BaseHandler):
    async def get(self):
        self.set_header('Content-Type', 'application/vnd.ms-excel')
        self.set_header('Transfer-Encoding', 'chunked')
        self.set_header('Content-Disposition', 'attachment;filename="example.xls')
        data = StringIO()
        data.write('Example Text\n')
        self.write(data.getvalue())
        self.finish()



