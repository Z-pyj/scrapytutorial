from scrapy.selector import Selector
import scrapy

# TODO: 官方文档：https://www.osgeo.cn/scrapy/topics/selectors.html
body = '<html><body><span>good</span></body></html>'
text1 = Selector(text=body).xpath('//span/text()').get()
text2 = Selector(text=body).css('span::text').extract_first()
print(text2)

sample = """<html>
 <head>
  <base href='http://example.com/' />
  <title>Example website</title>
 </head>
 <body>
  <div id='images'>
   <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
   <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
   <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
   <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
   <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
  </div>
 </body>
</html>"""

'''
根据W3C标准， CSS selectors 不支持选择文本节点或属性值。但是在Web抓取上下文中选择这些是非常重要的，以至于scrappy（parsel）实现了 non-standard pseudo-elements ：
1. 要选择文本节点，请使用 ::text
2. 要选择属性值，请使用 ::attr(name) 在哪里？ name 是要为其值的属性的名称
'''
# 如果只提取第一个匹配的元素，则可以调用选择器 .get() （或其别名） .extract_first() 常用于旧版本）：
reponse0 = Selector(text=sample).css('title::text').get()
# 要实际提取文本数据，必须调用选择器 .get() 或 .getall()
reponse1 = Selector(text=sample).css('title::text').getall()
# 作为捷径， .attrib 也可以直接在SelectorList上使用；它返回第一个匹配元素的属性：
reponse2 = Selector(text=sample).css('a').attrib['href']

print(reponse2)
# 获取属性值方法1
Selector(text=sample).css('a[href*=image]::attr(href)').getall()
# 获取属性值方法2
Selector(text=sample).xpath('//a[contains(@href, "image")]/img/@src').getall()
# 获取属性值方法3
Selector(text=sample).css('a[href*=image] img::attr(src)').getall()

# title::text 选择子代的子文本节点 <title> 元素
# *::text 选择当前选择器上下文的所有子代文本节点：
# foo::text 如果 foo 元素存在，但不包含文本（即文本为空）
# 这意味着 .css('foo::text').get() 即使元素存在，也无法返回“无”。使用 default='' 如果您总是想要字符串：
# a::attr(href) 选择 href 子链接的属性值