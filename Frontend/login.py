import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
import qtawesome as qta


class LoginWindow(QMainWindow):
    # Signal triggered on verified login success (passes username)
    login_successful = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("NexusAI 1.0")
        self.setMinimumSize(450, 550)
        self.init_ui()

    def init_ui(self):
        # Background / Central Widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 1. Main Glass-Style Card Container
        card_frame = QFrame()
        card_frame.setObjectName("CardFrame")
        card_frame.setFixedWidth(360)
        
        # Give the card a smooth drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 10)
        card_frame.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card_frame)
        card_layout.setSpacing(18)
        card_layout.setContentsMargins(30, 40, 30, 40)

        # 2. Header / Branding
        logo_label = QLabel()
        # Glowing terminal icon for NexusAI
        logo_label.setPixmap(qta.icon("fa5s.terminal", color="#3b82f6").pixmap(48, 48))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(logo_label)

        self.title_label = QLabel("NEXUSAI")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 26px; font-weight: 800; color: #ffffff; letter-spacing: 3px;")
        card_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel("SHRI HARAN B")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet("font-size: 10px; color:  #ffffff; font-weight: bold; letter-spacing: 5px;")
        card_layout.addWidget(self.subtitle_label)
        card_layout.addSpacing(10)

        # 3. Username Input Layout
        username_title = QLabel("Admin Name")
        username_title.setStyleSheet("font-size: 12px; font-weight: bold; color:  #ffffff;")
        card_layout.addWidget(username_title)

        username_container = QHBoxLayout()
        username_container.setSpacing(0)
        
        user_icon = QLabel()
        user_icon.setPixmap(qta.icon("fa5s.user", color="#64748b").pixmap(16, 16))
        user_icon.setStyleSheet("""
            QLabel {
                background-color: #0f172a; 
                border: 1px solid #334155; 
                border-right: none; 
                border-top-left-radius: 6px; 
                border-bottom-left-radius: 6px;
                min-height: 38px;
                max-height: 38px;
                padding: 0px 10px;
            }
        """)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Name")
        self.username_input.setStyleSheet("""
            QLineEdit { 
                border-top-left-radius: 0px; 
                border-bottom-left-radius: 0px; 
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                border: 1px solid #334155;
                min-height: 38px;
                max-height: 38px;
                padding: 0px 12px;
            }
        """)
        
        username_container.addWidget(user_icon)
        username_container.addWidget(self.username_input)
        card_layout.addLayout(username_container)

        # 4. Password Input Layout
        password_title = QLabel("Password")
        password_title.setStyleSheet("font-size: 12px; font-weight: bold; color:  #ffffff;")
        card_layout.addWidget(password_title)

        password_container = QHBoxLayout()
        password_container.setSpacing(0)
        
        lock_icon = QLabel()
        lock_icon.setPixmap(qta.icon("fa5s.lock", color="#64748b").pixmap(16, 16))
        lock_icon.setStyleSheet("""
            QLabel {
                background-color: #0f172a; 
                border: 1px solid #334155; 
                border-right: none; 
                border-top-left-radius: 6px; 
                border-bottom-left-radius: 6px;
                min-height: 38px;
                max-height: 38px;
                padding: 0px 10px;
            }
        """)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setStyleSheet("""
            QLineEdit { 
                border-radius: 0px; 
                border-top: 1px solid #334155; 
                border-bottom: 1px solid #334155; 
                border-left: none; 
                border-right: none; 
                min-height: 38px;
                max-height: 38px;
                padding: 0px 12px;
            }
        """)
        
        # Visibility Eye Toggle Button
        self.toggle_pass_btn = QPushButton()
        self.toggle_pass_btn.setIcon(qta.icon("fa5s.eye", color="#64748b"))
        self.toggle_pass_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_pass_btn.setCheckable(True)
        self.toggle_pass_btn.setStyleSheet("""
            QPushButton { 
                background-color: #0f172a; 
                border: 1px solid #334155; 
                border-left: none; 
                border-top-right-radius: 6px; 
                border-bottom-right-radius: 6px; 
                min-height: 38px;
                max-height: 38px;
                padding: 0px 12px;
            } 
            QPushButton:hover { 
                background-color: #1e293b; 
            }
        """)
        self.toggle_pass_btn.clicked.connect(self.toggle_password_visibility)

        password_container.addWidget(lock_icon)
        password_container.addWidget(self.password_input)
        password_container.addWidget(self.toggle_pass_btn)
        card_layout.addLayout(password_container)
        
        card_layout.addSpacing(15)

        # 5. Authentication Button
        self.login_button = QPushButton("LOGIN")
        self.login_button.setObjectName("LoginButton")
        self.login_button.setMinimumHeight(42)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Events
        self.login_button.clicked.connect(self.handle_verification)
        self.username_input.returnPressed.connect(self.handle_verification)
        self.password_input.returnPressed.connect(self.handle_verification)
        
        card_layout.addWidget(self.login_button)
        main_layout.addWidget(card_frame)

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_pass_btn.setIcon(qta.icon("fa5s.eye-slash", color="#3b82f6"))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_pass_btn.setIcon(qta.icon("fa5s.eye", color="#64748b"))

    def handle_verification(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        # Extraordinary Validation Alerts
        if not username and not password:
            self.show_custom_alert("Input Missing", "Security protocols require both Username and Password fields to be populated.", is_error=True)
            self.username_input.setFocus()
            return
        if not username:
            self.show_custom_alert("Identity Missing", "Please provide a valid Identity Credential username.", is_error=True)
            self.username_input.setFocus()
            return
        if not password:
            self.show_custom_alert("Security Block", "Password field cannot be empty. Enter cryptographic token.", is_error=True)
            self.password_input.setFocus()
            return

        # Core Check
        if username == "shriharanb" and password == "admin@666666":
            self.show_custom_alert("Access Authorized", f"Identity Decrypted. Welcome back, Master SHRI HARAN B.", is_error=False)
            self.login_successful.emit(username)
            self.close()
        else:
            self.show_custom_alert("Access Denied", "Signature Mismatch. Cryptographic authentication failed.", is_error=True)
            self.password_input.clear()
            self.password_input.setFocus()

    def show_custom_alert(self, title, text, is_error=True):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        if is_error:
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStyleSheet("QMessageBox { background-color: #0f172a; color: white; } QLabel { color: white; font-size: 13px; } QPushButton { background-color: #ef4444; color: white; border-radius: 4px; min-width: 80px; padding: 5px; font-weight: bold; }")
        else:
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStyleSheet("QMessageBox { background-color: #0f172a; color: white; } QLabel { color: white; font-size: 13px; } QPushButton { background-color: #10b981; color: white; border-radius: 4px; min-width: 80px; padding: 5px; font-weight: bold; }")
        msg.exec()


# Modern UI Styling Sheet Engine
STYLING_SHEET = """
    QMainWindow {
         background-color: rgba(30, 41, 59, 0.65);
    }
    QFrame#CardFrame {
        background-color: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.13);
        border-radius: 16px;
    }
    QLineEdit {
        background-color: #0f172a;
        color: #f8fafc;
        border: 1px solid #334155;
        font-size: 14px;
        selection-background-color: #3b82f6;
    }
    QLineEdit:focus {
        border: 1px solid #3b82f6;
    }
    QPushButton#LoginButton {
        background-color: #2563eb;
        color: #ffffff;
        font-weight: bold;
        font-size: 14px;
        letter-spacing: 1px;
        border: none;
        border-radius: 6px;
    }
    QPushButton#LoginButton:hover {
        background-color: #3b82f6;
    }
    QPushButton#LoginButton:pressed {
        background-color: #1d4ed8;
    }
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLING_SHEET)
    
    font = QFont("Sans-Serif", 10)
    app.setFont(font)
    
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())