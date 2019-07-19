
# 中文在vi中正常显示，但是cat显示乱码

[ubuntu 中文乱码 解决方法](http://blog.sina.com.cn/s/blog_976d93830101gz9x.html)
[ubuntu下的“用vim打开中文乱码，用cat打开正常显示”的解决方法](http://blog.csdn.net/nyist327/article/details/38873739)

[增加UBUNTU字符集 解决中文乱码问题](http://blog.sina.com.cn/s/blog_4cd5d2bb01014gyc.html),介绍了设置字符集的方法，但是不生效
## 问题说明
碰到一个奇怪问题，写java文件(Java8)，用vim编辑后，下面的中文可以正常显示。

```java
import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;


public class FileUtil {
    public static void main(String[] args) throws IOException {
        Path dir = Paths.get("./data/"+"测试");
        if(!Files.isDirectory(dir))Files.createDirectories(dir);//没有，则创建目录
        String fileName = dir.toFile().getAbsolutePath()+File.separatorChar+"目录信息.txt";
        Files.write(Paths.get(fileName), dir.toFile().toString().getBytes(StandardCharsets.UTF_8));//写目录信息
        Files.readAllLines(Paths.get(fileName), StandardCharsets.UTF_8).forEach(t -> System.out.println("newtest.txt:" + t));//读信息
    }
}
```
但是:
- 用cat和more，显示乱码
- 而且用javac ，提示编码异常

## 临时解决方法
cat和more乱码可以通过下面解决（[临时解决方法](http://blog.sina.com.cn/s/blog_976d93830101gz9x.html)）
```bash
cat FileUtil.java   | iconv -f GBK -t UTF-8
```

java编译时，可以要指定编码如下
```
javac -encoding GBK FileUtil.java
```

## vim保存时指定utf8格式

## VIM
vim的配置文件，在/etc/vim/vimrc，[参考](http://blog.csdn.net/nyist327/article/details/38873739)
vimrc脚本的注释是使用引号(")作行注释
Vim中有几个选项会影响对多字节编码的支持：

- `encoding（enc）`：encoding是Vim的内部使用编码，encoding的设置会影响Vim内部的Buffer、消息文字等。在 Unix环境下，encoding的默认设置等于locale；
- `fileencodings（fenc）`：Vim在打开文件时会根据fileencodings选项来识别文件编码，可以同时设置多个编码，Vim会根据设置的顺序来猜测所打开文件的编码。
- `fileencoding（fencs）` ：定义保存方式
    - 新建文件--》根据fileencoding设置
    - 已有文件--》根据打开文件时所识别的编码来保存，除非保存时重新设置fileencoding
- `termencodings（tenc）`：在终端环境下使用Vim时，通过termencoding项来告诉Vim终端所使用的编码。

Vim中的编码转换
Vim内部使用iconv库进行编码转换，如果这几个选项所设置的编码不一致，Vim就有可能会转换编码，所以经常会看到 __Vim提示[已转换]__.

- 打开文件：文件编码--》 encoding设置
- 终端环境：termencoding设置的--》encoding设置
- 保存文件：encoding设置--》fileencoding对应的编码

VIM内的几个命令
```
:help encoding-values 列出Vim支持的所有编码。
:set modifiable 否则会提示“提示 “不能修改，因为选项 "modifiable"是关的 ””
:set fileencoding=utf-8 另存为UTf-8编码
```

