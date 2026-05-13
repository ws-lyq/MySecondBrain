# Python 实用技巧

## 列表推导式
```python
# 传统写法
squares = []
for i in range(10):
    squares.append(i * i)

# 推导式
squares = [i * i for i in range(10)]
```

## 虚拟环境管理
```bash
# 创建虚拟环境
python -m venv venv

# 激活（Windows）
venv\Scripts\activate

# 导出依赖
pip freeze > requirements.txt
```

## 常用标准库
- `pathlib`：面向对象的文件路径操作
- `dataclasses`：简化数据类定义
- `functools`：高阶函数工具
- `itertools`：高效的迭代器工具
- `collections`：额外的容器数据类型

## 类型提示
```python
from typing import List, Optional

def process_items(items: List[str], prefix: Optional[str] = None) -> List[str]:
    if prefix:
        return [f"{prefix}{item}" for item in items]
    return items
```
