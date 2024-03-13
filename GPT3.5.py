import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout
from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=" ",
    base_url=" " 
)


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.resize(800, 600)
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        layout.addWidget(self.text_display)
        hbox = QHBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.input_box.setFixedWidth(550)
        self.input_box.setFixedHeight(100)
        hbox.addWidget(self.input_box)
        submit_button = QPushButton("Submit")
        submit_button.setFixedSize(100, 100)
        submit_button.clicked.connect(self.submit_question)
        hbox.addWidget(submit_button)
        submit_button.clicked.connect(self.clear_input_box)
        layout.addLayout(hbox)
        self.text_display.append("======================================"
                                 "====输入  0  结束聊天===================="
                                 "==============")
        self.setLayout(layout)

    def clear_input_box(self):
        self.input_box.clear()

    def submit_question(self):
        ask = self.input_box.text()

        if ask == '0':
            self.text_display.append("结束任务")
            self.input_box.setDisabled(True)
            return

        messages = [{'role': 'user', 'content': ask}]
        completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        reply = completion.choices[0].message.content

        self.text_display.append("用户问：{}\n".format(ask))
        self.text_display.append("AI回答：{}\n".format(reply))
        self.text_display.append("========================================"
                                 "======================================="
                                 "=============")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("GPT3.5-turbo学习版（Tanz）")
    widget = ChatWidget()
    widget.show()
    sys.exit(app.exec_())
