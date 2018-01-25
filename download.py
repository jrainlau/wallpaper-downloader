from bs4 import BeautifulSoup
import requests
import sys

if len(sys.argv) != 4:
    print('3 arguments were required but only find ' + str(len(sys.argv) - 1) + '!')
    exit()

category = sys.argv[1]

try:
    page_start = [int(sys.argv[2])]
    page_end = int(sys.argv[3])
except:
    print('The second and third arguments must be a number but not a string!')
    exit()

PAGE_DOMAIN = 'http://wallpaperswide.com'
PAGE_URL = 'http://wallpaperswide.com/' + category + '-desktop-wallpapers/page/'

def visit_page(url):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }
    r = requests.get(url, headers = headers)
    r.encoding = 'utf-8'
    return BeautifulSoup(r.text, 'lxml')

def get_paper_link(page):
    links = page.select('#content > div > ul > li > div > div a')
    return [link.get('href') for link in links]

def download_wallpaper(link, index, total, callback):
    wallpaper_source = visit_page(PAGE_DOMAIN + link)
    wallpaper_size_links = wallpaper_source.select('#wallpaper-resolutions > a')
    size_list = [{
        'size': eval(link.get_text().replace('x', '*')),
        'name': link.get('href').replace('/download/', ''),
        'url': link.get('href')
    } for link in wallpaper_size_links]

    biggest_one = max(size_list, key = lambda item: item['size'])
    print('Downloading the ' + str(index + 1) + '/' + str(total) + ' wallpaper: ' + biggest_one['name'])
    result = requests.get(PAGE_DOMAIN + biggest_one['url'])

    if result.status_code == 200:
        open('wallpapers/' + biggest_one['name'], 'wb').write(result.content)

    if index + 1 == total:
        print('Download completed!\n\n')
        callback()

def start():
    if page_start[0] <= page_end:
        print('Preparing to download the ' + str(page_start[0])  + ' page of all the "' + category + '" wallpapers...')
        PAGE_SOURCE = visit_page(PAGE_URL + str(page_start[0]))
        WALLPAPER_LINKS = get_paper_link(PAGE_SOURCE)
        page_start[0] = page_start[0] + 1

        for index, link in enumerate(WALLPAPER_LINKS):
            download_wallpaper(link, index, len(WALLPAPER_LINKS), start)

if __name__ == '__main__':
     start()
