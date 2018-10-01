#P76071200
#Chung-Yao Ma
#Course IR HW1
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


article_id = 30252254
text = ''
print("start")
for i in range(100):
    print(i)
    url = 'https://www.ncbi.nlm.nih.gov/pubmed/'+str(article_id)
    html = urllib.request.urlopen(url)
    soup_html = BeautifulSoup(html, "lxml")
    if soup_html is not None:
        text += soup_html.body.find('div', attrs={'class':'abstr'}).find('p').text

print(text)
f= open("eos_train.txt","w+")
f.write(text)
f.close()
