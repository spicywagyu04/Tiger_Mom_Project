from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox,
    QTabWidget, QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QStyle,
    QDialog, QTextEdit
)
from PyQt5.QtCore import Qt, QUrl, QVariantAnimation, QEasingCurve
from PyQt5.QtGui import QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from worker import Worker
import os

class DistractionItemWidget(QWidget):
    def __init__(self, text, remove_callback):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)
        
        self.label = QLabel(text)
        self.label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(self.label)
        
        self.remove_button = QPushButton("✕")
        self.remove_button.setFixedSize(24, 24)
        self.remove_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                color: #e74c3c;
            }
            """
        )
        layout.addWidget(self.remove_button)
        
        self.setLayout(layout)
        self.remove_button.clicked.connect(remove_callback)

class PunishmentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kitten Punishment")
        self.setModal(True)

        self.paragraph = (
            "I am sorry to myself for getting distracted from my task. "
            "Getting distracted is counterproductive and hinders my progress. "
            "I should strive to maintain focus and avoid such distractions in the future."
        )

        layout = QVBoxLayout()
        instructions = QLabel("To dismiss this alert, you must type the following paragraph exactly:")
        layout.addWidget(instructions)
        
        paragraph_label = QLabel(self.paragraph)
        paragraph_label.setWordWrap(True)
        layout.addWidget(paragraph_label)
        
        self.input_edit = QTextEdit()
        self.input_edit.textChanged.connect(self.check_input)
        layout.addWidget(self.input_edit)
        
        self.setLayout(layout)

    def check_input(self):
        if self.input_edit.toPlainText() == self.paragraph:
            self.accept()

    def reject(self):
        # placeholder
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tiger Mom Agent")
        self.setFixedSize(350, 500)
        
        self.worker = None
        self.audio_player = None
        
        self.tabs = QTabWidget()
        
        # Focus Task Tab
        self.focus_tab = QWidget()
        self.init_focus_tab()
        self.tabs.addTab(self.focus_tab, "Focus Task")
        
        # Distractions Tab
        self.distraction_tab = QWidget()
        self.init_distraction_tab()
        self.tabs.addTab(self.distraction_tab, "Distractions")
        
        self.setCentralWidget(self.tabs)
        self.apply_styles()

    def init_focus_tab(self):
        """
        Positions the power button and focus task input using stretch items.
        The start button mimics a device power button UI.
        """
        focus_layout = QVBoxLayout()
        focus_layout.setContentsMargins(20, 20, 20, 20)
        focus_layout.setSpacing(30)

        focus_layout.addStretch(1)

        # Center the power button.
        button_hbox = QHBoxLayout()
        button_hbox.setAlignment(Qt.AlignCenter)
        
        self.start_button = QPushButton("⏻")
        self.start_button.setCheckable(True)
        self.start_button.setFixedSize(150, 150)
        self.start_button.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #7f8c8d, stop:1 #34495e);"
            "border-radius: 75px; color: white; font-size: 24px;"
        )
        self.start_button.clicked.connect(self.toggle_start)
        button_hbox.addWidget(self.start_button)
        focus_layout.addLayout(button_hbox)

        focus_layout.addSpacing(50)

        # Center the focus task input field.
        input_hbox = QHBoxLayout()
        input_hbox.setAlignment(Qt.AlignCenter)
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter your focus task here")
        self.task_input.setAlignment(Qt.AlignCenter)
        self.task_input.setFixedWidth(300)
        input_hbox.addWidget(self.task_input)
        focus_layout.addLayout(input_hbox)

        focus_layout.addStretch(1)

        self.focus_tab.setLayout(focus_layout)

    def toggle_start(self, checked):
        if checked:
            user_task = self.task_input.text().strip()
            if not user_task:
                QMessageBox.warning(self, "Input Error", "Please enter a focus task before starting.")
                self.start_button.setChecked(False)
                return

            distractions = [
                self.distraction_list.itemWidget(self.distraction_list.item(i)).label.text() 
                for i in range(self.distraction_list.count())
            ] if hasattr(self, 'distraction_list') else []

            self.worker = Worker(user_task, distractions)
            self.worker.alert_signal.connect(self.show_focus_popup)
            self.worker.finished.connect(self.worker_finished)
            self.worker.start()
            
            self.animate_button_color(self.start_button, QColor("#7f8c8d"), QColor("#2ecc71"))
            self.start_button.setText("⏻")
            self.task_input.setEnabled(False)
        else:
            if self.worker:
                self.worker.stop()
                self.worker = None
            
            self.animate_button_color(self.start_button, QColor("#2ecc71"), QColor("#7f8c8d"))
            self.start_button.setText("⏻")
            self.task_input.setEnabled(True)

    def animate_button_color(self, button, start_color, end_color):
        """Animates the background color of the given button from start_color to end_color."""
        self.animation = QVariantAnimation(
            button,
            startValue=start_color,
            endValue=end_color,
            duration=500,
            valueChanged=lambda value: button.setStyleSheet(
                f"background-color: {value.name()}; border-radius: {button.width()//2}px; color: white; font-size: 24px;"
            ),
            easingCurve=QEasingCurve.InOutCubic
        )
        self.animation.start()

    def init_distraction_tab(self):
        """Initializes the distraction tab."""
        self.distraction_input = QLineEdit()
        self.distraction_input.setPlaceholderText("Enter distraction to avoid here")
        
        # Modern, round add distraction button.
        self.add_distraction_button = QPushButton("+")
        self.add_distraction_button.setFixedSize(40, 40)
        self.add_distraction_button.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #3498db, stop:1 #2980b9);"
            "border-radius: 20px; color: white; font-size: 20px;"
        )
        self.add_distraction_button.clicked.connect(self.add_distraction)
        
        self.distraction_list = QListWidget()
        
        distraction_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.distraction_input)
        input_layout.addWidget(self.add_distraction_button)
        distraction_layout.addLayout(input_layout)
        distraction_layout.addWidget(self.distraction_list)
        self.distraction_tab.setLayout(distraction_layout)

    def add_distraction(self):
        text = self.distraction_input.text().strip()
        if text:
            list_item = QListWidgetItem()
            widget = DistractionItemWidget(text, lambda: self.remove_distraction(list_item))
            list_item.setSizeHint(widget.sizeHint())
            self.distraction_list.addItem(list_item)
            self.distraction_list.setItemWidget(list_item, widget)
            self.distraction_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a distraction before adding.")

    def remove_distraction(self, item):
        row = self.distraction_list.row(item)
        self.distraction_list.takeItem(row)

    def apply_styles(self):
        style_file = os.path.join(os.path.dirname(__file__), "style.qss")
        try:
            with open(style_file, "r") as file:
                style = file.read()
                self.setStyleSheet(style)
        except Exception as e:
            print(f"Error loading style file: {e}")

    def show_focus_popup(self, message):
        self.audio_player = QMediaPlayer()
        media_path = QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "media", "grumpy_kitty.mp3"))
        self.audio_player.setMedia(QMediaContent(media_path))
        self.audio_player.setVolume(50)
        self.audio_player.play()
        
        dialog = PunishmentDialog(self)
        dialog.exec_()
        self.audio_player.stop()
        self.audio_player = None

    def worker_finished(self):
        self.start_button.setChecked(False)
        self.start_button.setText("⏻")
        self.task_input.setEnabled(True)
