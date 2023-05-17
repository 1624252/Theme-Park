from turtle import setup, tracer, update
from objects import *
from yaml import safe_load

from time import sleep

from os import listdir
from PIL import Image

screen: Screen = None

sections: list[Section] = []

ride_sections: list[Section] = []
restaurant_section: RestaurantSection
gift_shop: GiftShop
guest_list: Item
title: Item

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
    global screen, ride_sections, restaurant_section, gift_shop, guest_list, title
    screen = Screen()
    screen.title("Theme Park")
    import_screen()
    setup(1.0, 1.0)
    screen.bgpic("images/static/background.png")  # 1920x1080.

    # DON'T UNCOMMENT THIS UNTIL WE ARE SHOWING EVERYONE.
    # screen.getcanvas().winfo_toplevel().attributes('-fullscreen', True)

    already = listdir("images/items")
    already2 = listdir("images/static")
    for i in already:
        screen.addshape("images/items/" + i)
    for i in already2:
        if i[-4:] != ".gif":
            continue
        screen.addshape("images/static/" + i)

    positions = [
        (-540, 300),
        (0, 300),
        (540, 300),
        (-260, -195),
        (260, -195),
        (-740, -315),
        (740, -315),
    ]

    section_data = [
        ("Overhead City", "overhead.gif"),
        ("Commie Square", "commie.gif"),
        ("Muckland", "muck.gif"),
        ("Dusty City", "dusty.gif"),
        ("Shots Fired", "shots.gif"),
    ]
    ride_sections = []
    restaurants = []
    gifts = []
    characters = []

    tracer(0, 0)

    title = Item("Colors of History", "title.gif", "", prefix=static_image_prefix)
    title.set_pos(0, 30)

    with open("data.yaml", encoding="utf8") as file:
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
                        data["rides"][i * 2 + q]["offset"],
                        data["rides"][i * 2 + q]["width"],
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
            for section in data["characters"][i + 1]["sections"]:
                sections[section - 1].add_character(characters[-1])

    restaurant_section = RestaurantSection(positions[-2], "restaurants.gif", restaurants, hide_rest, menu)
    gift_shop = GiftShop(positions[-1], "gifts.gif", gifts, hide_rest, menu)
    sections.append(restaurant_section)
    sections.append(gift_shop)

    animation_limit = 100
    wait_limit = 70
    limit = animation_limit + wait_limit

    q = []
    for i in range(animation_limit):
        q.append((i / (animation_limit - 1)) ** 2)
    for i in range(wait_limit):
        q.append(q[-1])

    q2 = []
    for i in range(animation_limit):
        q2.append((i / (animation_limit - 1)) ** 2)
    for i in range(animation_limit // 2):
        q2.append((i / (animation_limit // 2 - 1)) ** 0.5)
    for i in range(wait_limit * 27):
        q2.append(q2[-1])

    def missile(ride: Ride, t: int):
        w = t % limit
        if t // limit % 2 == 1:
            w = -w
            if w == 0:
                w = -1
        ride.move_turtle.goto(ride.zoom_destination[0], ride.zoom_destination[1] + 10 - 290 * q[w])

    def free_fly(ride: Ride, t: int):
        w = t % limit
        ride.move_turtle.goto(ride.zoom_destination[0] - 300 * q[w], ride.zoom_destination[1] - 290 * q[w])

    def thunder(ride: Ride, t: int):
        w = t % limit
        if t // limit % 2 == 1:
            w = -w
            if w == 0:
                w = -1
        ride.move_turtle.goto(ride.zoom_destination[0], ride.zoom_destination[1] + 300 - 290 * 2 * q[w])

    def bay(ride: Ride, t: int):
        w = t % (animation_limit + animation_limit // 2 + wait_limit * 27)
        if w < animation_limit:
            ride.move_turtle.goto(ride.zoom_destination[0] - 300 + 320 * q[w],
                                  ride.zoom_destination[1] - 340 + 360 * q[w])
        elif w < animation_limit + animation_limit // 2:
            ride.move_turtle.goto(ride.zoom_destination[0] + 20 - 2700 * q2[w],
                                  ride.zoom_destination[1] + 20 - 470 * q2[w])

    ride_sections[0].items[0].set_animation(missile)
    ride_sections[0].items[1].set_animation(free_fly)
    ride_sections[1].items[1].set_animation(thunder)
    ride_sections[4].items[0].set_animation(bay)

    def bomb(x, y):
        print(x, y)
        if -412 <= x <= -535 and 57 <= y <= 119:
            old = gifts[0].turtle.shape()
            for i in range(5):
                gifts[0].turtle.shape(static_image_prefix + f"hbomb-{i + 1}.gif")
                sleep(0.5 if i != 4 else 5)
            gifts[0].turtle.shape(old)

    gifts[0].turtle.onclick(bomb)

    def berlin(x, y):
        print(x, y)
        if gifts[1].turtle.shape().endswith(f"berlin-zoom{zoom_limit - 1}.gif"):
            if 172 <= x <= 237 and 311 <= y <= 381:
                gifts[1].turtle.shape(static_image_prefix + "berlin-1.gif")
        else:
            if 61 <= x <= 144 and -18 <= y <= 61 and gifts[1].turtle.shape().endswith(f"berlin-1.gif"):
                gifts[1].turtle.shape(static_image_prefix + "berlin-2.gif")
            elif 7 <= x <= 146 and -30 <= y <= 178:
                gifts[1].turtle.shape(image_prefix + f"berlin-zoom{zoom_limit - 1}.gif")

    gifts[1].turtle.onclick(berlin)

    def open_list(x, y):
        if guest_list.popup is not None:
            try:
                guest_list.popup.destroy()
            except:
                pass
        guest_list.popup = Toplevel()
        image = PhotoImage(file=static_image_prefix + "guest-list.png")
        guest_list.popup.title("Guest List")
        guest_list.popup.geometry(
            f"{image.width()}x{image.height()}+{int((guest_list.popup.winfo_screenwidth() - image.width()) / 2)}+{int((guest_list.popup.winfo_screenheight() - image.height()) / 2)}")
        label = Label(guest_list.popup, image=image)
        label.pack()
        guest_list.popup.attributes("-topmost", True)
        guest_list.popup.mainloop()

    guest_list = Item("Guest List", "guest-list-button.gif", "", prefix=static_image_prefix)
    guest_list.set_pos(-810, 20)
    guest_list.turtle.onclick(open_list)

    tracer(1, 0)

    root = screen.getcanvas().winfo_toplevel()
    root.protocol("WM_DELETE_WINDOW", exit)


def menu():
    tracer(0, 0)
    for section in sections:
        section.menu()
        guest_list.turtle.showturtle()
        title.turtle.showturtle()
    update()
    tracer(1, 0)


def hide_rest(keep):
    tracer(0, 0)
    for section in sections:
        if section != keep:
            section.hide()
            guest_list.turtle.hideturtle()
            title.turtle.hideturtle()
            try:
                guest_list.popup.destroy()
            except:
                pass
    update()
    tracer(1, 0)
