# LPTHW
LPTHW EX 36 Game (Escape From The Haunted House)
Repository for LPTHW projects. First project is from EX 36.

The project involves writing a game similar to EX 35, but improving over about a weeks worth of time. I decided to craft a game closer to the old Scott Adams adventures, albeit much shorter. Instead of making every room a function with an optimal input that takes the player to the next room like EX 35, I opted for a free flowing map that allows the player to move throughout the house.

Some Design Decisions I Made
* I settled on a generic room function that takes room descriptors and attributes as arguments. Room attributes are laid out as follows:

Entrance

entrance_desc = """
Stone flooring radiates unforgiving cold and the gray walls seem to sap all
color from the room. The door behind you is shut tightly. """

entrance_exits = ['SOUTH', 'S', 'EAST', 'E']

entrance_inventory = []

entrance_contents = ['FIREPLACE']

entrance_puzzle = ['The fireplace is cold.', False,
'Fire crackles wildly in the fireplace.']

I wanted to avoid using global variables, but still wanted some permenance to actions the player takes. The downside is that there are a lot of variables to keep track of and pass back and forth between functions.

* I wanted an actual parser rather than each room having it's own interactions

I originally decided on wanting the parser to handle 2 to 4 word commands, but realized that it was a bit too much work given the scope of the game. A two word parser works fine for the complexity level of this project. The room function handles some commands (Inventory, Quit, and Movement). Everything else is passed to the parser function which splits up the words and handles interpretation. It's designed to spit back an error message of some sort if the command makes no sense or is more than 2 words long.

* I wanted the player to be able to change the environment in a limited fashion

This goes back to some of the old adventure games where actions had permenance. With that in mind, I set up the room_puzzle list as as a sort of switch. It starts off, which triggers the room function to display the first string. Once the room puzzle is solved, the switch is flipped to true and the second string is displayed. Certain actions also produce items, change descriptions, or add exits.
