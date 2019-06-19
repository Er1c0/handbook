# 官方解释
OXML是由微软公司为Office 2007产品开发的技术规范，现已成为国际文档格式标准,于2006年12月成为ECMA标准。
[ooxml百度百科](https://baike.baidu.com/item/OOXML)
[Office Open XML维基百科](https://zh.wikipedia.org/wiki/Office_Open_XML)
[微软在Office Open XML夹了多少私货?](https://www.zhihu.com/question/39196478)
[OFFICE OPEN XML OVERVIEW](https://www.ecma-international.org/news/TC45_current_work/OpenXML%20White%20Paper.pdf)
[Standard ECMA-376 Office Open XML File Formats ](https://www.ecma-international.org/publications/standards/Ecma-376.htm)
# WordprocessingML
http://officeopenxml.com/WPcontentOverview.php

- w:p 段，包含多个w:r
- w:pPr 段格式
- w:r Runs are non-block content; they define regions of text that do not necessarily begin on a new line，子元素为：br、cr、drawing、noBreakHyphen
- w:drawing 图片对象

## w:r text 