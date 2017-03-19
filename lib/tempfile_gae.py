#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'Liantian'
# __email__ = "liantian.me+code@gmail.com"
#
# Copyright 2015-2016 liantian
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>

"""Temporary files.
This module is a replacement for the stock tempfile module in Python,
and provides only in-memory temporary files as implemented by
cStringIO. The only functionality provided is the TemporaryFile
function.
"""
try:
  from cStringIO import StringIO
except ImportError:
  from StringIO import StringIO

import os
__all__ = [
  "TemporaryFile",
  "NamedTemporaryFile", "mkstemp", "mkdtemp", "mktemp",
  "TMP_MAX", "gettempprefix", "tempdir", "gettempdir",
]
TMP_MAX = 10000
template = "tmp"
tempdir = None
def TemporaryFile(mode='w+b', bufsize=-1, suffix="",
                  prefix=template, dir=None):
  """Create and return a temporary file.
  Arguments:
  'prefix', 'suffix', 'dir', 'mode', 'bufsize' are all ignored.
  Returns an object with a file-like interface.  The file is in memory
  only, and does not exist on disk.
  """
  return StringIO()
def PlaceHolder(*args, **kwargs):
  raise NotImplementedError("Only tempfile.TemporaryFile is available for use")
NamedTemporaryFile = PlaceHolder
mkstemp = PlaceHolder
mkdtemp = PlaceHolder
mktemp = PlaceHolder
gettempprefix = PlaceHolder
tempdir = PlaceHolder

def gettempdir(*args, **kwargs):
    return os.path.dirname(os.path.abspath(__file__)) + '/../tmp'