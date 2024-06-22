import sys
import os

# 添加 src 目录到 sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 运行 myopencv 包
import myopencv
myopencv.main()
