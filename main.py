import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

# Import your native custom components
from Frontend.login import LoginWindow, STYLING_SHEET
from Frontend.chat_window import ChatWindow, CHAT_STYLING


class NexusAIApplication:
    def __init__(self):
        # 1. Initialize the global login screen
        self.login_win = LoginWindow()
        
        # Merge login stylesheet with chat window specifications seamlessly
        combined_styling = STYLING_SHEET + "\n" + CHAT_STYLING
        self.login_win.setStyleSheet(combined_styling)
        
        # 2. Bind the custom success pipeline signal to your runtime window switcher
        self.login_win.login_successful.connect(self.switch_to_chat_workspace)
        self.login_win.show()

    def switch_to_chat_workspace(self, username: str):
        """Safely clean up authentication context and initialize workspace stream."""
        # Cleanly capture identity parsing formats
        formatted_name = username.upper() if username == "shriharan" else "SHRI HARAN "
        
        # 3. Instantiate and present the primary operations panel
        self.chat_win = ChatWindow(username=formatted_name)
        
        # Connect the logout signal to our custom redirection method
        self.chat_win.logout_requested.connect(self.switch_to_login_screen)
        
        # Re-apply styling directly to the workstation framework object
        self.chat_win.setStyleSheet(STYLING_SHEET + "\n" + CHAT_STYLING)
        self.chat_win.show()
        
        # Hide the login screen instead of keeping it open
        self.login_win.hide()

    def switch_to_login_screen(self):
        """Safely tears down the active workspace and recovers the login frame."""
        if hasattr(self, 'chat_win') and self.chat_win:
            self.chat_win.hide()
            self.chat_win.deleteLater() # Cleanly dump workspace allocations
            
        # Re-clear login fields for fresh security input session
        self.login_win.username_input.clear()
        self.login_win.password_input.clear()
        self.login_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Establish default system typography engine layouts
    system_font = QFont("Sans-Serif", 10)
    app.setFont(system_font)
    
    # Fire up the unified pipeline
    nexus_app = NexusAIApplication()
    
    sys.exit(app.exec())