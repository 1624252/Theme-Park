from turtle import setup, tracer, update
from objects import *
from yaml import safe_load

from os import listdir
from PIL import Image

screen: Screen = None

sections: list[Section] = []

ride_sections: list[Section] = []
restaurant_section: RestaurantSection
gift_shop: GiftShop

ignore = ("background.gif",)
default = (535, 250)


def image_setup():
    already = listdir("images/items")
    new = listdir("images")
    for i in new:
        if i[-4:] != ".gif" or i in ignore:
            continue
        image = Image.open("images/" + i)
        starting_size = image.size

        difference = (default[0], default[0] / starting_size[0] * starting_size[1])
        if difference[1] > default[1]:
            difference = (default[1] / starting_size[1] * starting_size[0], default[1])

        difference = ((difference[0] - starting_size[0])/(zoom_limit - 1), (difference[1] - starting_size[1])/(zoom_limit - 1))

        for q in range(zoom_limit):
            name = "images/items/" + i[:-4] + "-zoom" + str(zoom_limit - q - 1) + ".gif"

            if name[13:] in already:
                continue
            new = (starting_size[0] + difference[0] * q, starting_size[1] + difference[1] * q)

            image = image.resize((round(new[0]), round(new[1])))
            image.save(name, "PNG")
            if q == zoom_limit - 1:
                image.save("images/items/" + i, "PNG")


def initiate():
    global screen, ride_sections, restaurant_section, gift_shop
    screen = Screen()
    screen.title("Theme Park")
    import_screen()
    setup(1.0, 1.0)
    screen.bgpic("images/static/background.png")  # 1920x1080.

    # DON'T UNCOMMENT THIS UNTIL WE ARE SHOWING EVERYONE.
    # screen.getcanvas().winfo_toplevel().attributes('-fullscreen', True)

    already = listdir("images/items")
    for i in already:
        screen.addshape("images/items/" + i)

    positions = [
        (-540, 280),
        (0, 280),
        (540, 280),
        (-260, -195),
        (260, -195),
        (-740, -315),
        (740, -315),
    ]

    section_data = [
        ("Section 1", "banner1.gif"),
        ("Section 2", "banner2.gif"),
        ("Section 3", "banner3.gif"),
        ("Section 4", "banner1.gif"),
        ("Section 5", "banner2.gif"),
    ]
    ride_sections = []
    restaurants = []
    gifts = []
    characters = []

    tracer(0, 0)

    with open("data.yaml") as file:
        data = safe_load(file)

        print(data)

        for i in range(5):
            ride_sections.append(
                RideSection(
                    positions[i],
                    section_data[i][0],
                    section_data[i][1],
                    list(Ride(
                        data["rides"][i * 2 + q]["name"],
                        data["rides"][i * 2 + q]["image"],
                        data["rides"][i * 2 + q]["description"],
                        data["rides"][i * 2 + q]["location"],
                    ) for q in range(1, 3)),
                    hide_rest,
                    menu,
                )
            )
            sections.append(ride_sections[i])

        for i in range(3):
            restaurants.append(
                Restaurant(
                    data["restaurants"][i + 1]["name"],
                    data["restaurants"][i + 1]["image"],
                    data["restaurants"][i + 1]["description"],
                    data["restaurants"][i + 1]["menu"],
                    data["restaurants"][i + 1]["location"],
                )
            )

        for i in range(3):
            gifts.append(
                Gift(
                    data["gifts"][i + 1]["name"],
                    data["gifts"][i + 1]["image"],
                    data["gifts"][i + 1]["description"],
                    data["gifts"][i + 1]["location"],
                )
            )

        for i in range(3):
            characters.append(
                Character(
                    data["characters"][i + 1]["name"],
                    data["characters"][i + 1]["images"],
                    data["characters"][i + 1]["description"]
                )
            )

    restaurant_section = RestaurantSection(positions[-2], "banner2.gif", restaurants, hide_rest, menu)
    gift_shop = GiftShop(positions[-1], "banner3.gif", gifts, hide_rest, menu)
    sections.append(restaurant_section)
    sections.append(gift_shop)

    tracer(1, 0)

    root = screen.getcanvas().winfo_toplevel()
    root.protocol("WM_DELETE_WINDOW", exit)


def menu():
    tracer(0, 0)
    for section in sections:
        section.menu()
    update()
    tracer(1, 0)


def hide_rest(keep):
    tracer(0, 0)
    for section in sections:
        if section != keep:
            section.hide()
    update()
    tracer(1, 0)
