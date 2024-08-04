# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"it930x_eeprom", pos = wx.DefaultPosition, size = wx.Size( 620,550 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizerMain = wx.BoxSizer( wx.VERTICAL )

		self.m_notebookMain = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelBackup = wx.Panel( self.m_notebookMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerBackup = wx.BoxSizer( wx.VERTICAL )

		fgSizerBackup = wx.FlexGridSizer( 2, 3, 0, 0 )
		fgSizerBackup.AddGrowableCol( 1 )
		fgSizerBackup.SetFlexibleDirection( wx.BOTH )
		fgSizerBackup.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticTextBackup1 = wx.StaticText( self.m_panelBackup, wx.ID_ANY, u"チューナー", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextBackup1.Wrap( -1 )

		fgSizerBackup.Add( self.m_staticTextBackup1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		bSizerBackupTuner = wx.BoxSizer( wx.HORIZONTAL )

		m_choiceBackupTunerChoices = []
		self.m_choiceBackupTuner = wx.Choice( self.m_panelBackup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceBackupTunerChoices, 0 )
		self.m_choiceBackupTuner.SetSelection( 0 )
		bSizerBackupTuner.Add( self.m_choiceBackupTuner, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_staticTextBackup3 = wx.StaticText( self.m_panelBackup, wx.ID_ANY, u"VID:PID", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextBackup3.Wrap( -1 )

		bSizerBackupTuner.Add( self.m_staticTextBackup3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_spinCtrlBackupVid = wx.SpinCtrl( self.m_panelBackup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 65535, 0 )
		self.m_spinCtrlBackupVid.SetMinSize( wx.Size( 100,-1 ) )

		bSizerBackupTuner.Add( self.m_spinCtrlBackupVid, 1, wx.ALL, 5 )

		self.m_spinCtrlBackupPid = wx.SpinCtrl( self.m_panelBackup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 65535, 0 )
		self.m_spinCtrlBackupPid.SetMinSize( wx.Size( 100,-1 ) )

		bSizerBackupTuner.Add( self.m_spinCtrlBackupPid, 1, wx.ALL, 5 )


		fgSizerBackup.Add( bSizerBackupTuner, 1, wx.EXPAND, 5 )

		self.m_buttonBackupFind = wx.Button( self.m_panelBackup, wx.ID_ANY, u"検索", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerBackup.Add( self.m_buttonBackupFind, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticTextBackup2 = wx.StaticText( self.m_panelBackup, wx.ID_ANY, u"デバイス", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextBackup2.Wrap( -1 )

		fgSizerBackup.Add( self.m_staticTextBackup2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		m_choiceBackupDeviceChoices = []
		self.m_choiceBackupDevice = wx.Choice( self.m_panelBackup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceBackupDeviceChoices, 0 )
		self.m_choiceBackupDevice.SetSelection( 0 )
		self.m_choiceBackupDevice.Enable( False )

		fgSizerBackup.Add( self.m_choiceBackupDevice, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		self.m_buttonBackupRead = wx.Button( self.m_panelBackup, wx.ID_ANY, u"読み込み", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonBackupRead.Enable( False )

		fgSizerBackup.Add( self.m_buttonBackupRead, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizerBackup.Add( fgSizerBackup, 0, wx.EXPAND, 5 )

		self.m_notebookBackupDeviceEeprom = wx.Notebook( self.m_panelBackup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelBackupDeviceEeprom = wx.Panel( self.m_notebookBackupDeviceEeprom, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerBackupDeviceEeprom = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrlBackupDeviceEeprom = wx.TextCtrl( self.m_panelBackupDeviceEeprom, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_READONLY )
		self.m_textCtrlBackupDeviceEeprom.SetFont( wx.Font( 11, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Ubuntu Mono" ) )

		bSizerBackupDeviceEeprom.Add( self.m_textCtrlBackupDeviceEeprom, 1, wx.ALL|wx.EXPAND, 0 )


		self.m_panelBackupDeviceEeprom.SetSizer( bSizerBackupDeviceEeprom )
		self.m_panelBackupDeviceEeprom.Layout()
		bSizerBackupDeviceEeprom.Fit( self.m_panelBackupDeviceEeprom )
		self.m_notebookBackupDeviceEeprom.AddPage( self.m_panelBackupDeviceEeprom, u"デバイス", False )

		bSizerBackup.Add( self.m_notebookBackupDeviceEeprom, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_buttonBackupSave = wx.Button( self.m_panelBackup, wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonBackupSave.Enable( False )

		bSizerBackup.Add( self.m_buttonBackupSave, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panelBackup.SetSizer( bSizerBackup )
		self.m_panelBackup.Layout()
		bSizerBackup.Fit( self.m_panelBackup )
		self.m_notebookMain.AddPage( self.m_panelBackup, u"バックアップ", True )
		self.m_panelRestore = wx.Panel( self.m_notebookMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerRestore = wx.BoxSizer( wx.VERTICAL )

		fgSizerRestore = wx.FlexGridSizer( 3, 3, 0, 0 )
		fgSizerRestore.AddGrowableCol( 1 )
		fgSizerRestore.SetFlexibleDirection( wx.BOTH )
		fgSizerRestore.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticTextRestore1 = wx.StaticText( self.m_panelRestore, wx.ID_ANY, u"VID:PID", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextRestore1.Wrap( -1 )

		fgSizerRestore.Add( self.m_staticTextRestore1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		bSizerRestoreVidPid = wx.BoxSizer( wx.HORIZONTAL )

		self.m_spinCtrlRestoreVid = wx.SpinCtrl( self.m_panelRestore, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 65535, 1165 )
		self.m_spinCtrlRestoreVid.SetMinSize( wx.Size( 100,-1 ) )

		bSizerRestoreVidPid.Add( self.m_spinCtrlRestoreVid, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_spinCtrlRestorePid = wx.SpinCtrl( self.m_panelRestore, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 65535, 37638 )
		self.m_spinCtrlRestorePid.SetMinSize( wx.Size( 100,-1 ) )

		bSizerRestoreVidPid.Add( self.m_spinCtrlRestorePid, 1, wx.ALL|wx.EXPAND, 5 )


		fgSizerRestore.Add( bSizerRestoreVidPid, 1, wx.EXPAND, 5 )

		self.m_buttonRestoreFind = wx.Button( self.m_panelRestore, wx.ID_ANY, u"検索", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerRestore.Add( self.m_buttonRestoreFind, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_staticTextRestore2 = wx.StaticText( self.m_panelRestore, wx.ID_ANY, u"デバイス", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextRestore2.Wrap( -1 )

		fgSizerRestore.Add( self.m_staticTextRestore2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		m_choiceRestoreDeviceChoices = []
		self.m_choiceRestoreDevice = wx.Choice( self.m_panelRestore, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceRestoreDeviceChoices, 0 )
		self.m_choiceRestoreDevice.SetSelection( 0 )
		self.m_choiceRestoreDevice.Enable( False )

		fgSizerRestore.Add( self.m_choiceRestoreDevice, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		self.m_buttonRestoreRead = wx.Button( self.m_panelRestore, wx.ID_ANY, u"読み込み", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonRestoreRead.Enable( False )

		fgSizerRestore.Add( self.m_buttonRestoreRead, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_staticTextRestore3 = wx.StaticText( self.m_panelRestore, wx.ID_ANY, u"ファイル", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextRestore3.Wrap( -1 )

		fgSizerRestore.Add( self.m_staticTextRestore3, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_textCtrlRestoreFile = wx.TextCtrl( self.m_panelRestore, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizerRestore.Add( self.m_textCtrlRestoreFile, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		self.m_buttonRestoreBrowse = wx.Button( self.m_panelRestore, wx.ID_ANY, u"参照", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonRestoreBrowse.Enable( False )

		fgSizerRestore.Add( self.m_buttonRestoreBrowse, 0, wx.ALL, 5 )


		bSizerRestore.Add( fgSizerRestore, 0, wx.EXPAND, 5 )

		self.m_notebookRestoreDeviceEeprom = wx.Notebook( self.m_panelRestore, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelRestoreDeviceEeprom = wx.Panel( self.m_notebookRestoreDeviceEeprom, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerRestoreDeviceEepro = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrlRestoreDeviceEeprom = wx.TextCtrl( self.m_panelRestoreDeviceEeprom, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_READONLY )
		self.m_textCtrlRestoreDeviceEeprom.SetFont( wx.Font( 11, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Ubuntu Mono" ) )

		bSizerRestoreDeviceEepro.Add( self.m_textCtrlRestoreDeviceEeprom, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panelRestoreDeviceEeprom.SetSizer( bSizerRestoreDeviceEepro )
		self.m_panelRestoreDeviceEeprom.Layout()
		bSizerRestoreDeviceEepro.Fit( self.m_panelRestoreDeviceEeprom )
		self.m_notebookRestoreDeviceEeprom.AddPage( self.m_panelRestoreDeviceEeprom, u"デバイス", True )
		self.m_panelRestoreFileEeprom = wx.Panel( self.m_notebookRestoreDeviceEeprom, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerRestoreFileEeprom = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrlRestoreFileEeprom = wx.TextCtrl( self.m_panelRestoreFileEeprom, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_READONLY )
		self.m_textCtrlRestoreFileEeprom.SetFont( wx.Font( 10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Ubuntu Mono" ) )

		bSizerRestoreFileEeprom.Add( self.m_textCtrlRestoreFileEeprom, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panelRestoreFileEeprom.SetSizer( bSizerRestoreFileEeprom )
		self.m_panelRestoreFileEeprom.Layout()
		bSizerRestoreFileEeprom.Fit( self.m_panelRestoreFileEeprom )
		self.m_notebookRestoreDeviceEeprom.AddPage( self.m_panelRestoreFileEeprom, u"ファイル", False )
		self.m_panelRestoreLog = wx.Panel( self.m_notebookRestoreDeviceEeprom, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerRestoreLog = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrlRestoreLog = wx.TextCtrl( self.m_panelRestoreLog, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY )
		self.m_textCtrlRestoreLog.SetFont( wx.Font( 11, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Ubuntu Mono" ) )

		bSizerRestoreLog.Add( self.m_textCtrlRestoreLog, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panelRestoreLog.SetSizer( bSizerRestoreLog )
		self.m_panelRestoreLog.Layout()
		bSizerRestoreLog.Fit( self.m_panelRestoreLog )
		self.m_notebookRestoreDeviceEeprom.AddPage( self.m_panelRestoreLog, u"ログ", False )

		bSizerRestore.Add( self.m_notebookRestoreDeviceEeprom, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_buttonRestoreWrite = wx.Button( self.m_panelRestore, wx.ID_ANY, u"書き込み", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonRestoreWrite.Enable( False )

		bSizerRestore.Add( self.m_buttonRestoreWrite, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panelRestore.SetSizer( bSizerRestore )
		self.m_panelRestore.Layout()
		bSizerRestore.Fit( self.m_panelRestore )
		self.m_notebookMain.AddPage( self.m_panelRestore, u"リストア", False )

		bSizerMain.Add( self.m_notebookMain, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizerMain )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_choiceBackupTuner.Bind( wx.EVT_CHOICE, self.OnChoiceBackupTuner )
		self.m_buttonBackupFind.Bind( wx.EVT_BUTTON, self.OnButtonClickBackupFind )
		self.m_choiceBackupDevice.Bind( wx.EVT_CHOICE, self.OnChoiceBackupDevice )
		self.m_buttonBackupRead.Bind( wx.EVT_BUTTON, self.OnButtonClickBackupRead )
		self.m_buttonBackupSave.Bind( wx.EVT_BUTTON, self.OnButtonClickBackupSave )
		self.m_buttonRestoreFind.Bind( wx.EVT_BUTTON, self.OnButtonClickRestoreFind )
		self.m_buttonRestoreRead.Bind( wx.EVT_BUTTON, self.OnButtonClickRestoreRead )
		self.m_buttonRestoreBrowse.Bind( wx.EVT_BUTTON, self.OnButtonClickRestoreBrowse )
		self.m_buttonRestoreWrite.Bind( wx.EVT_BUTTON, self.OnButtonClickRestoreWrite )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OnChoiceBackupTuner( self, event ):
		event.Skip()

	def OnButtonClickBackupFind( self, event ):
		event.Skip()

	def OnChoiceBackupDevice( self, event ):
		event.Skip()

	def OnButtonClickBackupRead( self, event ):
		event.Skip()

	def OnButtonClickBackupSave( self, event ):
		event.Skip()

	def OnButtonClickRestoreFind( self, event ):
		event.Skip()

	def OnButtonClickRestoreRead( self, event ):
		event.Skip()

	def OnButtonClickRestoreBrowse( self, event ):
		event.Skip()

	def OnButtonClickRestoreWrite( self, event ):
		event.Skip()


