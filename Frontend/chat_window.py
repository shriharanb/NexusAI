import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QScrollArea, QFileDialog, QListWidget, QFrame, 
                             QSplitter, QTextEdit, QListWidgetItem)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QTextCursor
import qtawesome as qta


class ChatWindow(QMainWindow):
    def __init__(self, username="Master"):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"NexusAI Workstation - Logged in as {self.username}")
        self.setMinimumSize(1000, 700)
        self.init_ui()

    def init_ui(self):
        # Central baseline widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Splitter allows user to manually resize the sidebar width dynamically
        main_splitter = QSplitter(Qt.Orientation.Horizontal, central_widget)
        
        # --- LEFT SIDEBAR PANEL ---
        sidebar = QFrame()
        sidebar.setObjectName("SidebarFrame")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(12)
        
        # Branding Header inside Sidebar
        brand_layout = QHBoxLayout()
        sidebar_logo = QLabel()
        sidebar_logo.setPixmap(qta.icon("fa5s.brain", color="#3b82f6").pixmap(24, 24))
        brand_title = QLabel("NEXUS CORE")
        brand_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; letter-spacing: 1px;")
        brand_layout.addWidget(sidebar_logo)
        brand_layout.addWidget(brand_title)
        brand_layout.addStretch()
        sidebar_layout.addLayout(brand_layout)
        
        # File Upload Section (RAG Context Ingestion)
        rag_section_label = QLabel("DATA CONTEXT INGESTION")
        rag_section_label.setStyleSheet("font-size: 10px; font-weight: bold; color: #64748b; letter-spacing: 0.5px;")
        sidebar_layout.addWidget(rag_section_label)
        
        self.upload_btn = QPushButton(" Ingest Document (RAG)")
        self.upload_btn.setIcon(qta.icon("fa5s.file-upload", color="#ffffff"))
        self.upload_btn.setMinimumHeight(40)
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.setObjectName("SidebarButton")
        self.upload_btn.clicked.connect(self.handle_file_upload)
        sidebar_layout.addWidget(self.upload_btn)
        
        # Dynamic uploaded document tracker list (Reduced Height)
        self.uploaded_files_list = QListWidget()
        self.uploaded_files_list.setObjectName("SidebarList")
        self.uploaded_files_list.setFixedHeight(100)  # Constrained to maximize history viewing zone
        self.uploaded_files_list.setToolTip("No active document vectors loaded.")
        self.uploaded_files_list.itemClicked.connect(self.handle_file_removal)
        sidebar_layout.addWidget(self.uploaded_files_list)
        
        # Chat History Section
        history_section_label = QLabel("CONVERSATION REPOS")
        history_section_label.setStyleSheet("font-size: 10px; font-weight: bold; color: #64748b; letter-spacing: 0.5px;")
        sidebar_layout.addWidget(history_section_label)
        
        self.new_chat_btn = QPushButton(" New Session")
        self.new_chat_btn.setIcon(qta.icon("fa5s.plus", color="#ffffff"))
        self.new_chat_btn.setMinimumHeight(40)
        self.new_chat_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_chat_btn.setObjectName("SidebarButton") # Unified accent coloring matching upload actions
        sidebar_layout.addWidget(self.new_chat_btn)
        
        # Expanded Chat History View Panel
        self.history_list = QListWidget()
        self.history_list.setObjectName("SidebarList")
        self.history_list.addItems([
            "Session 01: Architecture Overview", 
            "Session 02: Model Diagnostic Logs",
            "Session 03: Vector Index Tuning",
            "Session 04: Production Verification Run"
        ])
        sidebar_layout.addWidget(self.history_list) # Takes remaining layout weight naturally
        
        # --- MAIN CHAT PANEL ---
        main_chat_area = QFrame()
        main_chat_area.setObjectName("MainChatArea")
        chat_layout = QVBoxLayout(main_chat_area)
        chat_layout.setContentsMargins(25, 20, 25, 20)
        
        # Workspace Status Banner Top Bar
        top_bar = QHBoxLayout()
        self.session_title = QLabel("Interactive Context Terminal")
        self.session_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        self.engine_badge = QLabel("Qwen-2.5-3B [Local]")
        self.engine_badge.setStyleSheet("background-color: #1e293b; color: #10b981; border: 1px solid #334155; border-radius: 4px; padding: 4px 8px; font-size: 11px; font-weight: bold;")
        top_bar.addWidget(self.session_title)
        top_bar.addStretch()
        top_bar.addWidget(self.engine_badge)
        chat_layout.addLayout(top_bar)
        
        # Chat History Message Feed Stream Container
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("ChatScrollArea")
        
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("ChatScrollContent")
        self.feed_layout = QVBoxLayout(self.scroll_content)
        self.feed_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.feed_layout.setSpacing(15)
        
        # Gemini-style Central Welcome Label Overlay Frame
        self.welcome_container = QFrame(self.scroll_content)
        self.welcome_container.setObjectName("WelcomeContainer")
        welcome_layout = QVBoxLayout(self.welcome_container)
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.setContentsMargins(0, 120, 0, 0)
        
        self.welcome_brand = QLabel("NEXUSAI")
        self.welcome_brand.setStyleSheet("font-size: 44px; font-weight: 800; color: #3b82f6; letter-spacing: 2px;")
        self.welcome_brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.welcome_subtitle = QLabel(f"Hii {self.username}")
        self.welcome_subtitle.setStyleSheet("font-size: 28px; font-weight: 600; color: #475569;")
        self.welcome_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        welcome_layout.addWidget(self.welcome_brand)
        welcome_layout.addWidget(self.welcome_subtitle)
        self.feed_layout.addWidget(self.welcome_container)
        
        self.scroll_area.setWidget(self.scroll_content)
        chat_layout.addWidget(self.scroll_area)
        
        # --- GEMINI-STYLE COMPACT FOOTER INPUT TRAY ---
        gemini_input_bar = QFrame()
        gemini_input_bar.setObjectName("GeminiInputTray")
        gemini_layout = QHBoxLayout(gemini_input_bar)
        gemini_layout.setContentsMargins(14, 4, 8, 4)
        gemini_layout.setSpacing(10)
        
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Ask NexusAI...")
        self.prompt_input.setMinimumHeight(40)
        self.prompt_input.setMaximumHeight(40)  # Stripped down layout tracking height
        self.prompt_input.setObjectName("GeminiPromptInput")
        
        self.send_btn = QPushButton()
        self.send_btn.setIcon(qta.icon("fa5s.paper-plane", color="#ffffff"))
        self.send_btn.setFixedSize(32, 32)  # Tiny, sharp action button
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.setObjectName("GeminiSendButton")
        self.send_btn.clicked.connect(self.handle_send_message)
        
        gemini_layout.addWidget(self.prompt_input)
        gemini_layout.addWidget(self.send_btn)
        
        # Center the compact input bar cleanly at the bottom
        input_alignment_wrapper = QHBoxLayout()
        input_alignment_wrapper.addStretch(1)
        input_alignment_wrapper.addWidget(gemini_input_bar, 4)  # Constraints width sprawl
        input_alignment_wrapper.addStretch(1)
        chat_layout.addLayout(input_alignment_wrapper)
        
        # Add layouts to main horizontal splitter engine
        main_splitter.addWidget(sidebar)
        main_splitter.addWidget(main_chat_area)
        main_splitter.setSizes([260, 740])
        
        layout = QVBoxLayout(central_widget)
        layout.addWidget(main_splitter)
        layout.setContentsMargins(0, 0, 0, 0)

        # Flag to monitor conversational state changes
        self.is_first_message = True

    def append_message(self, text, is_user=True):
        """Generates dynamic chat bubble interface objects injected down into the viewport layout stream"""
        bubble_frame = QFrame()
        bubble_layout = QVBoxLayout(bubble_frame)
        bubble_layout.setContentsMargins(15, 12, 15, 12)
        
        sender_title = QLabel("YOU" if is_user else "NEXUS AI")
        sender_title.setStyleSheet(f"font-size: 10px; font-weight: 800; color: {'#3b82f6' if is_user else '#10b981'};")
        
        message_body = QLabel(text)
        message_body.setWordWrap(True)
        message_body.setStyleSheet("font-size: 14px; color: #f1f5f9; line-height: 140%;")
        message_body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        bubble_layout.addWidget(sender_title)
        bubble_layout.addWidget(message_body)
        
        if is_user:
            bubble_frame.setStyleSheet("background-color: #1e293b; border: 1px solid #334155; border-radius: 8px;")
        else:
            bubble_frame.setStyleSheet("background-color: #0f172a; border: 1px solid #1e293b; border-radius: 8px;")
            
        self.feed_layout.addWidget(bubble_frame)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def handle_send_message(self):
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            return
            
        # Clear welcome elements immediately on initial query interaction
        if self.is_first_message:
            self.welcome_container.hide()
            self.welcome_container.deleteLater()
            self.is_first_message = False
            
        self.append_message(prompt, is_user=True)
        self.prompt_input.clear()
        
        # Local model verification loop response
        self.append_message(f"Processed request token receipt loop. Ready to map to Qwen logic.", is_user=False)

    def handle_file_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Knowledge Base Document", "", "Documents (*.pdf *.txt *.md *.csv)"
        )
        if file_path:
            file_name = file_path.split("/")[-1]
            # Formats item content cleanly with a trailing removal trigger label
            self.uploaded_files_list.addItem(f"📄 {file_name}   [X]")

    def handle_file_removal(self, item):
        """Allows direct vector removal actions by clicking an active element string row"""
        self.uploaded_files_list.takeItem(self.uploaded_files_list.row(item))


# Workspace Native CSS Custom Theme Engine
CHAT_STYLING = """
    QMainWindow {
        background-color: #020617;
    }
    QFrame#SidebarFrame {
        background-color: #0b0f19;
        border-right: 1px solid #1e293b;
    }
    QFrame#MainChatArea {
        background-color: #020617;
    }
    QListWidget#SidebarList {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 6px;
        color: #94a3b8;
        padding: 5px;
    }
    QListWidget#SidebarList::item {
        padding: 8px;
        color: #cbd5e1;
        border-bottom: 1px solid #1e293b;
    }
    QListWidget#SidebarList::item:hover {
        background-color: #1e293b;
        border-radius: 4px;
        color: #ef4444; /* Highlights color shifts to indicate deletion capability on file clicks */
    }
    QPushButton#SidebarButton {
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 6px;
    }
    QPushButton#SidebarButton:hover { background-color: #3b82f6; }

    QScrollArea#ChatScrollArea {
        border: none;
        background-color: transparent;
    }
    QWidget#ChatScrollContent {
        background-color: transparent;
    }
    
    /* Gemini Input Pill Architecture */
    QFrame#GeminiInputTray {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 22px;
        max-width: 650px;
    }
    QTextEdit#GeminiPromptInput {
        background-color: transparent;
        color: #f8fafc;
        border: none;
        font-size: 14px;
        padding-top: 8px;
    }
    QPushButton#GeminiSendButton {
        background-color: #2563eb;
        border: none;
        border-radius: 16px;
    }
    QPushButton#GeminiSendButton:hover { 
        background-color: #3b82f6; 
    }
    
    QScrollBar:vertical {
        border: none;
        background: #020617;
        width: 8px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #334155;
        min-height: 20px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical:hover {
        background: #475569;
    }
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(CHAT_STYLING)
    
    font = QFont("Sans-Serif", 10)
    app.setFont(font)
    
    window = ChatWindow("shri")
    window.show()
    sys.exit(app.exec())