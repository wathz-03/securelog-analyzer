import sys
import os
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
                border: 0.5px solid #3B82F6;
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
                border: 0.5px solid #3B82F6;
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
                border: 0.5px solid #3B82F6;
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
                border: 0.5px solid #3B82F6;
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
                border: 0.5px solid #3B82F6;
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
                border: 0.5px solid #3B82F6;
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
        self.search_input.textChanged.connect(self.apply_filters)
        self.level_combo.currentTextChanged.connect(self.apply_filters)

        self.populate_mock_data()

    def load_log_file(self, file_path):
        """Receives log files selected from dashbaord and parses them live into rows."""
        if not os.path.exists(file_path):
            print(f"[LogViewer] Specified log file target path missing: {file_path}")
            return

        parsed_rows = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    level = "INFO"
                    if "ERROR" in line or "failed" in line.lower() or "invalid" in line.lower():
                        level = "ERROR"
                    elif "WARN" in line or "denied" in line.lower():
                        level = "WARNING"
                    elif "CRITICAL" in line or "crash" in line.lower():
                        level = "CRITICAL"

                    parts = line.split(" ", maxsplit=2)
                    timestamp = f"{parts[0]} {parts[1]}" if len(parts) >= 2 else "Unknown Time"

                    ip = "System Control"
                    for chunk in line.split():
                        if chunk.count(".") == 3 and chunk.replace(".", "").isdigit():
                            ip = chunk
                            break

                    parsed_rows.append((timestamp, level, ip, line))
                
            if parsed_rows:
                self.render_custom_log_list(parsed_rows)
                print(f"[LogViewer] Success! Loaded {len(parsed_rows)} entries from {os.path.basename(file_path)}.")
        except Exception as e:
            print(f"[LogViewer] File parsing pipeline failure: {str(e)}")

    def render_custom_log_list(self, log_list):
        """Clears existing entires and paints list variable onto structural table view."""
        self.table.setRowCount(0)
        self.table.setRowCount(len(log_list))

        for row_idx, (timestamp, level, ip, message) in enumerate(log_list):
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


    def populate_mock_data(self):
        mock_logs = [
            ("2026-05-18 10:45:32", "ERROR", "192.168.1.15", "Invalid password attempt for user: admin"),
            ("2026-05-18 10:44:21", "WARNING", "201.0.145.56", "Access denied to file directory: /etc/passwd"),
            ("2026-05-18 10:43:10", "INFO", "192.168.1.10", "User logged in successfully: john_doe"),
            ("2026-05-18 10:42:05", "INFO", "192.168.1.12", "Accessed file metadata system: report.pdf"),
            ("2026-05-18 10:41:55", "WARNING", "203.0.113.45", "Multiple sequential authorization failures detected"),
            ("2026-05-18 10:40:33", "CRITICAL", "127.0.0.1", "Core runtime service sshd crashed unexpectedly"),
        ]

        self.render_custom_log_list(mock_logs)

    def display_log_details(self):
        selected_ranges = self.table.selectedRanges()
        if not selected_ranges:
            return
            
        row = selected_ranges[0].topRow()

        if not self.table.item(row, 0):
            return
        
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

    def apply_filters(self):
        search_query = self.search_input.text().lower().strip()
        selected_level = self.level_combo.currentText().strip()

        for row in range(self.table.rowCount()):
            matches_search = False
            matches_level = False

            combined_row_text = ""
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    combined_row_text += item.text().lower() + " "

            if not search_query or search_query in combined_row_text:
                matches_search = True

            level_item = self.table.item(row, 1)
            row_level_value = level_item.text() if level_item else ""

            if selected_level == "All Levels" or selected_level == "":
                matches_level = True
            elif selected_level.upper() == row_level_value.upper():
                matches_level = True

            if matches_search and matches_level:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = LogViewer()
    viewer.resize(1100, 650)
    viewer.show()
    sys.exit(app.exec())