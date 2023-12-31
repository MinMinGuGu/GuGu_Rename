<div align="center">
    <img src="https://badgen.net/badge/Python/v3.11.2" alt="Python-v3.11.2"/>
    <p>
        可以按照一定规则来重命名文件(也支持文件夹)
    </p>
</div>

## 使用场景

### 剧集管理

方便plex、emby、jellyfin等影音管理软件检索文件元数据。

#### 约定

如果有一部动画《哥布林杀手》，那么它的文件树结构为:

```txt
哥布林杀手
└─S1
        S01E01.JP.ass.txt
        S01E01.mkv
        S01E01.SC.ass.txt
        S01E01.TC.ass.txt
        S01E02.JP.ass.txt
        S01E02.mkv
        S01E02.SC.ass
        S01E02.TC.ass
        S01E03.JP.ass
        S01E03.mkv
        S01E03.SC.ass.txt
        S01E03.TC.ass.txt
```

描述为: 影片名/季度/当前季度的集数。

如果存在字幕，在字幕文件名与影片文件名相同的情况下(不包含第一个.后开始的后缀域)，会与影片一起匹配更改。

### 批量文件重命名

可以按照正则表达式来捕获与排除要重命名的文件，通过设置`format`参数来进行自定义格式重命名。

**如果有多个同名但后缀名不同的文件，则无法使用批量重命名，因为这会造成命名重复冲突。**

### 其他场景

如果有支持自定义命令行的方式执行的程序，那就可以搭配使用。

## 命令帮助

可以通过`-h`或者`--help`来获取命令帮助说明。
