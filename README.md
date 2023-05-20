# Colors of History
Theme Park Project created by JS, CH, and RS.
***
## Instructions
1. I just realized that it only works on screens that are 1920 x 1080 pixels, so if you do not have that, I apologize; it probably will not work properly on your screen.
2. Clone the repository.
3. Run the executable file (Colors of History.exe) or run main.py in Python.
4. It might take a few seconds for the program to run and load, so do not worry if you are stuck on a blank screen for a bit.
5. The simplest way to exit the park is to go back to the menu screen and click the red exit button in the top right corner. Sometimes in some park sections, simply clicking the X of the Theme Park window (the main window; small windows should work as expected) will not allow you to exit the park. However, the back arrows (top left) will get you to the menu screen, where you can then exit with the aforementioned red exit button.
***
Here is a list of everything you can do within the park:
### Menu Screen
- Click "Guest List" in the middle left for descriptions of guests. See the third point in [Notes](#Notes) if you are confused about why the guests do not seem to be performing all of the listed interactions.
- Click each section (either click the banner label or one of the rides) to explore further.
- Click "Exit" in the top right corner to exit the park.

### Park sections
- Click the back arrow in the top left corner to return to the menu.
- Certain sections have guests walking around. You are able to click and/or drag these characters multiple times. Sometimes, they might end up behind a moving ride, in which case you will be unable to click on them (if this happens, you must wait for them to walk to a more open area).
- Each ride has its description in a popup window somewhere near it. These mini windows may be moved or closed if desired (e.g., if you want to see more of the screen).
- In the restaurants section, click the "Menu" button in each description window to open the menu for the corresponding restaurant. Again, these menus will be in mini windows that can be closed. Mini windows also close whenever you return to the menu, so manually closing all of them is not required.
- In the gift shop, you are able to press the "DO NOT PRESS!" button of the hydrogen bomb souvenir. You are also able to press the top of the tail of the Berlin airplane chocolate dropper, the compartment that pops out, and the box in the compartment. <br> <img src="https://gyazo.com/a03f027e5d284eac6a46631a76c16502.gif" height="300" />

***

## Notes
- Unfortunately, yes, the zoom animation from the menu to each section is very choppy. It probably would have been better to use a different library than Python Turtle, which is somewhat limited for image animations.
- There are probably some bugs, and many things could have been improved in the design and in the code, but we were running low on time due to losing three days because of a competition. (Yes, there are probably inefficiencies in the code. Yes, I probably should not have committed to the master branch so often, but I am the only one working on the code anyway.)
- To anyone who points out how the guests do not perform all of the interactions listed in their descriptions, please familiarize yourself with the double-slit experiment. :D The characters are in fact interacting according to their descriptions, just not when you are looking at them.
- Uh, so, I did not realize that this would not work in different resolutions. Oops. Python Turtle was not the best choice to use for these type of things. I guess I could have used a bunch of ratios instead of exact numbers, but I did not think of that until now.

***

## Credits
- Descriptions and ideas: Mostly RS. Some from CH. Minimal from JS (park name, some section names, the JFK shot dead idea with help from CH, and checking over descriptions because RS forced JS to). Credit to classmate KC for coming up with the name "Commie Square".
- Drawings: Mostly CH. Some from JS (the grass, the section banner labels, the park title, the guest description design, the guest list and exit buttons, the hydrogen bomb souvenir, and the Berlin airplane chocolate dropper). RS made the menus. Credit to other classmate JI for helping adjust the walking person outline.
- Programming: JS. Credit to JL (also not in the group) for helping fix an error (it was only one word that had to be changed, but the one word was very crucial).

Completed after two nights of staying up until 6 AM because three days were lost due to a competition. :D JS thanks CH for staying up with JS until almost 6 AM the second day to finish most of the drawings.

***
