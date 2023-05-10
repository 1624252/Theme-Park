from turtle import Turtle, Screen


default_speed = 7
menu_position = 200
menu_position_up = 50

image_prefix = "images/"
screen: Screen


def import_screen():
    from setup import screen as s
    global screen
    screen = s


class Item:
    def __init__(self, image: str):
        image = image_prefix + image
        self.image = image
        screen.addshape(image)
        self.turtle = Turtle(image)
        self.turtle.hideturtle()
        self.turtle.penup()

    def set_pos(self, x: float, y: float, speed: int = default_speed):
        self.turtle.speed(0)
        self.turtle.goto(x, y)
        self.turtle.showturtle()
        self.turtle.speed(speed)

    def move(self, x: int, y: int):
        self.turtle.goto(x, y)

    def hide(self):
        self.turtle.hideturtle()


class Section:
    def __init__(self, position: tuple[int, int], name: str, title_image: str, items: list):
        self.name = name

        self.title_item = Item(title_image)
        self.title_image = image_prefix + title_image

        self.items = items
        self.position = position

    def menu(self):
        position = menu_position / (len(self.items) - 1)
        position_up = menu_position_up * (len(self.items) - 1)
        for i in range(len(self.items)):
            self.items[i].set_pos(self.position[0] + position * i - menu_position/2, self.position[1] + position_up * (i % 2))
        self.title_item.set_pos(self.position[0], self.position[1] - 100)


class Ride(Item):
    def __init__(self, name: str, image: str, description: str):
        super().__init__(image)
        self.name = name
        self.description = description


class RideSection(Section):
    def __init__(self, position: tuple[int, int], name: str, title_image: str, rides: list[Ride]):
        super().__init__(position, name, title_image, rides)


class Restaurant(Item):
    # Menu format is {name: (price, description)}.
    def __init__(self, name: str, image: str, description: str, menu: dict[str, list[int, str]]):
        super().__init__(image)
        self.name = name
        self.description = description
        self.menu = menu


class RestaurantSection(Section):
    def __init__(self, position: tuple[int, int], title_image: str, restaurants: list[Restaurant]):
        super().__init__(position, "Restaurants", title_image, restaurants)


class Character:
    # images is in the format [walking_left, walking_right, staring].
    def __init__(self, name: str, images: list[str], description: str):
        self.name = name
        self.images = tuple(image_prefix + image for image in images)
        self.description = description


class Gift(Item):
    def __init__(self, name: str, image: str, description: str):
        super().__init__(image)
        self.name = name
        self.description = description


class GiftShop(Section):
    def __init__(self, position: tuple[int, int], title_image: str, gifts: list[Gift]):
        super().__init__(position, "Gift Shop", title_image, gifts)

