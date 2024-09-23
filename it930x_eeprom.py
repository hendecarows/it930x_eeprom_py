#!/usr/bin/env python3

import collections.abc
import os
import platform
import sys
import usb1

import wx
import wx.xrc
from it930x_eeprom_gui import MainFrame

from logging import getLogger, DEBUG, NullHandler, StreamHandler, Formatter

#
# Simple Hexdump
# https://gist.github.com/NeatMonster/c06c61ba4114a2b31418a364341c26c0
#
class hexdump:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        for i in range(0, len(self.data), 16):
            bs = bytearray(self.data[i:i+16])
            line = '{:04x}  {:23}  {:23}  {:16}'.format(
                i,
                ' '.join(('{:02x}'.format(x) for x in bs[:8])),
                ' '.join(('{:02x}'.format(x) for x in bs[8:])),
                ''.join((chr(x) if 32 <= x < 127 else '.' for x in bs)),
            )
            yield line

    def __str__(self):
        return '\n'.join(self)

    def __repr__(self):
        return '\n'.join(self)

class Tuner:
    VidPid = {
        'PX-W3U4': (0x0511, 0x083f),
        'PX-W3PE4': (0x0511, 0x023f),
        'PX-W3PE5': (0x0511, 0x073f),
        'PX-Q3U4': (0x0511, 0x084a),
        'PX-Q3PE4': (0x0511, 0x024a),
        'PX-Q3PE5': (0x0511, 0x074a),
        'PX-MLT5PE': (0x0511, 0x024e),
        'PX-MLT5U': (0x0511, 0x084e),
        'PX-MLT8PE3': (0x0511, 0x0252),
        'PX-MLT8PE5': (0x0511, 0x0253),
        'PX-M1UR': (0x0511, 0x0854),
        'PX-S1UR': (0x0511, 0x0855),
        'DTV02-1T1S-U': (0x0511, 0x004b),
        'DTV02A-1T1S-U 2309': (0x0511, 0x084b),
        'DTV02A-4TS-P': (0x0511, 0x0254),
        'DTV02-5T-P': (0x0511, 0x024d),
        'DTV03A-1TU 202111': (0x0511, 0x0052),
        'UNKNOWN': (0x048d, 0x9306),
    }

    @classmethod
    def __iter__(cls):
        for tuner in cls.VidPid:
            yield tuner

    @classmethod
    def items(cls):
        for tuner, vid_pid in cls.VidPid.items():
            yield (tuner, vid_pid)

    @classmethod
    def get_vid_pid(cls, tuner):
        if tuner in cls.VidPid:
            return cls.VidPid[tuner]
        else:
            return None

    def get_tuner(cls, vid, pid):
        for tuner, vid_pid in cls.pid_vid.items():
            if vid_pid[0] == vid and vid_pid[1] == pid:
                return tuner
        return None


class IT930x:

    END_POINT1_IN = 0x81
    END_POINT2_OUT = 0x02

    def __init__(self):
        self.logger = getLogger(__name__)
        self.logger.addHandler(NullHandler())
        self.logger.setLevel(DEBUG)
        self.logger.propagate = True

        self.usb_vid = 0
        self.usb_pid = 0
        self.usb_bus = 0
        self.usb_address = 0
        self.usb_context = None
        self.usb_handle = None
        self._sequence = -1

    @property
    def sequence(self):
        self._sequence += 1
        if self._sequence > 0xff:
            self._sequence = 0
        return self._sequence

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.close_device()

    def to_hex(self, data):
        try:
            if isinstance(data, collections.abc.Iterable):
                return ' '.join(['{:02x}'.format(x) for x in data])
            else:
                return '{:02x}'.format(data)
        except ValueError:
            return '{}'.format(data)

    def debug_usb_bulk(self, read_write, endpoint, data):
        msg = '{} {:02x} {:02x} ; {}'.format(
            read_write, endpoint, len(data), self.to_hex(data)
        )
        self.logger.debug(msg)

    def get_checksum(self, data, omit_last_bytes=0, start_byte=1):
        size = len(data) - omit_last_bytes
        checksum = 0
        for i in range(start_byte, size):
            if i % 2 != 0:
                checksum += data[i] << 8
            else:
                checksum += data[i]
        checksum = ~checksum
        return checksum & 0xffff

    def add_checksum(self, data):
        checksum = self.get_checksum(data)
        # last 2bytes : checksum
        data.append((checksum >> 8) & 0xff)
        data.append(checksum & 0xff)
        # first byte : data length
        data[0] = len(data) - 1

    def write_command(self, command, write_data, read_length):
        '''
           write and read command
           bulk write        : 0b 00 00 00 01 02 00 00 12 22 db ec
           bulk read         : 05 00 00 01 fe ff

           [0] 0b            : data length from [1] to [11]
           [1-2] 00 00       : command
           [3] 00            : sequence number 00 to ff
           [4] 01            : read or write length
           [5] 02            : read or write address length
           [6-9] 00 00 12 22 : read or write address
           [10-11] db ec     : checksum from [1] to [9]

           [0] 05            : data length from [1] to [5]
           [1] 00            : sequence number
           [2] 00            : error code no error when 0
           [3] 01            : read data
           [4-5] fe ff       : checksum from [1] to [3]
        '''
        write_buf = [
            0,
            (command >> 8) & 0xff,
            command & 0xff,
            self.sequence,
        ]
        if isinstance(write_data, collections.abc.Iterable):
            write_buf.extend(write_data)
        else:
            if write_data is None:
                pass
            else:
                write_buf.append(write_data)
        self.add_checksum(write_buf)
        self.debug_usb_bulk('BW', self.END_POINT2_OUT, write_buf)
        write_length = self.usb_handle.bulkWrite(self.END_POINT2_OUT, bytes(write_buf))
        if write_length != len(write_buf):
            raise Exception(
                'fail to bulk write {:x} ; {}'.format(
                    self.END_POINT2_OUT, self.to_hex(write_buf)
                )
            )

        add_length = 5
        read_data = self.usb_handle.bulkRead(self.END_POINT1_IN, read_length + add_length)
        self.debug_usb_bulk('BR', self.END_POINT1_IN, read_data)
        # check error
        if read_data[2] != 0:
            raise Exception(
                'fail to transfer error code {:x}'.format(read_data[2])
            )
        # last 2 bytes : checksum
        tmpsum = int.from_bytes(read_data[-2:], 'big')
        checksum = self.get_checksum(read_data, omit_last_bytes=2)
        if checksum != tmpsum:
            raise Exception(
                'invalid checksum {:x} != {:x}'.format(checksum, tmpsum)
            )
        read_data_length = len(read_data) - add_length
        if read_data_length == 1:
            return read_data[3]
        elif read_data_length > 1:
            return read_data[3:-2]
        else:
            return None

    def read_eeprom(self, eeprom_address, read_address, read_length=1):
        '''
           bulk write   : 0a 00 04 a8 01 01 01 00 19 56 e0
           bulk read    : 05 a8 00 30 27 ff

           [0] 0a       : data length from [1] to [10]
           [1-2] 00 04  : command number (read eeprom)
           [3] a8       : sequence number 00 to ff
           [4] 01       : read value length
           [5] 01       : eeprom address
           [6] 01       : read address length
           [7-8] 00 19  : read address
           [9-10] 56 e0 : checksum from [1] to [8]

           [0] 05       : data length from [1] to [5]
           [1] a8       : sequence number
           [2] 00       : error code no error when 0
           [3] 30       : read value
           [4-5] 27 ff  : checksum from [1] to [3]
        '''
        # 0x0004 : read eeprom
        command = 0x0004
        if read_address > 0xff:
            read_address_length = 2
        else:
            read_address_length = 1
        write_data = [
            read_length & 0xff,
            eeprom_address & 0xff,
            read_address_length & 0xff,
        ]
        # append 2 bytes read address
        write_data.extend(read_address.to_bytes(2, 'big'))
        # write command
        return self.write_command(command, write_data, read_length)

    def write_eeprom(self, eeprom_address, write_address, write_values):
        '''
           bulk write    : 0b 00 05 05 01 01 01 00 a0 31 c8 58
           bulk read     : 04 05 00 fa ff

           [0] 0b        : data length from [1] to [11]
           [1-2] 00 05   : command number (write eeprom)
           [3] 05        : sequence number 00 to ff
           [4] 01        : write value length
           [5] 01        : eeprom address
           [6] 01        : write address length
           [7-8] 00 a0   : write address
           [9] 31        : write value
           [10-11] c8 58 : checksum from [1] to [9]

           [0] 04        : data length from [1] to [4]
           [1] 05        : sequence number
           [2] 00        : error code no error when 0
           [3-4] fa ff   : checksum from [1] to [2]
        '''
        # 0x0005 : write eeprom
        command = 0x0005
        if write_address > 0xff:
            write_address_length = 2
        else:
            write_address_length = 1
        if isinstance(write_values, collections.abc.Iterable):
            write_data_length = len(write_values)
        else:
            write_data_length = 1
            write_values = [write_values,]
        write_data = [
            write_data_length & 0xff,
            eeprom_address & 0xff,
            write_address_length & 0xff,
        ]
        # append 2 bytes write address
        write_data.extend(write_address.to_bytes(2, 'big'))
        # append write data
        write_data.extend(write_values)
        # write command (read_length = 0)
        self.write_command(command, write_data, 0)

    def dump_eeprom(self, eeprom_address=0x01, eeprom_size=256, read_size=16):
        data = bytearray()
        quotient, remainder = divmod(eeprom_size, read_size)
        size = quotient * read_size
        for address in range(0, size, read_size):
            data.extend(self.read_eeprom(eeprom_address, address, read_size))
        if remainder != 0:
            for address in range(size, eeprom_size):
                data.append(self.read_eeprom(eeprom_address, address))
        return data

    def enumerate_device(self, vid, pid):
        usb_devices = {}
        try:
            with usb1.USBContext() as context:
                for device in context.getDeviceIterator(skip_on_error=True):
                    if device.getVendorID() == vid and device.getProductID() == pid:
                        bus = device.getBusNumber()
                        address = device.getDeviceAddress()
                        key = 'VID={:#06x} PID={:#06x} BUS={} ADDRESS={}'.format(vid, pid, bus, address)
                        usb_devices[key] = (vid, pid, bus, address)
                        self.logger.debug('{} found'.format(key))
        except Exception as e:
            self.logger.debug(e)
            usb_devices = {}
        return usb_devices

    def open_device(self, vid, pid, bus, address, loglevel=usb1.LOG_LEVEL_INFO):
        try:
            self.close_device()
            self.usb_context = usb1.USBContext()
            self.usb_context.setDebug(loglevel)
            for device in self.usb_context.getDeviceIterator(skip_on_error=True):
                if device.getVendorID() != vid:
                    continue
                if device.getProductID() != pid:
                    continue
                if device.getBusNumber() != bus:
                    continue
                if device.getDeviceAddress() != address:
                    continue
                self.usb_handle = device.open()
                if usb1.hasCapability(usb1.CAP_SUPPORTS_DETACH_KERNEL_DRIVER):
                    self.logger.debug('supports detach kernel driver')
                    self.usb_handle.setAutoDetachKernelDriver(True)
                self.usb_handle.claimInterface(0)
                self.usb_vid = vid
                self.usb_pid = pid
                self.usb_bus = bus
                self.usb_address = address
                self.logger.debug('open vid={:0>4x} pid={:0>4x} bus={} address={} device'.format(vid, pid, bus, address))
                break
        except Exception as e:
            self.logger.debug(e)
            self.close_device()
            raise

    def close_device(self):
        if self.usb_handle is not None:
            self.usb_handle.close()
            self.usb_handle = None
        if self.usb_context is not None:
            self.usb_context.close()
            self.usb_context = None
        self.usb_vid = 0
        self.usb_pid = 0
        self.usb_bus = 0
        self.usb_address = 0


class MyApp(wx.App):

    def OnInit(self):
        self.logger = getLogger(__name__)
        self.logger.addHandler(NullHandler())
        self.logger.setLevel(DEBUG)
        self.logger.propagate = True

        self.platform = platform.system()
        self.tuner = 'unknown'
        self.vid = 0
        self.pid = 0
        self.backup_device_eeprom = None
        self.restore_device_eeprom = None
        self.restore_file_eeprom = None

        if self.platform == 'Windows':
            self.logger.debug('platform: {}'.format(self.platform))
            self.text_font = wx.Font(pointSize=10, family=wx.FONTFAMILY_MODERN,
                        style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, underline=False,
                        faceName='ＭＳ ゴシック', encoding=wx.FONTENCODING_DEFAULT)
        elif self.platform == 'Linux':
            self.logger.debug('platform: {}'.format(self.platform))
            self.text_font = wx.Font(pointSize=11, family=wx.FONTFAMILY_MODERN,
                        style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, underline=False,
                        faceName='Ubuntu Mono', encoding=wx.FONTENCODING_DEFAULT)
        elif self.platform == 'Darwin':
            self.logger.debug('platform: {}'.format(self.platform))
            self.text_font = wx.Font(pointSize=12, family=wx.FONTFAMILY_MODERN,
                        style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, underline=False,
                        faceName='Menlo', encoding=wx.FONTENCODING_DEFAULT)
        else:
            self.logger.debug('platform: {}'.format(self.platform))
            self.text_font = wx.Font(pointSize=10, family=wx.FONTFAMILY_MODERN,
                        style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, underline=False,
                        faceName='', encoding=wx.FONTENCODING_DEFAULT)

        self.frame : wx.Frame = MainFrame(None)
        self.notebookMain : wx.Notebook = self.frame.m_notebookMain
        self.choiceBackupTuner : wx.Choice = self.frame.m_choiceBackupTuner
        self.spinCtrlBackupVid : wx.SpinCtrl = self.frame.m_spinCtrlBackupVid
        self.spinCtrlBackupPid : wx.SpinCtrl = self.frame.m_spinCtrlBackupPid
        self.buttonBackupFind : wx.Button = self.frame.m_buttonBackupFind
        self.choiceBackupDevice : wx.Choice = self.frame.m_choiceBackupDevice
        self.buttonBackupRead : wx.Button = self.frame.m_buttonBackupRead
        self.notebookBackupDeviceEeprom : wx.Notebook = self.frame.m_notebookBackupDeviceEeprom
        self.textCtrlBackupDeviceEeprom : wx.TextCtrl = self.frame.m_textCtrlBackupDeviceEeprom
        self.buttonBackupSave : wx.Button = self.frame.m_buttonBackupSave

        self.textCtrlBackupDeviceEeprom.SetFont(self.text_font)
        for tuner, vid_pid in Tuner.items():
            self.choiceBackupTuner.Append(tuner, vid_pid)

        self.choiceBackupTuner.Bind(wx.EVT_CHOICE, self.OnChoiceBackupTuner)
        self.buttonBackupFind.Bind(wx.EVT_BUTTON, self.OnButtonClickBackupFind)
        self.buttonBackupRead.Bind(wx.EVT_BUTTON, self.OnButtonClickBackupRead)
        self.buttonBackupSave.Bind(wx.EVT_BUTTON, self.OnButtonClickBackupSave)

        self.spinCtrlRestoreVid : wx.SpinCtrl = self.frame.m_spinCtrlRestoreVid
        self.spinCtrlRestorePid : wx.SpinCtrl = self.frame.m_spinCtrlRestorePid
        self.buttonRestoreFind : wx.Button = self.frame.m_buttonRestoreFind
        self.choiceRestoreDevice : wx.Choice = self.frame.m_choiceRestoreDevice
        self.buttonRestoreRead : wx.Button = self.frame.m_buttonRestoreRead
        self.textCtrlRestoreFile : wx.TextCtrl = self.frame.m_textCtrlRestoreFile
        self.buttonRestoreBrowse : wx.Button = self.frame.m_buttonRestoreBrowse
        self.notebookRestoreDeviceEeprom : wx.Notebook = self.frame.m_notebookRestoreDeviceEeprom
        self.textCtrlRestoreDeviceEeprom : wx.TextCtrl = self.frame.m_textCtrlRestoreDeviceEeprom
        self.textCtrlRestoreFileEeprom : wx.TextCtrl = self.frame.m_textCtrlRestoreFileEeprom
        self.textCtrlRestoreLog : wx.TextCtrl = self.frame.m_textCtrlRestoreLog
        self.buttonRestoreWrite : wx.Button = self.frame.m_buttonRestoreWrite

        self.spinCtrlBackupVid.SetBase(16)
        self.spinCtrlBackupPid.SetBase(16)
        self.spinCtrlRestorePid.SetBase(16)
        self.spinCtrlRestoreVid.SetBase(16)
        self.spinCtrlRestorePid.SetValue(0x048d)
        self.spinCtrlRestoreVid.SetValue(0x9306)

        self.textCtrlRestoreDeviceEeprom.SetFont(self.text_font)
        self.textCtrlRestoreFileEeprom.SetFont(self.text_font)
        self.textCtrlRestoreLog.SetFont(self.text_font)

        self.buttonRestoreFind.Bind(wx.EVT_BUTTON, self.OnButtonClickRestoreFind)
        self.buttonRestoreRead.Bind(wx.EVT_BUTTON, self.OnButtonClickRestoreRead)
        self.buttonRestoreBrowse.Bind(wx.EVT_BUTTON, self.OnButtonClickRestoreBrowse)
        self.buttonRestoreWrite.Bind(wx.EVT_BUTTON, self.OnButtonClickRestoreWrite)

        icon = wx.Icon(self.GetResourcePath('eeprom.ico'), wx.BITMAP_TYPE_ICO)
        self.frame.SetIcon(icon)
        self.frame.Show()
        return True

    def GetResourcePath(self, filename):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, filename)
        else:
            return filename

    def ClearBackup(self):
        self.choiceBackupDevice.Clear()
        self.buttonBackupRead.Enable(False)
        self.textCtrlBackupDeviceEeprom.Clear()
        self.buttonBackupSave.Enable(False)
        self.backup_device_eeprom = None

    def ClearRestore(self, is_device : bool = True):
        if is_device:
            self.choiceRestoreDevice.Clear()
            self.buttonRestoreRead.Enable(False)
        self.textCtrlRestoreFile.Clear()
        self.buttonRestoreBrowse.Enable(False)
        self.textCtrlRestoreDeviceEeprom.Clear()
        self.textCtrlRestoreFileEeprom.Clear()
        self.textCtrlRestoreLog.Clear()
        self.buttonRestoreWrite.Enable(False)
        self.restore_device_eeprom = None
        self.restore_file_eeprom = None

    def OnChoiceBackupTuner(self, event):
        choice : wx.Choice = event.GetEventObject()
        n = choice.GetSelection()
        if n == wx.NOT_FOUND:
            return
        else:
            vid, pid = choice.GetClientData(n)
            self.spinCtrlBackupVid.SetValue(vid)
            self.spinCtrlBackupPid.SetValue(pid)
            self.ClearBackup()
            self.buttonBackupFind.Enable()

    def OnButtonClickBackupFind(self, event):
        self.ClearBackup()
        vid = self.spinCtrlBackupVid.GetValue()
        pid = self.spinCtrlBackupPid.GetValue()
        with IT930x() as it930x:
            devices = it930x.enumerate_device(vid, pid)
        if len(devices) == 0:
            wx.MessageBox(
                'VID:PID={:#06x}:{:#06x} デバイスが見つかりません'.format(vid, pid),
                caption='情報',
            )
        else:
            for key, val in devices.items():
                self.choiceBackupDevice.Append(key, val)
            self.choiceBackupDevice.Enable()
            self.choiceBackupDevice.SetSelection(0)
            self.buttonBackupRead.Enable()

    def OnButtonClickBackupRead(self, event):
        n = self.choiceBackupDevice.GetSelection()
        if n == wx.NOT_FOUND:
            return
        vid, pid, bus, address = self.choiceBackupDevice.GetClientData(n)
        self.logger.debug('backup device vid={:#06x} pid={:#06x} bus={} address={}'.format(vid, pid, bus, address))

        try:
            with IT930x() as it930x:
                it930x.open_device(vid, pid, bus, address)
                self.backup_device_eeprom = it930x.dump_eeprom()
                self.textCtrlBackupDeviceEeprom.SetValue(str(hexdump(self.backup_device_eeprom)))
                self.buttonBackupSave.Enable()
                self.tuner = 'unknown'
                self.vid = vid
                self.pid = pid
                self.tuner = self.GetTunerName(vid, pid)
        except Exception as e:
            self.logger.error(e)
            wx.MessageBox(str(e), caption='エラー', style=wx.OK | wx.ICON_ERROR)

    def OnButtonClickBackupSave(self, event):
        with wx.FileDialog(self.frame, 'ファイルの保存',
            defaultFile='{}_{:04x}_{:04x}.bin'.format(self.tuner, self.vid, self.pid),
            wildcard='EEPROMファイル (*.bin)|*.bin|すべてのファイル (*.*)|*.*',
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'wb') as file:
                    file.write(self.backup_device_eeprom)
            except IOError as e:
                self.logger.error(e)
                wx.MessageBox(str(e), caption='エラー', style=wx.OK | wx.ICON_ERROR)

    def OnButtonClickRestoreFind(self, event):
        self.ClearRestore()
        vid = self.spinCtrlRestoreVid.GetValue()
        pid = self.spinCtrlRestorePid.GetValue()
        with IT930x() as it930x:
            devices = it930x.enumerate_device(vid, pid)
        if len(devices) == 0:
            wx.MessageBox(
                'VID:PID={:#06x}:{:#06x} デバイスが見つかりません'.format(vid, pid),
                caption='情報',
            )
        else:
            for key, val in devices.items():
                self.choiceRestoreDevice.Append(key, val)
            self.choiceRestoreDevice.Enable()
            self.choiceRestoreDevice.SetSelection(0)
            self.buttonRestoreRead.Enable()

    def OnButtonClickRestoreRead(self, event):
        self.ClearRestore(is_device=False)
        n = self.choiceRestoreDevice.GetSelection()
        if n == wx.NOT_FOUND:
            return
        vid, pid, bus, address = self.choiceRestoreDevice.GetClientData(n)
        self.logger.debug('restore device vid={:#06x} pid={:#06x} bus={} address={}'.format(vid, pid, bus, address))

        try:
            with IT930x() as it930x:
                it930x.open_device(vid, pid, bus, address)
                self.restore_device_eeprom = it930x.dump_eeprom()
                self.textCtrlRestoreDeviceEeprom.SetValue(str(hexdump(self.restore_device_eeprom)))
                self.notebookRestoreDeviceEeprom.SetSelection(0)
                self.buttonRestoreBrowse.Enable()
        except Exception as e:
            self.logger.error(e)
            wx.MessageBox(str(e), caption='エラー', style=wx.OK | wx.ICON_ERROR)

    def OnButtonClickRestoreBrowse(self, event):
        with wx.FileDialog(self.frame, 'ファイルを開く',
            wildcard='EEPROMファイル (*.bin)|*.bin|すべてのファイル (*.*)|*.*',
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'rb') as file:
                    self.restore_file_eeprom = file.read()
                if len(self.restore_device_eeprom) != len(self.restore_file_eeprom):
                    msg = 'EEPROMのデータサイズがデバイス({})とファイル({})で違います。'.format(
                        len(self.restore_device_eeprom), len(self.restore_file_eeprom)
                    )
                    raise Exception(msg)

                self.buttonRestoreWrite.Enable(False)
                self.textCtrlRestoreFile.SetValue(pathname)
                self.textCtrlRestoreFileEeprom.SetValue(str(hexdump(self.restore_file_eeprom)))
                self.textCtrlRestoreLog.Clear()

                device_vid = int.from_bytes(self.restore_device_eeprom[0x08:0x0a], 'little')
                device_pid = int.from_bytes(self.restore_device_eeprom[0x0a:0x0c], 'little')
                file_vid = int.from_bytes(self.restore_file_eeprom[0x08:0x0a], 'little')
                file_pid = int.from_bytes(self.restore_file_eeprom[0x0a:0x0c], 'little')
                self.logger.debug('vid device={:#06x} file={:#06x}'.format(device_vid, file_vid))
                self.logger.debug('pid device={:#06x} file={:#06x}'.format(device_pid, file_pid))
                self.textCtrlRestoreLog.AppendText('VID デバイス={:#06x} ファイル={:#06x}\n'.format(device_vid, file_vid))
                self.textCtrlRestoreLog.AppendText('PID デバイス={:#06x} ファイル={:#06x}\n'.format(device_pid, file_pid))

                self.eeprom_differences = []
                for address, vd in enumerate(self.restore_device_eeprom):
                    vf = self.restore_file_eeprom[address]
                    if vd != vf:
                        self.eeprom_differences.append((address, vd, vf))
                        logger.debug('difference address={:#06x} device={:#04x} file={:#04x}'.format(address, vd, vf))
                        self.textCtrlRestoreLog.AppendText('差異 アドレス={:#06x} デバイス={:#04x} ファイル={:#04x}\n'.format(address, vd, vf))
                self.notebookRestoreDeviceEeprom.Enable()
                self.notebookRestoreDeviceEeprom.SetSelection(2)
                if len(self.eeprom_differences) == 0:
                    msg = 'デバイスとファイルの内容が一致しています。'
                    self.textCtrlRestoreLog.AppendText(msg + '\n')
                    wx.MessageBox(msg, caption='情報')
                elif device_vid != file_vid or device_pid != file_pid:
                    msg = 'VID:PIDがデバイス({:#06x}:{:#06x})とファイル({:#06x}:{:#06x})で一致していません。'.format(device_vid, device_pid, file_vid, file_pid)
                    self.textCtrlRestoreLog.AppendText(msg + '\n')
                    msg += '書き込みボタンを有効にしますか？'
                    ret = wx.MessageBox(msg, caption='警告', style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
                    if ret == wx.YES:
                        self.buttonRestoreWrite.Enable()
                else:
                    self.buttonRestoreWrite.Enable()
            except Exception as e:
                self.logger.error(e)
                wx.MessageBox(str(e), caption='エラー', style=wx.OK | wx.ICON_ERROR)

    def OnButtonClickRestoreWrite(self, event):
        n = self.choiceRestoreDevice.GetSelection()
        if n == wx.NOT_FOUND:
            return
        vid, pid, bus, address = self.choiceRestoreDevice.GetClientData(n)
        self.logger.debug('restore device vid={:#06x} pid={:#06x} bus={} address={}'.format(vid, pid, bus, address))

        try:
            with IT930x() as it930x:
                it930x.open_device(vid, pid, bus, address)
                for address, vd, vf in self.eeprom_differences:
                    logger.debug('write address={:#06x} device={:#04x} file={:#04x}'.format(address, vd, vf))
                    it930x.write_eeprom(0x01, address, vf)
                    self.textCtrlRestoreLog.AppendText('書き込み アドレス={:#06x} ファイル={:#04x}\n'.format(address, vf))
        except Exception as e:
            self.logger.error(e)
            wx.MessageBox(str(e), caption='エラー', style=wx.OK | wx.ICON_ERROR)

        self.buttonRestoreWrite.Enable(False)

    def GetTunerName(self, vid, pid):
        tuner = 'not_found'
        n = self.choiceBackupTuner.GetCount()
        for i in range(0, n):
            v, p = self.choiceBackupTuner.GetClientData(i)
            if vid == v and pid == p:
                tuner = self.choiceBackupTuner.GetString(i)
                break
        self.logger.debug('tuner:vid:pid = {}:{:04x}:{:04x}'.format(tuner, vid, pid))
        return tuner


def get_logger(log_level):
    logger = getLogger(__name__)
    handler = StreamHandler()
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s'))
    handler.setLevel(log_level)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger


if __name__ == '__main__':
    logger = get_logger(DEBUG)
    app = MyApp()
    app.MainLoop()
