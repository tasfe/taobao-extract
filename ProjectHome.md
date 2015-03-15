<b>功能说明</b>：
<br>
该系统旨在为商品比价、管理提供数据源，利用Python模块从淘宝店铺抓取出商品数据并过滤出有用信息存入本地数据库或者Excel，使用多线程进行爬虫以及IO操作。<br>
<br><br>
<b>存放数据格式说明</b>:<br>
<br>
商品名称 ： 货号 ： 大小 ：颜色 : 库存量 ：价格 ：商品URL  ： 店铺URL<br>
<br><br>
<b>程序开发</b>：<br>
<br>1，开发环境：eric4, python2.6.2<br>
<br>2，使用了第三方类库： pyExcelerator, py2exe.<br>
<br>3, 使用多线程20个线程进行同时抽取。<br>
<br><br>
<b>使用说明</b>：<br>
<br>
1,如果你的机器没有安装VS2008，使用前请务必先安装VS运行库环境（vcredist_x86.exe）,也可到官网下载该补丁（下载地址：<a href='http://www.microsoft.com/downloads/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&DisplayLang=en）'>http://www.microsoft.com/downloads/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&amp;DisplayLang=en）</a>.<br>
<br><br>
2,安装完成后，请先在shop.txt文件中输入你所抓取的商铺地址,例如：<a href='http://shop33570871.taobao.com'>http://shop33570871.taobao.com</a> 可以输入多个商铺地址，每个地址单独一行,输入完成后保存并关闭该文件。<br>
<br><br>
3,抓取的数据存在当前目录下，每个店铺的信息以一个excel保存。<br>
<br><br>
4，若重新运行该程序，新抓取的数据会覆盖掉以前存在的当前目录下的数据，如需保存以前抓取的商铺所有商品信息，请保存该商铺excel文件到其它地方。<br>
<br><br>
5,该工具无需安装，主程序为taobao_crawl.exe，直接点击即可运行，其它均为辅助程序或数据文件。<br>
<br><br>

<b>未来想法</b>
<br>
1, 加入自然语言处理、机器学习部分。目前大部分提取信息特征靠人工识别完成，维护工作量较大。如果能让程序自动学习，然后识别出店铺商品的相关数据，则可以增强改程序的稳定性。<b>难度较大，但可以做，慢慢完善。</b>
<br><br>
2,增加用户界面部分，增强对用户交互的友好性。可以利用QT（PyQT）来完成，难度不大，但需要时间。<br>
<br><br>

联系方式<br>
QQ: <b>529026768</b><br>
E-Mail:<b><a href='mailto:meixiaor@gmail.com'>meixiaor@gmail.com</a>