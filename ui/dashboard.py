import sys
import qtawesome as qta
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SecureLog Analyzer")
        self.setGeometry(100, 100, 1300, 800)
        self.setStyleSheet("background-color: #071826; color: white;")

        # ================= ROOT LAYOUT (VERTICAL) =================
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ================= HEADER =================
        header_container = QFrame()
        header_container.setFixedHeight(90)
        header_container.setStyleSheet("""
            background-color: #0B1A2B;
            border-bottom: 1px solid #1F2A44;
        """)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 10, 20, 10)

        # LEFT (logo + title)
        left_section = QHBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("assets/securelog-logo.png")
        logo.setPixmap(pixmap.scaled(90,90, Qt.AspectRatioMode.KeepAspectRatio))
        logo.setFixedSize(100, 100)

        title_layout = QVBoxLayout()

        title = QLabel("SecureLog Analyzer")
        title.setStyleSheet("font-size: 32px; font-weight: bold; left: 30px;")

        subtitle = QLabel("Analyze logs. Detect threats. Visualize insights.")
        subtitle.setStyleSheet("font-size: 12px; color: #9CA3AF; left: 30px;")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        left_section.addWidget(logo)
        left_section.addLayout(title_layout)

        # RIGHT (buttons)
        right_section = QHBoxLayout()

        settings_btn = QPushButton("⚙ Settings")
        about_btn = QPushButton("ℹ    About")

        for btn in [settings_btn, about_btn]:
            btn.setFixedWidth(120)
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                background-color: #1A2D45;
                padding: 8px 16px;
                border-radius: 8px;
            """)

        right_section.addWidget(settings_btn)
        right_section.addWidget(about_btn)

        header_layout.addLayout(left_section)
        header_layout.addStretch()
        header_layout.addLayout(right_section)

        header_container.setLayout(header_layout)

        # ================= SIDEBAR CONTAINER =================
        sidebar_frame = QFrame()
        sidebar_frame.setFixedWidth(260)
        sidebar_frame.setStyleSheet("""
            QFrame {
                background-color: #0B1A2B;
                border-radius: 20px;
                border: 0.5px solid #3B82F6;
            }
        """)

        # layout belongs to the FRAME, not the main window
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(15,20,15,20)
        sidebar_layout.setSpacing(12)

        menu_items = [
             ("Dashboard", "fa5s.th-large"),
             ("Log Viewer", "fa5s.file-alt"),
             ("Analysis", "fa5s.shield-alt"),
             ("Visualizations", "fa5s.chart-bar"),
             ("Reports", "fa5s.clipboard-list")
        ]

        for i, (name, icon_name) in enumerate(menu_items):
            icon_color = "white" if i == 0 else "#9CA3AF"
            icon = qta.icon(icon_name, color=icon_color)


            btn = QPushButton(f"  {name}")
            btn.setIcon(icon)
            btn.setIconSize(QSize(20,20))

            if i == 0:
                #active button
                btn.setStyleSheet("""
                    background-color: #1E3A5F;
                    color: white;
                    font-weight: bold;
                    padding: 12px;
                    border-radius: 10px;
                    text-align: left;
                """)
            else:
                #normal buttons
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #0F253A;
                        padding: 12px;
                        border-radius: 10px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        background-color: #1A2D45;
                    }
                """)

            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
# ================= SIDEBAR STATUS CONTAINER =================
        # Create the container frame
        status_container = QFrame()
        status_container.setStyleSheet("""
            QFrame {
                background-color: #1A2D45; /* Slightly darker than sidebar or same as header */
                border-radius: 12px;
                border: none;
            }
        """)
        status_container_layout = QVBoxLayout(status_container)

        # Create the status label
        # We split these so we can style the dot and the text better
        system_label = QLabel("System Status")
        system_label.setStyleSheet("""
            color: #9CA3AF; 
            font-size: 11px; 
            font-weight: bold;
            background: transparent;
        """)

        status_label = QLabel("● Ready")
        status_label.setStyleSheet("""
            color: #4CAF50; 
            font-size: 12px; 
            font-weight: bold;
            background: transparent;
        """)
        
        version_label = QLabel("Version 1.0.0")
        version_label.setStyleSheet("""
            color: #9CA3AF; 
            font-size: 11px;
            background: transparent;
        """)

        status_container_layout.addWidget(system_label)
        status_container_layout.addWidget(status_label)
        status_container_layout.addWidget(version_label)

        # Add the container to your existing sidebar layout
        sidebar_layout.addWidget(status_container)

        # ================= CONTENT =================
        content = QVBoxLayout()
        content.setSpacing(30)
        content.setContentsMargins(20, 20, 20, 20)

        # UPLOAD CARD CONTAINER
        upload_card = QFrame()
        upload_card.setStyleSheet("""
            QFrame {
                background-color: #0B1A2B;
                border-radius: 15px;
                border: 0.5px solid #3B82F6;
            }
        """)

        upload_card_layout = QHBoxLayout(upload_card)
        upload_card_layout.setContentsMargins(20, 20, 20, 20)
        upload_card_layout.setSpacing(15)

        # Drag & Drop Box
        upload_box = QLabel("⬆️ Drag & drop your log file here\n.txt, .log, .csv (Max: 50MB)")
        upload_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_box.setStyleSheet("""
            background-color: #1A2D45;
            color: #9CA3AF;
            font-size: 22px;
            padding: 30px;
            border-radius: 12px;
            border: 2px dashed #3B82F6;
        """)

        # Button layout
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        # Common style for both buttons
        btn_style = """
            QPushButton {
                background-color: #3B82F6;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
                color: white;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """

        browse_btn = QPushButton("Browse File")
        browse_btn.setFixedHeight(45)
        browse_btn.setFixedWidth(150)
        browse_btn.setStyleSheet(btn_style)

        analyze_btn = QPushButton("Analyze Logs")
        analyze_btn.setFixedHeight(45)
        analyze_btn.setFixedWidth(150)
        analyze_btn.setStyleSheet(btn_style.replace("#3B82F6", "#10B981").replace("#2563EB", "#059669"))

        button_layout.addWidget(browse_btn)
        button_layout.addWidget(analyze_btn)

        # Adding components to the upload card layout
        upload_card_layout.addWidget(upload_box, 4)
        upload_card_layout.addWidget(browse_btn, 1)
        upload_card_layout.addWidget(analyze_btn, 1)

        # Adding whole card to the content layout
        content.addWidget(upload_card)

        # STATS
        stats_layout = QHBoxLayout()

        def stat_card(text, color):
            card = QLabel(text)
            card.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card.setFixedHeight(110)
            card.setStyleSheet(f"""
                background-color: {color};
                border-radius: 12px;
                font-weight: bold;
            """)
            return card

        stats_layout.addWidget(stat_card("Total Entries\n500", "#2A4365"))
        stats_layout.addWidget(stat_card("Successful Logins\n359", "#2F855A"))
        stats_layout.addWidget(stat_card("Failed Logins\n141", "#9B2C2C"))
        stats_layout.addWidget(stat_card("Suspicious Events\n94", "#B7791F"))
        stats_layout.addWidget(stat_card("Unique IPs\n63", "#6B46C1"))

        content.addLayout(stats_layout)

        # BOTTOM
        bottom = QHBoxLayout()

        alerts = QVBoxLayout()
        alerts.addWidget(QLabel("Alerts"))

        for txt in ["Multiple Failed Logins", "Suspicious IP Activity", "Unusual Login Time", "Access Denied"]:
            lbl = QLabel(txt)
            lbl.setStyleSheet("""
                background-color: #1A2D45;
                padding: 12px;
                border-radius: 8px;
            """)
            alerts.addWidget(lbl)

        chart_layout = QVBoxLayout()
        chart_layout.addWidget(QLabel("Log Activity Over Time"))

        chart = QLabel("Chart will appear here")
        chart.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart.setStyleSheet("""
            background-color: #1A2D45;
            border-radius: 12px;
            padding: 120px;
        """)

        chart_layout.addWidget(chart)

        bottom.addLayout(alerts, 1)
        bottom.addLayout(chart_layout, 2)

        content.addLayout(bottom)

        # ================= BODY (SIDEBAR + CONTENT) =================
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(10, 10, 10, 10)

        body_layout.addWidget(sidebar_frame,1)
        body_layout.addLayout(content, 4)

        # ================= FINAL =================
        main_layout.addWidget(header_container)
        main_layout.addLayout(body_layout)

        self.setLayout(main_layout)


app = QApplication(sys.argv)
window = Dashboard()
window.show()
sys.exit(app.exec())