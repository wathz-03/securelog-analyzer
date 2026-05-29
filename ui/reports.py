import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class ReportsPage(QWidget):
    """
    Main Reports Dashboard view widget built using structural components
    to match the securelog-analyzer UI specification.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #071826; color: white; font-family: 'Segoe UI';")
        
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        # Core scroll framework for dynamic multi-device presentation scaling
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #071826; }")
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #071826;")
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(24)

        # 1. PAGE HEADER ROW
        header_layout = QHBoxLayout()
        
        title_vbox = QVBoxLayout()
        title_vbox.setSpacing(4)
        page_title = QLabel("Reports")
        page_title.setStyleSheet("font-size: 26px; font-weight: bold; color: white; border: none;")
        page_subtitle = QLabel("Generate and manage security reports")
        page_subtitle.setStyleSheet("font-size: 14px; color: #9CA3AF; border: none;")
        title_vbox.addWidget(page_title)
        title_vbox.addWidget(page_subtitle)
        header_layout.addLayout(title_vbox)
        
        header_layout.addStretch()
        
        btn_generate = QPushButton("+ Generate New Report")
        btn_generate.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: bold;
                font-size: 13px;
                border-radius: 6px;
                padding: 10px 16px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        header_layout.addWidget(btn_generate)
        main_layout.addLayout(header_layout)

        # 2. METRIC KPI SUMMARY RIBBON
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        stats_layout.addWidget(self.create_stat_card("Reports Generated", "24", "#1E293B"))
        stats_layout.addWidget(self.create_stat_card("Successful Reports", "22", "#064E3B"))
        stats_layout.addWidget(self.create_stat_card("Issues Found", "1,876", "#7F1D1D"))
        stats_layout.addWidget(self.create_stat_card("Critical Issues", "289", "#3B0764"))
        stats_layout.addWidget(self.create_stat_card("Exports", "18", "#115E59"))
        
        main_layout.addLayout(stats_layout)

        # 3. LOWER SPLIT CONTENT: TABLE WORKSPACE & SIDE PANELS
        workspace_layout = QHBoxLayout()
        workspace_layout.setSpacing(20)

        # Left Container: Generated Reports Data Table (75% width allocation)
        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")
        table_frame.setStyleSheet("""
            QFrame#tableFrame {
                background-color: #071826; 
                border: 0.5px solid #3B82F6; 
                border-radius: 10px;
            }
        """)
        table_vbox = QVBoxLayout(table_frame)
        table_vbox.setContentsMargins(16, 16, 16, 16)
        table_vbox.setSpacing(12)
        
        table_title = QLabel("Generated Reports")
        table_title.setStyleSheet("font-size: 16px; font-weight: bold; color: white; border: none;")
        table_vbox.addWidget(table_title)
        
        # Build Table Widget
        self.report_table = QTableWidget()
        self.init_data_table()
        table_vbox.addWidget(self.report_table)
        
        workspace_layout.addWidget(table_frame, stretch=75)

        # Right Container: Action Panels Stack (25% width allocation)
        side_panel_layout = QVBoxLayout()
        side_panel_layout.setSpacing(20)
        
        # Quick Actions Card
        actions_card = QFrame()
        actions_card.setObjectName("sideCard")
        actions_card.setStyleSheet("QFrame#sideCard { background-color: #1E293B; border-radius: 10px; }")
        actions_vbox = QVBoxLayout(actions_card)
        actions_vbox.setContentsMargins(16, 16, 16, 16)
        actions_vbox.setSpacing(12)
        
        actions_title = QLabel("Quick Actions")
        actions_title.setStyleSheet("font-size: 15px; font-weight: bold; color: white;")
        actions_vbox.addWidget(actions_title)
        
        # Clean helper macro loop for fast link building without redundancy
        for act_text in ["Generate Security Summary", "Generate Threat Analysis", "Generate Compliance Report"]:
            btn_action = QPushButton(f"⚡ {act_text}")
            btn_action.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    background: transparent;
                    color: #9CA3AF;
                    font-size: 13px;
                    border: none;
                    padding: 4px 0px;
                }
                QPushButton:hover {
                    color: #3B82F6;
                }
            """)
            actions_vbox.addWidget(btn_action)
        
        side_panel_layout.addWidget(actions_card)
        workspace_layout.addLayout(side_panel_layout, stretch=25)

        main_layout.addLayout(workspace_layout)
        
        # Final Assembler
        scroll.setWidget(content_widget)
        outer_layout.addWidget(scroll)

    def create_stat_card(self, title, value, bg_color):
        """Generates standardized metric trackers containing strict stylesheet inheritance safety bounds."""
        card = QFrame()
        card.setObjectName("cardFrame")
        card.setStyleSheet(f"""
            QFrame#cardFrame {{
                background-color: {bg_color};
                border: 0.5px solid #3B82F6;
                border-radius: 8px;
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(6)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #9CA3AF; font-size: 13px; font-weight: 500;")
        
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        
        card_layout.addWidget(lbl_title)
        card_layout.addWidget(lbl_val)
        return card

    def init_data_table(self):
        """Prepares metadata dimensions and visual configurations for the security tracking list."""
        headers = ["Report Name", "Type", "Date Generated", "Issues Found", "Status"]
        self.report_table.setColumnCount(len(headers))
        self.report_table.setHorizontalHeaderLabels(headers)
        
        # Layout metrics & constraints handling
        self.report_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.report_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.report_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.report_table.setShowGrid(False)
        self.report_table.verticalHeader().setVisible(False)
        
        # Clean custom flat styling over active elements 
        self.report_table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
                gridline-color: transparent;
                color: #E5E7EB;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #1F2937;
                color: #9CA3AF;
                font-weight: bold;
                padding: 8px;
                border: none;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 0.5px solid #1F2937;
            }
            QTableWidget::item:selected {
                background-color: #1E293B;
                color: white;
            }
        """)
        
        # Auto-stretching layout controls
        header = self.report_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            
        # Add a placeholder sample dataset immediately
        sample_data = [
            ("Security Summary - Weekly", "Security Summary", "2026-05-28", "312", "Completed"),
            ("Threat Analysis - External IPs", "Threat Analysis", "2026-05-27", "156", "Completed"),
            ("Compliance - PCI DSS", "Compliance", "2026-05-25", "89", "Completed"),
            ("System Health Report", "System Health", "2026-05-24", "0", "Failed")
        ]
        
        self.report_table.setRowCount(len(sample_data))
        for row_idx, row_data in enumerate(sample_data):
            for col_idx, text in enumerate(row_data):
                item = QTableWidgetItem(text)
                
                # Context styling logic for the status column
                if col_idx == 4:
                    if text == "Completed":
                        item.setForeground(Qt.GlobalColor.green)
                    else:
                        item.setForeground(Qt.GlobalColor.red)
                        
                self.report_table.setItem(row_idx, col_idx, item)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    preview_window = ReportsPage()
    preview_window.setWindowTitle("SecureLog Analyzer - Reports Preview")
    preview_window.resize(1100, 750)
    preview_window.show()
    sys.exit(app.exec())