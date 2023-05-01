import requests
import pygame
import os
import random

geocode_maps_endpoint = "http://geocode-maps.yandex.ru/1.x/"
static_maps_endpoint = "http://static-maps.yandex.ru/1.x/"


def get_object_size(object):
    bbox = object["boundedBy"]["Envelope"]
    lt_1, ln_1 = bbox["lowerCorner"].split(" ")
    lt_2, ln_2 = bbox["upperCorner"].split(" ")
    delta_ln = (abs(float(ln_1) - float(ln_2)) / 2) * 0.01
    delta_lt = (abs(float(lt_1) - float(lt_2)) / 2) * 0.01
    return delta_ln, delta_lt


cities = ["Прага", "Ковров", "Пекин", "Караганда", "Вильнюс", "Комсомольск-на-Амуре", "Ачинск"]
view_options = ["map", "sat"]
slides = []

for i in range(len(cities)):
    geocode_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": cities[i],
        "format": "json"}
    response_geo = requests.get(geocode_maps_endpoint, params=geocode_params).json()
    city_geo_object = response_geo["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    city_size = map(str, get_object_size(city_geo_object))
    city_pos = city_geo_object["Point"]["pos"]
    ln, lt = city_pos.split(' ')
    map_params = {
        "ll": ','.join((ln, lt)),
        "spn": ','.join(city_size),
        "l": random.choice(view_options),
        "size": "450,450"
    }
    response_map = requests.get(static_maps_endpoint, params=map_params)
    slide = f'slide_{i}.png'
    with open(slide, 'wb') as map_slide:
        map_slide.write(response_map.content)
    slides.append(slide)

pygame.init()
screen = pygame.display.set_mode((450, 450))
pygame.display.set_caption('Угадай-ка город - Слайд-шоу')
running = True

count = 0
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(pygame.image.load(slides[count % len(slides)]), (0, 0))
    pygame.display.flip()
    clock.tick(1)
    count += 1
pygame.quit()

[os.remove(slide) for slide in slides]
