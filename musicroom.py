import requests
from lxml import html
from w3lib.html import remove_tags
import json

block=0
count=0
head="https://www.musicroom.com/"

def targetPage(url):

	global count
	count=count+1
	print("Page Number:",count)
	composerProductCountList=[]	

	response=requests.get(url)
	
	tree = html.fromstring(response.content)
	
	title="".join(tree.xpath('//h1/text()')).strip()

	
	details=tree.xpath('//tr//td[contains(@class ,"tblRight")]//span/text()')
	
	composer=','.join(tree.xpath('//tr//td//a[contains(@href, "composer")]/text()'))
	composerProducturl=tree.xpath('//tr//td//a[contains(@href, "composer")]/@href')
	for i in composerProducturl:
		par=head+i
		composerProductCountList.append(composorCount(par))
		
	composerProductCount=",".join(composerProductCountList)

	description="".join(tree.xpath('(//*[@class="controlProductDetailsDescriptionContainer"]/text())|//p//text()')).strip() 
	catlog_number="".join(details[-1]).strip()

	edition_number="".join(details[-2]).strip()
	
	if catlog_number is "":
		catlog_number="".join(details[-3]).strip()
		edition_number="".join(details[-4]).strip()

	print("**************************************************************************************************************************************")
	print("Title:",title,"Composer:",composer,"Composer Products:",composerProductCount,"Description:",description,"Edition Number:",edition_number,"Catlog Number:",catlog_number, sep="\n")
	print("**************************************************************************************************************************************")

	musicroom={"Title":title,"Composer":composer,"Composer Products":composerProductCount,"Description":description,"Edition Number":edition_number,"Catlog Number":catlog_number}
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
	
	for i in urllist:
		par=head+i
		print(par)
		targetPage(par)
		

	nexturl="".join(tree.xpath('//a[@id="ctl00_ctl00_ctl00_SiteContent_SiteContent_SiteContent_uxProducts_ProductBlocks_ctl26_ddPagerBottom_HyperLink3"]/@href'))

	
	print("////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
	if nexturl :
		par=head+nexturl
		print(par)
		nextPage(par)
	
		

def composorCount(url):

	response=requests.get(url)
	
	tree=html.fromstring(response.content)
	productCount= "".join(tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "lblNumberOfResults", " " ))]/text()')) 
	return productCount

nextPage('https://www.musicroom.com/productlist/piano+sheet+music+and+songbooks/piano-sheet-music-songbooks.aspx')
