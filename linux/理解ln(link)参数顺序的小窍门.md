linux的ln是建立软连接的常用方法，其命令参数如下:
```
usage: ln [-Ffhinsv] source_file [target_file]
       ln [-Ffhinsv] source_file ... target_dir
       link source_file target_file
```

那么问题来了，谁是source谁是target呢，我是经常搞混的，后来找到一个小窍门,按下面方式理解就再也不会搞反顺序了。
```
cp    existing_thing new_thing
ln -s existing_thing new_thing
```

关于这个命令的讨论还是很热烈的:
[I always forget the argument order of the `ln -s` command](https://news.ycombinator.com/item?id=1984456)