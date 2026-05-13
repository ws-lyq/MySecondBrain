# Streamlit 快速入门

## 什么是 Streamlit
Streamlit 是一个开源的 Python 框架，用于快速构建数据应用和 AI 应用的 Web 界面。无需编写 HTML/CSS/JavaScript，纯 Python 即可构建交互式 UI。

## 安装
```bash
pip install streamlit
```

## 常用 API

### 文本元素
```python
st.title("标题")
st.header("一级标题")
st.subheader("二级标题")
st.markdown("支持 **Markdown** 语法")
st.write("万能输出函数")

# 带颜色的文本
st.success("成功消息")
st.info("提示消息")
st.warning("警告消息")
st.error("错误消息")
```

### 交互组件
```python
st.button("按钮")
st.text_input("文本输入")
st.text_area("多行文本")
st.selectbox("下拉选择", ["选项1", "选项2"])
st.slider("滑块", 0, 100, 50)
st.file_uploader("文件上传")
st.chat_input("聊天输入")  # 聊天专用
```

### 布局
```python
# 并列列
col1, col2 = st.columns(2)
col1.write("左列")
col2.write("右列")

# 侧边栏
st.sidebar.title("侧边栏标题")

# 可折叠区域
with st.expander("点击展开"):
    st.write("隐藏的内容")

# 标签页
tab1, tab2 = st.tabs(["标签1", "标签2"])
```

### 状态与缓存
```python
# 跨重绘保持状态
if "count" not in st.session_state:
    st.session_state.count = 0

# 缓存计算结果
@st.cache_data
def expensive_function():
    return compute_something()

# 运行方式
# streamlit run app.py
```
