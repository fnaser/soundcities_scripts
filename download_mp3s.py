import urllib2
import xml.etree.ElementTree as ET
import urllib2
import os
import subprocess

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


def download_and_convert(snd, name):
    tmp_url = snd.find('file').text

    print snd.find('description').text
    print tmp_url

    if not os.path.exists(name):
        os.makedirs(name)

    # get mp3
    os.chdir(name)
    download_file(tmp_url)

    # convert it to wav
    file_name = tmp_url[tmp_url.rfind('/')+1:tmp_url.rfind('.')]
    subprocess.call(['ffmpeg', '-i', name+"/"+file_name + '.mp3', name+"/"+file_name + '.wav'])


if __name__ == '__main__':

    url_feeds = "http://www.soundcities.com/global/xml.php"
    sdb_file_name = "soundcities_feeds.xml"
    download_dir = "/home/fnaser/Music/"

    sdb = ET.parse(sdb_file_name).getroot()

    print "/////////////////////////////////////////////////////////////////"

    for snd in sdb.iter('snd'):

        #if "motorbike" in snd.find('description').text or "motor bike" in snd.find('description').text:
        #    download_and_convert(snd, download_dir + "motorbike")

        #if "horn" in snd.find('description').text:
        #    download_and_convert(snd, download_dir + "horn")

        if "traffic" in snd.find('description').text:
            download_and_convert(snd, download_dir + "traffic")

    print "/////////////////////////////////////////////////////////////////"

