from geolocation2 import map_at

import geopy

geocoder=geopy.geocoders.GoogleV3(domain="maps.google.co.uk")
def geolocate(place):
  return geocoder.geocode(place,exactly_one=False)[0][1]
london_location=geolocate("London")
print london_location


def is_green(r,g,b):
 threshold=1.1
 return g>r*threshold and g>b*threshold

import png
from itertools import izip

def count_green_in_png(data):
    image=png.Reader(file=StringIO(data.content)).asRGB()
    count = 0
    for row in image[2]:
        pixels=izip(*[iter(row)]*3)
        count+=sum(1 for pixel in pixels if is_green(*pixel))
    return count


from StringIO import StringIO
print count_green_in_png(map_at(*london_location))



def show_green_in_png(data):
    image=png.Reader(file=StringIO(data.content)).asRGB()
    count = 0
    out=[]
    for row in image[2]:
        outrow=[]
        pixels=izip(*[iter(row)]*3)
        for pixel in pixels:
            outrow.append(0)
            if is_green(*pixel):
                outrow.append(255)
            else:
                outrow.append(0)
            outrow.append(0)
        out.append(outrow)
    buffer=StringIO()
    result = png.from_array(out,mode='RGB')
    result.save(buffer)
    return buffer.getvalue()

	
	
	
from numpy import linspace
def location_sequence(start,end,steps):
  # Would actually prefer this if steps
  # were deduced from zoomlevel
  # But need projection code for that
  lats=linspace(start[0],end[0],steps)
  longs=linspace(start[1],end[1],steps)
  return zip(lats,longs)
[count_green_in_png(map_at(*location,zoom=10,satellite=True))
            for location in location_sequence(geolocate("London"),geolocate("Birmingham"),10)]
			
			
			
			
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
with open('green.png','w') as green:
    green.write(show_green_in_png(map_at(*london_location,
        zoom=10,satellite=True)))
plt.plot([
    count_green_in_png(
        map_at(*location,zoom=10,satellite=True))
          for location in location_sequence(
              geolocate("London"),
              geolocate("Birmingham"),10)]) 

plt.savefig('greengraph.png')
