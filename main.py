import sys
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import simulate        # module của bạn chứa show_polygons_and_lines, animate_squares_along_paths
from mainwindow_ui import Ui_MainWindow  # file pyuic5 sinh ra
from matplotlib.animation import FuncAnimation
from process import handle_open_file, handle_close_file

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Thiết lập UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Tạo figure và canvas
        self.fig, self.ax = simulate.plt.subplots(figsize=(30, 18))
        simulate.show_polygons_and_lines(self.ax, simulate.polygons, simulate.lines)
        self.ax.set_aspect('equal')
        self.ax.autoscale(enable=True)
        self.ax.invert_yaxis()
        self.ax.axis('off')
        self.canvas = FigureCanvas(self.fig)

        # Đặt canvas vào sim_frame
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.ui.sim_frame.setLayout(layout)
        layout.addWidget(self.canvas)

        self.ui.open_bottom.clicked.connect(lambda: handle_open_file(self.ui))
        self.ui.close_bottom.clicked.connect(lambda: handle_close_file(self.ui))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec_())