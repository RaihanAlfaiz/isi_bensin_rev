from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect, QProgressBar, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QRect, QRectF, QUrl, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap, QLinearGradient, QPainterPath, QImage
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QVideoSink
from config import BASE_DIR

class LayoutButton(QPushButton):
    def sizeHint(self):
        lay = self.layout()
        if lay:
            return lay.sizeHint()
        return super().sizeHint()

    def minimumSizeHint(self):
        lay = self.layout()
        if lay:
            return lay.minimumSize()
        return super().minimumSizeHint()


class PulsingDot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(12, 12)
        self.alpha = 255
        self.direction = -1
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pulse)
        self.timer.start(50)  # 20 fps
        
    def update_pulse(self):
        self.alpha += self.direction * 15
        if self.alpha <= 80:
            self.alpha = 80
            self.direction = 1
        elif self.alpha >= 255:
            self.alpha = 255
            self.direction = -1
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(78, 222, 163, self.alpha))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())


class FullscreenVideoPlayer(QWidget):
    frame_received = pyqtSignal(QImage)

    def __init__(self, media_player, inline_container):
        super().__init__()
        self.media_player = media_player
        self.inline_container = inline_container
        
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: #0b1326;")
        
        self.video_sink = QVideoSink()
        self.video_sink.videoFrameChanged.connect(self.on_video_frame_changed)
        self.frame_received.connect(self.on_safe_frame_received)
        self.current_frame_image = None
        self.current_frame_pixmap = None
        self.is_active = False
        self.target_w = 0
        self.target_h = 0
        
        self.is_playing = (self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState)
        
        self.setup_ui()
        
        # Connect player signals to fullscreen UI
        self.media_player.positionChanged.connect(self.on_position_changed)
        self.media_player.durationChanged.connect(self.on_duration_changed)
        self.media_player.setVideoOutput(self.video_sink)
        
        # Show fullscreen
        self.showFullScreen()
        
    def setup_ui(self):
        # Fullscreen main vertical layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Top-middle spacer
        layout.addStretch(1)
        
        # Center Play Overlay
        self.center_overlay = QWidget()
        overlay_layout = QVBoxLayout(self.center_overlay)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overlay_layout.setSpacing(16)
        
        # Play Button
        self.play_btn = QPushButton()
        self.play_btn.setFixedSize(90, 90)
        self.play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #4edea3;
                border: none;
                border-radius: 45px;
            }
            QPushButton:hover {
                background-color: #3bd095;
            }
            QPushButton:pressed {
                background-color: #2ebc83;
            }
        """)
        self.play_btn.clicked.connect(self.play_video)
        
        play_btn_layout = QHBoxLayout(self.play_btn)
        play_btn_layout.setContentsMargins(0, 0, 0, 0)
        play_btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        play_icon = QLabel("play_arrow")
        play_icon.setFont(QFont("Material Symbols Outlined", 44))
        play_icon.setStyleSheet("color: #003824; background: transparent; border: none;")
        play_btn_layout.addWidget(play_icon)
        
        # Glow
        play_shadow = QGraphicsDropShadowEffect(self.play_btn)
        play_shadow.setBlurRadius(30)
        play_shadow.setColor(QColor(78, 222, 163, 128))
        play_shadow.setOffset(0, 0)
        self.play_btn.setGraphicsEffect(play_shadow)
        
        overlay_layout.addWidget(self.play_btn, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.center_overlay, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        
        # Bottom Video Controls Bar
        self.control_bar = QWidget()
        self.control_bar.setFixedHeight(80)
        self.control_bar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 0.9));
            }
        """)
        
        control_layout = QHBoxLayout(self.control_bar)
        control_layout.setContentsMargins(40, 0, 40, 20)
        control_layout.setSpacing(24)
        control_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # Pause Button
        self.pause_btn = QPushButton()
        self.pause_btn.setFixedSize(40, 40)
        self.pause_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pause_btn.setStyleSheet("background: transparent; border: none;")
        self.pause_btn.clicked.connect(self.toggle_play)
        
        pause_btn_layout = QHBoxLayout(self.pause_btn)
        pause_btn_layout.setContentsMargins(0, 0, 0, 0)
        pause_btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.pause_icon = QLabel("pause" if self.is_playing else "play_arrow")
        self.pause_icon.setFont(QFont("Material Symbols Outlined", 32))
        self.pause_icon.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        pause_btn_layout.addWidget(self.pause_icon)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.15);
                border: none;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #4edea3;
                border-radius: 4px;
            }
        """)
        
        prog_shadow = QGraphicsDropShadowEffect(self.progress_bar)
        prog_shadow.setBlurRadius(10)
        prog_shadow.setColor(QColor(78, 222, 163, 100))
        prog_shadow.setOffset(0, 0)
        self.progress_bar.setGraphicsEffect(prog_shadow)
        
        # Time counter Label
        self.time_lbl = QLabel("00:00 / 00:00")
        self.time_lbl.setFont(QFont("Space Grotesk", 14))
        self.time_lbl.setStyleSheet("color: rgba(255, 255, 255, 0.85); background: transparent; border: none;")
        
        # Exit Fullscreen Button
        exit_btn = QPushButton()
        exit_btn.setFixedSize(40, 40)
        exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        exit_btn.setStyleSheet("background: transparent; border: none;")
        exit_btn.clicked.connect(self.close_fullscreen)
        
        exit_btn_layout = QHBoxLayout(exit_btn)
        exit_btn_layout.setContentsMargins(0, 0, 0, 0)
        exit_btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        exit_icon = QLabel("fullscreen_exit")
        exit_icon.setFont(QFont("Material Symbols Outlined", 32))
        exit_icon.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        exit_btn_layout.addWidget(exit_icon)
        
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.progress_bar, 1)
        control_layout.addWidget(self.time_lbl)
        control_layout.addWidget(exit_btn)
        
        layout.addWidget(self.control_bar)
        
        self.update_control_ui()
        
    def on_video_frame_changed(self, frame):
        if not self.is_active or not frame.isValid():
            return
        img = frame.toImage()
        if img.isNull():
            return
        w, h = self.target_w, self.target_h
        if w > 0 and h > 0:
            target_ratio = 16.0 / 9.0
            if w / h > target_ratio:
                new_h = h
                new_w = int(h * target_ratio)
            else:
                new_w = w
                new_h = int(w / target_ratio)
            scaled_img = img.scaled(
                new_w, new_h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.frame_received.emit(scaled_img)

    def on_safe_frame_received(self, img):
        self.current_frame_image = img
        self.current_frame_pixmap = QPixmap.fromImage(img)
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        self.is_active = True
        self.target_w = self.width()
        self.target_h = self.height()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.is_active = False
        self.current_frame_image = None
        self.current_frame_pixmap = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        self.target_w = size.width()
        self.target_h = size.height()
        
    def toggle_play(self):
        if self.is_playing:
            self.pause_video()
        else:
            self.play_video()
            
    def play_video(self):
        self.is_playing = True
        self.media_player.play()
        self.update_control_ui()
        
    def pause_video(self):
        self.is_playing = False
        self.media_player.pause()
        self.update_control_ui()
        
    def update_control_ui(self):
        if self.is_playing:
            self.center_overlay.setVisible(False)
            self.pause_icon.setText("pause")
        else:
            self.center_overlay.setVisible(True)
            self.pause_icon.setText("play_arrow")
            
    def on_duration_changed(self, duration_ms):
        self.update_time_label()
        
    def on_position_changed(self, position_ms):
        duration = self.media_player.duration()
        if duration > 0:
            val = int((position_ms / duration) * 100.0)
            self.progress_bar.setValue(val)
        self.update_time_label()
        
    def update_time_label(self):
        position = self.media_player.position()
        duration = self.media_player.duration()
        
        pos_sec = position // 1000
        dur_sec = duration // 1000
        
        pos_m = pos_sec // 60
        pos_s = pos_sec % 60
        
        dur_m = dur_sec // 60
        dur_s = dur_sec % 60
        
        self.time_lbl.setText(f"{pos_m:02d}:{pos_s:02d} / {dur_m:02d}:{dur_s:02d}")
        
    def close_fullscreen(self):
        try:
            self.media_player.positionChanged.disconnect(self.on_position_changed)
            self.media_player.durationChanged.disconnect(self.on_duration_changed)
        except Exception:
            pass
            
        self.media_player.setVideoOutput(self.inline_container.video_sink)
        self.inline_container.is_playing = (self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState)
        self.inline_container.update_control_ui()
        self.inline_container.update()
        self.close()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close_fullscreen()
        super().keyPressEvent(event)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        target_ratio = 16.0 / 9.0
        w = rect.width()
        h = rect.height()
        
        if w / h > target_ratio:
            new_h = h
            new_w = int(h * target_ratio)
        else:
            new_w = w
            new_h = int(w / target_ratio)
            
        x = (w - new_w) // 2
        y = (h - new_h) // 2
        video_rect = QRect(x, y, new_w, new_h)
        
        drawn = False
        if self.current_frame_pixmap is not None and not self.current_frame_pixmap.isNull():
            px = x + (new_w - self.current_frame_pixmap.width()) // 2
            py = y + (new_h - self.current_frame_pixmap.height()) // 2
            painter.drawPixmap(px, py, self.current_frame_pixmap)
            drawn = True
                
        if not drawn:
            painter.fillRect(video_rect, QColor(0, 0, 0))
            
        painter.fillRect(video_rect, QColor(11, 19, 38, 100))


class VideoContainer(QWidget):
    frame_received = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(str(BASE_DIR / "resources" / "images" / "plug_in_guide.jpg"))
        self.is_playing = False
        self.video_position = 0
        self.video_duration = 0
        self.current_frame_image = None
        self.current_frame_pixmap = None
        self.cover_pixmap_cached = None
        self.fullscreen_player = None
        self.is_active = False
        self.target_w = 0
        self.target_h = 0
        
        # 1. Media Player setup
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.5)
        self.media_player.setAudioOutput(self.audio_output)
        
        # 2. Video Sink setup
        self.video_sink = QVideoSink()
        self.media_player.setVideoOutput(self.video_sink)
        self.video_sink.videoFrameChanged.connect(self.on_video_frame_changed)
        self.frame_received.connect(self.on_safe_frame_received)
        
        video_path = BASE_DIR / "resources" / "video" / "Animasi Mobil Cas.mp4"
        self.media_player.setSource(QUrl.fromLocalFile(str(video_path)))
        self.media_player.setLoops(QMediaPlayer.Loops.Infinite)
        
        self.media_player.positionChanged.connect(self.on_position_changed)
        self.media_player.durationChanged.connect(self.on_duration_changed)
        
        # 3. Controls layout setup
        self.setup_ui()
        
    def setup_ui(self):
        # Main vertical layout inside video card
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Top-middle spacer to push play overlay to center
        layout.addStretch(1)
        
        # Center Play Overlay
        self.center_overlay = QWidget()
        overlay_layout = QVBoxLayout(self.center_overlay)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overlay_layout.setSpacing(16)
        
        # 1. Circular Play Button
        self.play_btn = QPushButton()
        self.play_btn.setFixedSize(90, 90)
        self.play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #4edea3;
                border: none;
                border-radius: 45px;
            }
            QPushButton:hover {
                background-color: #3bd095;
            }
            QPushButton:pressed {
                background-color: #2ebc83;
            }
        """)
        self.play_btn.clicked.connect(self.play_video)
        
        play_btn_layout = QHBoxLayout(self.play_btn)
        play_btn_layout.setContentsMargins(0, 0, 0, 0)
        play_btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        play_icon = QLabel("play_arrow")
        play_icon.setFont(QFont("Material Symbols Outlined", 44))
        play_icon.setStyleSheet("color: #003824; background: transparent; border: none;")
        play_btn_layout.addWidget(play_icon)
        
        # Play button glow
        play_shadow = QGraphicsDropShadowEffect(self.play_btn)
        play_shadow.setBlurRadius(30)
        play_shadow.setColor(QColor(78, 222, 163, 128))
        play_shadow.setOffset(0, 0)
        self.play_btn.setGraphicsEffect(play_shadow)
        
        # 2. Titles inside overlay
        titles_widget = QWidget()
        titles_layout = QVBoxLayout(titles_widget)
        titles_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titles_layout.setSpacing(6)
        
        self.video_title_lbl = QLabel("VIDEO INSTRUKSIONAL")
        self.video_title_lbl.setFont(QFont("Space Grotesk", 18, QFont.Weight.Bold))
        self.video_title_lbl.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        self.video_title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.video_sub_lbl = QLabel("Cara colok charger • scan RFID • mulai charging")
        self.video_sub_lbl.setFont(QFont("Inter", 12))
        self.video_sub_lbl.setStyleSheet("color: rgba(173, 198, 255, 0.8); background: transparent; border: none;")
        self.video_sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        titles_layout.addWidget(self.video_title_lbl)
        titles_layout.addWidget(self.video_sub_lbl)
        
        overlay_layout.addWidget(self.play_btn, 0, Qt.AlignmentFlag.AlignCenter)
        overlay_layout.addWidget(titles_widget, 0, Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.center_overlay, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        
        # Bottom Video Controls Bar
        self.control_bar = QWidget()
        self.control_bar.setFixedHeight(60)
        self.control_bar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 0.85));
                border-bottom-left-radius: 30px;
                border-bottom-right-radius: 30px;
            }
        """)
        
        control_layout = QHBoxLayout(self.control_bar)
        control_layout.setContentsMargins(24, 0, 24, 10)
        control_layout.setSpacing(16)
        control_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # Play/Pause Toggle Button in control bar
        self.pause_btn = QPushButton()
        self.pause_btn.setFixedSize(30, 30)
        self.pause_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pause_btn.setStyleSheet("background: transparent; border: none;")
        self.pause_btn.clicked.connect(self.toggle_play)
        
        pause_btn_layout = QHBoxLayout(self.pause_btn)
        pause_btn_layout.setContentsMargins(0, 0, 0, 0)
        pause_btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.pause_icon = QLabel("play_arrow")
        self.pause_icon.setFont(QFont("Material Symbols Outlined", 24))
        self.pause_icon.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        pause_btn_layout.addWidget(self.pause_icon)
        
        # Styled Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.15);
                border: none;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #4edea3;
                border-radius: 3px;
            }
        """)
        self.progress_bar.setValue(0)
        
        # Progress Bar glow shadow
        prog_shadow = QGraphicsDropShadowEffect(self.progress_bar)
        prog_shadow.setBlurRadius(10)
        prog_shadow.setColor(QColor(78, 222, 163, 100))
        prog_shadow.setOffset(0, 0)
        self.progress_bar.setGraphicsEffect(prog_shadow)
        
        # Time counter Label
        self.time_lbl = QLabel("00:00 / 00:00")
        self.time_lbl.setFont(QFont("Space Grotesk", 11))
        self.time_lbl.setStyleSheet("color: rgba(255, 255, 255, 0.85); background: transparent; border: none;")
        
        # Fullscreen Button
        self.fullscreen_btn = QPushButton()
        self.fullscreen_btn.setFixedSize(24, 24)
        self.fullscreen_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.fullscreen_btn.setStyleSheet("background: transparent; border: none;")
        self.fullscreen_btn.clicked.connect(self.open_fullscreen)
        
        fs_layout = QHBoxLayout(self.fullscreen_btn)
        fs_layout.setContentsMargins(0, 0, 0, 0)
        fs_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        fs_icon = QLabel("fullscreen")
        fs_icon.setFont(QFont("Material Symbols Outlined", 24))
        fs_icon.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        fs_layout.addWidget(fs_icon)
        
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.progress_bar, 1) # Expand progress bar
        control_layout.addWidget(self.time_lbl)
        control_layout.addWidget(self.fullscreen_btn)
        
        layout.addWidget(self.control_bar)
        
    def on_video_frame_changed(self, frame):
        if not self.is_active or not frame.isValid():
            return
        img = frame.toImage()
        if img.isNull():
            return
        w, h = self.target_w, self.target_h
        if w > 0 and h > 0:
            scaled_img = img.scaled(
                w, h,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self.frame_received.emit(scaled_img)

    def on_safe_frame_received(self, img):
        self.current_frame_image = img
        self.current_frame_pixmap = QPixmap.fromImage(img)
        self.update()
        
    def toggle_play(self):
        if self.is_playing:
            self.pause_video()
        else:
            self.play_video()
            
    def play_video(self):
        self.is_playing = True
        self.media_player.play()
        self.update_control_ui()
        
    def pause_video(self):
        self.is_playing = False
        self.media_player.pause()
        self.update_control_ui()
        
    def update_control_ui(self):
        if self.is_playing:
            self.center_overlay.setVisible(False)
            self.pause_icon.setText("pause")
        else:
            self.center_overlay.setVisible(True)
            self.pause_icon.setText("play_arrow")
            
    def open_fullscreen(self):
        self.fullscreen_player = FullscreenVideoPlayer(self.media_player, self)
        
    def on_duration_changed(self, duration_ms):
        self.video_duration = duration_ms
        self.update_time_label()
        
    def on_position_changed(self, position_ms):
        self.video_position = position_ms
        if self.video_duration > 0:
            val = int((position_ms / self.video_duration) * 100.0)
            self.progress_bar.setValue(val)
        self.update_time_label()
        
    def update_time_label(self):
        pos_sec = self.video_position // 1000
        dur_sec = self.video_duration // 1000
        
        pos_m = pos_sec // 60
        pos_s = pos_sec % 60
        
        dur_m = dur_sec // 60
        dur_s = dur_sec % 60
        
        self.time_lbl.setText(f"{pos_m:02d}:{pos_s:02d} / {dur_m:02d}:{dur_s:02d}")

    def showEvent(self, event):
        super().showEvent(event)
        self.is_active = True
        self.target_w = self.width()
        self.target_h = self.height()
        self.update_cover_cache()
        if self.is_playing:
            self.media_player.play()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.is_active = False
        self.media_player.stop()
        self.current_frame_image = None
        self.current_frame_pixmap = None
        self.cover_pixmap_cached = None

    def update_cover_cache(self):
        w, h = self.target_w, self.target_h
        if w > 0 and h > 0 and not self.pixmap.isNull():
            self.cover_pixmap_cached = self.pixmap.scaled(
                w, h,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
        else:
            self.cover_pixmap_cached = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        self.target_w = size.width()
        self.target_h = size.height()
        self.update_cover_cache()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        # 1. Rounded Clip Path
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 30.0, 30.0)
        painter.save()
        painter.setClipPath(path)
        
        # 2. Draw Frame or Cover Image
        drawn = False
        if self.current_frame_pixmap is not None and not self.current_frame_pixmap.isNull():
            src_x = (self.current_frame_pixmap.width() - rect.width()) // 2
            src_y = (self.current_frame_pixmap.height() - rect.height()) // 2
            painter.drawPixmap(rect, self.current_frame_pixmap, QRect(src_x, src_y, rect.width(), rect.height()))
            drawn = True
                
        if not drawn and self.cover_pixmap_cached is not None and not self.cover_pixmap_cached.isNull():
            src_x = (self.cover_pixmap_cached.width() - rect.width()) // 2
            src_y = (self.cover_pixmap_cached.height() - rect.height()) // 2
            painter.drawPixmap(rect, self.cover_pixmap_cached, QRect(src_x, src_y, rect.width(), rect.height()))
            
        # 3. Transparent tint overlay for movie screen aesthetic
        painter.fillRect(rect, QColor(11, 19, 38, 140)) # mix-blend dark opacity
        painter.restore()
        
        # 4. Subtle inner border glow
        painter.setPen(QColor(0, 219, 233, 25))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5), 30.0, 30.0)


class VideoWrapper(QWidget):
    def __init__(self, video_widget, parent=None):
        super().__init__(parent)
        self.video_widget = video_widget
        self.video_widget.setParent(self)
        
        size_policy = self.sizePolicy()
        size_policy.setHeightForWidth(True)
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Preferred)
        self.setSizePolicy(size_policy)
        
    def heightForWidth(self, width):
        return int(width * 9.0 / 16.0)
        
    def resizeEvent(self, event):
        self.video_widget.setGeometry(self.rect())


class InstructionCard(QPushButton):
    def sizeHint(self):
        lay = self.layout()
        if lay:
            return lay.sizeHint()
        return super().sizeHint()

    def minimumSizeHint(self):
        lay = self.layout()
        if lay:
            return lay.minimumSize()
        return super().minimumSizeHint()

    def __init__(self, icon_str, title_str, desc_str, accent_color, parent=None):
        super().__init__(parent)
        self.accent_color = accent_color
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.setStyleSheet("""
            InstructionCard {
                background-color: #131b2e;
                border: 1px solid rgba(255, 255, 255, 0.03);
                border-radius: 16px;
                text-align: left;
            }
            InstructionCard:hover {
                background-color: #171f33;
                border: 1px solid rgba(0, 240, 255, 0.25);
            }
            InstructionCard:pressed {
                background-color: #0b1326;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Accent vertical bar on the left
        accent_bar = QWidget()
        accent_bar.setFixedWidth(4)
        accent_bar.setStyleSheet(f"background-color: {accent_color}; border-radius: 2px;")
        
        # Content vertical layout
        content_layout = QVBoxLayout()
        content_layout.setSpacing(6)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        self.icon_lbl = QLabel(icon_str)
        self.icon_lbl.setFont(QFont("Material Symbols Outlined", 24))
        self.icon_lbl.setStyleSheet(f"color: {accent_color}; background: transparent; border: none;")
        
        self.title_lbl = QLabel(title_str)
        self.title_lbl.setFont(QFont("Space Grotesk", 13, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet("color: #dbfcff; background: transparent; border: none;")
        
        self.desc_lbl = QLabel(desc_str)
        self.desc_lbl.setFont(QFont("Inter", 10))
        self.desc_lbl.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        self.desc_lbl.setWordWrap(True)
        
        content_layout.addWidget(self.icon_lbl)
        content_layout.addWidget(self.title_lbl)
        content_layout.addWidget(self.desc_lbl)
        
        layout.addWidget(accent_bar)
        layout.addLayout(content_layout, 1)
        self.setMinimumWidth(180)


class PlugInState(QWidget):
    proceed_to_payment = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.update_language("en")  # English default
        
    def setup_ui(self):
        # Outer main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 20)
        main_layout.setSpacing(24)
        
        # 1. Header Row
        header_row = QHBoxLayout()
        header_row.setSpacing(12)
        
        # Pulsing green dot and title layout
        title_container = QHBoxLayout()
        title_container.setSpacing(12)
        title_container.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        self.pulse_dot = PulsingDot()
        
        self.header_title = QLabel("PLUG IN STATE")
        header_font = QFont("Space Grotesk", 20, QFont.Weight.Bold)
        header_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 110)
        self.header_title.setFont(header_font)
        self.header_title.setStyleSheet("color: #4edea3; background: transparent; padding-right: 20px;")
        
        title_container.addWidget(self.pulse_dot)
        title_container.addWidget(self.header_title)
        
        # Estimated time pill container
        self.est_container = QWidget()
        self.est_container.setStyleSheet("""
            QWidget {
                background-color: #171f33;
                border: 1px solid rgba(59, 73, 75, 0.2);
                border-radius: 20px;
            }
        """)
        self.est_container.setFixedHeight(40)
        
        est_layout = QHBoxLayout(self.est_container)
        est_layout.setContentsMargins(18, 0, 18, 0)
        est_layout.setSpacing(8)
        
        self.est_time = QLabel("00:45")
        self.est_time.setFont(QFont("Space Grotesk", 14, QFont.Weight.Bold))
        self.est_time.setStyleSheet("color: #00dbe9; background: transparent; border: none;")
        
        self.est_lbl = QLabel("ESTIMATED")
        self.est_lbl.setFont(QFont("Inter", 10))
        self.est_lbl.setStyleSheet("color: #b9cacb; background: transparent; border: none;")
        
        est_layout.addWidget(self.est_time)
        est_layout.addWidget(self.est_lbl)
        
        header_row.addLayout(title_container)
        header_row.addStretch()
        header_row.addWidget(self.est_container)
        
        main_layout.addLayout(header_row)
        
        # 2. Aspect-locked Video Player
        self.video_container = VideoContainer()
        self.video_wrapper = VideoWrapper(self.video_container)
        self.video_wrapper.setMinimumHeight(240)
        
        # We give the video wrapper 100% of stretch factor so it resizes beautifully
        main_layout.addWidget(self.video_wrapper, 1)
        
        # 3. Secondary Instructions Cards (Row of 3)
        self.cards_row = QHBoxLayout()
        self.cards_row.setSpacing(16)
        
        self.card1 = InstructionCard("power", "", "", "#4edea3")
        self.card2 = InstructionCard("contactless", "", "", "rgba(0, 240, 255, 0.4)")
        self.card3 = InstructionCard("bolt", "", "", "rgba(0, 240, 255, 0.4)")
        
        self.cards_row.addWidget(self.card1)
        self.cards_row.addWidget(self.card2)
        self.cards_row.addWidget(self.card3)
        
        main_layout.addLayout(self.cards_row)
        
        # 4. Help Support & Proceed Button Row
        help_row = QHBoxLayout()
        
        self.help_btn = LayoutButton()
        self.help_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.help_btn.setStyleSheet("""
            QPushButton {
                background-color: #222a3d;
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                padding-left: 20px;
                padding-right: 20px;
                min-height: 42px;
            }
            QPushButton:hover {
                background-color: #31394d;
            }
            QPushButton:pressed {
                background-color: #171f33;
            }
        """)
        
        help_btn_layout = QHBoxLayout(self.help_btn)
        help_btn_layout.setSpacing(8)
        help_btn_layout.setContentsMargins(20, 0, 20, 0)
        
        help_icon = QLabel("help")
        help_icon.setFont(QFont("Material Symbols Outlined", 20))
        help_icon.setStyleSheet("color: #dbfcff; background: transparent; border: none;")
        
        self.help_txt = QLabel("Get Assistance")
        self.help_txt.setFont(QFont("Space Grotesk", 13, QFont.Weight.Bold))
        self.help_txt.setStyleSheet("color: #dbfcff; background: transparent; border: none;")
        
        help_btn_layout.addWidget(help_icon)
        help_btn_layout.addWidget(self.help_txt)
        
        # Proceed Button
        self.proceed_btn = LayoutButton()
        self.proceed_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.proceed_btn.setStyleSheet("""
            QPushButton {
                background-color: #00f0ff;
                border: none;
                border-radius: 12px;
                padding-left: 24px;
                padding-right: 24px;
                min-height: 42px;
            }
            QPushButton:hover {
                background-color: #00dbe9;
            }
            QPushButton:pressed {
                background-color: #00b8c4;
            }
        """)
        
        proceed_shadow = QGraphicsDropShadowEffect(self.proceed_btn)
        proceed_shadow.setBlurRadius(20)
        proceed_shadow.setColor(QColor(0, 240, 255, 120))
        proceed_shadow.setOffset(0, 3)
        self.proceed_btn.setGraphicsEffect(proceed_shadow)
        
        proceed_layout = QHBoxLayout(self.proceed_btn)
        proceed_layout.setSpacing(8)
        proceed_layout.setContentsMargins(20, 0, 20, 0)
        
        self.proceed_txt = QLabel("PROCEED TO PAYMENT")
        self.proceed_txt.setFont(QFont("Space Grotesk", 13, QFont.Weight.Bold))
        self.proceed_txt.setStyleSheet("color: #00363a; background: transparent; border: none;")
        
        proceed_icon = QLabel("arrow_forward")
        proceed_icon.setFont(QFont("Material Symbols Outlined", 20))
        proceed_icon.setStyleSheet("color: #00363a; background: transparent; border: none;")
        
        proceed_layout.addWidget(self.proceed_txt)
        proceed_layout.addWidget(proceed_icon)
        
        # Connect buttons & Card 3 click
        self.proceed_btn.clicked.connect(self.proceed_to_payment.emit)
        self.card3.clicked.connect(self.proceed_btn.click)
        
        help_row.addWidget(self.help_btn)
        help_row.addStretch()
        help_row.addWidget(self.proceed_btn)
        
        main_layout.addLayout(help_row)

    def update_language(self, lang):
        if lang == "en":
            self.header_title.setText("PLUG IN STATE")
            self.est_lbl.setText("ESTIMATED")
            self.help_txt.setText("Get Assistance")
            self.proceed_txt.setText("PROCEED TO PAYMENT")
            
            self.video_container.video_title_lbl.setText("INSTRUCTIONAL VIDEO")
            self.video_container.video_sub_lbl.setText("How to plug in charger • scan RFID • start charging")
            
            self.card1.title_lbl.setText("1. Connect Cable")
            self.card1.desc_lbl.setText("Firmly insert the CCS2 connector into your vehicle port until you hear a click.")
            
            self.card2.title_lbl.setText("2. Authenticate")
            self.card2.desc_lbl.setText("Tap your RFID card or scan the QR code using the Voltcore mobile app.")
            
            self.card3.title_lbl.setText("3. Start Charge")
            self.card3.desc_lbl.setText("Session will begin automatically once handshake protocol is verified.")
        else: # id
            self.header_title.setText("HUBUNGKAN KONEKTOR")
            self.est_lbl.setText("ESTIMASI")
            self.help_txt.setText("Bantuan")
            self.proceed_txt.setText("LANJUT KE PEMBAYARAN")
            
            self.video_container.video_title_lbl.setText("VIDEO INSTRUKSIONAL")
            self.video_container.video_sub_lbl.setText("Cara colok charger • scan RFID • mulai charging")
            
            self.card1.title_lbl.setText("1. Hubungkan Kabel")
            self.card1.desc_lbl.setText("Masukkan konektor CCS2 dengan kuat ke port kendaraan Anda sampai terdengar bunyi klik.")
            
            self.card2.title_lbl.setText("2. Autentikasi")
            self.card2.desc_lbl.setText("Tempelkan kartu RFID Anda atau pindai kode QR menggunakan aplikasi Voltcore.")
            
            self.card3.title_lbl.setText("3. Mulai Pengisian")
            self.card3.desc_lbl.setText("Sesi pengisian akan dimulai secara otomatis setelah protokol jabat tangan diverifikasi.")

    def hideEvent(self, event):
        self.video_container.media_player.pause()
        self.video_container.pause_video()
        super().hideEvent(event)
