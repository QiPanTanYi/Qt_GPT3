import sys
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=" ",
    base_url=" "
)


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.resize(1000, 800)
        font = QFont("微软雅黑", 12)  # 设置字体为"微软雅黑"，大小为12
        self.text_display = QTextEdit()
        self.text_display.setFont(font)  # 应用设置的字体
        self.text_display.setReadOnly(True)
        layout.addWidget(self.text_display)
        hbox = QHBoxLayout()

        self.input_box = QTextEdit()

        self.input_box.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.input_box.setFixedWidth(830)
        self.input_box.setFixedHeight(150)
        self.input_box.setFont(font)
        self.input_box.setLineWrapMode(QTextEdit.WidgetWidth)
        self.input_box.installEventFilter(self)
        hbox.addWidget(self.input_box)
        submit_button = QPushButton("Submit")
        submit_button.setFixedSize(150, 150)
        submit_button.setFont(font)
        submit_button.clicked.connect(self.submit_question)
        hbox.addWidget(submit_button)
        submit_button.clicked.connect(self.clear_input_box)
        layout.addLayout(hbox)
        self.text_display.append(" ===========================输入  0  结束聊天=="
                                 "=====================")
        self.setLayout(layout)

    def clear_input_box(self):
        self.input_box.clear()

    def eventFilter(self, obj, event):
        if obj is self.input_box and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.submit_question()
                self.clear_input_box()
                return True
        return super().eventFilter(obj, event)

    def submit_question(self):
        ask = self.input_box.toPlainText()

        if ask == '0' or not ask:
            self.text_display.append("结束任务")
            self.input_box.setDisabled(True)
            return

        messages = [{'role': 'user', 'content': ask}]
        completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        reply = completion.choices[0].message.content

        self.text_display.append("😀：{}\n".format(ask))
        self.text_display.append("🤖：")
        self.display_reply(reply)

    def display_reply(self, reply):
        self.reply_to_show = reply
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_next_char)
        self.char_index = 0
        self.timer.start(10)    # 打字流式速度、毫秒

    def show_next_char(self):
        if self.char_index < len(self.reply_to_show):
            self.text_display.moveCursor(QTextCursor.End)
            self.text_display.insertPlainText(self.reply_to_show[self.char_index])
            self.char_index += 1
        else:
            self.timer.stop()
            self.text_display.append(" =============================="
                                     "================================")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("GPT3.5-turbo学习版（Tanz）")
    widget = ChatWidget()
    widget.show()
    sys.exit(app.exec_())
