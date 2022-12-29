import random

from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.response import Response
from core.models import CarModel
from core.api.pagination import ResultsSetPagination
from core.api.serializers import CarSerializer
from core.utils import open_data, get_page_length
import json
import requests
from bs4 import BeautifulSoup


@csrf_exempt
@cache_page(60 * 15)
def get_car_data(request):
    data = get_page_length('https://www.cars.com/shopping/results/')
    result = []
    for i in range(data):

        if i == 0:
            g_url = 'https://www.cars.com/shopping/results/'
        else:
            g_url = 'https://www.cars.com/shopping/results/' + '?page=' + str(i)

        page = requests.get(str(g_url))
        soup = BeautifulSoup(page.content, 'html.parser')
        data = soup.find('div', class_='sds-page-section listings-page')['data-site-activity']

        if request.method == 'GET':
            for i in range(len(json.loads(data)['vehicleArray'])):
                page2 = requests.get(
                    'https://www.cars.com/vehicledetail/' + str(json.loads(data)['vehicleArray'][i]['listing_id']))
                soup2 = BeautifulSoup(page2.content, 'html.parser')
                if soup2.find_all('dd')[5].text:
                    transmission = soup2.find_all('dd')[5].text
                else:
                    transmission = None
                a = {
                    'bodystyle': json.loads(data)['vehicleArray'][i]['bodystyle'],
                    'canonical_mmt': json.loads(data)['vehicleArray'][i]['canonical_mmt'],
                    'customer_id': json.loads(data)['vehicleArray'][i]['customer_id'],
                    'fuel_type': json.loads(data)['vehicleArray'][i]['fuel_type'],
                    'listing_id': json.loads(data)['vehicleArray'][i]['listing_id'],
                    'make': json.loads(data)['vehicleArray'][i]['make'],
                    'mileage': json.loads(data)['vehicleArray'][i]['mileage'],
                    'model': json.loads(data)['vehicleArray'][i]['model'],
                    'msrp': json.loads(data)['vehicleArray'][i]['msrp'],
                    'price': json.loads(data)['vehicleArray'][i]['price'],
                    'seller_type': json.loads(data)['vehicleArray'][i]['seller_type'],
                    'stock_type': json.loads(data)['vehicleArray'][i]['stock_type'],
                    'trim': json.loads(data)['vehicleArray'][i]['trim'],
                    'vin': json.loads(data)['vehicleArray'][i]['vin'],
                    'year': json.loads(data)['vehicleArray'][i]['year'],
                    'exterior_color': json.loads(data)['vehicleArray'][i]['exterior_color'],
                    'transmission': transmission
                }

                result.append(a)

                with open('data.json', 'w') as f:
                    json.dump(result, f, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            return HttpResponse('Method not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

    return HttpResponse(result)


class CarViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarSerializer
    pagination_class = ResultsSetPagination

    def filter_queryset(self, queryset):
        q_make = self.request.query_params.get('make', None)
        q_model = self.request.query_params.get('model', None)
        q_year = self.request.query_params.get('year', None)
        q_exterior_color = self.request.query_params.get('exterior_color', None)
        q_count = self.request.query_params.get('count', None)
        q_transmission = self.request.query_params.get('transmission', None)

        if q_count is not None:
            queryset = queryset[:int(q_count)]

        if q_transmission is not None:
            queryset = queryset.filter(transmission__icontains=q_transmission)

        if q_make is not None:
            queryset = queryset.filter(make=q_make)
        if q_model is not None:
            queryset = queryset.filter(model=q_model)
        if q_year is not None:
            queryset = queryset.filter(year=q_year)
        if q_exterior_color is not None:
            queryset = queryset.filter(exterior_color__contains=q_exterior_color)

        return queryset

    def create(self, request, *args, **kwargs):
        data = open_data()
        for i in range(len(data)):
            liste = []
            for k in data:
                CarModel.objects.get_or_create(
                    bodystyle=k['bodystyle'],
                    canonical_mmt=k['canonical_mmt'],
                    customer_id=k['customer_id'],
                    fuel_type=k['fuel_type'],
                    listing_id=k['listing_id'],
                    make=k['make'],
                    mileage=k['mileage'],
                    model=k['model'],
                    msrp=k['msrp'],
                    price=k['price'],
                    seller_type=k['seller_type'],
                    stock_type=k['stock_type'],
                    trim=k['trim'],
                    vin=k['vin'],
                    year=k['year'],
                    exterior_color=k['exterior_color'],
                    transmission=k['transmission']
                )
                liste.append(k)
            return Response(liste, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        response_data = []
        for data in range(len(serializer.data)):
            car_title = serializer.data[data]['make'] + ' ' + serializer.data[data]['model'] + ' ' + \
                        serializer.data[data]['year']
            car_price = serializer.data[data]['price']
            car_url = 'https://www.cars.com/vehicledetail/' + str(
                serializer.data[data]['listing_id'])
            car_make = serializer.data[data]['make']
            car_year = serializer.data[data]['year']
            car_exterior_color = serializer.data[data]['exterior_color']
            car_transmission = serializer.data[data]['transmission']

            all_data = {
                'Car Title': car_title,
                'Car Price': car_price,
                'Car Url': car_url,
                'Car Make': car_make,
                'Car Year': car_year,
                'Car Exterior Color': car_exterior_color,
                'Car Transmission': car_transmission
            }
            response_data.append(all_data)

        return Response({'count': queryset.count(), 'result': random.choices(response_data, k=50)}, status=status.HTTP_200_OK)
        # return Response({'count': queryset.count(), 'result': (response_data[:50])}, status=status.HTTP_200_OK)
