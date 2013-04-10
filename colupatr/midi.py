# Copyright (C) 2007,2010-2013	Valek Filippov (frob@df.ru)
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

import sys,struct

pitches = {
	0x0:'C(-1)',0x1:'Db(-1)',0x2:'D(-1)',0x3:'Eb(-1)',
	0x4:'E(-1)',0x5:'F(-1)',0x6:'Gb(-1)',0x7:'G(-1)',
	0x8:'Ab(-1)',0x9:'A(-1)',0x0A:'Bb(-1)',0x0B:'B(-1)',
	0x0C:'C0',0x0D:'Db0',0x0E:'D0',0x0F:'Eb0',
	0x10:'E0',0x11:'F0',0x12:'Gb0',0x13:'G0',
	0x14:'Ab0',0x15:'A0',0x16:'Bb0',0x17:'B0',
	0x18:'C1',0x19:'Db1',0x1A:'D1',0x1B:'Eb1',
	0x1C:'E1',0x1D:'F1',0x1E:'Gb1',0x1F:'G1',
	0x20:'Ab1',0x21:'A1',0x22:'Bb1',0x23:'B1',
	0x24:'C2',0x25:'Db2',0x26:'D2',0x27:'Eb2',
	0x28:'E2',0x29:'F2',0x2A:'Gb2',0x2B:'G2',
	0x2C:'Ab2',0x2D:'A2',0x2E:'Bb2',0x2F:'B2',
	0x30:'C3',0x31:'Db3',0x32:'D3',0x33:'Eb3',
	0x34:'E3',0x35:'F3',0x36:'Gb3',0x37:'G3',
	0x38:'Ab3',0x39:'A3',0x3A:'Bb3',0x3B:'B3',
	0x3C:'C4',0x3D:'Db4',0x3E:'D4',0x3F:'Eb4',
	0x40:'E4',0x41:'F4',0x42:'Gb4',0x43:'G4',
	0x44:'Ab4',0x45:'A4',0x46:'Bb4',0x47:'B4',
	0x48:'C5',0x49:'Db5',0x4A:'D5',0x4B:'Eb5',
	0x4C:'E5',0x4D:'F5',0x4E:'Gb5',0x4F:'G5',
	0x50:'Ab5',0x51:'A5',0x52:'Bb5',0x53:'B5',
	0x54:'C6',0x55:'Db6',0x56:'D6',0x57:'Eb6',
	0x58:'E6',0x59:'F6',0x5A:'Gb6',0x5B:'G6',
	0x5C:'Ab6',0x5D:'A6',0x5E:'Bb6',0x5F:'B6',
	0x60:'C7',0x61:'Db7',0x62:'D7',0x63:'Eb7',
	0x64:'E7',0x65:'F7',0x66:'Gb7',0x67:'G7',
	0x68:'Ab7',0x69:'A7',0x6A:'Bb7',0x6B:'B7',
	0x6C:'C8',0x6D:'Db8',0x6E:'D8',0x6F:'Eb8',
	0x70:'E8',0x71:'F8',0x72:'Gb8',0x73:'G8',
	0x74:'Ab8',0x75:'A8',0x76:'Bb8',0x77:'B8',
	0x78:'C9',0x79:'Db9',0x7A:'D9',0x7B:'Eb9',
	0x7C:'E9',0x7D:'F9',0x7E:'Gb9',0x7F:'G9'}

controllers = {
	0x00:'Bank Select',
	0x01:'Modulation',
	0x02:'Breath Controller',
	0x04:'Foot Controller',
	0x05:'Portamento Time',
	0x06:'Data Entry (MSB)',
	0x07:'Main Volume',
	0x08:'Balance',
	0x0A:'Pan',
	0x0B:'Expression Controller',
	0x0C:'Effect Control 1',
	0x0D:'Effect Control 2',
	0x10:'General-Purpose Controller 1',
	0x11:'General-Purpose Controller 2',
	0x12:'General-Purpose Controller 3',
	0x13:'General-Purpose Controller 4',
	0x20:'LSB for controller 0',
	0x21:'LSB for controller 1',
	0x22:'LSB for controller 2',
	0x23:'LSB for controller 3',
	0x24:'LSB for controller 4',
	0x25:'LSB for controller 5',
	0x26:'LSB for controller 6',
	0x27:'LSB for controller 7',
	0x28:'LSB for controller 8',
	0x29:'LSB for controller 9',
	0x2A:'LSB for controller 10',
	0x2B:'LSB for controller 11',
	0x2C:'LSB for controller 12',
	0x2D:'LSB for controller 13',
	0x2E:'LSB for controller 14',
	0x2F:'LSB for controller 15',
	0x30:'LSB for controller 16',
	0x31:'LSB for controller 17',
	0x32:'LSB for controller 18',
	0x33:'LSB for controller 19',
	0x34:'LSB for controller 20',
	0x35:'LSB for controller 21',
	0x36:'LSB for controller 22',
	0x37:'LSB for controller 23',
	0x38:'LSB for controller 24',
	0x39:'LSB for controller 25',
	0x3A:'LSB for controller 26',
	0x3B:'LSB for controller 27',
	0x3C:'LSB for controller 28',
	0x3D:'LSB for controller 29',
	0x3E:'LSB for controller 30',
	0x3F:'LSB for controller 31',
	0x40:'Damper pedal',
	0x41:'Portamento',
	0x42:'Sostenuto',
	0x43:'Soft Pedal',
	0x44:'Legato Footswitch',
	0x45:'Hold 2',
	0x46:'Sound Controller 1',
	0x47:'Sound Controller 2',
	0x48:'Sound Controller 3',
	0x49:'Sound Controller 4',
	0x4A:'Sound Controller 5',
	0x4B:'Sound Controller 6',
	0x4C:'Sound Controller 7',
	0x4D:'Sound Controller 8',
	0x4E:'Sound Controller 9',
	0x4F:'Sound Controller 10',
	0x50:'General-Purpose Controller 5',
	0x51:'General-Purpose Controller 6',
	0x52:'General-Purpose Controller 7',
	0x53:'General-Purpose Controller 8',
	0x54:'Portamento Control',
	0x5B:'Effects 1 Depth',
	0x5C:'Effects 2 Depth',
	0x5D:'Effects 3 Depth',
	0x5E:'Effects 4 Depth',
	0x5F:'Effects 5 Depth',
	0x60:'Data Increment',
	0x61:'Data Decrement',
	0x62:'Non-Registered Parameter Number (LSB)',
	0x63:'Non-Registered Parameter Number (MSB)',
	0x64:'Registered Parameter Number (LSB)',
	0x65:'Registered Parameter Number (MSB)',
	0x79:'Reset All Controllers',
	0x7A:'Local Control',
	0x7B:'All Notes Off',
	0x7C:'Omni Off',
	0x7D:'Omni On',
	0x7E:'Mono On (Poly Off)',
	0x7F:'Poly On (Mono Off)'
}