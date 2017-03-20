#Escape The Haunted House V1.2
#Eric Peterson 2/19/2017

#Find Player's Position In House
def where_is_player(x,y):
    # Check coordinates and return room name
    # If the coordinates are OOB, return No Move which will
    # kill the program once it returns and kick out an Error
    # message.

    if (x == 0):
        if (y == 2):
            return "Study"
        else:
            return "No Move"
    elif (x == 1):
        if (y == 0):
            return "Entrance"
        elif (y == 1):
            return "North Hall"
        elif (y == 2):
            return "South Hall"
        elif (y == 3):
            return "Dining Room"
        elif (y == 4):
            return "Kitchen"
        elif (y == 5):
            return "Basement"
        else:
            return "No Move"
    elif (x == 2):
        if (y == 0):
            return "Coat Room"
        elif (y == 2):
            return "Bedroom"
        else:
            return "No Move"
    elif (x == 3):
        if (y == 2):
            return "Dungeon"
        else:
            return "No Move"
    else:
        return "No Move"

# Examine or look at item or object
def examine(item, player_inventory, room_inventory, room_contents, descriptions):

    item_present = (item in player_inventory or item in room_inventory or item in room_contents)

    if item_present:
        print descriptions[item]
    else:
        print "I don't see %s here." % item

    return

# Pick up item from room and place in player inventory
def Pick_up (player_inventory, room_inventory, item):
    # Check to see if item is in room. If it is, add it to the player's
    # inventory and remove it from the room's inventory. Tell player that
    # the item has been picked up. Otherwise, change nothing and inform player
    # that item is not in the room. Return both inventories.
    i = item
    if item in room_inventory:

        player_inventory.append(i)
        room_inventory.remove(i)
        print "You pick up the %s" % i
        return (player_inventory, room_inventory)

    else:
        print "I don't see %s here." % item

    return (player_inventory, room_inventory)

# Drop item from player inventory into room
def drop_item (player_inventory, room_inventory, item):
    # Check to see if item is in player inventory. If it is, add it to the
    # room's inventory and remove it from the player's. Inform player that
    # the item has been dropped. Otherwise, change nothing and inform player
    # that player is not carrying the item.

    if (item in player_inventory):

        room_inventory.append(item)
        player_inventory.remove(item)
        print "You drop the %s" % item
        return (player_inventory, room_inventory)

    else:
        print "You aren't carrying %s" % item

    return (player_inventory, room_inventory)

# Throw item
def throw_item (player_inventory, room_inventory, player_input,
room_contents, room_puzzle):
    # Check to see if item is in player inventory
    # Check to see if there is a target. Note, throw will only
    # be called from parse_2 or parse_4

    if (len(player_input) == 4):
        return

    elif (len(player_input) == 2):

        if (player_input[1] in player_inventory):
            room_inventory.append(player_input[1])
            player_inventory.remove(player_input[1])
            print "You throw the %s. It falls to the ground." % player_input[1]

        else:
            print "You are not carrying the %s." % player_input[1]

    else:
        print "Your command makes no sense."

    return (player_inventory, room_inventory, room_puzzle)

# Push, pull, or move object in room.
def move(player_input, room_contents, room_inventory, room_puzzle):
    return

# Handle fatal player actions
def player_death():
    # Kill player and game (placeholder)
    dead()

# Break player input into words and return that list along with the
# number of words in the list.
def parse_input(player_input):
    parsed_words = player_input.split(' ')
    parsed_length = len(parsed_words)
    return parsed_words, parsed_length

# Parse two word commands
def parse_two(player_input, room_name, room_inventory,
player_inventory, room_contents, room_puzzle, room_exits, descriptions):

    # Look for verbs used in two word commands. Commands that could see
    # a lot of use or do something that has an effect no matter where or
    # what the player is working with have their own functions.
    throw = (player_input[0] == 'THROW' or player_input[0] == 'HURL')

    examine = (player_input[0] == "EXAMINE" or player_input[0] == "INSPECT")

    move = (player_input[0] == "PUSH" or player_input[0] == "MOVE"
    or player_input[0] == "PULL")

    hit = (player_input[0] == "HIT" or player_input[0] == "STRIKE"
    or player_input[0] == "ATTACK")

    drop = (player_input[0] == "DROP" or player_input[0] == "PLACE")

    fire = (player_input[1] == "FIRE" or player_input[1] == "FIREPLACE"
    or player_input[1] == "MATCH")

    show = (player_input[0] == "SHOW" or player_input[0] == "DISPLAY")

    draw = (player_input[0] == "DRAW" or player_input[0] == "INSCRIBE")

    if (player_input[0] == "GET"):
        (player_inventory, room_inventory) = Pick_up(player_inventory,
        room_inventory, player_input[1])

    elif (throw):
        (player_inventory, room_inventory) = throw(player_inventory,
        room_inventory, player_input[1])

    elif (examine):
        examine(player_input[1], player_inventory, room_inventory,
        room_contents, descriptions)

    elif (move):
        (room_puzzle, room_exits) = move(player_input, room_contents,
        room_inventory, room_puzzle)

    elif (hit):
        (room_puzzle, room_contents, descriptions) = hit(player_input, player_inventory,
        room_contents, room_inventory, room_puzzle, descriptions)

    elif (drop):
        (player_inventory, room_inventory) = drop_item(player_inventory,
        room_inventory, player_input[1])

    elif (player_input[0] == "SEARCH"):
        coats = (player_input[1] == "COATS" or player_input[1] == "PILE")
        books = (player_input[1] == "BOOKS" or player_input[1] == "BOOKSHELF")

        if (coats and room_name == 'Coat Room' and room_puzzle[1] == False):

            print "You search the pile of coats furiously ..."
            print "\n Exhausted, you are about to give up ..."
            print "\n A box of matches falls out of a coat pocket."

            room_inventory.append('MATCHES')
            room_puzzle[1] = True

        elif (books and room_name == 'Study' and room_puzzle[1] == False):

            print "You start flipping through the books on the shelf"
            print "hoping to find some clue. Page after page, book after book,"
            print "your vision starts to blur and it gets difficult to focus"
            print "until a single page flutters to the floor from the book"
            print "you are currently holding."

            room_inventory.append('PAGE')
            room_puzzle[1] = True

        else:
            print "You search %s, but it proves fruitless." % player_input[1]

    elif (player_input[0] == "LIGHT" and fire):

        have_matches == ('MATCHES' in player_inventory)

        if (have_matches and room_name == "Coat Room"):

            print "There's a whiff of sulfur as you light a match."
            print "Something jostles you, causing you to drop it into"
            print "the moldy pile of coats. The mold combusts and flames"
            print "fill the room. Thick, black smoke overwhelms you and"
            print "you sink to the floor, choking as the world goes back."
            print "Years later, they find your charred remains, still"
            print "reaching for the door."

            player_death()

        elif (have_matches and "FIREPLACE" in room_contents and !room_puzzle[1]):

            print "You light the match and watch it flare, the flames dancing"
            print "around the head of the match. You throw it in the fireplace"
            print "and it roars to life. The room grows warm at an unnatural"
            print "rate and a little dread is lifted from your soul. Something"
            print "falls from the flames and lands at your feet."

            room_puzzle[1] = True
            room_inventory.append("CHARCOAL")

        elif (have_matches):
            print "You light the match and watch it flare. Eventually it fades"
            print "and goes out."

        else:
            print "With what?"

    elif (player_input[0] == "READ"):

        book = (player_input[1] == "BOOK" or player_input[1] == "HIDEBOUND BOOK")
        page = (player_input[1] == "PAGE")
        book_present = ("HIDEBOUND BOOK" in room_inventory
        or "HIDEBOUND BOOK" in player_inventory)
        page_present = ("PAGE" in room_inventory or "PAGE" in player_inventory)

        if (book and book_present):
            print """
            BOOK TEXT (PLACEHOLDER)
            """
        elif (page and page_present):
            print "There's no writing, only a diagram."

        elif (book and room_name == "Study"):
            print "It would take you forever to read all these."
        else:
            print "Nothing to read here."

    elif (show):
        has_locket = ("LOCKET" in player_inventory)
        has_blessed_locket = ("BLESSED LOCKET" in player_inventory)
        ghost_present = ("GHOST" in room_contents)

        if (has_locket and ghost_present):

            print "The ghost looks forelornly at the locket but makes no move."

        elif (has_blessed_locket and ghost_present):

            print """
            The ghost reaches toward you, but you hold up the glowing curio
            and she backs off. The glow intensifies, engulfing her in a bright,
            white light. She screams as her incorporeal form disintigrates
            before your eyes. The oppressive atmosphere of the house falls
            away, leaving you with nothing between yourself and freedom.
            """
            room_puzzle[1] == True
            room_exits.append["SOUTH"]
            room_exits.append["S"]

        else:
            print "Nothing happens."
            print "You feel kind of stupid holding up this %s" % player_input[1]

    elif (draw and player_input[1] == "DIAGRAM"):
        page_present = ("PAGE" in room_inventory or "PAGE" in player_inventory)
        charcoal_present = ("CHARCOAL" in player_inventory)

        if (page_present and charcoal_present and room_name = "South Hall"):

            print """
            DRAWING TEXT (Placeholder)
            """
            room_puzzle[1] = True

        elif (charcoal_present and room_name = "South Hall"):

            print """
            You try to draw the diagram from memory, but it is far too complicated.
            As you finish, the ghost appears, a cadaverous female apparition with
            talons for hands. She rends you limb from limb and you die in agony.
            """
            player_death()

        elif (charcoal_present):

            print """
            You spend some time doodling on various objects and the walls. It
            leads no where. You should probably get back to the task at hand.
            """
        else:
            print "You have nothing to draw with."

    return (player_inventory, room_inventory, room_contents,
            room_puzzle, room_exits, descriptions)


# Most complicated part of game. Take player input and parse it, then
# compare actions to room contents, inventory, and puzzle and return
# the values of those.
def parser (player_input, room_name, room_inventory,
player_inventory, room_contents, room_puzzle, room_exits, descriptions):

    # Break up player input with the parse_input function
    parsed_words, parsed_length = parse_input(player_input)

    # Look for two word commands and send to parser. Return an
    # error message if player tries to use more (or less) words.
    if (parsed_length == 2):

        (player_inventory, room_inventory, room_contents,
        room_puzzle, room_exits, descriptions) = parse_two(parsed_words,
        room_name, room_inventory, player_inventory, room_contents, room_puzzle,
        room_exits, descriptions)
    else:
        print "I don't understand what you are trying to say."
        print "Use only two words, please."

    return (player_inventory, room_inventory, room_contents,
           room_puzzle, room_exits, descriptions)


# Run the room indicated by player position
def room (room_desc, room_inventory, room_contents, room_puzzle, room_name,
player_inventory, player_pos_x, player_pos_y, room_exits, descriptions):

    # Loop function while player remains in room or quits game.
    while True:

        # Takes room variables and provides handling for player action in
        # each specific room.
        print "\n****** %s ******" % room_name
        print room_desc
        print room_contents

        # Check to see if the room puzzle has been solved and display
        # the correct description.

        if (room_puzzle[1] == True):
            print room_puzzle[2]
        else:
            print room_puzzle[0]

        # Display the room inventory.
        print "The following are lying on the ground:"
        print room_inventory

        # Display exits
        print "There are exits to the:"
        print room_exits

        #Prompt player for input. Capitalize input to standardize
        #it and make parsing easier.
        player_raw = str(raw_input(">>"))
        player_input = player_raw.upper()

        # Check to see if player wants to quit
        if (player_input == "QUIT"):
            quit("Goodbye and thanks for playing.")

        # Check to see if player wants to view inventory
        if (player_input == "INVENTORY" or player_input == "I"):
            print "You are carrying:\n"
            print player_inventory
            return (player_pos_x, player_pos_y, player_inventory,
            room_inventory, room_contents, room_puzzle, descriptions)

        #Debugging code for tracking player location
        #print "Current location: x:%r, y:%r" % (player_pos_x,
        #player_pos_y)

        # Check to see if player wants to move. If so, move player
        # and go back to room selection. Note that south is positive
        # and North is negative in this game since the player is working
        # their way south toward the ultimate exit.
        if (player_input in room_exits):

            if (player_input == "NORTH" or player_input == "N"):

                player_pos_y -= 1

                return (player_pos_x, player_pos_y, player_inventory,
                room_inventory, room_contents, room_puzzle, descriptions)

            elif (player_input == "SOUTH" or player_input == "S"):
                player_pos_y += 1

                return (player_pos_x, player_pos_y, player_inventory,
                room_inventory, room_contents, room_puzzle, descriptions)

            elif (player_input == "EAST" or player_input == "E"):
                player_pos_x += 1

                return (player_pos_x, player_pos_y, player_inventory,
                room_inventory, room_contents, room_puzzle, descriptions)

            elif (player_input == "WEST" or player_input == "W"):
                player_pos_x -= 1

                return (player_pos_x, player_pos_y, player_inventory,
                room_inventory, room_contents, room_puzzle, descriptions)

            else:
                print "There is no exit in that direction."
                return (player_pos_x, player_pos_y, player_inventory,
                room_inventory, room_contents, room_puzzle, descriptions)
        else:
            (player_inventory, room_inventory, room_contents,
            room_puzzle, room_exits, descriptions) = parser(player_input, room_name,
            room_inventory, player_inventory, room_contents,
            room_puzzle, room_exits, descriptions)

# Set up room variables and player defaults

# Entrance
entrance_desc = """
Stone flooring radiates unforgiving cold and the gray walls seem to sap all
color from the room. The door behind you is shut tightly. """
entrance_exits = ['SOUTH', 'S', 'EAST', 'E']
entrance_inventory = ['FLASHLIGHT','ROCK']
entrance_contents = ['FIREPLACE']
entrance_puzzle = ['The fireplace is cold.', False,
'Fire crackles wildly in the fireplace.']

# Coat Room
coat_room_desc = """
This room is almost a closet and moldy coats are piled haphazardly on the floor.
A large coat rack leans against the far wall. """
coat_room_exits = ['WEST', 'W']
coat_room_inventory = []
coat_room_contents = ['COAT RACK']
coat_room_puzzle = ['The pile of coats lies undisturbed', False,
'Coats are strewn across the room.']

# North Hall
north_hall_desc = """Ancient suits of armor line the walls as the hallway
disappears into apparent darkness. There are no doors, only faded portraits
and crests. Dust is thick in the chill air."""
north_hall_exits = ['NORTH', 'N', 'SOUTH', 'S']
north_hall_inventory = []
north_hall_contents = ['ARMOR']
north_hall_puzzle = ['A strange suit of armor stands here.', False,
'A strange suit of armor, now missing an arm, stands here.']

# South Hall
south_hall_desc = """The further in you go, the more the malevolence of this
place engulfs you. Doors lie at the end."""
south_hall_exits = ['NORTH', 'N', 'SOUTH', 'S', 'EAST', 'E', 'WEST', 'W']
south_hall_inventory = []
south_hall_contents = ['STRANGE PAINTING']
south_hall_puzzle = ['The floor is surprisingly smooth here.', False,
'An intricate design has been drawn on the floor in chalk.']

# Study
study_desc = """There is a thick coating of dust on every surface here, pristine
and undisturbed. Bookshelves line the walls and a small reading table occupies
the far corner."""
study_exits = ['EAST', 'E']
study_inventory = ['HIDEBOUND BOOK']
study_contents = ['BOOKSHELF']
study_puzzle = ['The bookshelf is full of books.', False,
 'Books are piled on the floor.']

# Bedroom
bedroom_desc = """A large, four poster bed dominates the center of the room. It
is flanked by a large vanity on one side and an immense chest of drawers on the
other side. The bed sheets are stained brown and brittle, soaked through with
old blood."""
bedroom_exits = ['EAST', 'E', 'WEST', 'W']
bedroom_inventory = []
bedroom_contents = ['DRESSER']
bedroom_puzzle = ['The dresser lies flat against the far wall. ', False,
'The dresser has been moved rom the wall, exposing a new door. ']

# Dungeon
dungeon_desc = """The stink of this room hits you like a sledgehammer. Every
inch seems to be stained. The cold stone all but glows with malevolence."""
dungeon_exits = ['WEST', 'W']
dungeon_inventory = []
dungeon_contents = ['SHACKLES', 'SKELETON']
dungeon_puzzle = ['A female skeleton hangs, shackled to the wall.', False,
'The remains of a female skeleton litter the floor.']

# Dining Room
dining_room_desc = """The last meal of whoever owned this house lies on the
table, green with mold and smelling strongly of decay."""
dining_room_exits = ['NORTH', 'N', 'SOUTH', 'S']
dining_room_inventory = ['KNIFE']
dining_room_contents = ['SERVING DISH']
dining_room_puzzle = ['One serving dish remains covered.', False,
'A rotted head looks up at you from the table, eyes blank and ruined.']

# Kitchen
kitchen_desc = """The kitchen is a wreck. It looks as if there was a fight here,
and someone came out the definite loser. Old bloodstains abound from counter to
floor."""
kitchen_exits = ['NORTH', 'N', 'SOUTH', 'S']
kitchen_inventory = []
kitchen_contents = ['OVEN', 'BASEMENT DOOR']
kitchen_puzzle = ['The oven is strangely warm.', False,
 'The oven is now cold and lifeless.']

# Basement
basement_desc = """Dank and cold, the basement smells of earth and old wood.
At the far end is a door leading out to salvation."""
basement_exits = ['NORTH', 'N']
basement_inventory = []
basement_contents = ['GHOST']
basement_puzzle = ['The ghost howls, \'You will join me!\'', False,
'The way out is clear.']

# Player Starting Position
player_pos_x = 1
player_pos_y = 0

# Player inventory
player_inventory = []

# Store descriptions in a dictionary for 'examine'
# Descriptions can be changed.

descriptions = {
'FLASHLIGHT': """A standard D-Cell flashlight. It is off.""",

'FIREPLACE': """The fireplace is old and soot covered. A loose brick
is visible above the mantle.""",

'DRESSER': """An antique chest of drawers made from dark wood with a satin
finish. The floor underneath is heavily scraped""",

'FLOOR': """The floor is made of the same gray brick as the rest of the
house.""",

'COAT RACK': """There's a heavy fur coat dangling from one peg.""",

'ARMOR': """A medeival suit of armor held together by pins. One arm appears
to be loose.""",

'HIDEBOUND BOOK': """An old, heavy tome wrapped in thin, almost paper-like leather.
Best not to ask what animal it came from.""",

'PAGE': """This page has seen better days. There's an intricate diagram inscribed
on it.""",




}

Loc_map = {(0,2): 'Entrance', (0,1): 'Coat Room'}
# Main Part of Program

# Show Intro When Game Starts
print """The path is wooded and moonlight streams in sharp lines through the
dead tree branches. Your heart thunders in your chest as you run, pursued
by a howling apparition you can not see, but you can certainly feel. It's
malevolence is palatible, driving you further, faster. Up ahead you see a
house. The door is open and a sickly yellow light becons from within.
Grasping at that lifeline, you barrel through the entrance. The door slams
shut behind you, leaving you panting in the eerie half light. The musty
smell of the place nearly overwhelms you. As you gasp for air you hear a
high-pitched, peeling laugh echo through the house. Instinctively, you
know you must escape ...\n\nWELCOME TO:\nESCAPE FROM THE HAUNTED HOUSE"""

# Loop while playing the game.
while True:
    # Find the location of the player in the house.
    room_name = where_is_player(player_pos_x, player_pos_y)

    # Run room function with data for room player is in.
    if (room_name == "Entrance"):

        (player_pos_x, player_pos_y, player_inventory, entrance_inventory,
        entrance_contents, entrance_puzzle, descriptions) = room(entrance_desc,
        entrance_inventory, entrance_contents, entrance_puzzle, room_name,
        player_inventory, player_pos_x, player_pos_y, entrance_exits, descriptions)

    elif (room_name == "Coat Room"):

        (player_pos_x, player_pos_y, player_inventory, coat_room_inventory,
        coat_room_contents, coat_room_puzzle, descriptions) = room(coat_room_desc,
        coat_room_inventory, coat_room_contents, coat_room_puzzle, room_name,
        player_inventory, player_pos_x, player_pos_y, coat_room_exits, descriptions)

    elif (room_name == "North Hall"):

        (player_pos_x, player_pos_y, player_inventory, north_hall_inventory,
        north_hall_contents, north_hall_puzzle, descriptions) = room(north_hall_desc,
        north_hall_inventory, north_hall_contents, north_hall_puzzle, room_name,
        player_inventory, player_pos_x, player_pos_y, north_hall_exits, descriptions)

    elif (room_name == "South Hall"):

        (player_pos_x, player_pos_y, player_inventory, south_hall_inventory,
        south_hall_contents, south_hall_puzzle, descriptions) = room(south_hall_desc,
        south_hall_inventory, south_hall_contents, south_hall_puzzle, room_name,
        player_inventory, player_pos_x, player_pos_y, south_hall_exits, descriptions)

    elif (room_name == "Study"):

        (player_pos_x, player_pos_y, player_inventory, study_inventory,
        study_contents, study_puzzle, descriptions) = room(study_desc,
        study_inventory, study_contents, study_puzzle, room_name,
        player_inventory, player_pos_x, player_pos_y, study_exits, descriptions)

    elif (room_name == "Bedroom"):

        (player_pos_x, player_pos_y, player_inventory, bedroom_inventory,
        bedroom_contents, bedroom_puzzle, descriptions) = room(bedroom_desc,
        bedroom_inventory, bedroom_contents, bedroom_puzzle, room_name,
        player_inventory, player_pos_x, player_pos_y, bedroom_exits, descriptions)

    elif (room_name == "Dungeon"):

        (player_pos_x, player_pos_y, player_inventory, dungeon_inventory,
        dungeon_contents, dungeon_puzzle, descriptions) = room(dungeon_desc,
        dungeon_inventory, dungeon_contents, dungeon_puzzle, room_name,
        player_inventory, player_pos_x, player_pos_y, dungeon_exits, descriptions)

    elif (room_name == "Dining Room"):

        (player_pos_x, player_pos_y, player_inventory, dining_room_inventory,
        dining_room_contents, dining_room_puzzle, descriptions) = room(dining_room_desc,
        dining_room_inventory, dining_room_contents, dining_room_puzzle,
        room_name, player_inventory, player_pos_x, player_pos_y,
        dining_room_exits, descriptions)

    elif (room_name == "Kitchen"):

        (player_pos_x, player_pos_y, player_inventory, kitchen_inventory,
        kitchen_contents, kitchen_puzzle, descriptions) = room(kitchen_desc,
        kitchen_inventory, kitchen_contents, kitchen_puzzle, room_name,
        player_inventory, player_pos_x, player_pos_y, kitchen_exits, descriptions)

    elif (room_name == "Basement"):

        (player_pos_x, player_pos_y, player_inventory, basement_inventory,
        basement_contents, basement_puzzle, descriptions) = room(basement_desc,
        basement_inventory, basement_contents, basement_puzzle, room_name,
        player_inventory, player_pos_x, player_pos_y, basement_exits, descriptions)

    else:
        print "You are in a nonexistant area. Goodbye!"
        print "Error: Player out of bounds."
        quit()
