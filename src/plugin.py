#Authors: AliAbdul, Dima73, vadim72, nikolasi, MegANDREtH
from . import _
from Components.ActionMap import ActionMap
from Components.config import config, ConfigInteger, ConfigNumber, ConfigSelection, ConfigSequence, ConfigSubsection, ConfigYesNo, getConfigListEntry
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Pixmap import Pixmap, MovingPixmap
from enigma import eTimer, getDesktop
from Plugins.Plugin import PluginDescriptor
from Screens.InfoBar import InfoBar, MoviePlayer
from Screens.Screen import Screen
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS

config.plugins.TimeSeekBar = ConfigSubsection()
config.plugins.TimeSeekBar.sensibility = ConfigInteger(default=10, limits=(1, 50))
config.plugins.TimeSeekBar.defaulttime = ConfigInteger(default=5, limits=(1, 60))

if (getDesktop(0).size().width()) > 1280:
	HD = True
else:
	HD = False

class Setup_config(ConfigListScreen, Screen):
	if HD:
		skin = """
<screen title="%s" position="center,960" size="690,120" >
	<widget name="config" position="8,0" size="674,76" font="Regular;30" foregroundColor="#00ffcc33" itemHeight="38" />
	<eLabel text="Cancel" position="174,76" size="170,33" font="Regular;30" halign="center" />
	<eLabel text="Save" position="346,76" size="170,33" font="Regular;30" halign="center" />
	<eLabel position="174,114" size="170,3" backgroundColor="#00c60000" />
	<eLabel position="346,114" size="170,3" backgroundColor="#001caa00" />
</screen>""" % _("TimeSeekBar Setup")
	else:
		skin = """
<screen title="%s" position="center,640" size="460,80" >
	<widget name="config" position="5,0" size="450,50" font="Regular;20" foregroundColor="#00ffcc33" itemHeight="25" />
	<eLabel text="Cancel" position="117,50" size="110,22" font="Regular;20" halign="center" />
	<eLabel text="Save" position="232,50" size="110,22" font="Regular;20" halign="center" />
	<eLabel position="117,75" size="110,2" backgroundColor="#00c60000" />
	<eLabel position="232,75" size="110,2" backgroundColor="#001caa00" />
</screen>""" % _("TimeSeekBar Setup")

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.list = []
		self.list.append(getConfigListEntry(_("Default skip time"), config.plugins.TimeSeekBar.defaulttime))
		self.list.append(getConfigListEntry(_("Sensibility of the search (1-50%)"), config.plugins.TimeSeekBar.sensibility))
		ConfigListScreen.__init__(self, self.list)
		self["setupActions"] = ActionMap(["WizardActions", "ColorActions"], {"red": self.exit,
		 "green": self.save,
		 "back": self.exit,
		 "ok": self.save}, -2)

	def save(self):
		for x in self["config"].list:
			x[1].save()
		self.close()

	def exit(self):
		for x in self["config"].list:
			x[1].cancel()
		self.close()


class TimeSeekBar(ConfigListScreen, Screen):
	if HD:
		skin = """
<screen title="%s" position="center,960" size="690,120" >
	<widget name="config" position="8,0" size="674,114" font="Regular;30" itemHeight="38" foregroundColor="#00ffcc33" />
	<widget name="cursor" pixmap="skin_default/position_arrow.png" position="145,78" size="12,27" zPosition="3" alphatest="on" transparent="1" />
	<eLabel position="145,96" size="400,6" backgroundColor="#00555555" zPosition="1" />
	<eLabel position="242,96" size="6,6" backgroundColor="#00c60000" zPosition="3" />
	<eLabel position="275,96" size="6,6" backgroundColor="#001caa00" zPosition="3" />
	<eLabel position="408,96" size="6,6" backgroundColor="#00c6aa00" zPosition="3" />
	<eLabel position="442,96" size="6,6" backgroundColor="#001c1cff" zPosition="3" />
	<widget source="session.CurrentService" render="PositionGauge" position="145,90" size="400,18" zPosition="2" pointer="/usr/lib/enigma2/python/Plugins/Extensions/TimeSeekBar/position_pointer-fhd.png:1536,4" transparent="1" >
		<convert type="ServicePosition">Gauge</convert>
	</widget>
	<widget name="time" position="0,76" size="143,30" font="Regular;30" foregroundColor="#00ffcc33" halign="center" zPosition="2" transparent="1" />
	<widget source="session.CurrentService" render="Label" position="548,76" size="143,30" font="Regular;30" foregroundColor="#00ffcc33" halign="center" zPosition="2" transparent="1" >
		<convert type="ServicePosition">Length,ShowHours</convert>
	</widget>
	<eLabel position="2,114" size="170,3" backgroundColor="#00c60000" />
	<eLabel position="174,114" size="170,3" backgroundColor="#001caa00" />
	<eLabel position="346,114" size="170,3" backgroundColor="#00c6aa00" />
	<eLabel position="518,114" size="170,3" backgroundColor="#001c1cff" />
</screen>""" % _("TimeSeekBar")
	else:
		skin = """
<screen title="%s" position="center,640" size="460,80" >
	<widget name="config" position="5,0" size="450,75" font="Regular;20" itemHeight="25" foregroundColor="#00ffcc33" />
	<widget name="cursor" pixmap="skin_default/position_arrow.png" position="97,52" size="8,18" zPosition="3" alphatest="on" transparent="1" />
	<eLabel position="98,65" size="264,4" backgroundColor="#00555555" zPosition="1" />
	<eLabel position="162,65" size="4,4" backgroundColor="#00c60000" zPosition="3" />
	<eLabel position="184,65" size="4,4" backgroundColor="#001caa00" zPosition="3" />
	<eLabel position="272,65" size="4,4" backgroundColor="#00c6aa00" zPosition="3" />
	<eLabel position="294,65" size="4,4" backgroundColor="#001c1cff" zPosition="3" />
	<widget source="session.CurrentService" render="PositionGauge" position="97,60" size="266,12" zPosition="2" pointer="/usr/lib/enigma2/python/Plugins/Extensions/TimeSeekBar/position_pointer-hd.png:1012,0" transparent="1" >
		<convert type="ServicePosition">Gauge</convert>
	</widget>
	<widget name="time" position="0,50" size="95,20" font="Regular;20" foregroundColor="#00ffcc33" halign="center" zPosition="2" transparent="1" />
	<widget source="session.CurrentService" render="Label" position="365,50" size="95,20" font="Regular;20" foregroundColor="#00ffcc33" halign="center" zPosition="2" transparent="1" >
		<convert type="ServicePosition">Length,ShowHours</convert>
	</widget>
	<eLabel position="2,75" size="110,2" backgroundColor="#00c60000" />
	<eLabel position="117,75" size="110,2" backgroundColor="#001caa00" />
	<eLabel position="232,75" size="110,2" backgroundColor="#00c6aa00" />
	<eLabel position="347,75" size="110,2" backgroundColor="#001c1cff" />
</screen>""" % _("TimeSeekBar")

	def __init__(self, session, instance, fwd):
		Screen.__init__(self, session)
		self.session = session
		self.infobarInstance = instance
		self.fwd = fwd
		try:
			self.castuasay = isinstance(session.current_dialog, CastPlayer)
		except:
			self.castuasay = False
		try:
			self.cscvod = isinstance(session.current_dialog, VODplayer)
		except:
			self.cscvod = False
		try:
			self.cutlisteditor = isinstance(session.current_dialog, CutListEditor)
		except:
			self.cutlisteditor = False
		try:
			self.dvd_pli = isinstance(session.current_dialog, DVDPlayer)
		except:
			self.dvd_pli = False
		try:
			self.kodi = isinstance(session.current_dialog, KodiVideoPlayer)
		except:
			self.kodi = False
		try:
			self.mediacenter = isinstance(session.current_dialog, MC_MoviePlayer)
		except:
			self.mediacenter = False
		try:
			self.mediaplayer = isinstance(session.current_dialog, MediaPlayer)
		except:
			self.mediaplayer = False
		try:
			self.mediaplayer2 = isinstance(session.current_dialog, MediaPlayer)
		except:
			self.mediaplayer2 = False
		try:
			self.merlin = isinstance(session.current_dialog, MerlinMusicPlayerScreen)
		except:
			self.merlin = False
		try:
			self.movie = isinstance(session.current_dialog, MoviePlayer)
		except:
			self.movie = False
		try:
			self.movieplayer = isinstance(session.current_dialog, MoviePlayer2)
		except:
			self.movieplayer = False
		try:
			self.mytube = isinstance(session.current_dialog, MyTubePlayer)
		except:
			self.mytube = False
		try:
			self.nvod = isinstance(session.current_dialog, nVODplayer)
		except:
			self.nvod = False
		try:
			self.russianmediapark = isinstance(session.current_dialog, RMParkPlayer)
		except:
			self.russianmediapark = False
		try:
			self.old_dvd = isinstance(session.current_dialog, DVDPlayer2)
		except:
			self.old_dvd = False
		try:
			self.seasondream = isinstance(session.current_dialog, Player)
		except:
			self.seasondream = False
		try:
			self.timeshift = isinstance(session.current_dialog, InfoBar)
		except:
			self.timeshift = False
		try:
			self.tmbd = isinstance(session.current_dialog, tmbdTrailerPlayer)
		except:
			self.tmbd = False
		try:
			self.vod = isinstance(session.current_dialog, nVODplayer)
		except:
			self.vod = False
		try:
			self.youtube = isinstance(session.current_dialog, YouTubePlayer)
		except:
			self.youtube = False
		self.percent = 0.0
		self.length = None
		defaulttime = config.plugins.TimeSeekBar.defaulttime.value
		service = session.nav.getCurrentService()
		if self.fwd == False:
			deftime = - config.plugins.TimeSeekBar.defaulttime.value
		else:
			deftime = config.plugins.TimeSeekBar.defaulttime.value
		xdeftime = int(float(deftime) * 60 * 90000)
		self.initime = xdeftime
		if service:
			self.seek = service.seek()
			if self.seek:
				self.length = self.seek.getLength()
				position = self.seek.getPlayPosition()
				if self.length and position:
					if int(position[1]) > 0:
						if float(self.length[1]) <> 0:
							self.percent = float(position[1]) * 100.0 / float(self.length[1])
						else:
							self.close()
		self.minuteInput = ConfigNumber(default=defaulttime)
		self.positionEntry = ConfigSelection(choices=[' '], default=' ')
		self.manualInput = ConfigSequence(seperator=':', default=[int(position[1] / 60 / 60 / 90000), int(position[1] / 60 / 90000 % 60), int(position[1] / 90000 % 60)], limits=[(0, 9), (0, 59), (0, 59)])
		if self.fwd:
			txt = _("Jump X minutes forward")
		else:
			txt = _("Jump X minutes back")
		ConfigListScreen.__init__(self, [
			getConfigListEntry(txt, self.minuteInput),
			getConfigListEntry(_("Go to position"), self.manualInput),
			getConfigListEntry(_(" "), self.positionEntry)])
		self["cursor"] = MovingPixmap()
		self["time"] = Label()
		self["actions"] = ActionMap(["WizardActions", "ColorActions", "MenuActions", "NumberActions"],
		{"back": self.exit,
		 "menu": self.keyMenu,
		 "red": self.goto25percent,
		 "green": self.goto33percent,
		 "yellow": self.goto66percent,
		 "blue": self.goto75percent}, -1)
		self.cursorTimer = eTimer()
		self.cursorTimer.callback.append(self.updateCursor)
		self.onLayoutFinish.append(self.firstStart)
		return

	def firstStart(self):
		try:
			longitud = float(self.length[1])
			if longitud <= 0:
				longitud = 1
			self.percent = float(self.seek.getPlayPosition()[1] + self.initime) * 100.0 / longitud
		except:
			pass

		self.updateCursor()
		self.cursorTimer.start(200, False)
		self["config"].setCurrentIndex(2)

	def updateCursor(self):
		if self.length:
			if self.percent > 100.0:
				self.percent = 100.0
			elif self.percent < 0.0:
				self.percent = 0.0
			if HD:
				x = 145 + int(4.00 * self.percent)
				posy = self["cursor"].instance.position().y()
				self["cursor"].moveTo(x - 6, posy, 1)
				self["cursor"].startMoving()
				pts = int(float(self.length[1]) / 100.0 * self.percent)
				self["time"].setText("%d:%02d:%02d" % (pts / 60 / 60 / 90000, pts / 60 / 90000 % 60, pts / 90000 % 60))
			else:
				x = 98 + int(2.64 * self.percent)
				posy = self["cursor"].instance.position().y()
				self["cursor"].moveTo(x - 4, posy, 1)
				self["cursor"].startMoving()
				pts = int(float(self.length[1]) / 100.0 * self.percent)
				self["time"].setText("%d:%02d:%02d" % (pts / 60 / 60 / 90000, pts / 60 / 90000 % 60, pts / 90000 % 60))

	def goto25percent(self):
		self.percent = 25.0
		self["config"].setCurrentIndex(2)
		self.keyOK()

	def goto33percent(self):
		self.percent = 33.0
		self["config"].setCurrentIndex(2)
		self.keyOK()

	def goto66percent(self):
		self.percent = 66.0
		self["config"].setCurrentIndex(2)
		self.keyOK()

	def goto75percent(self):
		self.percent = 75.0
		self["config"].setCurrentIndex(2)
		self.keyOK()

	def keyMenu(self):
		self.session.open(Setup_config)

	def exit(self):
		self.cursorTimer.stop()
		ConfigListScreen.saveAll(self)
		self.close()

	def keyOK(self):
		sel = self["config"].getCurrent()[1]
		if sel == self.positionEntry:
			if self.length:
				if self.timeshift:
					self.seek.seekTo(int(float(self.length[1]) / 100.0 * self.percent))
				else:	
					oldPosition = self.seek.getPlayPosition()[1]
					newPosition = int(float(self.length[1]) / 100.0 * self.percent)
					if newPosition > oldPosition:
						pts = newPosition - oldPosition
					else:
						pts = -1 * (oldPosition - newPosition)
					if self.castuasay:
						CastPlayer.doSeekRelative(self.infobarInstance, pts)
					elif self.cscvod:
						VODplayer.doSeekRelative(self.infobarInstance, pts)
					elif self.cutlisteditor:
						CutListEditor.doSeekRelative(self.infobarInstance, pts)
					elif self.dvd_pli:
						DVDPlayer.doSeekRelative(self.infobarInstance, pts)
					elif self.kodi:
						KodiVideoPlayer.doSeekRelative(self.infobarInstance, pts)
					elif self.mediacenter:
						MC_MoviePlayer.doSeekRelative(self.infobarInstance, pts)
					elif self.mediaplayer:
						MediaPlayer.doSeekRelative(self.infobarInstance, pts)
					elif self.mediaplayer2:
						MediaPlayer.doSeekRelative(self.infobarInstance, pts)
					elif self.merlin:
						MerlinMusicPlayerScreen.doSeekRelative(self.infobarInstance, pts)
					elif self.movie:
						self.seek.seekTo(int(float(self.length[1]) / 100.0 * self.percent))
					elif self.movieplayer:
						MoviePlayer2.doSeekRelative(self.infobarInstance, pts)
					elif self.mytube:
						MyTubePlayer.doSeekRelative(self.infobarInstance, pts)
					elif self.nvod:
						nVODplayer.doSeekRelative(self.infobarInstance, pts)
					elif self.old_dvd: # seekTo() doesn't work for DVD Player
						DVDPlayer2.doSeekRelative(self.infobarInstance, pts)
					elif self.russianmediapark:
						RMParkPlayer.doSeekRelative(self.infobarInstance, pts)
					elif self.seasondream:
						Player.doSeekRelative(self.infobarInstance, pts)
					elif self.tmbd:
						tmbdTrailerPlayer.doSeekRelative(self.infobarInstance, pts)
					elif self.vod:
						VODplayer.doSeekRelative(self.infobarInstance, pts)
					elif self.youtube:
						YouTubePlayer.doSeekRelative(self.infobarInstance, pts)
					else:
						pass
				self.exit()
		elif sel == self.minuteInput:
			pts = self.minuteInput.value * 60 * 90000
			if self.fwd == False:
				pts = -1*pts
			if self.castuasay:
				CastPlayer.doSeekRelative(self.infobarInstance, pts)
			elif self.cscvod:
				VODplayer.doSeekRelative(self.infobarInstance, pts)
			elif self.cutlisteditor:
				CutListEditor.doSeekRelative(self.infobarInstance, pts)
			elif self.dvd_pli:
				DVDPlayer.doSeekRelative(self.infobarInstance, pts)
			elif self.kodi:
				KodiVideoPlayer.doSeekRelative(self.infobarInstance, pts)
			elif self.mediacenter:
				MC_MoviePlayer.doSeekRelative(self.infobarInstance, pts)
			elif self.mediaplayer:
				MediaPlayer.doSeekRelative(self.infobarInstance, pts)
			elif self.mediaplayer2:
				MediaPlayer.doSeekRelative(self.infobarInstance, pts)
			elif self.merlin:
				MerlinMusicPlayerScreen.doSeekRelative(self.infobarInstance, pts)
			elif self.movie:
				MoviePlayer.doSeekRelative(self.infobarInstance, pts)
			elif self.movielayer:
				MoviePlayer2.doSeekRelative(self.infobarInstance, pts)
			elif self.mytube:
				MyTubePlayer.doSeekRelative(self.infobarInstance, pts)
			elif self.nvod:
				nVODplayer.doSeekRelative(self.infobarInstance, pts)
			elif self.old_dvd:
				DVDPlayer2.doSeekRelative(self.infobarInstance, pts)
			elif self.russianmediapark:
				RMParkPlayer.doSeekRelative(self.infobarInstance, pts)
			elif self.seasondream:
				Player.doSeekRelative(self.infobarInstance, pts)
			elif self.timeshift:
				InfoBar.doSeekRelative(self.infobarInstance, pts)
			elif self.tmbd:
				tmbdTrailerPlayer.doSeekRelative(self.infobarInstance, pts)
			elif self.vod:
				VODplayer.doSeekRelative(self.infobarInstance, pts)
			elif self.youtube:
				YouTubePlayer.doSeekRelative(self.infobarInstance, pts)
			else:
				pass
			self.exit()
		elif sel == self.manualInput:
			if self.length:
				if self.dvd_pli:
					oldPosition = self.seek.getPlayPosition()[1]
					newPosition = self.manualInput.value[0] * 60 * 60 * 90000 + self.manualInput.value[1] * 60 * 90000 + self.manualInput.value[2] * 90000
					if newPosition > oldPosition:
						pts = newPosition - oldPosition
					else:
						pts = -1 * (oldPosition - newPosition)
				else:
					self.seek.seekTo(self.manualInput.value[0] * 60 * 60 * 90000 + self.manualInput.value[1] * 60 * 90000 + self.manualInput.value[2] * 90000)
				self.exit()

	def keyLeft(self):
		sel = self["config"].getCurrent()[1]
		if sel == self.positionEntry:
			self.percent -= float(config.plugins.TimeSeekBar.sensibility.value)
			if self.percent < 0.0:
				self.percent = 0.0
		else:
			ConfigListScreen.keyLeft(self)
			if sel == self.minuteInput:
				pts = int(float(self.minuteInput.value) * 60 * 90000)
				longitud = float(self.length[1])
				if longitud <= 0:
					longitud = 1
				self.percent = float(self.seek.getPlayPosition()[1] + pts) * 100.0 / longitud
				if self.percent < 0.0:
					self.percent = 0.0
				elif self.percent > 100.0:
					self.percent = 100.0

	def keyRight(self):
		sel = self["config"].getCurrent()[1]
		if sel == self.positionEntry:
			self.percent += float(config.plugins.TimeSeekBar.sensibility.value)
			if self.percent > 100.0:
				self.percent = 100.0
		else:
			ConfigListScreen.keyRight(self)
			if sel == self.minuteInput:
				pts = int(float(self.minuteInput.value) * 60 * 90000)
				longitud = float(self.length[1])
				if longitud <= 0:
					longitud = 1
				self.percent = float(self.seek.getPlayPosition()[1] + pts) * 100.0 / longitud
				if self.percent < 0.0:
					self.percent = 0.0
				elif self.percent > 100.0:
					self.percent = 100.0

	def keyNumberGlobal(self, number):
		sel = self["config"].getCurrent()[1]
		if sel == self.positionEntry:
			self.percent = float(number) * 10.0
			self["config"].setCurrentIndex(2)
			self.keyOK()
		else:
			ConfigListScreen.keyNumberGlobal(self, number)

def timeseekbar(instance, fwd = True):
	if instance and instance.session:
		instance.session.open(TimeSeekBar, instance, fwd)

def timeseekbarBack(instance):
	timeseekbar(instance, False)

MoviePlayer.right = timeseekbar
MoviePlayer.left = timeseekbarBack
InfoBar.seekFwdManual = timeseekbar
InfoBar.seekBackManual = timeseekbarBack

castuasay = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/CastUASAY/plugin.pyo")
if fileExists(castuasay):
	try:
		from Plugins.Extensions.CastUASAY.panel.CastPlayer import CastPlayer
		CastPlayer.seekFwdManual = timeseekbar
		CastPlayer.seekBackManual = timeseekbarBack
	except:
		pass
		
cscvod = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/cScVOD/plugin.pyo")
if fileExists(cscvod):
	try:
		from Plugins.Extensions.cScVOD.plugin import VODplayer
		VODplayer.seekFwdManual = timeseekbar
		VODplayer.seekBackManual = timeseekbarBack
	except:
		pass

cutlisteditor = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/CutListEditor/plugin.pyo")
if fileExists(cutlisteditor):
	try:
		from Plugins.Extensions.CutListEditor.ui import CutListEditor
		CutListEditor.seekFwdManual = timeseekbar
		CutListEditor.seekBackManual = timeseekbarBack
	except:
		pass
		
if fileExists("/usr/lib/enigma2/python/Screens/DVD.pyo"):
	try:
		from Screens.DVD import DVDPlayer
		DVDPlayer.seekFwdManual = timeseekbar
		DVDPlayer.seekBackManual = timeseekbarBack
	except:
		pass

kodi = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/Kodi/plugin.pyo")
if fileExists(kodi):
	try:
		from Plugins.Extensions.Kodi.plugin import KodiVideoPlayer
		KodiVideoPlayer.seekFwdManual = timeseekbar
		KodiVideoPlayer.seekBackManual = timeseekbarBack
	except:
		pass

mediacenter = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/MediaCenter/MC_MoviePlayer.pyo")
if fileExists(mediacenter):
	try:
		from Plugins.Extensions.MediaCenter.MC_MoviePlayer import MC_MoviePlayer
		MC_MoviePlayer.seekFwdManual = timeseekbar
		MC_MoviePlayer.seekBackManual = timeseekbarBack
	except:
		pass

mediaplayer = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/MediaPlayer/plugin.pyo")
if fileExists(mediaplayer):
	try:
		from Plugins.Extensions.MediaPlayer.plugin import MediaPlayer
		MediaPlayer.seekFwdManual = timeseekbar
		MediaPlayer.seekBackManual = timeseekbarBack
	except:
		pass

mediaplayer2 = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/MediaPlayer2/plugin.pyo")
if fileExists(mediaplayer2):
	try:
		from Plugins.Extensions.MediaPlayer2.plugin import MediaPlayer
		MediaPlayer.seekFwdManual = timeseekbar
		MediaPlayer.seekBackManual = timeseekbarBack
	except:
		pass

merlinmusic = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/MerlinMusicPlayer/plugin.pyo")
if fileExists(merlinmusic):
	try:
		from Plugins.Extensions.MerlinMusicPlayer.plugin import MerlinMusicPlayerScreen
		MerlinMusicPlayerScreen.seekFwdManual = timeseekbar
		MerlinMusicPlayerScreen.seekBackManual = timeseekbarBack
	except:
		pass

movieplayer = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/MediaPlayer/plugin.pyo")
if fileExists(movieplayer):
	try:
		from Plugins.Extensions.MediaPlayer.plugin import MediaPlayer as MoviePlayer2
		MoviePlayer2.seekFwdManual = timeseekbar
		MoviePlayer2.seekBackManual = timeseekbarBack
	except:
		pass

mytube = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/MyTube/plugin.pyo")
if fileExists(mytube):
	try:
		from Plugins.Extensions.MyTube.plugin import MyTubePlayer
		MyTubePlayer.seekFwdManual = timeseekbar
		MyTubePlayer.seekBackManual = timeseekbarBack
	except:
		pass

nstreamvod = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/nStreamVOD/plugin.pyo")
if fileExists(nstreamvod):
	try:
		from Plugins.Extensions.nStreamVOD.plugin import nVODplayer
		nVODplayer.seekFwdManual = timeseekbar
		nVODplayer.seekBackManual = timeseekbarBack
	except:
		pass

old_dvd = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/DVDPlayer/plugin.pyo")
old_dvdkeymap = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/DVDPlayer/keymap.xml")
if fileExists(old_dvd) and fileExists(old_dvdkeymap):
	try:
		from Plugins.Extensions.DVDPlayer.plugin import DVDPlayer as DVDPlayer2
		DVDPlayer2.seekFwdManual = timeseekbar
		DVDPlayer2.seekBackManual = timeseekbarBack
	except:
		pass

russianmediapark = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/RussianMediaPark/plugin.pyo")
if fileExists(russianmediapark):
	try:
		from Plugins.Extensions.RussianMediaPark.plugin import RMParkPlayer
		RMParkPlayer.seekFwdManual = timeseekbar
		RMParkPlayer.seekBackManual = timeseekbarBack
	except:
		pass

seasondream = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/Seasondream/plugin.pyo")
if fileExists(seasondream):
	try:
		from Plugins.Extensions.Seasondream.Player import Player
		Player.seekFwdManual = timeseekbar
		Player.seekBackManual = timeseekbarBack
	except:
		pass

tmbd = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/TMBD/plugin.pyo")
tmbdyttrailer = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/TMBD/tmbdYTTrailer.pyo")
if fileExists(tmbd) and fileExists(tmbdyttrailer):
	try:
		from Plugins.Extensions.TMBD.tmbdYTTrailer import tmbdTrailerPlayer
		tmbdTrailerPlayer.seekFwdManual = timeseekbar
		tmbdTrailerPlayer.seekBackManual = timeseekbarBack
	except:
		pass

vod = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/VOD/plugin.pyo")
if fileExists(vod):
	try:
		from Plugins.Extensions.VOD.plugin import VODplayer
		VODplayer.seekFwdManual = timeseekbar
		VODplayer.seekBackManual = timeseekbarBack
	except:
		pass

youtube = "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/YouTube/plugin.pyo")
if fileExists(youtube):
	try:
		from Plugins.Extensions.YouTube.YouTubeUi import YouTubePlayer
		YouTubePlayer.seekFwdManual = timeseekbar
		YouTubePlayer.seekBackManual = timeseekbarBack
	except:
		pass

def Plugins(**kwargs):
	return []
