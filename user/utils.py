from django.contrib.gis.geoip2 import GeoIP2

def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon



    # fuction for toking location from customer
# def location(request):
#     if request.method == 'POST':
#         place = request.POST['place']
#         # geolocator = Nominatim(user_agent='user')
        
#         # destination = geolocator.geocode(place)
#         # print(destination)
#         # d_lon = destination.longitude
#         # d_lat = destination.latitude
#         # pointA = (d_lat, d_lon)
     
#         # data  = JobSeeker.objects.all()
        
#         # for x in data:
#         #     place_sample = x.place
#         #     destiny = geolocator.geocode(place_sample)
#         #     sample_lat = destiny.latitude
#         #     sample_lon = destiny.longitude
#         #     pointB = (sample_lat, sample_lon)
#         #     distance = round(geodesic(pointA, pointB).km, 2)
#         #     # print(place_sample)
#         #     # print(distance)
#         #     if distance <= 100:
#         #         places = []
#         #         places.append(x)
#         #         print(places)
#         # request.session['places'] = places
#         # context = {"places":places}     
#         return redirect(registered_customer_homepage)
#     else: 
#         return render(request, 'customer/location.html')