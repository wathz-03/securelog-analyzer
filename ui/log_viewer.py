import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont


class LogViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        
        self.setStyleSheet("background-color: #071826; color: white; font-family: 'Segoe UI';")
        
        # Main split layout 
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # LEFT COLUMN
        left_column = QVBoxLayout()
        left_column.setSpacing(15)

        # Section Title
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        viewer_title = QLabel("Log Viewer")
        viewer_title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        viewer_subtitle = QLabel("View and explore your parsed log data.")
        viewer_subtitle.setStyleSheet("font-size: 12px; color: #9CA3AF;")
        title_layout.addWidget(viewer_title)
        title_layout.addWidget(viewer_subtitle)
        left_column.addLayout(title_layout)

        # Clean Filter Bar 
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: #0B1A2B;
                border-radius: 12px;
                border: 0.5px solid #1E3A5F;
            }
        """)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(15, 12, 15, 12)
        filter_layout.setSpacing(15)

        # Text Filter
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by IP, username, keyword...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #1A2D45;
                color: white;
                border: 1px solid #1F2A44;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
        """)
        filter_layout.addWidget(self.search_input, stretch=3)

        # Level Dropdown Filter
        self.level_combo = QComboBox()
        self.level_combo.addItems(["All Levels", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.level_combo.setStyleSheet("""
            QComboBox {
                background-color: #1A2D45;
                color: white;
                border: 1px solid #1F2A44;
                border-radius: 6px;
                padding: 8px;
                min-width: 120px;
            }
            QComboBox QAbstractItemView {
                background-color: #0B1A2B;
                color: white;
                selection-background-color: #3B82F6;
            }
        """)
        filter_layout.addWidget(self.level_combo, stretch=1)

        left_column.addWidget(filter_frame)

        # Main Table Element
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: #0B1A2B;
                border-radius: 12px;
                border: 0.5px solid #1E3A5F;
            }
        """)
        table_container_layout = QVBoxLayout(table_frame)
        table_container_layout.setContentsMargins(10, 10, 10, 10)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Level", "Source IP", "Message"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
                gridline-color: transparent;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #14253D;
            }
            QTableWidget::item:selected {
                background-color: #1A365D;
                color: white;
            }
            QHeaderView::section {
                background-color: #112237;
                color: #9CA3AF;
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
                border: none;
                border-bottom: 2px solid #1E3A5F;
            }
        """)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        table_container_layout.addWidget(self.table)
        left_column.addWidget(table_frame, stretch=1)
        
        main_layout.addLayout(left_column, stretch=3)

        # RIGHT COLUMN: DYNAMIC LOG DETAILS INSPECTOR PANEL
        self.details_panel = QFrame()
        self.details_panel.setFixedWidth(340)
        self.details_panel.setStyleSheet("""
            QFrame {
                background-color: #0B1A2B;
                border-radius: 12px;
                border: 0.5px solid #1E3A5F;
            }
        """)
        
        details_layout = QVBoxLayout(self.details_panel)
        details_layout.setContentsMargins(20, 20, 20, 20)
        details_layout.setSpacing(15)

        details_title = QLabel("Log Details")
        details_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; border: none;")
        details_layout.addWidget(details_title)


        self.details_text_box = QTextBrowser()
        self.details_text_box.setHtml("<p style='color: #9CA3AF; font-size: 13px;'>Select a specific log row from the viewer table to inspect detailed item properties.</p>")
        self.details_text_box.setStyleSheet("""
            QTextBrowser {
                background-color: #071826;
                border: 1px solid #14253D;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
                line-height: 1.6;
            }
        """)
        details_layout.addWidget(self.details_text_box, stretch=1)

        main_layout.addWidget(self.details_panel)

        # Wire up connection hook
        self.table.itemSelectionChanged.connect(self.display_log_details)

        self.populate_mock_data()

    def populate_mock_data(self):
        mock_logs = [
            ("2026-05-18 10:45:32", "ERROR", "192.168.1.15", "Invalid password attempt for user: admin"),
            ("2026-05-18 10:44:21", "WARNING", "201.0.145.56", "Access denied to file directory: /etc/passwd"),
            ("2026-05-18 10:43:10", "INFO", "192.168.1.10", "User logged in successfully: john_doe"),
            ("2026-05-18 10:42:05", "INFO", "192.168.1.12", "Accessed file metadata system: report.pdf"),
            ("2026-05-18 10:41:55", "WARNING", "203.0.113.45", "Multiple sequential authorization failures detected"),
            ("2026-05-18 10:40:33", "CRITICAL", "127.0.0.1", "Core runtime service sshd crashed unexpectedly"),
        ]

        self.table.setRowCount(len(mock_logs))
        
        for row_idx, (timestamp, level, ip, message) in enumerate(mock_logs):
    
            ts_item = QTableWidgetItem(timestamp)
            lvl_item = QTableWidgetItem(level)
            ip_item = QTableWidgetItem(ip)
            msg_item = QTableWidgetItem(message)

            if level == "ERROR":
                lvl_item.setForeground(QColor("#EF4444")) 
            elif level == "WARNING":
                lvl_item.setForeground(QColor("#F59E0B")) 
            elif level == "CRITICAL":
                lvl_item.setForeground(QColor("#A855F7")) 
            elif level == "INFO":
                lvl_item.setForeground(QColor("#10B981")) 

            
            lvl_item.setFont(QFont("Segoe UI", weight=QFont.Weight.Bold))
            
            self.table.setItem(row_idx, 0, ts_item)
            self.table.setItem(row_idx, 1, lvl_item)
            self.table.setItem(row_idx, 2, ip_item)
            self.table.setItem(row_idx, 3, msg_item)

    def display_log_details(self):
        selected_ranges = self.table.selectedRanges()
        if not selected_ranges:
            return
            
        row = selected_ranges[0].topRow()
        
        timestamp = self.table.item(row, 0).text()
        level = self.table.item(row, 1).text()
        ip = self.table.item(row, 2).text()
        message = self.table.item(row, 3).text()

        html_details = f"""
        <table width="100%" style="color: white; font-size: 13px;">
            <tr><td style="color: #9CA3AF; padding-bottom: 8px;"><b>Timestamp:</b></td><td style="padding-bottom: 8px;">{timestamp}</td></tr>
            <tr><td style="color: #9CA3AF; padding-bottom: 8px;"><b>Log Level:</b></td><td style="padding-bottom: 8px;"><b>{level}</b></td></tr>
            <tr><td style="color: #9CA3AF; padding-bottom: 8px;"><b>Source IP:</b></td><td style="padding-bottom: 8px; color: #3B82F6;">{ip}</td></tr>
            <tr><td style="color: #9CA3AF; padding-bottom: 8px;"><b>Context:</b></td><td style="padding-bottom: 8px;">System Security Event Log</td></tr>
            <tr><td colspan="2" style="color: #9CA3AF; padding-top: 10px; padding-bottom: 4px;"><b>Full Message:</b></td></tr>
            <tr><td colspan="2" style="background-color: #112237; padding: 10px; border-radius: 6px; color: #E5E7EB; font-family: monospace;">{message}</td></tr>
        </table>
        """
        self.details_text_box.setHtml(html_details)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = LogViewer()
    viewer.resize(1100, 650)
    viewer.show()
    sys.exit(app.exec())