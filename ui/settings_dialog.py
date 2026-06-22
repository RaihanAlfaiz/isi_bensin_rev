from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QCheckBox, QSpinBox, QLineEdit, QPushButton, QGridLayout, QFrame
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QFont

class SettingsDialog(QDialog):
    def __init__(self, main_win):
        super().__init__(main_win)
        self.main_win = main_win
        
        self.setWindowTitle("VOLTCORE Simulator Control Panel")
        self.resize(480, 560)
        self.setStyleSheet("""
            QDialog {
                background-color: #0b1326;
                border: 2px solid #00f0ff;
                border-radius: 16px;
            }
            QLabel {
                color: #dbfcff;
                font-family: 'Space Grotesk', 'Inter';
            }
            QComboBox, QLineEdit, QSpinBox {
                background-color: #131b2e;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 6px;
                color: #ffffff;
                font-family: 'Inter';
            }
            QComboBox:hover, QLineEdit:hover, QSpinBox:hover {
                border-color: #00f0ff;
            }
            QCheckBox {
                color: #b9cacb;
                font-family: 'Inter';
            }
            QPushButton {
                background-color: #131b2e;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 8px 12px;
                color: #dbfcff;
                font-family: 'Space Grotesk';
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 240, 255, 0.15);
                border-color: #00f0ff;
            }
            QPushButton#btn_apply {
                background-color: #00dbe9;
                color: #002022;
                border: none;
            }
            QPushButton#btn_apply:hover {
                background-color: #00f0ff;
            }
        """)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Title
        title_lbl = QLabel("SIMULATOR CONTROL PANEL")
        title_lbl.setFont(QFont("Space Grotesk", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #00f0ff; letter-spacing: 1px; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_lbl)

        # Separator line
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        sep.setStyleSheet("background-color: rgba(255, 255, 255, 0.05); max-height: 1px;")
        layout.addWidget(sep)

        # 1. Status Section
        status_layout = QHBoxLayout()
        status_lbl = QLabel("Charger Status:")
        status_lbl.setFont(QFont("Space Grotesk", 11, QFont.Weight.Bold))
        
        self.status_cb = QComboBox()
        self.status_cb.addItems(["Available", "Preparing", "Charging", "Finishing", "Reserved", "Scheduled", "Faulted"])
        
        # Select current state
        current_state = self.main_win.sidebar.status_state
        state_map = {
            "idle": "Available",
            "available": "Available",
            "preparing": "Preparing",
            "charging": "Charging",
            "finishing": "Finishing",
            "reserved": "Reserved",
            "scheduled": "Scheduled",
            "faulted": "Faulted"
        }
        self.status_cb.setCurrentText(state_map.get(current_state, "Available"))
        
        status_layout.addWidget(status_lbl)
        status_layout.addWidget(self.status_cb, 1)
        layout.addLayout(status_layout)

        # 2. Queue Section
        queue_group = QVBoxLayout()
        queue_group.setSpacing(8)
        
        queue_hdr = QLabel("Queue Information")
        queue_hdr.setFont(QFont("Space Grotesk", 11, QFont.Weight.Bold))
        queue_hdr.setStyleSheet("color: #00dbe9;")
        queue_group.addWidget(queue_hdr)
        
        self.queue_active_chk = QCheckBox("Enable Waiting Queue")
        self.queue_active_chk.setChecked(self.main_win.sidebar.queue_active)
        queue_group.addWidget(self.queue_active_chk)
        
        # Spinners
        spinners_layout = QHBoxLayout()
        
        users_lbl = QLabel("Waiting Users:")
        self.users_spin = QSpinBox()
        self.users_spin.setRange(0, 20)
        self.users_spin.setValue(self.main_win.sidebar.waiting_users)
        
        wait_lbl = QLabel("Est. Wait (Mins):")
        self.wait_spin = QSpinBox()
        self.wait_spin.setRange(0, 180)
        self.wait_spin.setValue(self.main_win.sidebar.est_wait_time)
        
        spinners_layout.addWidget(users_lbl)
        spinners_layout.addWidget(self.users_spin)
        spinners_layout.addWidget(wait_lbl)
        spinners_layout.addWidget(self.wait_spin)
        queue_group.addLayout(spinners_layout)
        layout.addLayout(queue_group)

        # 3. Reservation Info Section
        res_group = QVBoxLayout()
        res_group.setSpacing(8)
        
        res_hdr = QLabel("Reservation Details")
        res_hdr.setFont(QFont("Space Grotesk", 11, QFont.Weight.Bold))
        res_hdr.setStyleSheet("color: #ffaa44;")
        res_group.addWidget(res_hdr)
        
        res_form = QGridLayout()
        res_form.setSpacing(8)
        
        res_form.addWidget(QLabel("Booked By:"), 0, 0)
        self.res_user_input = QLineEdit()
        self.res_user_input.setText(self.main_win.sidebar.reservation_card.user)
        res_form.addWidget(self.res_user_input, 0, 1)
        
        res_form.addWidget(QLabel("Start Time:"), 1, 0)
        self.res_time_input = QLineEdit()
        self.res_time_input.setText(self.main_win.sidebar.reservation_card.start_time.replace("Start Time: ", ""))
        res_form.addWidget(self.res_time_input, 1, 1)
        
        res_group.addLayout(res_form)
        layout.addLayout(res_group)

        # Separator line
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setFrameShadow(QFrame.Shadow.Sunken)
        sep2.setStyleSheet("background-color: rgba(255, 255, 255, 0.05); max-height: 1px;")
        layout.addWidget(sep2)

        # 4. Trigger Events Section
        event_group = QVBoxLayout()
        event_group.setSpacing(8)
        
        event_hdr = QLabel("Manual Event Triggers")
        event_hdr.setFont(QFont("Space Grotesk", 11, QFont.Weight.Bold))
        event_group.addWidget(event_hdr)
        
        event_grid = QGridLayout()
        event_grid.setSpacing(8)
        
        btn_conn = QPushButton("Vehicle Connected")
        btn_start = QPushButton("Charging Started")
        btn_finish = QPushButton("Charging Finished")
        btn_res = QPushButton("Reservation Created")
        btn_q = QPushButton("Queue Updated")
        btn_fault = QPushButton("Fault Detected")
        
        btn_conn.clicked.connect(lambda: self.trigger_manual_event("connected"))
        btn_start.clicked.connect(lambda: self.trigger_manual_event("started"))
        btn_finish.clicked.connect(lambda: self.trigger_manual_event("finished"))
        btn_res.clicked.connect(lambda: self.trigger_manual_event("reservation"))
        btn_q.clicked.connect(lambda: self.trigger_manual_event("queue"))
        btn_fault.clicked.connect(lambda: self.trigger_manual_event("fault"))
        
        event_grid.addWidget(btn_conn, 0, 0)
        event_grid.addWidget(btn_start, 0, 1)
        event_grid.addWidget(btn_finish, 1, 0)
        event_grid.addWidget(btn_res, 1, 1)
        event_grid.addWidget(btn_q, 2, 0)
        event_grid.addWidget(btn_fault, 2, 1)
        
        event_group.addLayout(event_grid)
        layout.addLayout(event_group)

        # Spacer
        layout.addStretch()

        # Apply Button
        self.apply_btn = QPushButton("APPLY SIMULATION CHANGES")
        self.apply_btn.setObjectName("btn_apply")
        self.apply_btn.setFont(QFont("Space Grotesk", 12, QFont.Weight.Bold))
        self.apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_btn.setFixedHeight(48)
        self.apply_btn.clicked.connect(self.apply_settings)
        layout.addWidget(self.apply_btn)

    def apply_settings(self):
        # 1. Update Status
        status_map = {
            "Available": "idle",
            "Preparing": "preparing",
            "Charging": "charging",
            "Finishing": "finishing",
            "Reserved": "reserved",
            "Scheduled": "scheduled",
            "Faulted": "faulted"
        }
        selected_status_name = self.status_cb.currentText()
        selected_status_code = status_map[selected_status_name]
        
        # Only change if different
        if self.main_win.sidebar.status_state != selected_status_code:
            self.main_win.set_system_status(selected_status_code)
            
            # Auto-trigger status events
            time_str = QTime.currentTime().toString("HH:mm")
            if selected_status_code == "reserved":
                self.main_win.idle_page.add_system_event(
                    "Reserved Session Created",
                    "Sesi Reservasi Dibuat",
                    icon="bookmark",
                    color="#ffaa44"
                )
            elif selected_status_code == "faulted":
                self.main_win.idle_page.add_system_event(
                    "Fault Detected",
                    "Gangguan Terdeteksi",
                    icon="error",
                    color="#ff7b7b"
                )
            elif selected_status_code == "preparing":
                self.main_win.idle_page.add_system_event(
                    "Vehicle Connected",
                    "Kendaraan Terhubung",
                    icon="link",
                    color="#4edea3"
                )
            elif selected_status_code == "charging":
                self.main_win.idle_page.add_system_event(
                    "Charging Started",
                    "Pengisian Dimulai",
                    icon="bolt",
                    color="#00f0ff"
                )
            elif selected_status_code == "finishing":
                self.main_win.idle_page.add_system_event(
                    "Charging Finished",
                    "Pengisian Selesai",
                    icon="check_circle",
                    color="#b57cff"
                )

        # 2. Update Queue
        queue_active = self.queue_active_chk.isChecked()
        users = self.users_spin.value()
        wait_time = self.wait_spin.value()
        
        # Check if queue changed
        if (self.main_win.sidebar.queue_active != queue_active or 
            self.main_win.sidebar.waiting_users != users or 
            self.main_win.sidebar.est_wait_time != wait_time):
            
            self.main_win.sidebar.update_queue_info(queue_active, users, wait_time)
            
            # Log queue updated event
            self.main_win.idle_page.add_system_event(
                f"Queue Updated ({users} users waiting)",
                f"Antrean Diperbarui ({users} pengguna antre)",
                icon="people",
                color="#00dbe9"
            )

        # 3. Update Reservation details
        res_user = self.res_user_input.text()
        res_time = self.res_time_input.text()
        self.main_win.sidebar.reservation_card.set_reservation_details(
            selected_status_name,
            res_user,
            f"Start Time: {res_time}"
        )

        self.accept()

    def trigger_manual_event(self, event_type):
        time_str = QTime.currentTime().toString("HH:mm")
        if event_type == "connected":
            self.main_win.idle_page.add_system_event(
                "Vehicle Connected",
                "Kendaraan Terhubung",
                icon="link",
                color="#4edea3"
            )
        elif event_type == "started":
            self.main_win.idle_page.add_system_event(
                "Charging Started",
                "Pengisian Dimulai",
                icon="bolt",
                color="#00f0ff"
            )
        elif event_type == "finished":
            self.main_win.idle_page.add_system_event(
                "Charging Finished",
                "Pengisian Selesai",
                icon="check_circle",
                color="#b57cff"
            )
        elif event_type == "reservation":
            self.main_win.idle_page.add_system_event(
                "Reserved Session Created",
                "Sesi Reservasi Dibuat",
                icon="bookmark",
                color="#ffaa44"
            )
        elif event_type == "queue":
            users = self.users_spin.value()
            self.main_win.idle_page.add_system_event(
                f"Queue Updated ({users} users waiting)",
                f"Antrean Diperbarui ({users} pengguna antre)",
                icon="people",
                color="#00dbe9"
            )
        elif event_type == "fault":
            self.main_win.idle_page.add_system_event(
                "Fault Detected",
                "Gangguan Terdeteksi",
                icon="error",
                color="#ff7b7b"
            )
