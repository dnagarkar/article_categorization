from bs4 import BeautifulSoup
import urllib2,cookielib
import urllib2
import os, os.path
import sys

# def medium_search_result_links(url):
# 	hdr = {'User-Agent': 'Magic Browser', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

# 	req = urllib2.Request(url, None, hdr)
# 	response = urllib2.urlopen(req)
# 	the_page = response.read()

# 	soup = BeautifulSoup(the_page, "html.parser")
# 	soup.prettify()

# 	links = soup.find_all("a", href=True)

# 	print links.string

def parse_article(url, file_name):
	print "parsing"

	f = open(file_name, 'w')

	hdr = {'User-Agent': 'Magic Browser', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

	req = urllib2.Request(url, None, hdr)
	response = urllib2.urlopen(req)
	the_page = response.read()

	soup = BeautifulSoup(the_page, "html.parser")
	soup.prettify()

	body = soup.find_all("div", { "class" : "section-inner sectionLayout--insetColumn"})

	for i in range(0, len(body)):
		try:
			f.write(body[i].get_text(separator="\n").encode('utf-8'))
		except UnicodeEncodeError:
			f.write(body[i].get_text(separator="\n").encode('ISO-8859-2'))

	f.close()
	#print into the filename


def create_single_article_file_train(url, category):
	folders = os.listdir(os.getcwd())
	# print os.getcwd()
	if category in folders:
		# count how many files
		current_path = os.getcwd()
		os.chdir(current_path+ "/" + category)
		new_path = os.getcwd()
		# print os.getcwd()
		count = len([name for name in os.listdir('.') if os.path.isfile(name)])
		# print count
		#checking to see if DS_store files are being counted
		# if os.path.exists(new_path + "/.DS_store"):
		# 	count = count - 1
		#create new file
		file_name = os.getcwd() + "/" + category + str(count+1) + ".txt"
		# print file_name
		os.chdir(current_path)
		# print os.getcwd()

	else:
		#create new folder
		print os.getcwd()
		os.makedirs(category)
		current_path = os.getcwd()
		os.chdir(current_path + "/" + category)
		print os.getcwd()
		#create new file
		file_name = os.getcwd() + "/" + category + str(1) + ".txt"
		os.chdir(current_path)
		print os.getcwd()

	parse_article(url, file_name)
	#call parse_article on url and file

def create_test_file_from_list(filename):
	# current_path = os.getcwd()
	# os.chdir(current_path+ "/train")
	folders = os.listdir(os.getcwd())
	category = raw_input("Category of following articles: ")
	with open(filename) as f:
		for line in f:
			create_single_article_file_train(line, category)


def create_article_file_test(url):
	#goes into test folder
	current_path = os.getcwd()
	os.chdir(current_path + "/test_new/second_level")

	count = len([name for name in os.listdir('.') if os.path.isfile(name)])

	#checking to see if DS_store files are being counted
	new_path = os.getcwd()
	if os.path.exists(new_path + "/.DS_store"):
		count = count - 1

	#create new file
	file_name = "test" + str(count+1)

	#call parse_article on url and file
	parse_article(url, file_name)



##create a single parsed file for training given url and category
#url = raw_input("Url: ")
# category = raw_input("Category: ")
#create_single_article_file_train(url, category)

##create parsed files for training given a file with a list of urls (all must be in one category) and category
current_path = os.getcwd()
print current_path
os.chdir(current_path+ "/train")
filename= raw_input("filepath of file of links: ")
create_test_file_from_list(filename)

##create a single parsed file for testing given url
#url = raw_input("Url: ")
#create_article_file_test(url)





