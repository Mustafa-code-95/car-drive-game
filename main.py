from ursina import camera
from ursina import time
from ursina import application
from ursina import Text
from ursina import Ursina
from ursina import Entity
from ursina import invoke
from ursina import color
from ursina import mouse
from ursina import clamp
from ursina import destroy
from ursina import held_keys
import random

app = Ursina()

camera.orthographic = True
camera.fov = 10

background = Entity(model='quad', texture='road.jpg', scale=(20, 12), z=10)

game_over = False
game_start = False
score = 0
cars = []
car_index = 0
car_list = ['car0.png', 'car1.png', 'car2.png', 'car3.png', 'car4.png',
            'car5.png', 'car6.png', 'car7.png', 'car8.png', 'car9.png',
            'car10.png', 'car11.png', 'car12.png', 'car13.png']

player = Entity(model='cube', color=color.white, texture=car_list[car_index], scale=(1, 2), position=(0, 0), collider='box')
feil_right = Entity(model='quad', texture='feil1.png', scale=1, position=(6, 0), collider='box')
feil_left = Entity(model='quad', texture='feil.png', scale=1, position=(-6, 0), collider='box')

mouse_clicked = False


def add_car():
    x = random.randint(-8, 8)
    car = Entity(rotation_z=180, model='cube', color=color.white, texture=random.choice(car_list), scale=(1, 2), position=(x, 6), collider='box')
    cars.append(car)


def spawn_cars():
    if game_start and not game_over:
        add_car()
        invoke(spawn_cars, delay=1)


def update():
    global game_start, game_over, car_index, mouse_clicked

    if not game_start:
        if not mouse_clicked:
            if feil_left.hovered and mouse.left:
                car_index = (car_index - 1) % len(car_list)
                player.texture = car_list[car_index]
                mouse_clicked = True
            elif feil_right.hovered and mouse.left:
                car_index = (car_index + 1) % len(car_list)
                player.texture = car_list[car_index]
                mouse_clicked = True
        if mouse_clicked and not mouse.left:
            mouse_clicked = False

        if held_keys['space']:
            game_start = True
            destroy(feil_left)
            destroy(feil_right)
            player.position = (0, -3.8)
            spawn_cars()

    elif not game_over:
        if held_keys['a']:
            player.x -= 10 * time.dt
        if held_keys['d']:
            player.x += 10 * time.dt
        player.x = clamp(player.x, -8, 8)

        for car in cars[:]:
            car.y -= 5 * time.dt
            if car.y < -6:
                destroy(car)
                cars.remove(car)
            elif player.intersects(car).hit:
                game_over = True
                a = Text(text='', origin=(0,0), scale=5, color=color.red)
                a.text = 'Game Over'

    else:
        if held_keys['q']:
            application.quit()


app.run()
