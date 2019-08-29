 #                           ____        _   _ _ _   _     _     
 #     /\                   |  _ \      | \ | (_) | (_)   | |    
 #    /  \   _ __  _ __  ___| |_) |_   _|  \| |_| |_ _ ___| |__  
 #   / /\ \ | '_ \| '_ \/ __|  _ <| | | | . ` | | __| / __| '_ \ 
 #  / ____ \| |_) | |_) \__ \ |_) | |_| | |\  | | |_| \__ \ | | |
 # /_/    \_\ .__/| .__/|___/____/ \__, |_| \_|_|\__|_|___/_| |_|
 #          | |   | |               __/ |                        
 #          |_|   |_|              |___/                         
 #					
 #							SlideDown
 # 		fork me at : https://github.com/NitishGadangi/SlideDown
 #				Developed and Maintained by Nitish
 #



from bs4 import BeautifulSoup
import requests
import itertools
import threading
import time
import sys
import urllib.request
import img2pdf
import os

done = False
process = "loading "

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\r'+ process + c)
        sys.stdout.flush()
        time.sleep(0.1)

t = threading.Thread(target=animate)

def get_image_list(url):
	code=requests.get(url)
	soup=BeautifulSoup(code.text,"html.parser")
	print(f"Title: {soup.title.get_text()}")
	imgs=soup.find_all("img")
	img_urls=[]
	for temp_url in imgs:
		temp_link=temp_url.get("data-full")
		if temp_link is not None:
			img_urls.append(temp_link)
	return img_urls

def download_imgs(links):
	pg_no=1
	os.makedirs(".cache", exist_ok=True)
	all_files=[]
	for link in links:
		print(f"fetching (slide{pg_no})")
		file=f"slide{pg_no}.jpg"
		urllib.request.urlretrieve(link,".cache/"+file)
		all_files.append(".cache/"+file)
		pg_no=pg_no+1
	return all_files

def merge(all_files):
	output_name=input("\n\nEnter a name for file: ")
	with open(output_name+".pdf", "wb") as f:
		f.write(img2pdf.convert(all_files))
	for i in all_files:
		os.remove(i)

print("Paste any slideshare link below:")
main_link=input()
t.start()
all_urls=get_image_list(main_link)
if len(all_urls) is 0:
	print("Sorry no downloadable slides found...")
	done=True
else:
	print(f"Slides found: {len(all_urls)}")
	all_files=download_imgs(all_urls)
	done=True
	merge(all_files)
print("Done..")