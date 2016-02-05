import urllib, urllib2

def getUrl():
    print 'Enter URL of image page: '
    url = raw_input()
    return url

def getPage(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return str(html)

def getStorePath():
    
    print 'Enter output filename: '
    filename = raw_input()
    l = [filename]
    return l 

def getImageUrl(page_source):
    before = '<meta property=\"og:image\" content=\"'
    pos=str(page_source).find(before)
    pos+=35
    image_link=''
    while page_source[pos]!='\"':
        image_link+=page_source[pos]
        pos+=1
    return image_link

def getImage(image_link):
    print image_link
    l=getStorePath()
    path= ''# Give the path to download the image here
    filename=l[0]
    TOTAL_PATH = path + filename + '.jpg'
    urllib.urlretrieve(image_link,TOTAL_PATH)
    
def main():
    getImage(getImageUrl(getPage(getUrl())))
    
if __name__ == '__main__':
    main()