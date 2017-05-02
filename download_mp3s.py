import urllib2
import xml.etree.ElementTree as ET
import urllib2
import os

# http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python

def download_file(url):

    file_name = url.split('/')[-1]

    try:
        u = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print e.code
        print e.msg
        return

    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()
    print file_name


if __name__ == '__main__':

    url_feeds = "http://www.soundcities.com/global/xml.php"

    # sound data base
    sdb_file_name = "soundcities_feeds.xml"
    sdb = ET.parse(sdb_file_name).getroot()

    print "/////////////////////////////////////////////////////////////////"

    for snd in sdb.iter('snd'):

        if "motorbike" in snd.find('description').text or "motor bike" in snd.find('description').text:
            print snd.find('description').text
            print snd.find('file').text
            if not os.path.exists("motorbike"):
                os.makedirs("motorbike")
            os.chdir("motorbike")
            download_file(snd.find('file').text)
            os.chdir("..")

        if "horn" in snd.find('description').text:
            print snd.find('description').text
            print snd.find('file').text
            if not os.path.exists("horn"):
                os.makedirs("horn")
            os.chdir("horn")
            download_file(snd.find('file').text)
            os.chdir("..")

    print "/////////////////////////////////////////////////////////////////"

