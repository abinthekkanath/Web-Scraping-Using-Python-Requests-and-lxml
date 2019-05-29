import requests
from lxml import html
from w3lib.html import remove_tags
import json

block=0
count=0

def targetPage(url):

	global count
	count=count+1
			
	print("Item Count:",count)
	response=requests.get(url)
	
	tree = html.fromstring(response.content)
	
	title="".join(tree.xpath('//h1/text()')).strip()

	
	details=tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "lblProductAttributeValue", " " ))]/text()')
	
	composer=details[0]

	description="".join(tree.xpath('//p/text()|//*[contains(concat( " ", @class, " " ), concat( " ", "controlProductDetailsDescriptionContainer", " " ))]/text()')).strip()
	
	catlog_number="".join(details[-1]).strip()

	edition_number="".join(details[-2]).strip()
	
	if catlog_number is "":
		catlog_number="".join(details[-3]).strip()
		edition_number="".join(details[-4]).strip()

	print("**************************************************************************************************************************************")
	print("Title:",title,"Composer:",composer,"Description:",description,"Edition Number:",edition_number,"Catlog Number:",catlog_number, sep="\n")
	print("**************************************************************************************************************************************")

	musicroom={"Title":title,"Composer":composer,"Description":description,"Edition Number":edition_number,"Catlog Number":catlog_number}
	with open('musicroom.json', 'a+') as f:
		json.dump(musicroom, f, indent=2, ensure_ascii=False)

def nextPage(url):
	
	global block

	block=block+1
	print("Block Number:",block)
	print("////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")

	response=requests.get(url)
	
	tree=html.fromstring(response.content)
	
	urllist=tree.xpath('//a[@class="pbTitle"]/@product-url')
	
	head="https://www.musicroom.com/"
	
	
	
	
	for i in urllist:
		par=head+i
		print(par)
		targetPage(par)
		

	nexturl="".join(tree.xpath('//a[@id="ctl00_ctl00_ctl00_SiteContent_SiteContent_SiteContent_uxProducts_ProductBlocks_ctl26_ddPagerBottom_HyperLink3"]/@href'))
	
	head="https://www.musicroom.com/"
	
	print("////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
	if nexturl :
		par=head+nexturl
		print(par)
		nextPage(par)
	
		

nextPage('https://www.musicroom.com/productlist/piano+sheet+music+and+songbooks/piano-sheet-music-songbooks.aspx')
