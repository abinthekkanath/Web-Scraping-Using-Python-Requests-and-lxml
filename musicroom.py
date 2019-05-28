import requests
from lxml import html
from w3lib.html import remove_tags
import json

block=0

def targetPage(url):

	
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
	response=requests.get(url)
	
	tree=html.fromstring(response.content)
	
	urllist=tree.xpath('//a[@class="pbTitle"]/@product-url')
	
	head="https://www.musicroom.com/"
	
	count=0
	
	print(count)
	
	for i in urllist:
		par=head+i
		print(par)
		targetPage(par)
		count=count+1
		print(count)

	nexturl="".join(tree.xpath('//a[@id="ctl00_ctl00_ctl00_SiteContent_SiteContent_SiteContent_uxProducts_ProductBlocks_ctl26_ddPagerBottom_HyperLink3"]/@href'))
	
	head="https://www.musicroom.com/"
	
	if nexturl :
		par=head+nexturl
		print(par)
		print("////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
		nextPage(par)
		print("////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
		block=block+1
		print(block)

nextPage('https://www.musicroom.com/productlist/piano+sheet+music+and+songbooks/piano-sheet-music-songbooks.aspx')