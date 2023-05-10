from turtle import setup, tracer, update
from objects import *
from yaml import safe_load

screen: Screen = None

sections: list[Section] = []

ride_sections: list[Section] = []
restaurant_section: RestaurantSection
gift_shop: GiftShop


def initiate():
    global screen, ride_sections, restaurant_section, gift_shop
    screen = Screen()
    import_screen()
    setup(1.0, 1.0)
    screen.bgpic("images/background.gif")  # 1920x1080.

    # DON'T UNCOMMENT THIS UNTIL WE ARE SHOWING EVERYONE.
    # screen.getcanvas().winfo_toplevel().attributes('-fullscreen', True)

    positions = [
        (-520, 280),
        (0, 280),
        (520, 280),
        (-245, -225),
        (245, -225),
        (-740, -305),
        (740, -305),
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
                        data["rides"][i * 2 + q]["description"]
                    ) for q in range(1, 3))
                )
            )
            sections.append(ride_sections[i])

        for i in range(3):
            restaurants.append(
                Restaurant(
                    data["restaurants"][i + 1]["name"],
                    data["restaurants"][i + 1]["image"],
                    data["restaurants"][i + 1]["description"],
                    data["restaurants"][i + 1]["menu"]
                )
            )

        for i in range(3):
            gifts.append(
                Gift(
                    data["gifts"][i + 1]["name"],
                    data["gifts"][i + 1]["image"],
                    data["gifts"][i + 1]["description"]
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

    restaurant_section = RestaurantSection(positions[-2], "banner2.gif", restaurants)
    gift_shop = GiftShop(positions[-1], "banner3.gif", gifts)
    sections.append(restaurant_section)
    sections.append(gift_shop)

    tracer(1, 0)


def menu():
    tracer(0, 0)
    for section in sections:
        section.menu()
    update()
    tracer(1, 0)
