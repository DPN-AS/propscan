import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QFileDialog,
    QMessageBox,
)
import main


class MainWindow(QWidget):
    """Simple GUI for ordering properties by proximity."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Property Proximity Sorter")

        layout = QVBoxLayout()
        self.open_button = QPushButton("Open CSV...")
        self.open_button.clicked.connect(self.load_csv)
        layout.addWidget(self.open_button)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def load_csv(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV", "", "CSV Files (*.csv)"
        )
        if not path:
            return
        try:
            props = main.read_properties(path)
            ordered = main.order_properties(props)
            self.list_widget.clear()
            for prop in ordered:
                self.list_widget.addItem(prop.address)
        except Exception as e:  # pragma: no cover - GUI error handling
            QMessageBox.critical(self, "Error", str(e))


def main_gui(argv: list[str] | None = None) -> None:
    app = QApplication(argv or sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main_gui()
