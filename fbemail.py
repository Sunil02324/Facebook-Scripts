import time
import urllib2
from bs4 import BeautifulSoup

start_time = time.time()
user_name_array=[]
def get_fb_username(id):
    try:        
        url=urllib2.urlopen('https://graph.facebook.com/'+str(id)).read()
        soup = BeautifulSoup(url)
        all_attr=soup.prettify()
        
                  
        if all_attr.find('username'):
            start_quote=all_attr.find('username')+10
            end_quote=all_attr.find('"',start_quote+1)
            user_name=all_attr[start_quote:end_quote+1].strip('"')+'@facebook.com'
            user_name_array.append(user_name)
            f = open("email2.txt","a")
            try:
                f.write (user_name + "\n")
                
            finally:
                f.close()
    except IOError:
        pass

for i in range(1,40,1):
    get_fb_username(i+1)
print user_name_array

end_time = time.time()
print("Elapsed time was %g minutes!" % ((end_time - start_time)/60))