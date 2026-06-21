import sys
import uuid  # Generate crisp unique tracking session IDs
import sqlite3
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QScrollArea, QFileDialog, QListWidget, QFrame, 
                             QSplitter, QTextEdit, QListWidgetItem)
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QFont, QTextCursor, QKeyEvent
import qtawesome as qta

# Internal Architecture Engine Imports
from Chat.NexusChat import NexusAI
from rag.NexusDB import save_chat_turn, DB_PATH  


class ChatWindow(QMainWindow):
    def __init__(self, username="Master"):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"NexusAI Workstation - Logged in as {self.username}")
        self.setMinimumSize(1000, 700)
        
        # Track live session mapping connections to prevent duplicate sidebar row spawns
        self.session_data = {}
        
        # Initialize a distinct session sequence tracker for your message schema mapping
        self.current_session_id = str(uuid.uuid4())
        
        self.init_ui()
        
        # 🎯 Automatically restore historical records into the sidebar layout on startup
        self.load_past_sessions_from_db()

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
        brand_title = QLabel("NEXUSAI")
        brand_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; letter-spacing: 1px;")
        brand_layout.addWidget(sidebar_logo)
        brand_layout.addWidget(brand_title)
        brand_layout.addStretch()
        sidebar_layout.addLayout(brand_layout)
        
        # File Upload Section (RAG Context Ingestion)
        rag_section_label = QLabel("Nexus Rag System")
        rag_section_label.setStyleSheet("font-size: 10px; font-weight: bold; color: #64748b; letter-spacing: 0.5px;")
        sidebar_layout.addWidget(rag_section_label)
        
        self.upload_btn = QPushButton(" Ingest Document")
        self.upload_btn.setIcon(qta.icon("fa5s.file-upload", color="#ffffff"))
        self.upload_btn.setMinimumHeight(40)
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.setObjectName("SidebarButton")
        self.upload_btn.clicked.connect(self.handle_file_upload)
        sidebar_layout.addWidget(self.upload_btn)
        
        # Dynamic uploaded document tracker list (Reduced Height)
        self.uploaded_files_list = QListWidget()
        self.uploaded_files_list.setObjectName("SidebarList")
        self.uploaded_files_list.setFixedHeight(115)  
        self.uploaded_files_list.setToolTip("No active document vectors loaded.")
        sidebar_layout.addWidget(self.uploaded_files_list)
        
        # Chat History Section
        history_section_label = QLabel("Chat History")
        history_section_label.setStyleSheet("font-size: 10px; font-weight: bold; color: #64748b; letter-spacing: 0.5px;")
        sidebar_layout.addWidget(history_section_label)
        
        self.new_chat_btn = QPushButton(" New Session")
        self.new_chat_btn.setIcon(qta.icon("fa5s.plus", color="#ffffff"))
        self.new_chat_btn.setMinimumHeight(40)
        self.new_chat_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_chat_btn.setObjectName("SidebarButton")
        self.new_chat_btn.clicked.connect(self.handle_new_session)
        sidebar_layout.addWidget(self.new_chat_btn)
        
        # Expanded Chat History View Panel
        self.history_list = QListWidget()
        self.history_list.setObjectName("SidebarList")
        self.history_list.itemClicked.connect(self.handle_history_item_clicked)
        sidebar_layout.addWidget(self.history_list)
        
        # --- MAIN CHAT PANEL ---
        main_chat_area = QFrame()
        main_chat_area.setObjectName("MainChatArea")
        chat_layout = QVBoxLayout(main_chat_area)
        chat_layout.setContentsMargins(25, 20, 25, 20)
        
        # --- WORKSPACE STATUS BANNER TOP BAR ---
        top_bar = QHBoxLayout()
        
        top_logo = QLabel()
        top_logo.setPixmap(qta.icon("fa5s.brain", color="#3b82f6").pixmap(24, 24))
        
        self.session_title = QLabel("NEXUSAI")
        self.session_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; letter-spacing: 1px;")
        
        top_bar.addWidget(top_logo)
        top_bar.addWidget(self.session_title)
        top_bar.addStretch()
        
        self.engine_badge = QLabel("Qwen-2.5-3B [LLM]")
        self.engine_badge.setStyleSheet("background-color: #1e293b; color: #10b981; border: 1px solid #334155; border-radius: 4px; padding: 4px 8px; font-size: 11px; font-weight: bold;")
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
        
        # --- GEMINI-STYLE CENTRAL WELCOME LABEL OVERLAY FRAME ---
        self.welcome_container = QFrame(self.scroll_content)
        self.welcome_container.setObjectName("WelcomeContainer")
        
        welcome_layout = QVBoxLayout(self.welcome_container)
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.setContentsMargins(0, 0, 0, 0)
        welcome_layout.setSpacing(15)
        
        welcome_layout.addStretch(1)
        
        center_brand_layout = QHBoxLayout()
        center_brand_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_brand_layout.setSpacing(16)
        
        center_logo = QLabel()
        center_logo.setPixmap(qta.icon("fa5s.brain", color="#3b82f6").pixmap(48, 48))
        center_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.welcome_brand = QLabel("NEXUSAI")
        self.welcome_brand.setStyleSheet("font-size: 44px; font-weight: 800; color: #ffffff; letter-spacing: 2px;")
        self.welcome_brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        center_brand_layout.addWidget(center_logo, alignment=Qt.AlignmentFlag.AlignVCenter)
        center_brand_layout.addWidget(self.welcome_brand, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        self.welcome_subtitle = QLabel(f"Hello {self.username}")
        self.welcome_subtitle.setStyleSheet("font-size: 28px; font-weight: 600; color: #475569;")
        self.welcome_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        welcome_layout.addLayout(center_brand_layout)
        welcome_layout.addWidget(self.welcome_subtitle)
        
        welcome_layout.addStretch(1)
        
        self.feed_layout.addWidget(self.welcome_container)
        
        self.scroll_area.setWidget(self.scroll_content)
        chat_layout.addWidget(self.scroll_area)
        
        # --- GEMINI-STYLE COMPACT FOOTER INPUT TRAY ---
        gemini_input_bar = QFrame()
        gemini_input_bar.setObjectName("NexusInputTray")
        gemini_layout = QHBoxLayout(gemini_input_bar)
        gemini_layout.setContentsMargins(14, 4, 8, 4)
        gemini_layout.setSpacing(10)
        
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Ask NexusAI...")
        self.prompt_input.setMinimumHeight(60)
        self.prompt_input.setMaximumHeight(60)
        self.prompt_input.setObjectName("NexusPromptInput")
        
        self.prompt_input.installEventFilter(self)
        
        self.send_btn = QPushButton()
        self.send_btn.setIcon(qta.icon("fa5s.paper-plane", color="#ffffff"))
        self.send_btn.setFixedSize(32, 32)
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.setObjectName("NexusSendButton")
        self.send_btn.clicked.connect(self.handle_send_message)
        
        gemini_layout.addWidget(self.prompt_input)
        gemini_layout.addWidget(self.send_btn)
        
        input_alignment_wrapper = QHBoxLayout()
        input_alignment_wrapper.addStretch(1)
        input_alignment_wrapper.addWidget(gemini_input_bar, 4)
        input_alignment_wrapper.addStretch(1)
        chat_layout.addLayout(input_alignment_wrapper)
        
        main_splitter.addWidget(sidebar)
        main_splitter.addWidget(main_chat_area)
        main_splitter.setSizes([260, 1040])
        
        layout = QVBoxLayout(central_widget)
        layout.addWidget(main_splitter)
        layout.setContentsMargins(0, 0, 0, 0)

        self.is_first_message = True

    def load_past_sessions_from_db(self):
        """🎯 Reads older logged sessions out of SQLite on startup and renders them inside the sidebar panel layout."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Find the active tracking table name inside sqlite structure records
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            target_table = None
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table});")
                cols = [c[1] for c in cursor.fetchall()]
                if "session_id" in cols and "user_query" in cols:
                    target_table = table
                    break
                    
            if target_table:
                # Group entries by distinct session_id and grab the first query as the preview text label
                cursor.execute(f"""
                    SELECT session_id, user_query 
                    FROM {target_table} 
                    GROUP BY session_id 
                    ORDER BY id DESC
                """)
                past_sessions = cursor.fetchall()
                
                for session_id, first_query in past_sessions:
                    if session_id and session_id not in self.session_data:
                        self.add_session_to_sidebar(session_id, first_query)
            conn.close()
        except Exception as e:
            print(f"Startup history retrieval context info skip: {e}")

    def eventFilter(self, obj, event):
        if obj is self.prompt_input and event.type() == QEvent.Type.KeyPress:
            key_event = QKeyEvent(event)
            if key_event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and not (key_event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
                self.handle_send_message()
                return True
        return super().eventFilter(obj, event)

    def append_message(self, text, is_user=True):
        bubble_frame = QFrame()
        bubble_frame.setMinimumWidth(200)
        bubble_layout = QVBoxLayout(bubble_frame)
        bubble_layout.setContentsMargins(15, 12, 15, 12)
        
        sender_title = QLabel("YOU" if is_user else "NEXUSAI")
        sender_title.setStyleSheet(f"font-size: 10px; font-weight: 800; color: {'#3b82f6' if is_user else '#10b981'};")
        
        message_body = QLabel(text)
        message_body.setWordWrap(True)
        message_body.setStyleSheet("font-size: 14px; color: #f1f5f9; line-height: 140%;")
        message_body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        bubble_layout.addWidget(sender_title)
        bubble_layout.addWidget(message_body)
        
        if is_user:
            bubble_frame.setStyleSheet("background-color: #1e293b; border: 0px solid #334155; border-radius: 8px;")
        else:
            bubble_frame.setStyleSheet("background-color: #0f172a; border: 0px solid #1e293b; border-radius: 8px;")
            
        self.feed_layout.addWidget(bubble_frame)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def add_session_to_sidebar(self, session_id, preview_text):
        if len(preview_text) > 22:
            preview_text = preview_text[:22] + "..."
            
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(6, 2, 6, 2)
        row_layout.setSpacing(8)
        
        chat_label = QLabel(f"💬 {preview_text}")
        chat_label.setStyleSheet("color: #cbd5e1; font-size: 12px; background: transparent; border: none;")
        
        delete_btn = QPushButton()
        delete_btn.setFixedSize(20, 20)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setObjectName("DocumentRemoveButton")  
        delete_btn.setIcon(qta.icon("fa5s.trash-alt", color="#94a3b8"))
        delete_btn.setIconSize(QSize(10, 10))
        
        row_layout.addWidget(chat_label, 1)
        row_layout.addWidget(delete_btn, 0)
        
        list_item = QListWidgetItem(self.history_list)
        list_item.setSizeHint(QSize(0, 32))
        list_item.setData(Qt.ItemDataRole.UserRole, session_id)
        
        self.history_list.setItemWidget(list_item, row_widget)
        
        self.session_data[session_id] = {"item": list_item, "widget": row_widget}
        delete_btn.clicked.connect(lambda: self.handle_session_deletion(session_id))

    def handle_history_item_clicked(self, item):
        session_id = item.data(Qt.ItemDataRole.UserRole)
        if not session_id or session_id == self.current_session_id:
            return
            
        self._clear_chat_feed()
        
        self.current_session_id = session_id
        self.is_first_message = False
        
        turns = self._fetch_session_turns_from_db(session_id)
        
        for user_q, model_r in turns:
            self.append_message(user_q, is_user=True)
            self.append_message(model_r, is_user=False)

    def _fetch_session_turns_from_db(self, session_id):
        turns = []
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            target_table = None
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table});")
                cols = [c[1] for c in cursor.fetchall()]
                if "session_id" in cols and "user_query" in cols:
                    target_table = table
                    break
            
            if target_table:
                cursor.execute(
                    f"SELECT user_query, model_response FROM {target_table} WHERE session_id = ? ORDER BY id ASC", 
                    (session_id,)
                )
                turns = cursor.fetchall()
            conn.close()
        except Exception as e:
            print(f"Database lookups extraction skip context info trace: {e}")
        return turns

    def _clear_chat_feed(self):
        if hasattr(self, 'welcome_container') and self.welcome_container:
            try:
                self.welcome_container.hide()
                self.welcome_container.deleteLater()
            except:
                pass
        while self.feed_layout.count():
            item = self.feed_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def handle_session_deletion(self, session_id):
        if session_id in self.session_data:
            target_item = self.session_data[session_id]["item"]
            row_idx = self.history_list.row(target_item)
            if row_idx >= 0:
                self.history_list.takeItem(row_idx)
            del self.session_data[session_id]
            
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Non-critical database history sync cleanup skip: {e}")
            
        if self.current_session_id == session_id:
            self.handle_new_session()

    def handle_send_message(self):
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            return
            
        is_fresh_session_start = self.is_first_message
            
        if self.is_first_message:
            self._clear_chat_feed()
            self.is_first_message = False
            
        self.append_message(prompt, is_user=True)
        self.prompt_input.clear()
        
        NexusResponse = NexusAI(prompt) 
        self.append_message(f"{NexusResponse}", is_user=False)
        
        save_chat_turn(self.current_session_id, prompt, str(NexusResponse))
        
        if is_fresh_session_start and (self.current_session_id not in self.session_data):
            self.add_session_to_sidebar(self.current_session_id, prompt)

    def handle_new_session(self):
        self.current_session_id = str(uuid.uuid4())
        self.is_first_message = True
        
        self._clear_chat_feed()
                
        self.welcome_container = QFrame(self.scroll_content)
        self.welcome_container.setObjectName("WelcomeContainer")
        welcome_layout = QVBoxLayout(self.welcome_container)
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.setContentsMargins(0, 0, 0, 0)
        welcome_layout.setSpacing(15)
        welcome_layout.addStretch(1)
        
        center_brand_layout = QHBoxLayout()
        center_brand_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_brand_layout.setSpacing(16)
        center_logo = QLabel()
        center_logo.setPixmap(qta.icon("fa5s.brain", color="#3b82f6").pixmap(48, 48))
        self.welcome_brand = QLabel("NEXUSAI")
        self.welcome_brand.setStyleSheet("font-size: 44px; font-weight: 800; color: #ffffff; letter-spacing: 2px;")
        center_brand_layout.addWidget(center_logo)
        center_brand_layout.addWidget(self.welcome_brand)
        
        self.welcome_subtitle = QLabel(f"Hello {self.username}")
        self.welcome_subtitle.setStyleSheet("font-size: 28px; font-weight: 600; color: #475569;")
        self.welcome_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        welcome_layout.addLayout(center_brand_layout)
        welcome_layout.addWidget(self.welcome_subtitle)
        welcome_layout.addStretch(1)
        
        self.feed_layout.addWidget(self.welcome_container)

    def handle_file_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Your Document", "", "Documents (*.pdf *.txt *.md)"
        )
        if file_path:
            file_name = file_path.split("/")[-1]
            
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(6, 2, 6, 2)
            row_layout.setSpacing(8)
            
            doc_label = QLabel(f"📄 {file_name}")
            doc_label.setStyleSheet("color: #cbd5e1; font-size: 12px; background: transparent; border: none;")
            doc_label.setToolTip(file_name)
            
            remove_btn = QPushButton()
            remove_btn.setFixedSize(20, 20)
            remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            remove_btn.setObjectName("DocumentRemoveButton")
            remove_btn.setIcon(qta.icon("fa5s.times", color="#94a3b8"))
            remove_btn.setIconSize(QSize(10, 10))
            
            row_layout.addWidget(doc_label, 1)
            row_layout.addWidget(remove_btn, 0)
            
            list_item = QListWidgetItem(self.uploaded_files_list)
            list_item.setSizeHint(QSize(0, 32)) 
            
            self.uploaded_files_list.setItemWidget(list_item, row_widget)
            remove_btn.clicked.connect(lambda: self.handle_custom_widget_removal(list_item))

    def handle_custom_widget_removal(self, item):
        if item:
            row_idx = self.uploaded_files_list.row(item)
            if row_idx >= 0:
                self.uploaded_files_list.takeItem(row_idx)


# Workspace Native CSS Custom Theme Engine
CHAT_STYLING = """
    QMainWindow { background-color: #020617; }
    QFrame#SidebarFrame { background-color: #0b0f19; border-right: 1px solid #1e293b; }
    QFrame#MainChatArea { background-color: #020617; }
    QListWidget#SidebarList {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 6px;
        color: #94a3b8;
        padding: 5px;
    }
    QListWidget#SidebarList::item {
        padding: 4px;
        color: #cbd5e1;
        border-bottom: 1px solid #1e293b;
    }
    QListWidget#SidebarList::item:hover { background-color: #1e293b; border-radius: 4px; }
    
    QPushButton#DocumentRemoveButton {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
    }
    QPushButton#DocumentRemoveButton:hover {
        background-color: #ef4444;
        border: 1px solid #f87171;
    }

    QPushButton#SidebarButton {
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 6px;
    }
    QPushButton#SidebarButton:hover { background-color: #3b82f6; }

    QScrollArea#ChatScrollArea { border: none; background-color: transparent; }
    QWidget#ChatScrollContent { background-color: transparent; }
    
    QFrame#NexusInputTray {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 22px;
        max-width: 650px;
        max-height: 100px;
    }
    QTextEdit#NexusPromptInput {
        background-color: transparent;
        color: #f8fafc;
        border: none;
        font-size: 14px;
        padding-top: 18px;
    }
    QPushButton#NexusSendButton { background-color: #2563eb; border: none; border-radius: 16px; }
    QPushButton#NexusSendButton:hover { background-color: #3b82f6; }
    
    QScrollBar:vertical { border: none; background: #020617; width: 8px; margin: 0px; }
    QScrollBar::handle:vertical { background: #334155; min-height: 20px; border-radius: 4px; }
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(CHAT_STYLING)
    
    font = QFont("Sans-Serif", 10)
    app.setFont(font)
    
    window = ChatWindow("SHRI HARAN")
    window.show()
    sys.exit(app.exec())