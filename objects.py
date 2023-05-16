from turtle import Turtle, Screen
from tkinter import Tk, Label, Button, PhotoImage


default_speed = 7
menu_position = 200
menu_position_up = 50

zoom_limit = 20

image_prefix = "images/items/"
screen: Screen


def import_screen():
    from setup import screen as s
    global screen
    screen = s


class Item:
    def __init__(self, name: str, image: str, description: str, zoom_destination: tuple[float, float] = (0, 0)):
        image = image_prefix + image
        self.image = image
        self.description = description
        self.name = name

        self.turtle = Turtle(image)
        self.turtle.hideturtle()
        self.turtle.penup()

        self.zoom_destination = zoom_destination
        self.is_zooming = False
        self.add = None
        self.add_use = None
        self.popup = None

    def get_popup_width(self):
        return 400

    def get_popup_height(self, tk, width):
        label = Label(tk, text=self.name + "\n\n" + self.description, font=("Candara", 15, "normal"), bg="white",
                      wraplength=width - 40, justify="left")
        tk.geometry("0x0")
        label.place(y=20, x=20)
        tk.update()
        return label.winfo_height() + 40

    def get_description_geometry(self, width, height):
        offset = (0, -320)

        return f"+{round(screen.getcanvas().winfo_rootx() + screen.window_width() / 2 + self.zoom_destination[0] - width / 2 + offset[0])}+{round(screen.getcanvas().winfo_rooty() + screen.window_height() / 2 + self.zoom_destination[1] + offset[1])}"

    def create_description(self):
        self.popup = tk = Tk()
        tk.title("")

        tk.configure(bg="white")
        tk.attributes('-topmost', True)

        width = self.get_popup_width()
        height = self.get_popup_height(tk, width)

        tk.geometry(f"{width}x{height}" + self.get_description_geometry(width, height))

        return tk

    def destroy_window(self):
        if self.popup:
            self.popup.destroy()

    def set_pos(self, x: float, y: float, speed: int = default_speed):
        self.turtle.speed(0)
        self.turtle.goto(x, y)
        self.turtle.showturtle()
        self.turtle.speed(speed)

    def move(self, x: int, y: int):
        self.turtle.goto(x, y)

    def hide(self):
        self.turtle.hideturtle()

    def zoom_in(self):
        for i in range(zoom_limit):
            self.zoom(i)

    def calculate_zoom(self):
        self.add = [(self.zoom_destination[0] - self.turtle.xcor()) / zoom_limit, (self.zoom_destination[1] - self.turtle.ycor()) / zoom_limit]

    def zoom(self, step, forward=True):
        assert 0 <= step < zoom_limit
        if not self.is_zooming:
            self.is_zooming = True
            self.add_use = self.add
            if not forward:
                self.add_use = [-self.add[0], -self.add[1]]
        self.move(round(self.turtle.xcor() + self.add_use[0]), round(self.turtle.ycor() + self.add_use[1]))
        self.turtle.shape(self.image[:-4] + "-zoom" + str(step) + ".gif")

        if forward and step == zoom_limit - 1:
            self.is_zooming = False
            self.add_use = None
        elif not forward and step == 0:
            self.is_zooming = False
            self.add_use = None


class Section:
    def __init__(self, position: tuple[int, int], name: str, title_image: str, items: list, hide_rest, show_all, title_destination: tuple[int, int] = (-600, -410)):
        self.name = name
        self.title_item = Item("", title_image, "", title_destination)
        self.title_image = image_prefix + title_image

        self.items = items
        self.position = position
        self.hide_rest = hide_rest
        self.show_all = show_all

        self.back = Turtle()
        self.back.speed(0)
        self.back.shapesize(11, 14)
        self.back.pencolor("white")
        self.back.pensize(20)
        self.back.penup()
        self.back.goto(-950, 440)
        self.back.left(180)
        self.back.hideturtle()

        self.group = self.items + [self.title_item]
        self.zoomed = False

        def on_click(x, y):
            if not self.zoomed:
                old = self.group[0].turtle.speed()
                for item in self.group:
                    item.turtle.speed(1)

                self.hide_rest(self)

                for i in range(zoom_limit):
                    for item in self.group:
                        item.zoom(i)

                for item in self.items:
                    item.create_description()

                for item in self.group:
                    item.turtle.speed(old)

                self.zoomed = True
                self.back.showturtle()

        for item in self.group:
            item.turtle.onclick(on_click)

        def return_menu(x, y):
            if not self.zoomed:
                return

            self.back.hideturtle()
            for item in self.items:
                item.destroy_window()

            old = self.group[0].turtle.speed()
            for item in self.group:
                item.turtle.speed(1)

            for i in range(zoom_limit - 1, -1, -1):
                for item in self.group:
                    item.zoom(i, False)

            for item in self.group:
                item.turtle.speed(old)

            self.show_all()

            self.zoomed = False

        self.back.onclick(return_menu)

    def menu(self):
        position = menu_position / (len(self.items) - 1)
        position_up = menu_position_up * (len(self.items) - 1)
        for i in range(len(self.items)):
            self.items[i].set_pos(self.position[0] + position * i - menu_position/2, self.position[1] + position_up * (i % 2))
        self.title_item.set_pos(self.position[0], self.position[1] - 100)

        if self.items[0].add is None:
            for item in self.group:
                item.calculate_zoom()

    def hide(self):
        for item in self.group:
            item.turtle.hideturtle()


class Ride(Item):
    def __init__(self, name: str, image: str, description: str, zoom_destination: tuple[float, float]):
        super().__init__(name, image, description, zoom_destination)
        self.name = name
        self.description = description


class RideSection(Section):
    def __init__(self, position: tuple[int, int], name: str, title_image: str, rides: list[Ride], hide_rest, show_all):
        super().__init__(position, name, title_image, rides, hide_rest, show_all)


class Restaurant(Item):
    def __init__(self, name: str, image: str, description: str, menu: str, zoom_destination: tuple[float, float]):
        super().__init__(name, image, description, zoom_destination)
        self.name = name
        self.description = description
        self.menu = menu

    def get_popup_height(self, tk, width):
        label = Label(tk, text=self.name + "\n\n" + self.description, font=("Candara", 15, "normal"), bg="white",
                      wraplength=width - 40, justify="left")
        button = Button(tk, text="Menu", font=("Candara", 15, "normal"), bg="cyan", command=lambda: self.open_menu())
        tk.geometry("0x0")
        label.place(y=20, x=20)
        tk.update()
        button.place(y=label.winfo_height() + 40, relx=0.5, anchor="center")
        tk.update()
        return 40 + label.winfo_height() + button.winfo_height()

    def open_menu(self):
        tk = Tk()
        image = PhotoImage(file="images/static/menu-placeholder.png")
        tk.geometry(f"{image.width()}x{image.height()}")
        label = Label(tk, image=image)
        label.pack()
        tk.mainloop()
        # TODO: Fix.


class RestaurantSection(Section):
    def __init__(self, position: tuple[int, int], title_image: str, restaurants: list[Restaurant], hide_rest, show_all):
        super().__init__(position, "Restaurants", title_image, restaurants, hide_rest, show_all)


class Character:
    # images is in the format [walking_left, walking_right, staring].
    def __init__(self, name: str, images: list[str], description: str):
        self.name = name
        self.images = tuple(image_prefix + image for image in images)
        self.description = description


class Gift(Item):
    def __init__(self, name: str, image: str, description: str, zoom_destination: tuple[float, float]):
        super().__init__(name, image, description, zoom_destination)
        self.name = name
        self.description = description


class GiftShop(Section):
    def __init__(self, position: tuple[int, int], title_image: str, gifts: list[Gift], hide_rest, show_all):
        super().__init__(position, "Gift Shop", title_image, gifts, hide_rest, show_all)

