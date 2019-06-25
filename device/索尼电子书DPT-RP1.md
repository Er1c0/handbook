# 准备开始
https://www.pro.sony.com.cn/cn/softDownload/productinfo/dpt/online/contents/TP0001690844.html
## 打开/关闭电源
- 打开电源
- 关闭电源：按3秒
- 进入/取消睡眠模式：按电源键，降低电池消耗
- 自动睡眠
## 关于电池
- 按主页按钮时，出现电池图标，可检查剩余电量
- 延长电池寿命
  - 长时间不使用时，关闭电源
  - 不能在不充电情况下闲置，否则会降低电池性能
  - 不使用电脑上的Digital Paper app时，关闭Wifi和蓝牙
## 安全
- 画面锁定，需要输入密码
- Felica设备解锁(`用不到`)
## 电子纸画面
![](https://www.pro.sony.com.cn/cn/softDownload/productinfo/dpt/online/contents/image/i0160_CS.png)
- 主页菜单（按主页按钮时）
  - 功能图标
  - 状态图标：NFC、Bluetooth、Wifi、电池


![](https://www.pro.sony.com.cn/cn/softDownload/productinfo/dpt/online/contents/image/i0170_CS.png)
- 文档画面(轻触文档画面的任意问题时打开，轻触工具栏之外区域关闭)
  - 快速访问列表
  - 页面位置指示：沿线条轻触可切换页面
  - 粘贴
  - 手写笔设置：颜色、粗细、橡皮擦大小
  - 放大
  - 搜索：文本内容或者手写标记
  - ![](https://www.pro.sony.com.cn/cn/softDownload/productinfo/dpt/online/contents/image/S0130.png)选项，根据情况显示可操作的菜单


# url-to-pdf
简直是一个神器啊！
[url-to-pdf-api](https://github.com/alvarcarto/url-to-pdf-api)

特点如下：

- 把任意URL和HTMl内容转换成PDF或者图片(PNG或者JPEG)
- 通过Puppeteer渲染，通过chrome生成的页面都能够转换为PDF
- 优雅的默认参数，所有参数都是可配置的
- 单页面应用也能支持。会等待所有的网络请求结束后再渲染。
- 轻松部署到Heroku，我们喜欢lambda 但是 一键部署Heroku
- 渲染懒加载元素(scrollPage选项)
- 支持x-api-key 授权(API_TOKENS 环境变量)

PDF可以通过多种方式生成，其中一种是将HTML+CSS内容转换为PDF。这个API就是这样做的



常用参数:

Parameter | Type | Default | Description
----------|------|---------|------------
url | string | - | URL to render as PDF. (required)
output | string | pdf | 定义输出格式: `pdf` or `screenshot`.
emulateScreenMedia | boolean | `true` | 当渲染pdf时模仿屏幕 `@media screen`.
ignoreHttpsErrors | boolean | `false` | 当导航到某个页面是是否忽略HTTPS错误.
scrollPage | boolean | `false` | 在渲染前滚动页面，以触发懒加载元素.
waitFor | number or string | - | 在渲染前等待的毫秒数，或者等待某个selector元素出现比如input.
attachmentName | string | - | 当设置该参数时， `content-disposition`参数被设置到headers，浏览器下载pdf而不是以内联方式打开.这个参数就是下载后保存的文件名.
viewport.width | number | `1600` | Viewport width.
viewport.height | number | `1200` | Viewport height.
viewport.deviceScaleFactor | number | `1` | Device scale factor (could be thought of as dpr).
viewport.isMobile | boolean | `false` | Whether the meta viewport tag is taken into account.
viewport.hasTouch | boolean | `false` | Specifies if viewport supports touch events.
viewport.isLandscape | boolean | `false` | Specifies if viewport is in landscape mode.
cookies[0][name] | string | - | Cookie name (required)
cookies[0][value] | string | - | Cookie value (required)
cookies[0][url] | string | - | Cookie url
cookies[0][domain] | string | - | Cookie domain
cookies[0][path] | string | - | Cookie path
cookies[0][expires] | number | - | Cookie expiry in unix time
cookies[0][httpOnly] | boolean | - | Cookie httpOnly
cookies[0][secure] | boolean | - | Cookie secure
cookies[0][sameSite] | string | - | `Strict` or `Lax`
goto.timeout | number | `30000` |  单位毫秒，最大导航时间，等于0时表示无超时.
goto.waitUntil | string | `networkidle` | 如何判断导航成功. 选项: `load`, `networkidle`. `load` = load时间触发后. `networkidle` = 网络事件处于空闲状态，空闲时间由 `goto.networkIdleTimeout`定义(单位毫秒).
goto.networkIdleInflight | number | `2` | 被视为“空闲”的最大飞行请求数量. 仅使用goto.waitUntil：'networkidle'参数时生效.
goto.networkIdleTimeout | number | `2000` | 在完成导航之前等待的超时市场(单位毫秒)。 仅在waitUntil：'networkidle'参数中生效.
pdf.scale | number | `1` | 网页呈现的比例.
pdf.printBackground | boolean | `false`| 打印背景图形.
pdf.displayHeaderFooter | boolean | `false` | 显示页眉和页脚.
pdf.headerTemplate | string | - | 在PDF的每页作为页眉使用的HTML模板. **目前Puppeteer基本上只支持单行文本，你必须使用pdf.margins + CSS来显示标题!** See https://github.com/alvarcarto/url-to-pdf-api/issues/77.
pdf.footerTemplate | string | - | 在PDF的每页作为页脚使用的HTML模板. **目前Puppeteer基本上只支持单行文本，你必须使用pdf.margins + CSS来显示标题!** See https://github.com/alvarcarto/url-to-pdf-api/issues/77.
pdf.landscape | boolean | `false` | 纸张方向.
pdf.pageRanges | string | - | 要打印的纸张范围，例如'1-5,8,11-13'。 默认为空字符串，表示打印所有页面.
pdf.format | string | `A4` | 纸张格式如A5\A3。 如果设置，则优先于宽度或高度选项.
pdf.width | string | - | 纸张宽度，接受标有单位的值，如100px.
pdf.height | string | - | 纸张高度，接受标有单位的值，如100px.
pdf.margin.top | string | - | 上边距，接受标有单位的值.
pdf.margin.right | string | - | 右边距，接受标有单位的值.
pdf.margin.bottom | string | - | 下边距，接受标有单位的值.
pdf.margin.left | string | - | 左边距，接受标有单位的值..
screenshot.fullPage | boolean | `true` | When true, takes a screenshot of the full scrollable page.
screenshot.type | string | `png` | Screenshot image type. Possible values: `png`, `jpeg`
screenshot.quality | number | - | The quality of the JPEG image, between 0-100. Only applies when `screenshot.type` is `jpeg`.
screenshot.omitBackground | boolean | `false` | Hides default white background and allows capturing screenshots with transparency.
screenshot.clip.x | number | - | Specifies x-coordinate of top-left corner of clipping region of the page.
screenshot.clip.y | number | - | Specifies y-coordinate of top-left corner of clipping region of the page.
screenshot.clip.width | number | - | Specifies width of clipping region of the page.
screenshot.clip.height | number | - | Specifies height of clipping region of the page.



## Puppeteer 操纵木偶的人
- [github puppeteer](https://github.com/GoogleChrome/puppeteer)
- [Puppeteer: 更友好的 Headless Chrome Node API](https://www.cnblogs.com/dolphinX/p/7715268.html) 
  
手工可以在浏览器上做的事情 Puppeteer 都能胜任

- 生成网页截图或者 PDF
- 爬取大量异步渲染内容的网页，基本就是人肉爬虫
- 模拟键盘输入、表单自动提交、UI 自动化测试