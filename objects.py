from turtle import Turtle, Screen, tracer, update
from tkinter import Tk, Label, Button, PhotoImage, Toplevel, TclError
from random import randint

character_speed = 0.5

default_speed = 7
menu_position = 200
menu_position_up = 50

zoom_limit = 20

image_prefix = "images/items/"
static_image_prefix = "images/static/"
screen: Screen


def import_screen():
    from setup import screen as s
    global screen
    screen = s


class Character:
    # images is in the format [walking_left, walking_right, staring].
    def __init__(self, name: str, images: list[str], description: str):
        self.name = name
        self.images = tuple(static_image_prefix + image for image in images)
        self.current_image = 0
        self.description = description

        self.do_animate = True

        self.turtle = Turtle(self.images[self.current_image])
        self.turtle.hideturtle()
        self.turtle.penup()

        self.turtle.setpos(randint(round(-screen.window_width() / 2), round(screen.window_width() / 2)),
                           randint(round(-screen.window_height() / 2), round(screen.window_height() / 2)))
        self.pop_up = None

        def on_click(x, y):
            if self.current_image != 2:
                self.set_image(2)  # HAHA KILL JFK.
                self.do_animate = False
            else:
                self.do_animate = True

        self.turtle.ondrag(self.turtle.goto)
        self.turtle.onclick(on_click)

        self.new_position = self.turtle.position()
        self.add = []
        self.loops = 0
        self.counter = 0

    def set_image(self, number):
        if number == self.current_image:
            return
        self.current_image = number
        self.turtle.shape(self.images[self.current_image])

    def reset(self):
        self.do_animate = True
        self.loops = self.counter = 0

    def setup(self):
        self.reset()
        self.turtle.showturtle()

    def animate(self, t: int):
        if not self.do_animate:
            return
        if self.loops == self.counter:
            self.new_position = (randint(round(-screen.window_width() / 2 * .8), round(screen.window_width() / 2 * .8)),
                                 randint(round(-screen.window_height() / 2 * .8),
                                         round(screen.window_height() / 2 * .8)))
            self.add = [self.new_position[0] - self.turtle.position()[0],
                        self.new_position[1] - self.turtle.position()[1]]
            self.loops = max(abs(self.add[0]), abs(self.add[1])) // character_speed
            self.add = [self.add[0] / self.loops, self.add[1] / self.loops]
            self.counter = 0
        if self.add[0] > 0:
            self.set_image(1)
        elif self.add[0] < 0:
            self.set_image(0)
        self.turtle.goto(self.turtle.position()[0] + self.add[0],
                         self.turtle.position()[1] + self.add[1])
        self.counter += 1


class Item:
    def __init__(self, name: str, image: str, description: str, zoom_destination: tuple[float, float] = (0, 0), prefix: str = image_prefix):
        image = prefix + image
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
        label = Label(tk, text=self.name + "\n\n" + self.description, font=("Candara", 12, "normal"), bg="white",
                      wraplength=width - 40, justify="left")
        tk.geometry("0x0")
        label.place(y=20, x=20)
        tk.update()
        return label.winfo_height() + 40

    def get_description_geometry(self, width, height):
        offset = (0, -160)

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
            try:
                self.popup.destroy()
            except TclError:
                pass

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
        self.add = [(self.zoom_destination[0] - self.turtle.xcor()) / zoom_limit,
                    (self.zoom_destination[1] - self.turtle.ycor()) / zoom_limit]

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
    def __init__(self, position: tuple[int, int], name: str, title_image: str, items: list, hide_rest, show_all,
                 title_destination: tuple[int, int] = (-600, -410), prefix: str = image_prefix):
        self.name = name
        self.title_item = Item("", title_image, "", title_destination)
        self.title_image = prefix + title_image
        self.characters = []

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

        self.destroy_functions = []
        self.update_functions = []

        for item in self.items:
            self.destroy_functions.append(item.destroy_window)

        def on_click(x, y):
            if not self.zoomed:
                self.zoomed = True

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

                self.back.showturtle()

                for item in self.items:
                    if isinstance(item, Ride) and item.animation is not None:
                        self.update_functions.append(item.animation)
                for c in self.characters:
                    c.setup()
                    self.update_functions.append(c.animate)

                i = 0
                while len(self.update_functions) > 0:
                    tracer(0, 10)
                    self.update_section(i)
                    update()
                    i += 1

        for item in self.group:
            item.turtle.onclick(on_click)

        def return_menu(x, y):
            if not self.zoomed:
                return

            tracer(1, 0)
            self.update_functions = []
            self.back.hideturtle()
            for f in self.destroy_functions:
                f()

            for c in self.characters:
                c.turtle.hideturtle()
                c.reset()

            old = self.group[0].turtle.speed()
            for item in self.group:
                item.turtle.showturtle()
                if isinstance(item, Ride) and item.move_turtle is not None:
                    item.turtle.shape(item.image)
                    item.move_turtle.hideturtle()
                item.turtle.speed(1)

            for i in range(zoom_limit - 1, -1, -1):
                for item in self.group:
                    item.zoom(i, False)

            for item in self.group:
                item.turtle.speed(old)

            self.show_all()

            self.zoomed = False

        self.back.onclick(return_menu)

    def add_character(self, character: Character):
        self.update_functions.append(character.animate)
        self.characters.append(character)

    def update_section(self, t: int):
        for f in self.update_functions:
            f(t)

    def menu(self):
        position = menu_position / (len(self.items) - 1)
        position_up = menu_position_up * (len(self.items) - 1)
        for i in range(len(self.items)):
            self.items[i].set_pos(self.position[0] + position * i - menu_position / 2,
                                  self.position[1] + position_up * (i % 2))
        self.title_item.set_pos(self.position[0], self.position[1] - 130)

        if self.items[0].add is None:
            for item in self.group:
                item.calculate_zoom()

    def hide(self):
        for item in self.group:
            item.turtle.hideturtle()


class Ride(Item):
    def __init__(self, name: str, image: str, description: str, zoom_destination: tuple[float, float],
                 description_offset: tuple[float, float] = (0, 0), width: int = 1000):
        super().__init__(name, image, description, zoom_destination)
        self.name = name
        self.description = description
        self.description_offset = description_offset
        self.animation = None
        self.prepare_animation = None
        self.move_turtle = None
        self.prepared = False
        self.width = width

    def get_popup_width(self):
        return self.width

    def get_description_geometry(self, width, height):
        return "{:+}{:+}".format(round(self.description_offset[
                                           0] + screen.getcanvas().winfo_rootx() + screen.window_width() / 2 + self.turtle.xcor() - width / 2),
                                 round(
                                     self.description_offset[
                                         1] + screen.getcanvas().winfo_rootx() + screen.window_width() / 4))

    def set_animation(self, function, prepare_function=None):
        def animate(t: int):
            function(self, t)

        self.animation = animate
        if prepare_function is None:
            def prepare_function():
                self.turtle.shape(static_image_prefix + self.image[13:-4] + "-base.gif")

                if self.prepared:
                    self.move_turtle.showturtle()
                    return

                tracer(0, 0)
                self.move_turtle = Turtle(static_image_prefix + self.image[13:-4] + "-move.gif")
                self.move_turtle.speed(0)
                self.move_turtle.penup()
                self.move_turtle.goto(self.turtle.xcor(), self.turtle.ycor())

                tracer(1, 0)
                self.prepared = True

        self.prepare_animation = prepare_function

    def zoom(self, step, forward=True):
        super().zoom(step, forward)
        if step == zoom_limit - 1 and forward and self.prepare_animation is not None:
            self.prepare_animation()


class RideSection(Section):
    def __init__(self, position: tuple[int, int], name: str, title_image: str, rides: list[Ride], hide_rest, show_all):
        super().__init__(position, name, title_image, rides, hide_rest, show_all)


class Restaurant(Item):
    def __init__(self, name: str, image: str, description: str, menu: str, zoom_destination: tuple[float, float]):
        super().__init__(name, image, description, zoom_destination)
        self.name = name
        self.description = description
        self.menu = static_image_prefix + menu
        self.menu_tk = None

    def get_popup_height(self, tk, width):
        label = Label(tk, text=self.name + "\n\n" + self.description, font=("Candara", 12, "normal"), bg="white",
                      wraplength=width - 40, justify="left")
        button = Button(tk, text="Menu", font=("Candara", 15, "normal"), bg="cyan", command=lambda: self.open_menu())
        tk.geometry("0x0")
        label.place(y=20, x=20)
        tk.update()
        button.place(y=label.winfo_height() + 40, relx=0.5, anchor="center")
        tk.update()
        return 40 + label.winfo_height() + button.winfo_height()

    def open_menu(self):
        self.menu_tk = Toplevel()
        image = PhotoImage(file=self.menu)
        self.menu_tk.title(self.name + " Menu")
        self.menu_tk.geometry(
            f"{image.width()}x{image.height()}+{int((self.menu_tk.winfo_screenwidth() - image.width()) / 2)}+{int((self.menu_tk.winfo_screenheight() - image.height()) / 2)}")
        label = Label(self.menu_tk, image=image)
        label.pack()
        self.menu_tk.attributes("-topmost", True)
        self.menu_tk.mainloop()

    def destroy_window(self):
        self.destroy_menu()
        super().destroy_window()

    def destroy_menu(self):
        if self.menu_tk is not None:
            self.menu_tk.destroy()
            self.menu_tk = None


class RestaurantSection(Section):
    def __init__(self, position: tuple[int, int], title_image: str, restaurants: list[Restaurant], hide_rest, show_all):
        super().__init__(position, "Restaurants", title_image, restaurants, hide_rest, show_all)


class Gift(Item):
    def __init__(self, name: str, image: str, description: str, zoom_destination: tuple[float, float]):
        super().__init__(name, image, description, zoom_destination)
        self.name = name
        self.description = description


class GiftShop(Section):
    def __init__(self, position: tuple[int, int], title_image: str, gifts: list[Gift], hide_rest, show_all):
        super().__init__(position, "Gift Shop", title_image, gifts, hide_rest, show_all)
