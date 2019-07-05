# 阅读材料
- [Node.js+TypeScript写后端工具](https://juejin.im/post/5a8fff275188257a5a4cc7d9)

# 重要的开源库deno
[deno](https://github.com/denoland/deno)
是nodejs之父Ryan Dahl重新搞的轮子 https://www.quora.com/What-happened-to-Ryan-Dahl
[如何理解 Ryan Dahl 最近专访中的言论“Node 也许不是构建大型服务的最佳选择”？](https://www.zhihu.com/question/64968947)

**哲学:**

- 旨在为现代程序员提供高效，安全的脚本环境。
- 它将始终作为单个可执行文件分发-并且该可执行文件将是运行任何deno程序的足够软件。给定一个deno程序的URL，你应该能够用50兆字节的deno可执行文件执行它。
- 明确地承担了运行时和包管理器的角色。 它使用标准的浏览器兼容协议来加载模块：URL。
- 提供有关程序如何访问系统的安全保证，默认情况下是最严格的安全沙箱。
- 提供了一组经过审核（审核）的标准模块，可以保证与Deno一起使用

**目标:**

- 支持TypeScript开箱即用。
- 与浏览器一样，允许从URL导入：`import * as log from "https://deno.land/std/log/mod.ts";`;
- 远程代码在首次执行时被提取和缓存，只有使用`--reload`标志才会更新。
- 使用“ES模块”，不在支持`require`
- 可以控制文件系统和网络访问以运行沙箱代码。 V8（非特权）和Rust（特权）之间的访问只能通过此flatbuffer中定义的序列化消息完成。这使审计变得容易，例如，要启用写访问`--allow-write`或网络访问`--allow-net`。
- 只发送一个可执行文件。
- 永远死于未捕获的错误。
- 浏览器兼容：Deno程序的子集完全用JavaScript编写，不使用全局的Deno命名空间（或功能测试），也应该能够在现代Web浏览器中运行而无需更改。
- 支持顶级`await`。
- 能够有效地提供HTTP服务。(目前相对较慢）
- 提供开箱即用的有用工具：
    + 命令行调试器（还没有）
    + linter(还没有)
    + 依赖检查员（deno info）
    + 代码格式化程序（deno fmt），


**Non的目标**

- 没有package.json
- 没有npm
- 不与node明确兼容