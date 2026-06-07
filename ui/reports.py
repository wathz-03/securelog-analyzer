import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class ReportsPage(QWidget):
    """
    Main Reports Dashboard view widget built using structural components
    to match the securelog-analyzer UI specification.
    """
    def __init__(self):
        super().__init__()
        self.historical_records = []
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #071826; color: white; font-family: 'Segoe UI';")
        
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
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
        main_layout.addLayout(header_layout)

        # 2. METRIC KPI SUMMARY RIBBON
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        self.lbl_reports = QLabel("0")
        self.lbl_successful = QLabel("0")
        self.lbl_issues = QLabel("0")
        self.lbl_critical = QLabel("0")

        card_rep = self.setup_stat_card(self.lbl_reports, "Reports Generated", "#1E293B")
        card_succ = self.setup_stat_card(self.lbl_successful, "Successful Reports", "#064E3B")
        card_iss = self.setup_stat_card(self.lbl_issues, "Issues Found", "#7F1D1D")
        card_crit = self.setup_stat_card(self.lbl_critical, "Critical Issues", "#3B0764")
    
        stats_layout.addWidget(card_rep)
        stats_layout.addWidget(card_succ)
        stats_layout.addWidget(card_iss)
        stats_layout.addWidget(card_crit)
        
        main_layout.addLayout(stats_layout)

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
        table_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

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

        main_layout.addWidget(table_frame, stretch=1)

        scroll.setWidget(content_widget)
        outer_layout.addWidget(scroll)

        self.load_initial_dataset()
        

    def setup_stat_card(self, label_widget, title, bg_color):
        """Assembles a KPI card using an explicitly maintained layout reference parameter."""
        card = QFrame()
        card.setObjectName("cardFrame")
        card.setMinimumHeight(100)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
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
        
        label_widget.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        
        card_layout.addWidget(lbl_title)
        card_layout.addWidget(label_widget)

        return card

    def init_data_table(self):
        """Prepares metadata dimensions and visual configurations for the security tracking list."""
        headers = ["Report Name", "Type", "Date Generated", "Issues Found", "Status"]
        self.report_table.setColumnCount(len(headers))
        self.report_table.setHorizontalHeaderLabels(headers)
        
        self.report_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.report_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.report_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.report_table.setShowGrid(False)
        self.report_table.verticalHeader().setVisible(False)
        
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
        
        header = self.report_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            
    def load_initial_dataset(self):
        """Loads starting baseline datasets matching active application specs."""
        self.historical_records = [
            ["Security Summary - Weekly", "Security Summary", "2026-05-28", "312", "Completed"],
            ["Threat Analysis - External IPs", "Threat Analysis", "2026-05-27", "156", "Completed"],
            ["Compliance - PCI DSS", "Compliance", "2026-05-25", "89", "Completed"],
            ["System Health Report", "System Health", "2026-05-24", "0", "Failed"]
        ]
        self.render_table_rows()
        self.recalculate_ribbon_counters()

    def render_table_rows(self):
        """Clears view frame and maps current historical records directly onto widget."""
        self.report_table.setRowCount(0)
        self.report_table.setRowCount(len(self.historical_records))
        
        for row_idx, row_data in enumerate(self.historical_records):
            for col_idx, text in enumerate(row_data):
                item = QTableWidgetItem(text)
                if col_idx == 3:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                
                if col_idx == 4:
                    if text == "Completed":
                        item.setForeground(QColor("#10B981"))
                    else:
                        item.setForeground(QColor("#EF4444"))

                self.report_table.setItem(row_idx, col_idx, item)

    def recalculate_ribbon_counters(self):
        """Aggregates row numbers dynamically to synchronize counter trackers accurately."""
        total_reports = len(self.historical_records)
        successful = sum(1 for r in self.historical_records if r[4] == "Completed")
        
        total_issues = 0
        for r in self.historical_records:
            try:
                total_issues += int(r[3].replace(",", ""))
            except ValueError:
                pass

        critical_issues = int(total_issues * 0.15)

        self.lbl_reports.setText(str(total_reports))
        self.lbl_successful.setText(str(successful))
        self.lbl_issues.setText(f"{total_issues:,}")
        self.lbl_critical.setText(f"{critical_issues:,}")

    def handle_quick_action_click(self, action_name):
        """Gracefully logs or executes targeted reporting operations without crashing."""
        print(f"[Quick Action] Initializing generation sequence for: {action_name}")
    
    def generate_historical_summary(self, metrics_data, file_name):
        """Intercepts analytical metric data objects and generates a new record entry row entry."""
        if not file_name:
            return
        
        import datetime

        failed = metrics_data.get("failed_logins", 0)
        suspicious = metrics_data.get("suspicious_events", 0)
        total_issues_count = failed + suspicious

        today_str = datetime.date.today().strftime("%Y-%m-%d")
        clean_name = f"Analysis - {file_name}"
        
        new_row = [clean_name, "Log Analysis", today_str, f"{total_issues_count:,}", "Completed"]
        self.historical_records.insert(0, new_row)
        
        self.render_table_rows()
        self.recalculate_ribbon_counters()


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    preview_window = ReportsPage()
    preview_window.setWindowTitle("SecureLog Analyzer - Reports Preview")
    preview_window.resize(1100, 750)
    preview_window.show()
    sys.exit(app.exec())