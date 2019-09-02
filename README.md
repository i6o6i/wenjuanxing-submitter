# wenjuanxing-submitter
可用于（批量）提交问卷星问卷。

## Requirements
* Python 3
* Requests
* Pillow
* OpenCV 3

```
pip3 install requests
pip3 install pillow
pip3 install opencv-python
```

## Usage
1. 在列表l中指定各个问题选项的权  
   如第一个问题第一个选项占`40%`,  
   第二个选项占`30%`,第三个`20%`,第四个`10%`  
   第二个问题是选择男或女(各占一半)  
   ```python
   l=[[4,3,2,1 ],
      [1,1]]
   ```
2. 改变`times`变量指定答题次数,验证码有时会识别错误,  
   正确率一般在10%左右(但机器人请求效率特别高,以量取胜)  
   如你想得到100份有效问卷，times要设为1000以上  

```
python3 wjx_submitter.py
```

## 备注
3. 谨慎使用，以免问卷星升级验证码 :)
