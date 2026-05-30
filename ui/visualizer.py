import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QFrame, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker


class LogActivityChart(FigureCanvas):
    """
    Custom Matplotlib canvas rendering the multi-line trend graph for
    Log Activity Over Time matching the UI mockup constraints.
    """
    def __init__(self, parent=None):
        fig = Figure(figsize=(6, 4), facecolor='#071826')
        super().__init__(fig)
        self.ax = fig.add_subplot(111)
        self.ax.set_facecolor('#071826')
        
        self.plot_trends(0, 0, 0)

    def plot_trends(self, success=0, failed=0, total=0):
        self.ax.clear()
        
        # Timeline data points from the design mockup
        if total == 0:
            days = ['Baseline']
            total_events = [0]
            success_logins = [0]
            failed_logins = [0]
        else:
            days = ['T-2h', 'T-1h', 'Current Run']
            total_events = [int(total*0.3), int(total*0.6), total]
            success_logins = [int(success*0.2), int(success*0.5), success]
            failed_logins = [int(failed*0.4), int(failed*0.8), failed]
        
        # Draw anti-aliased trend lines with distinct marker nodes matching your color scheme
        self.ax.plot(days, total_events, marker='o', markersize=5, color='#3B82F6', label='Total Events', linewidth=2)
        self.ax.plot(days, success_logins, marker='o', markersize=5, color='#10B981', label='Successful Logins', linewidth=2)
        self.ax.plot(days, failed_logins, marker='o', markersize=5, color='#EF4444', label='Failed Logins', linewidth=2)
        
        # Structural boundary cleanup (Removing top/right borders for a clean modern flat look)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#374151')
        self.ax.spines['bottom'].set_color('#374151')
        
        # Subtle horizontal gridlines
        self.ax.grid(True, linestyle='--', alpha=0.07, color='#FFFFFF', axis='y')
        self.ax.tick_params(colors='#9CA3AF', labelsize=9)
        
        # Style layout legend
        leg = self.ax.legend(facecolor='#1F2937', edgecolor='none', loc='upper left', framealpha=0.6)
        if leg:
            for text in leg.get_texts():
                text.set_color('white')
                text.set_fontsize(9)
            
        self.ax.set_title("Log Activity Over Time", color='white', fontsize=12, pad=15, loc='left', weight='bold')
        self.figure.tight_layout()
        self.draw()


class EventDistributionChart(FigureCanvas):
    """
    Custom Matplotlib canvas rendering the modern center-cut Donut chart
    representing structural categorical threat metric types.
    """
    def __init__(self, parent=None):
        fig = Figure(figsize=(4, 4), facecolor='#071826')
        super().__init__(fig)
        self.ax = fig.add_subplot(111)
        self.ax.set_facecolor('#071826')
        
        self.plot_distribution(0, 0)

    def plot_distribution(self, failed_logins=0, suspicious_events=0):
        self.ax.clear()
        
        # Data distributions matching your UI specifications
        if failed_logins == 0 and suspicious_events == 0:
            labels = ['No Anomalies Detected']
            sizes = [100]
            colors = ['#10B981']
        else:
            labels = [f'Failed Logins ({failed_logins})', f'Suspicious Events ({suspicious_events})']
            sizes = [failed_logins, suspicious_events] if (failed_logins + suspicious_events) > 0 else [1, 1]
            colors = ['#EF4444', '#F59E0B']
        
        # Build donut chart container rings using wedgeprops parameters
        wedges, texts = self.ax.pie(
            sizes, 
            labels=labels, 
            colors=colors, 
            startangle=140,
            textprops=dict(color='#9CA3AF', fontsize=9),
            wedgeprops=dict(width=0.35, edgecolor='#071826', linewidth=3)
        )
        
        self.ax.set_title("Event Type Distribution", color='white', fontsize=12, pad=15, loc='left', weight='bold')
        self.figure.tight_layout()
        self.draw()


class VisualizerPage(QWidget):
    """
    Main Visualizations Dashboard view widget to be wired into your
    QStackedWidget view controller framework.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Match securelog-analyzer core window hex color properties
        self.setStyleSheet("background-color: #071826; color: white; font-family: 'Segoe UI';")
        
        # Outer layout boundary
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        # Wrap everything in a clean scroll area so it behaves well on smaller laptop screens
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #071826; }")
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #071826;")
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(24)

        # PAGE HEADER BLOCK
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        
        page_title = QLabel("Visualizations")
        page_title.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        
        page_subtitle = QLabel("Explore interactive charts and graphs from your log data")
        page_subtitle.setStyleSheet("font-size: 14px; color: #9CA3AF;")
        
        header_layout.addWidget(page_title)
        header_layout.addWidget(page_subtitle)
        main_layout.addLayout(header_layout)

        # METRIC KPI SUMMARY ROW
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)

        # Capture the internal value label references fo dynamic dashboard
        self.lbl_total, card_total = self.create_stat_card("Total Log Entries", "0", "#1E293B")
        self.lbl_successful, card_success = self.create_stat_card("Successful Logins", "0", "#064E3B")
        self.lbl_failed, card_failed = self.create_stat_card("Failed Logins", "0", "#7F1D1D")
        self.lbl_ips, card_ips = self.create_stat_card("Unique IP Addresses", "0", "#3B0764")
        self.lbl_suspicious, card_suspicious = self.create_stat_card("Suspicious Events", "0", "#78350F")

        # Generate the 5 critical tracking parameters directly from the design schema
        stats_layout.addWidget(card_total)
        stats_layout.addWidget(card_success)
        stats_layout.addWidget(card_failed)
        stats_layout.addWidget(card_ips)
        stats_layout.addWidget(card_suspicious)
        
        main_layout.addLayout(stats_layout)

        # PRIMARY VISUALIZATION CHART WRAPPERS
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)

        # Wrapper card for Line Chart (60% horizontal distribution ratio)
        line_frame = QFrame()
        line_frame.setObjectName("chartFrame")
        line_frame.setStyleSheet("""
            QFrame#chartFrame {
                background-color: #071826; 
                border: 0.5px solid #3B82F6; 
                border-radius: 10px;
            }
        """)

        line_vbox = QVBoxLayout(line_frame)
        line_vbox.setContentsMargins(10, 10, 10, 10)
        self.line_canvas = LogActivityChart()
        line_vbox.addWidget(self.line_canvas)
        charts_layout.addWidget(line_frame, stretch=6)

        # Wrapper card for Donut Chart (40% horizontal distribution ratio)
        donut_frame = QFrame()
        donut_frame.setObjectName("donutFrame")
        donut_frame.setStyleSheet("""
            QFrame#donutFrame {
                background-color: #071826;
                border: 0.5px solid #3B82F6;
                border-radius: 10px;
            }
        """)
        donut_vbox = QVBoxLayout(donut_frame)
        donut_vbox.setContentsMargins(10, 10, 10, 10)
        self.donut_canvas = EventDistributionChart()
        donut_vbox.addWidget(self.donut_canvas)
        charts_layout.addWidget(donut_frame, stretch=4)

        main_layout.addLayout(charts_layout)
        
        # Assemble scroll interface structure
        scroll.setWidget(content_widget)
        outer_layout.addWidget(scroll)

    def render_metrics_charts(self, metrics_data):
        """Updates tracking labels and forces graphs to refresh"""
        self.lbl_total.setText(str(metrics_data.get("total_entries", "0")))
        self.lbl_successful.setText(str(metrics_data.get("success_logins", "0")))
        self.lbl_failed.setText(str(metrics_data.get("failed_logins", "0")))
        
        ips_data = metrics_data.get("unique_ips", 0)
        if isinstance(ips_data, (set, list)):
            self.lbl_ips.setText(str(len(ips_data)))
        else:
            self.lbl_ips.setText(str(ips_data))

        self.lbl_suspicious.setText(str(metrics_data.get("suspicious_events", "0")))

        success = metrics_data.get("success_logins", 0)
        failed = metrics_data.get("failed_logins", 0)
        total = metrics_data.get("total_entries", 0)
        suspicious = metrics_data.get("suspicious_events", 0)

        self.line_canvas.plot_trends(success, failed, total)
        self.donut_canvas.plot_distribution(failed, suspicious)

        print("[Visualizer] Live canvas update sequence executed successfully.")

    def create_stat_card(self, title, value, bg_color):
        """Generates functional stat cards returning both the update label and frame layout parent."""
        card = QFrame()
        card.setObjectName("cardFrame")
        card.setStyleSheet(f"""
            QFrame#cardFrame {{
                background-color: {bg_color};
                border: 0.5px solid #3B82F6;
                border-radius: 8px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(6)
        
        lbl_title = QLabel(title, card)
        lbl_title.setStyleSheet("color: #9CA3AF; font-size: 13px; font-weight: 500; background: transparent;")
        
        lbl_val = QLabel(value, card)
        lbl_val.setStyleSheet("color: white; font-size: 24px; font-weight: bold; background: transparent;")
        
        card_layout.addWidget(lbl_title)
        card_layout.addWidget(lbl_val)
        return lbl_val, card
    
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    preview_window = VisualizerPage()
    preview_window.setWindowTitle("SecureLog Analyzer - Visualizer Panel Preview")
    preview_window.resize(1100, 750)  
    preview_window.show()
    sys.exit(app.exec())