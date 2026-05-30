import sys
import os
import qtawesome as qta
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize, QFileInfo 
from PyQt6.QtGui import QFont, QPixmap
from ui.log_viewer import LogViewer
from ui.analysis import AnalysisPage
from ui.visualizer import VisualizerPage 
from ui.reports import ReportsPage
from logic.parser import LogParserEngine


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.default_log_path = os.path.join("data", "sample_secure.log")
        self.parser = LogParserEngine(self.default_log_path)
        self.live_metrics = self.parser.parse_logs()

        self.setWindowTitle("SecureLog Analyzer")
        self.setGeometry(100, 100, 1300, 850)
        self.setStyleSheet("background-color: #071826; color: white;")

        self.sidebar_buttons = []

        # ROOT LAYOUT 
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        #  HEADER 
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
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio))
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
        about_btn = QPushButton("ℹ     About")

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

        # SIDEBAR CONTAINER 
        sidebar_frame = QFrame()
        sidebar_frame.setFixedWidth(260)
        sidebar_frame.setStyleSheet("""
            QFrame {
                background-color: #0B1A2B;
                border-radius: 20px;
                border: 0.5px solid #3B82F6;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
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
            btn.setIconSize(QSize(20, 20))

            if i == 0:
                btn.setStyleSheet("""
                    background-color: #1E3A5F;
                    color: white;
                    font-weight: bold;
                    padding: 12px;
                    border-radius: 10px;
                    text-align: left;
                """)
            else:
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
            btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))
            sidebar_layout.addWidget(btn)
            self.sidebar_buttons.append(btn)

        sidebar_layout.addStretch()

        #  SIDEBAR STATUS CONTAINER 
        status_container = QFrame()
        status_container.setStyleSheet("""
            QFrame {
                background-color: #1A2D45;
                border-radius: 12px;
                border: none;
            }
        """)
        status_container_layout = QVBoxLayout(status_container)

        system_label = QLabel("System Status")
        system_label.setStyleSheet("color: #9CA3AF; font-size: 11px; font-weight: bold; background: transparent;")

        status_label = QLabel("● Ready")
        status_label.setStyleSheet("color: #4CAF50; font-size: 12px; font-weight: bold; background: transparent;")
        
        version_label = QLabel("Version 1.0.0")
        version_label.setStyleSheet("color: #9CA3AF; font-size: 11px; background: transparent;")

        status_container_layout.addWidget(system_label)
        status_container_layout.addWidget(status_label)
        status_container_layout.addWidget(version_label)

        sidebar_layout.addWidget(status_container)

        #  SCROLLABLE CONTENT BODY 
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #0B1A2B;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #1A2D45;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: transparent;")
        content = QVBoxLayout(content_widget)
        content.setSpacing(25)  
        content.setContentsMargins(10, 10, 10, 10)

        #  UPLOAD CARD CONTAINER 
        upload_container = QFrame()
        upload_container.setStyleSheet("""
            QFrame {
                background-color: #0B1A2B;
                border-radius: 20px;
                border: 0.5px solid #3B82F6;
            }
        """)

        upload_card_layout = QGridLayout(upload_container)
        upload_card_layout.setContentsMargins(25, 20, 25, 25)
        upload_card_layout.setSpacing(15)

        upload_header = QLabel("Upload Log File")
        upload_header.setStyleSheet("font-size: 18px; font-weight: bold; color: white; border: none; background: transparent;")
        upload_card_layout.addWidget(upload_header, 0, 0, 1, 2)

        self.upload_box = QLabel("⬆️ Drag & drop your log file here\n.txt, .log, .csv (Max: 50MB)")
        self.upload_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upload_box.setMinimumHeight(130)  
        self.upload_box.setStyleSheet("""
            QLabel {
                background-color: #1A2D45;
                color: #9CA3AF;
                font-size: 16px;
                border-radius: 12px;
                border: 1px dashed #3B82F6;
            }
        """)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        btn_style = """
            QPushButton {
                background-color: #3B82F6;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
                color: white;
                border: none;
            }
            QPushButton:hover { background-color: #2563EB; }
        """

        browse_btn = QPushButton("Browse File")
        browse_btn.setFixedSize(150, 45)
        browse_btn.setStyleSheet(btn_style)
        browse_btn.clicked.connect(self.browse_log_file)

        analyze_btn = QPushButton("Analyze Logs")
        analyze_btn.setFixedSize(150, 45)
        analyze_btn.setStyleSheet(btn_style.replace("#3B82F6", "#10B981").replace("#2563EB", "#059669"))
        analyze_btn.clicked.connect(self.trigger_log_analysis)

        button_layout.addWidget(browse_btn)
        button_layout.addWidget(analyze_btn)

        upload_card_layout.addWidget(self.upload_box, 1, 0)
        upload_card_layout.addLayout(button_layout, 1, 1)
        upload_card_layout.setColumnStretch(0, 1)  

        content.addWidget(upload_container)

        # QUICK STATS CONTAINER 
        quick_stats_container = QFrame()
        quick_stats_container.setStyleSheet("""
            QFrame {
                background-color: #0B1A2B;
                border-radius: 20px;
                border: 0.5px solid #3B82F6;
            }
        """)

        outer_layout = QVBoxLayout(quick_stats_container)
        outer_layout.setContentsMargins(20, 15, 20, 20)

        stats_header = QLabel("Quick Stats")
        stats_header.setStyleSheet("font-size: 18px; font-weight: bold; color: white; border: none;")
        outer_layout.addWidget(stats_header)

        stats_row_layout = QHBoxLayout()
        stats_row_layout.setSpacing(15)


        def create_stat_card(title, value, subtitle, icon_name, color, bg_color):
            card = QFrame()
            card.setFixedHeight(120)
            card.setStyleSheet(f"""
                background-color: {bg_color};
                border-radius: 12px;
                border: 1px solid {color};
            """)

            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(15, 10, 15, 10)

            icon_label = QLabel()
            icon = qta.icon(icon_name, color=color)
            icon_label.setPixmap(icon.pixmap(35, 35))
            icon_label.setStyleSheet("background: transparent; border: none;")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            text_container = QVBoxLayout()
            text_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
            text_container.setSpacing(2)

            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold; background: transparent; border: none;")

            value_label = QLabel(value)
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold; background: transparent; border: none;")

            subtitle_label = QLabel(subtitle)
            subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            subtitle_label.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: bold; background: transparent; border: none;")

            text_container.addWidget(title_label)
            text_container.addWidget(value_label)
            text_container.addWidget(subtitle_label)

            card_layout.addWidget(icon_label, 1)
            card_layout.addLayout(text_container, 2)

            return card, value_label

        self.lbl_total, card_total = create_stat_card("Total Entries", "0", "All log records", "fa5s.file-alt", "#3B82F6", "#172A45")
        self.lbl_success, card_success = create_stat_card("Successful Logins", "0", "70.1% ↑", "fa5s.check-circle", "#10B981", "#064E3B")
        self.lbl_failed, card_failed = create_stat_card("Failed Logins", "0", "29.9% ↓", "fa5s.times-circle", "#EF4444", "#451A1A")
        self.lbl_suspicious, card_suspicious = create_stat_card("Suspicious Events", "0", "10.3% ⚠", "fa5s.exclamation-triangle", "#F59E0B", "#453015")
        self.lbl_ips, card_ips = create_stat_card("Unique IPs", "0", "Found", "fa5s.globe", "#8B5CF6", "#2D1A45")

        stats_row_layout.addWidget(card_total)
        stats_row_layout.addWidget(card_success)
        stats_row_layout.addWidget(card_failed)
        stats_row_layout.addWidget(card_suspicious)
        stats_row_layout.addWidget(card_ips)

        outer_layout.addLayout(stats_row_layout)
        content.addWidget(quick_stats_container)

        # BOTTOM SPLIT ROW 
        bottom = QHBoxLayout()
        bottom.setSpacing(20)

        # ALERTS CONTAINER 
        alerts_container = QFrame()
        alerts_container.setStyleSheet("""
            QFrame {
                background-color: #0B1A2B;
                border: 1px solid #1F2A44;
                border-radius: 20px;
            }
        """)
        
        alerts_outer_layout = QVBoxLayout(alerts_container)
        alerts_outer_layout.setContentsMargins(20, 20, 20, 20)
        alerts_outer_layout.setSpacing(15)

        header_row = QHBoxLayout()
        alerts_title = QLabel("Alerts")
        alerts_title.setStyleSheet("font-size: 24px; font-weight: bold; color: white; border: none; background: transparent;")
        
        view_all_btn = QPushButton("View All")
        view_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_all_btn.setStyleSheet("""
            QPushButton {
                color: #3B82F6;
                font-size: 14px;
                font-weight: bold;
                border: none;
                background: transparent;
            }
            QPushButton:hover { color: #60A5FA; text-decoration: underline; }
        """)

        view_all_btn.clicked.connect(lambda: self.switch_page(1))  

        header_row.addWidget(alerts_title)
        header_row.addStretch()
        header_row.addWidget(view_all_btn)
        alerts_outer_layout.addLayout(header_row)

        def create_alert_item(title, details, time_str, priority_text, main_color, bg_color):
            alert_card = QFrame()
            alert_card.setFixedHeight(80) 
            alert_card.setStyleSheet(f"background-color: {bg_color}; border-radius: 12px; border: none;")
            
            card_layout = QHBoxLayout(alert_card)
            card_layout.setContentsMargins(0, 0, 15, 0)
            card_layout.setSpacing(15)

            accent_bar = QFrame()
            accent_bar.setFixedWidth(6)
            accent_bar.setStyleSheet(f"""
                background-color: {main_color};
                border-top-left-radius: 12px;
                border-bottom-left-radius: 12px;
                border: none;
            """)
            
            dot_indicator = QLabel()
            dot_indicator.setFixedSize(14, 14)
            dot_indicator.setStyleSheet(f"background-color: {main_color}; border-radius: 7px; border: none;")

            text_container = QWidget()
            text_container.setStyleSheet("background: transparent; border: none;")
            text_layout = QVBoxLayout(text_container)
            text_layout.setContentsMargins(0, 5, 0, 5)
            text_layout.setSpacing(2)
            text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            t_lbl = QLabel(title)
            t_lbl.setStyleSheet("color: white; font-size: 15px; font-weight: bold; background: transparent;")
            
            d_lbl = QLabel(details)
            d_lbl.setStyleSheet("color: #D1D5DB; font-size: 11px; background: transparent;")
            
            time_lbl = QLabel(time_str)
            time_lbl.setStyleSheet("color: #6B7280; font-size: 10px; background: transparent;")

            text_layout.addWidget(t_lbl)
            text_layout.addWidget(d_lbl)
            text_layout.addWidget(time_lbl)

            badge = QPushButton(priority_text)
            badge.setFixedSize(115, 26)
            badge.setStyleSheet(f"""
                QPushButton {{
                    background-color: {main_color}; 
                    color: #FFFFFF;
                    border: none;
                    border-radius: 6px;
                    font-size: 10px;
                    font-weight: bold;
                }}
            """)

            card_layout.addWidget(accent_bar)
            card_layout.addWidget(dot_indicator, alignment=Qt.AlignmentFlag.AlignVCenter)
            card_layout.addWidget(text_container, stretch=1)
            card_layout.addWidget(badge, alignment=Qt.AlignmentFlag.AlignVCenter)
            
            return alert_card

        alerts_list_layout = QVBoxLayout()
        alerts_list_layout.setSpacing(10)

        alerts_list_layout.addWidget(create_alert_item("Multiple Failed Logins", "User 'admin' has 5 failed login attempts from 192.168.1.15", "10:24 AM", "High Priority", "#EF4444", "#2D1A1E"))
        alerts_list_layout.addWidget(create_alert_item("Suspicious IP Activity", "IP 203.0.113.45 has failed logins for 3 users", "10:20 AM", "Medium Priority", "#F59E0B", "#2D2415"))
        alerts_list_layout.addWidget(create_alert_item("Unusual Login Time", "User 'John_Doe' logged in outside business hours (02:17 AM)", "02:17 AM", "Low Priority", "#10B981", "#152D20"))
        alerts_list_layout.addWidget(create_alert_item("Access Denied", "Guest user attempted to access restricted file", "11:26 PM", "Medium Priority", "#F59E0B", "#2D2415"))

        alerts_outer_layout.addLayout(alerts_list_layout)

        #  CHART CONTAINER
        chart_container = QFrame()
        chart_container.setStyleSheet("""
            QFrame {
                background-color: #0B1A2B;
                border: 1px solid #1F2A44;
                border-radius: 20px;
            }
        """)
        chart_outer_layout = QVBoxLayout(chart_container)
        chart_outer_layout.setContentsMargins(20, 20, 20, 20)
        
        chart_title = QLabel("Log Activity Over Time")
        chart_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; border: none; background: transparent;")
        
        chart_placeholder = QLabel("Chart will appear here")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setMinimumHeight(350) 
        chart_placeholder.setStyleSheet("""
            background-color: #1A2D45;
            border-radius: 12px;
            color: #9CA3AF;
        """)

        chart_outer_layout.addWidget(chart_title)
        chart_outer_layout.addWidget(chart_placeholder, stretch=1)

        bottom.addWidget(alerts_container, 1)
        bottom.addWidget(chart_container, 1)  

        content.addLayout(bottom)
        content.addStretch(1) 

        scroll_area.setWidget(content_widget)

        self.main_pages = QStackedWidget()
        self.main_pages.addWidget(scroll_area)

        self.log_viewer_page = LogViewer()
        self.main_pages.addWidget(self.log_viewer_page)
        
        self.analysis_page = AnalysisPage()
        self.main_pages.addWidget(self.analysis_page)

        self.visualizer_page = VisualizerPage()
        self.main_pages.addWidget(self.visualizer_page)

        self.reports_page = ReportsPage()
        self.main_pages.addWidget(self.reports_page)

        # SIDEBAR + SCROLL CONTENT
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(15, 15, 15, 15)
        body_layout.setSpacing(15)

        body_layout.addWidget(sidebar_frame, 0) 
        body_layout.addWidget(self.main_pages, 1)   

        #  FINAL GLOBAL PACKING 
        main_layout.addWidget(header_container)
        main_layout.addLayout(body_layout)

        self.setLayout(main_layout)

        self.update_dashboard_ui_labels(self.live_metrics)

    def browse_log_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Log File",
            "",
            "Log Files (*.log *.txt *.csv);;All Files (*)"
        )
        if file_path:
            file_info = QFileInfo(file_path)
            file_name = file_info.fileName()

            self.upload_box.setText(f"📄 Loaded: {file_name}\nReady for deep analysis.")
            self.upload_box.setStyleSheet("""
                QLabel {
                    background-color: #1E3A8A;
                    color: #93C5FD;
                    font_size: 16px;
                    border-radius: 12px;
                    border: 2px solid #3B82F6;
                }
            """)
            self.default_log_path = file_path

    def update_dashboard_ui_labels(self, metrics):
        total_label = self.lbl_total.findChild(QLabel) if hasattr(self.lbl_total, 'findChild') else self.lbl_total
        success_label = self.lbl_success.findChild(QLabel) if hasattr(self.lbl_success, 'findChild') else self.lbl_success
        failed_label = self.lbl_failed.findChild(QLabel) if hasattr(self.lbl_failed, 'findChild') else self.lbl_failed

        if total_label:
            total_label.setText(str(metrics.get("total_entries", "0")))
        if success_label:
            success_label.setText(str(metrics.get("success_logins", "0")))
        if failed_label:
            failed_label.setText(str(metrics.get("failed_logins", "0")))

    def trigger_log_analysis(self):
        self.parser = LogParserEngine(self.default_log_path)
        self.live_metrics = self.parser.parse_logs()

        self.update_dashboard_ui_labels(self.live_metrics)

        file_name = QFileInfo(self.default_log_path).fileName()
        self.log_viewer_page.load_log_file(self.default_log_path)
        self.visualizer_page.render_metrics_charts(self.live_metrics)
        self.reports_page.generate_historical_summary(self.live_metrics, file_name)
        self.analysis_page.load_analysis_metrics(self.live_metrics)
        print("Re-parsing complete! Live metrics refreshed.")

    # NAVIGATION FUNCTION
    def switch_page(self, index):
        if index >= self.main_pages.count():
            return
        
        self.main_pages.setCurrentIndex(index)

        for i, btn in enumerate(self.sidebar_buttons):
            if i == index:
                btn.setStyleSheet("""
                    background-color: #1E3A5F;
                    color: white;
                    font-weight: bold;
                    padding: 12px;
                    border-radius: 10px;
                    text-align: left;
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #0F253A;
                        color: #9CA3AF;
                        padding: 12px;
                        border-radius: 10px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        background-color: #1A2D45;
                        color: white;
                    }       
                """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())