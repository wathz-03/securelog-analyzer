import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QFrame, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Matplotlib integration for PyQt6 backend
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
        
        self.plot_trends()

    def plot_trends(self):
        self.ax.clear()
        
        # Timeline data points from the design mockup
        days = ['May 1', 'May 4', 'May 7', 'May 10', 'May 13', 'May 16', 'May 18']
        total_events = [700, 900, 750, 1600, 1000, 1500, 1100]
        success_logins = [400, 600, 500, 1100, 700, 1000, 800]
        failed_logins = [300, 300, 250, 500, 300, 500, 300]
        
        # Draw anti-aliased trend lines with distinct marker nodes matching your color scheme
        self.ax.plot(days, total_events, marker='o', markersize=4, color='#3B82F6', label='Total Events', linewidth=2)
        self.ax.plot(days, success_logins, marker='o', markersize=4, color='#10B981', label='Successful Logins', linewidth=2)
        self.ax.plot(days, failed_logins, marker='o', markersize=4, color='#EF4444', label='Failed Logins', linewidth=2)
        
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
        
        self.plot_distribution()

    def plot_distribution(self):
        self.ax.clear()
        
        # Data distributions matching your UI specifications
        labels = ['Failed Login (27.7%)', 'Access Denied (17.2%)', 'Brute Force (15.1%)', 'Login Success (14.8%)']
        sizes = [27.7, 17.2, 15.1, 14.8]
        colors = ['#EF4444', '#F59E0B', '#3B82F6', '#10B981']
        
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
        
        # Generate the 5 critical tracking parameters directly from the design schema
        stats_layout.addWidget(self.create_stat_card("Total Log Entries", "12,458", "#1E293B"))
        stats_layout.addWidget(self.create_stat_card("Successful Logins", "7,234", "#064E3B"))
        stats_layout.addWidget(self.create_stat_card("Failed Logins", "5,224", "#7F1D1D"))
        stats_layout.addWidget(self.create_stat_card("Unique IP Addresses", "1,248", "#3B0764"))
        stats_layout.addWidget(self.create_stat_card("Suspicious Events", "2,123", "#78350F"))
        
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
        line_frame.setPadding = lambda x: line_frame.setContentsMargins(x, x, x, x)

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

    def create_stat_card(self, title, value, bg_color):
        """Generates unified, low-profile stat metrics cards matching layout scales."""
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
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #9CA3AF; font-size: 13px; font-weight: 500; background: transparent;")
        
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet("color: white; font-size: 24px; font-weight: bold; background: transparent;")
        
        card_layout.addWidget(lbl_title)
        card_layout.addWidget(lbl_val)
        return card
    
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    preview_window = VisualizerPage()
    preview_window.setWindowTitle("SecureLog Analyzer - Visualizer Panel Preview")
    preview_window.resize(1100, 750)  
    preview_window.show()
    sys.exit(app.exec())