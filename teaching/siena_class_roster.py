import requests 
#import BeautifulSoup
from bs4 import BeautifulSoup
import HTMLParser
from HTMLParser import HTMLParser
import sys
import os

# Open the file.
r = open(sys.argv[1])

if not os.path.isdir('Detail_Class_List_files'):
    os.rename('Detail Class List_files', 'Detail_Class_List_files')

# Try to parse the webpage by looking for the tables.
soup = BeautifulSoup(r)

print "\documentclass{article}"
print "\usepackage{graphicx}"
print "\usepackage{subfig}"

print "\hoffset=-1.50in"
print "\setlength{\\textwidth}{7.5in}"
print "\setlength{\\textheight}{9in}"
print "\setlength{\\voffset}{0pt}"
print "\setlength{\\topmargin}{0pt}"
print "\setlength{\headheight}{0pt}"
print "\setlength{\headsep}{0pt}"


h2s = soup.find_all('h2')
caption = 'Default'
for h in h2s:
    if h.string.find('Class Roster For')>=0:
        caption = h.string

tables = soup.find_all('table')

icount = 0
closed_figure = False
for table in tables:
    
    if table['class'][0]=='datadisplaytable':
       
        rows = table.findAll('tr')
        
        image = None
        name = None
        for row in rows:
            cols = row.findAll('td')
        
            for col in cols:
                
                img = col.findAll('img')
                
                a = col.findAll('a')
                #if len(a)>0:
                #    import pdb ; pdb.set_trace()
                
                if len(img)>0 and img[0]['src'].find('jpg')>=0:
                    image = img[0]['src']
                    image = image.replace(' ','_').replace('%20', '_')
                    if not os.path.isfile(image):
                        import pdb ; pdb.set_trace()
                    #if os.path.isfile(image):
                    #    import pdb ; pdb.set_trace()
                        
                if len(a)>0 and 'mailto' in a[0]['href']:
                    name = a[0]['target']
                #if len(a)>0 and a[0]['class']==['leftaligntext']:
                #    name = a[0].string
                #    print(image, a[0].string)
                #import pdb ; pdb.set_trace()

                if name is not None and image is not None:
                    if icount%25==0:
                        if icount > 0:
                            print "\\clearpage"
                        else:
                            print "\\begin{document}"
                        print "\\begin{figure}"
                        print "\centering"
                        closed_figure = False

                    if os.stat(image).st_size < 250:
                        #image = './file_not_found.jpg'
                        image = './smiley.png'

                    if icount%5==4:
                        print "\subfloat[%s]{\includegraphics[height=0.19\\textwidth]{%s}}\\\\" % (name,image)
                    else:
                        print "\subfloat[%s]{\includegraphics[height=0.19\\textwidth]{%s}}\\hfill" % (name,image)

                    image = None
                    name = None

                    if icount%25==24:
                        print "\caption{%s}" % (caption)
                        print "\end{figure}"
                        closed_figure = True

                    icount += 1
                    

if not closed_figure:
    print "\caption{%s}" % (caption)
    print "\end{figure}"
print "\end{document}"

