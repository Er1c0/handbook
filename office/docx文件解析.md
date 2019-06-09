# 需求场景

- 用户自己编辑docx文件，把需要替换的内容用符号标记，程序可以根据标记动态生成新的文件

解决方案：

- 可以借用docx自身特性，采用zip解压，修改替换后再打包生成新的docx文件

[How to zip a WordprocessingML folder into readable docx](https://stackoverflow.com/questions/1514052/how-to-zip-a-wordprocessingml-folder-into-readable-docx
)

对docx文件进行unzip再zip的过程
```
unzip -d unziped_docx a.docx
cd unziped_docx
zip -r ../a_out.docx unziped_docx
```

该方法针对xlsx也同样适用
```
unzip -d unziped_xlsx a.xlsx
cd unziped_xlsx
zip -r ../a_out.xlsx unziped_xlsx
```
