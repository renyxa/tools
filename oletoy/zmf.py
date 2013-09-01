# Copyright (C) 2013 David Tardon (dtardon@redhat.com)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 or later of the GNU General Public
# License as published by the Free Software Foundation.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA
#

import struct

from utils import add_iter, add_pgiter, rdata

def read(data, offset, fmt):
	return rdata(data, offset, fmt)[0]

class ZMF5Parser(object):

	def __init__(self, data, page, parent):
		self.data = data
		self.page = page
		self.parent = parent

	def parse(self):
		content = self.parse_header()
		self.parse_content(content)

	def parse_header(self):
		offset = int(read(self.data, 0x20, '<I'))
		data = self.data[0:offset]
		add_pgiter(self.page, 'Header', 'zmf', 'zmf5_header', data, self.parent)
		return offset

	def parse_content(self, begin):
		data = self.data[begin:]
		content_iter = add_pgiter(self.page, 'Content', 'zmf', 0, data, self.parent)
		self._parse_group(data, content_iter)

	def parse_object(self, data, parent):
		objiter = add_pgiter(self.page, 'Object', 'zmf', 'zmf5_object', data, parent)
		add_pgiter(self.page, 'Header', 'zmf', 'zmf5_object_header', data[0:32], objiter)
		off = 4
		# TODO: this is probably set of flags
		(typ, off) = rdata(data, off, '<I')
		if typ == 0xc or typ == 0xd:
			self._parse_group(data[32:], objiter)
		else:
			add_pgiter(self.page, 'Data', 'zmf', 0, data[32:], objiter)

	def _parse_group(self, data, parent):
		off = 0
		while off + 4 <= len(data):
			length = int(read(data, off, '<I'))
			if off + length <= len(data):
				self.parse_object(data[off:off + length], parent)
			off += length

def parse_header(page, data, parent):
	pass

def parse_text_styles(page, data, parent):
	pass

def parse_pages(page, data, parent):
	pass

def parse_doc(page, data, parent):
	pass

def add_zmf5_header(hd, size, data):
	off = 8
	(sig, off) = rdata(data, off, '<I')
	add_iter(hd, 'Signature', '0x%x' % sig, off - 4, 4, '<I')
	(version, off) = rdata(data, off, '<I')
	add_iter(hd, 'Version', version, off - 4, 4, '<I')
	off += 12
	(count, off) = rdata(data, off, '<I')
	add_iter(hd, 'Count of objects', count, off - 4, 4, '<I')
	(content, off) = rdata(data, off, '<I')
	add_iter(hd, 'Start of content', content, off - 4, 4, '<I')
	(preview, off) = rdata(data, off, '<I')
	add_iter(hd, 'Start of preview bitmap', preview, off - 4, 4, '<I')
	off += 16
	(size, off) = rdata(data, off, '<I')
	add_iter(hd, 'File size', size, off - 4, 4, '<I')

def add_zmf5_object_header(hd, size, data):
	(size, off) = rdata(data, 0, '<I')
	add_iter(hd, 'Size', size, off - 4, 4, '<I')
	(typ, off) = rdata(data, off, '<I')
	add_iter(hd, 'Type', typ, off - 4, 4, '<I')

zmf_ids = {
	'zmf5_header': add_zmf5_header,
	'zmf5_object_header': add_zmf5_object_header,
}

def zmf3_open(page, data, parent, fname):
	if fname == 'Header':
		parse_header(page, data, parent)
	if fname == 'TextStyles.zmf':
		parse_text_styles(page, data, parent)
	elif fname == 'Callisto_doc.zmf':
		parse_doc(page, data, parent)
	elif fname == 'Callisto_pages.zmf':
		parse_pages(page, data, parent)

def zmf5_open(data, page, parent):
	parser = ZMF5Parser(data, page, parent)
	parser.parse()

# vim: set ft=python sts=4 sw=4 noet: