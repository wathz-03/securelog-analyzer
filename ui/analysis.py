import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QFont

class AnalysisPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Base background matches the seamless main view panel background
        self.setStyleSheet("background-color: #0A1523; color: white; font-family: 'Segoe UI';")
        
        # Main layout with explicit outer margins to prevent raw edge stretching
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(15)

        # HEADER BLOCK
        header_layout = QHBoxLayout()
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        page_title = QLabel("Analysis")
        page_title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        page_subtitle = QLabel("System threat posture assessment and log intelligence insights.")
        page_subtitle.setStyleSheet("font-size: 12px; color: #708599;")
        title_layout.addWidget(page_title)
        title_layout.addWidget(page_subtitle)
        header_layout.addLayout(title_layout)

        header_layout.addStretch()

        run_btn = QPushButton("Run New Analysis")
        run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        run_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border: 0.5px solid #3B82F6;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        header_layout.addWidget(run_btn)
        main_layout.addLayout(header_layout)

        # 1. TOP SECTION: SOLID QUICK STATS PANEL
        stats_container = QFrame()
        stats_container.setStyleSheet("""
            QFrame {
                background-color: #0E1E31;
                border: 0.5px solid #3B82F6;
                border-radius: 8px;
            }
        """)
        stats_outer_layout = QVBoxLayout(stats_container)
        stats_outer_layout.setContentsMargins(15, 12, 15, 12)
        
        stats_title = QLabel("Quick Posture Stats")
        stats_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #708599; border: none; padding-bottom: 5px;")
        stats_outer_layout.addWidget(stats_title)

        stats_grid_layout = QHBoxLayout()
        stats_grid_layout.setSpacing(12)

        self.total_analyzed_lbl, card_tot = self.create_stat_card("Total Analyzed", "12,458", "Log entries", "#13273F", "#1D3B61", "#3B82F6")
        self.normal_events_lbl, card_norm = self.create_stat_card("Normal Events", "7,234", "58.0% of total", "#0E3326", "#144D39", "#10B981")
        self.potential_threats_lbl, card_thr = self.create_stat_card("Potential Threats", "2,123", "17.0% risk", "#3D2A0F", "#5C3E14", "#F59E0B")
        self.critical_events_lbl, card_crit = self.create_stat_card("Critical Events", "1,225", "9.9% action", "#3D1418", "#5C1E24", "#EF4444")

        stats_grid_layout.addWidget(card_tot)
        stats_grid_layout.addWidget(card_norm)
        stats_grid_layout.addWidget(card_thr)
        stats_grid_layout.addWidget(card_crit)

        stats_outer_layout.addLayout(stats_grid_layout)
        main_layout.addWidget(stats_container, stretch=1)

        # 2. MIDDLE SECTION: DATA MATRIX WRAPPER GRID
        matrix_grid_layout = QHBoxLayout()
        matrix_grid_layout.setSpacing(15)

        # Left Split Container: Top Attack Types Panel
        attack_frame = QFrame()
        attack_frame.setStyleSheet("background-color: #0E1E31; border: 0.5px solid #3B82F6; border-radius: 8px;")
        attack_layout = QVBoxLayout(attack_frame)
        attack_layout.setContentsMargins(15, 12, 15, 12)
        
        attack_title = QLabel("Top Attack Types")
        attack_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #708599; border: none; padding-bottom: 6px;")
        attack_layout.addWidget(attack_title)

        attacks = [
            ("Failed Login Attempts", "3,456 (27.7%)", "#EF4444"),
            ("Access Denied", "2,145 (17.2%)", "#F59E0B"),
            ("Brute Force Attacks", "1,876 (15.1%)", "#A855F7"),
            ("Privilege Escalation", "1,234 (9.9%)", "#3B82F6")
        ]
        for name, count, accent_clr in attacks:
            row_w = QWidget()
            row_w.setStyleSheet("background: transparent; border: none;")
            row_lay = QHBoxLayout(row_w)
            row_lay.setContentsMargins(0, 4, 0, 4)
            
            bullet = QLabel("●")
            bullet.setStyleSheet(f"color: {accent_clr}; font-size: 11px; background: transparent;")
            lbl_name = QLabel(name)
            lbl_name.setStyleSheet("font-size: 12px; color: #E5E7EB; background: transparent;")
            lbl_count = QLabel(count)
            lbl_count.setStyleSheet("font-size: 12px; color: #9CA3AF; font-weight: bold; background: transparent;")
            
            row_lay.addWidget(bullet)
            row_lay.addWidget(lbl_name)
            row_lay.addStretch()
            row_lay.addWidget(lbl_count)
            attack_layout.addWidget(row_w)

            if "Failed" in name: self.failed_attack_lbl = lbl_count
            elif "Brute" in name: self.brute_attack_lbl = lbl_count
            
        attack_layout.addStretch()
        matrix_grid_layout.addWidget(attack_frame, stretch=1)

        # Right Split Container: Top Source IPs Table
        ip_frame = QFrame()
        ip_frame.setStyleSheet("background-color: #0E1E31; border: 0.5px solid #3B82F6; border-radius: 8px;")
        ip_layout = QVBoxLayout(ip_frame)
        ip_layout.setContentsMargins(15, 12, 15, 12)

        ip_title = QLabel("Top Source IPs")
        ip_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #708599; border: none; padding-bottom: 6px;")
        ip_layout.addWidget(ip_title)

        self.ip_table = QTableWidget()
        self.ip_table.setColumnCount(3)
        self.ip_table.setHorizontalHeaderLabels(["IP Address", "Events", "Risk"])
        self.ip_table.verticalHeader().setVisible(False)
        self.ip_table.setShowGrid(False)
        self.ip_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ip_table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 12px;
            }
            QTableWidget::item {
                border-bottom: 1px solid #14253D;
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #12253F;
                color: #708599;
                font-weight: bold;
                border: none;
                font-size: 10px;
                padding: 4px;
            }
        """)
        
        ip_header = self.ip_table.horizontalHeader()
        ip_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        ip_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        ip_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        mock_ips = [
            ("192.168.1.15", "892", "High", "#EF4444"),
            ("201.0.145.56", "756", "Medium", "#F59E0B"),
            ("203.0.113.45", "623", "Medium", "#F59E0B"),
            ("198.51.100.23", "512", "Low", "#10B981")
        ]
        
        self.ip_table.setRowCount(len(mock_ips))
        for row_idx, (ip, ev, risk, r_color) in enumerate(mock_ips):
            self.ip_table.setItem(row_idx, 0, QTableWidgetItem(ip))
            self.ip_table.setItem(row_idx, 1, QTableWidgetItem(ev))
            
            risk_item = QTableWidgetItem(risk)
            risk_item.setForeground(QColor(r_color))
            risk_item.setFont(QFont("Segoe UI", weight=QFont.Weight.Bold))
            self.ip_table.setItem(row_idx, 2, risk_item)

        ip_layout.addWidget(self.ip_table)
        matrix_grid_layout.addWidget(ip_frame, stretch=1)

        main_layout.addLayout(matrix_grid_layout, stretch=2)

        # 3. BOTTOM SECTION: INTEGRATED RECOMMENDATIONS PANEL
        rec_frame = QFrame()
        rec_frame.setStyleSheet("background-color: #0E1E31; border: 0.5px solid #3B82F6; border-radius: 8px;")
        rec_layout = QVBoxLayout(rec_frame)
        rec_layout.setContentsMargins(15, 12, 15, 12)

        rec_title = QLabel("Security Action Recommendations")
        rec_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #708599; border: none; padding-bottom: 5px;")
        rec_layout.addWidget(rec_title)

        rec_items = [
            "Investigate multiple failed root login attempts registered from source node 192.168.1.15.",
            "Review inbound traffic spikes and port scan signatures on external network interfaces.",
            "Enforce absolute multi-factor authentication (MFA) rule updates across corporate admin roles."
        ]

        for text in rec_items:
            lbl_rec = QLabel(text)
            lbl_rec.setStyleSheet("font-size: 12px; color: #D1D5DB; border: none; padding: 2px 0;")
            rec_layout.addWidget(lbl_rec)

        main_layout.addWidget(rec_frame, stretch=1)

    def create_stat_card(self, title, val, sub, bg_color, border_color, text_color):
        """Memory-safe layout constructor tracking text handles directly."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 6px;
            }}
        """)
        card_vbox = QVBoxLayout(card)
        card_vbox.setContentsMargins(12, 10, 12, 10)
        card_vbox.setSpacing(2)

        lbl_title = QLabel(title, card)
        lbl_title.setStyleSheet("font-size: 11px; color: #9CA3AF; font-weight: bold; border: none; background: transparent;")
        
        lbl_val = QLabel(val, card)
        lbl_val.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {text_color}; border: none; background: transparent;")
        
        lbl_sub = QLabel(sub, card)
        lbl_sub.setStyleSheet("font-size: 10px; color: #9CA3AF; border: none; background: transparent;")

        card_vbox.addWidget(lbl_title)
        card_vbox.addWidget(lbl_val)
        card_vbox.addWidget(lbl_sub)
        
        return lbl_val, card

    def load_analysis_metrics(self, metrics_dict):
        """Accepts live data maps from the core dashboard pipeline without thread blocking."""
        try:
            total_logs = metrics_dict.get("total_entries", 0)
            failed_logins = metrics_dict.get("failed_logins", 0)
            suspicious = metrics_dict.get("suspicious_events", 0)
            
            critical = int(failed_logins * 0.4)
            potential = suspicious + (failed_logins - critical)
            normal = max(0, total_logs - (potential + critical))
            
            self.total_analyzed_lbl.setText(f"{total_logs:,}")
            self.normal_events_lbl.setText(f"{normal:,}")
            self.potential_threats_lbl.setText(f"{potential:,}")
            self.critical_events_lbl.setText(f"{critical:,}")
            
            if hasattr(self, 'failed_attack_lbl'):
                self.failed_attack_lbl.setText(f"{failed_logins:,} entries")
            if hasattr(self, 'brute_attack_lbl'):
                self.brute_attack_lbl.setText(f"{critical:,} matches")
                
            print("[Analysis] Structural metrics updated flawlessly.")
        except Exception as e:
            print(f"[Analysis] Stream connection updating failure: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    page = AnalysisPage()
    window.setCentralWidget(page)
    window.resize(1100, 620)
    window.show()
    sys.exit(app.exec())