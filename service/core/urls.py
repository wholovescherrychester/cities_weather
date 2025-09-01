from django.urls import path
from .views import (home_page, temp_city_page, cities_distance,
                    city_list_temp, city_list_dist_1, city_list_dist_2)


app_name = 'core'

urlpatterns = [
    path('',home_page,name='home'),
    path('temperature/<slug:city_slug>',temp_city_page,name='temp_city'),
    path('distance', cities_distance, name='distance')
]

htmx_urlpatterns = [
    path('cities-temp',city_list_temp,name='cities_temp'),
    path('cities-dist-1',city_list_dist_1,name='cities_dist_1'),
    path('cities-dist-2',city_list_dist_2,name='cities_dist_2'),
]

urlpatterns += htmx_urlpatterns