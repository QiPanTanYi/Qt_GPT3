# Qt_GPT3
使用PyQt开发的ChatGPT 3 Api 接口接收极简版客户端，接口来源于https://github.com/chatanywhere/GPT_API_free

```python
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=" ",
    base_url=" " 
)
```

代码块中的api_key和base_url需要手动填写。

采用pyinstaller打包为exe文件👇

```shell
pyinstaller --onefile --noconsole GPT3.5.py
```

最后可以在pyinstaller的dict中找到对应的exe文件。



演示效果：

![演示](./image.jpg)