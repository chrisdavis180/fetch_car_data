from urllib.request import Request, urlopen
import bs4 as bs
import requests
import re

base_url = 'https://www.thecarconnection.com'
img_base_url = 'images.hgmsites.net'

def fetch(page, addition=''):
    return bs.BeautifulSoup(urlopen(Request(page + addition,
                            headers={'User-Agent': 'Opera/9.80 (X11; Linux i686; Ub'
                                     'untu/14.10) Presto/2.12.388 Version/12.16'})).read(),
                                     'lxml')

def all_makes():
    all_makes_list = []
    print('Fetching all makes...')
    for div in fetch(base_url, "/new-cars").find_all("div", {"class": "menu-column"}):
      for a in div.find_all("a"):
        all_makes_list.append(a['href'])
    return all_makes_list

def model_list(listed):
    model_list = []
    print('Buliding model list...')
    for make in listed: 
        for div in fetch(base_url, make).find_all("div", {"class": "make"}):
            model_list.append(div.find_all("a")[0]['href'])
    print('All models have been fetched...')
    return model_list

def fetch_pic_urls(listed):
  list_of_pics = []
  print('Saving all image urls...')
  for car_url in listed:
    img_url_suffix_arr = re.findall('hug.+?_h.jpg', str(fetch(base_url, car_url)))

    for img in img_url_suffix_arr:
        image_url = img.split(':')[-1]
        image_url = image_url.replace("\/", '/').replace('//', '')
        if img_base_url in image_url:
        
            list_of_pics.append('https://' + image_url)
    print('Saved all image urls...')
  return list_of_pics

def dump_imgs_to_dir(image_urls):
  base_path = '/your/path/to/images/' # replace your img path here

  for image_url in image_urls:
    image_name = image_url.split('/')[-1]
    data = requests.get(image_url).content
    
    f = open(f"{base_path}{image_name}.jpg",'wb')
      
    # Storing the image data inside the data variable to the file
    f.write(data)
    f.close()

# makes_arr = all_makes()
# model_arr = model_list(makes_arr)
# saved_imgs = fetch_pic_urls(model_arr)
# dump_imgs_to_dir(saved_imgs)
