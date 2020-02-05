import exifread
import sys
import PIL
import hashlib
from PIL import Image
import os
import glob
import base64
import matplotlib.pyplot as plt
import folium
import folium.plugins
from folium.plugins import AntPath
from folium import IFrame
import io
from PIL import ImageFile
import datetime
from datetime import datetime
ImageFile.LOAD_TRUNCATED_IMAGES = True

files = []
dates = []

def openme(photo, mp, index):
	'''
	Opens a photo and plots the initial gps values to the createMap function using dmstodd to get the correct format of lat lon.
	'''
	global dates
	with open(photo,"rb") as p:
		tags = exifread.process_file(p)
		if (isgpsthere(tags,'GPS GPSLatitude')):
			print("GPS:" + str(dmstodd(tags.get('GPS GPSLatitude'), tags.get('GPS GPSLatitudeRef'))) + "," + str(dmstodd(tags.get('GPS GPSLongitude'), tags.get('GPS GPSLongitudeRef'))))
			createMap(mp,dmstodd(tags.get('GPS GPSLatitude'), tags.get('GPS GPSLatitudeRef')),dmstodd(tags.get('GPS GPSLongitude'), tags.get('GPS GPSLongitudeRef')),str(tags.get('EXIF DateTimeOriginal')), photo, index)
		else:
			print("No Exif GPS Data in " + str(photo))

def chrono(path):
	'''
	Sorts image dates into chronological order
	'''
	global dates
	with open(path,"rb") as p:
		tags = exifread.process_file(p)
		ds = str(tags.get('EXIF DateTimeOriginal')).split(" ")
		da = ds[0].split(":")
		time = ds[1]
		d = da[2]+"/"+da[1]+"/"+da[0]
		dt = d + " " + time
		dto = datetime.strptime(dt, '%d/%m/%Y %H:%M:%S')
		dates.append(dto)


def isgpsthere(tocheck,key):
	'''
	Checks if a key is in a tag. if not, returns false
	'''
	if key in tocheck:
		return True
	return False

def organise(index,filenames):
	'''
	Goes through the dates array in order using the index variable. then checks if the specified date with the index of the index variable matches
	any of the files dates.  if it is, its added to files in the correct chronological order.
	'''
	for filename in filenames:
		with open(filename,"rb") as p:
			tags = exifread.process_file(p)
			if (isgpsthere(tags,'EXIF DateTimeOriginal')):
				ds = str(tags.get('EXIF DateTimeOriginal')).split(" ")
				da = ds[0].split(":")
				time = ds[1]
				d = da[2]+"/"+da[1]+"/"+da[0]
				dt = d + " " + time
				dto = datetime.strptime(dt, '%d/%m/%Y %H:%M:%S')
				if(dto == dates[index]):
					print("match found")
					files.append([filename,dto])
			else:
				print("No Date Data in " + str(filename))

def addlines(mp):
	'''
	Using Folium's AntPath plugin, draws the timeline of the provided images using the data in files array
	'''
	internal =[]
	for ob in files:
		with open(ob[0],"rb") as p:
			tags = exifread.process_file(p)
			if (isgpsthere(tags,'GPS GPSLatitude')):
				latlon = [dmstodd(tags.get('GPS GPSLatitude'), tags.get('GPS GPSLatitudeRef')),dmstodd(tags.get('GPS GPSLongitude'), tags.get('GPS GPSLongitudeRef'))]
				internal.append(latlon)
	folium.plugins.AntPath(internal, color="red", weight=2.5, pulseColor="#ffb3b3", opacity=1, tooltip="Timeline Route").add_to(mp)
            

def createMap(mp,latitude, longitude, date, path, index):
	'''
	Takes 5 arguments corresponding to map data needed to plot markers on the map.  Converts the photo to a smaller resolution, then
	puts it into an IFrame by directly converting it to base64 within the Iframe's data. Presents the data alongside the image for better
	organisation. This is then added to a marker on the folium map
	'''

	sha = hashlib.sha512()
	md5 = hashlib.md5()
	with open(path, 'rb') as p:
		while True:
			picdata = p.read(65536)
			if not picdata:
				break
			sha.update(picdata)
			md5.update(picdata)
	op = io.BytesIO()
	img = Image.open(path)
	newimg = img.resize((500,500))
	newimg.save(op, format='JPEG')
	encoded = base64.b64encode(op.getvalue())
	ds = str(date).split(" ")
	da = ds[0].split(":")
	time = ds[1]
	daate = da[2]+"/"+da[1]+"/"+da[0] 
	y = '<html><body style="background:black;"><h3 style="text-align:center;color:white;">' + os.path.basename(path) + '</h3>' + '<div style="left:0px;"><img style="float:left;width:50%;height:75%;" src="data:image/jpeg;base64,{}"> ' + '<p style="background:black;color:white;text-align:center;display:inline-block; width:50%;word-wrap:break-word;">Date: ' + date + '<br>Time: ' + time + '<br> Lat: ' + str(latitude) + '<br>Long: ' + str(longitude) + '<br><br>SHA-512: ' + sha.hexdigest() + '<br><br>MD5: ' + md5.hexdigest() + '</p></div></body></html>'  
	html = y.format
	iframe = IFrame(html(encoded.decode('UTF-8')), width=(7*75)+20, height=400)
	popup = folium.Popup(iframe, max_width=2650, max_height=10000) 
	folium.Marker([latitude,longitude], popup=popup, tooltip=index).add_to(mp)
	

def dmstodd(dms,bearing):
	'''
	Changes Degree Minute Second formatted co-ordinates into Decimal Degree format following the formulae D + (M/60) + (S/3600).  uses the
	bearing to ensure which direction the DD value is.  returns Decimal Degree.
	'''

	s = dms.values
	deg = float(s[0].num) / float(s[0].den)
	minu = float(s[1].num) / float(s[1].den)
	sec = float(s[2].num) / float(s[2].den)
	dd = deg +(minu/60.0)+(sec/3600.0)
	if str(bearing) in ('S','W','s','w'):
		return dd*-1
	return dd	


def start():
	global dates
	global files
	''' 
	creates folium map and runs the program. First dates are put into chronological order to compare in order against.
	Then file names are array'd in date order. This can then be plotted to map in chronological order
	'''
	print("#####################################################################################")
	print("")
	print("Welcome to ExifTool")
	print("")
	print("#####################################################################################")
	print("")
	filenamesdude = []
	for filename in glob.glob(os.path.join(sys.argv[1],'*.jpg')):
		filenamesdude.append(filename)
	mp = mp = folium.Map(location=[51.5085297,-0.12574], zoom_start=10)
	s = 1
	for filename in filenamesdude:
		print("Processing " + str(s) + "/" + str(len(filenamesdude)))
		chrono(filename)
		s=s+1
	dates = sorted(dates)
	for t in range(0,len(dates)):
		print("Organising filename " + str(t+1) +"/"+str(len(dates)))
		organise(t,filenamesdude)
	q = 0
	for file in files:
		print("Plotting file: " + file[0] + " | " + str(q+1) +"/" + str(len(files)))
		if q == 0:
			openme(file[0],mp, "Start Here")
		elif q == (len(files)-1):
			openme(file[0],mp,"End Here")
		else:
			openme(file[0],mp,str(q))
		q=q+1
	addlines(mp)
	mp.save('map.html')
	print("Map saved to map.html")



if __name__ == '__main__':
	'''
	Ensures the python file is being called DIRECTLY, and is not being used as an external library
	'''
	start()
