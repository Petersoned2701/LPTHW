###############################################################################
# Escape The Haunted House V1.3
# A Simple Text Adventure
# Eric Peterson 2/19/2017
###############################################################################

# Find Player's Position In House
def where_is_player(x,y):
    #########################################################################
    # Check coordinates and return room name
    # If the coordinates are OOB, return No Move which will
    # kill the program once it returns and kick out an Error
    # message.
    #########################################################################
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
        elif (y == 6):
            return "Escape"
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
        try:
            print descriptions[item]
        except:
            pass
    else:
        print "I don't see %s here." % item

    return

# Pick up item from room and place in player inventory
def Pick_up (player_inventory, room_inventory, item):

    #########################################################################
    # Check to see if item is in room. If it is, add it to the player's
    # inventory and remove it from the room's inventory. Tell player that
    # the item has been picked up. Otherwise, change nothing and inform player
    # that item is not in the room. Return both inventories.
    #########################################################################

    if item in room_inventory:

        player_inventory.append(item)
        room_inventory.remove(item)
        print "You pick up the %s" % item
        return (player_inventory, room_inventory)

    else:
        print "I don't see %s here." % item

    return (player_inventory, room_inventory)

# Drop item from player inventory into room
def drop_item (player_inventory, room_inventory, item):

    ##########################################################################
    # Check to see if item is in player inventory. If it is, add it to the
    # room's inventory and remove it from the player's. Inform player that
    # the item has been dropped. Otherwise, change nothing and inform player
    # that player is not carrying the item.
    ##########################################################################

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

    blessed_locket = (player_input[1] == "BLESSED LOCKET")
    locket = (player_input[1] == "LOCKET")
    ghost_present = ("GHOST" in room_contents)

    # Check to see if item is in player inventory
    if (player_input[1] in player_inventory):

        if (locket and ghost_present):
            print "You throw the locket at the ghost."
            print "She seems to cringe, although it's hard to tell given"
            print "her spectral form. You wait in breathless anticipation"
            print "as it makes contact.\n"
            print "It passes through her and falls to the floor."
            print "But that is the least of your worries. She turns on you,"
            print "snarling. Her talons are like hot knives, rending your"
            print "flesh from your bones. Your agony lasts for an enternity."

            player_death()

        elif (blessed_locket and ghost_present):

            print """
            The ghost reaches toward you, but you throw the gloing curio at her.
            The glow intensifies, engulfing her in a bright, white light.
            She screams as her incorporeal form disintigrates before your eyes.
            The oppressive atmosphere of the house falls away, leaving you with
            nothing between yourself and freedom. The locket lies on the ground,
            still glowing.
            """
            room_inventory.append(player_input[1])
            player_inventory.remove(player_input[1])
            room_contents.remove('GHOST')
            room_exits.append("SOUTH")
            room_exits.append("S")
        else:
            print "You throw the %s. It falls to the ground." % player_input[1]

    else:
            print "You are not carrying the %s." % player_input[1]

    return (player_inventory, room_inventory, room_puzzle)

# Push, pull, or move object in room.
def move_object(player_input, room_contents, room_inventory, room_puzzle,
                room_exits, descriptions):

    dresser_present = 'DRESSER' in room_contents
    armor_present = 'ARMOR' in room_contents
    pull_arm = player_input[1] == 'ARM'

    if dresser_present and room_puzzle[1] == False:
        print "With a grunt, you push and pull on the dresser."
        print "It's heavy, real heavy, but, just when you think"
        print "it's never going to move, it starts to slide."
        print "As it moves away from the wall, you see the faint outline"
        print "of a door."

        room_puzzle[1] = True
        room_exits.append('EAST')
        room_exits.append('E')

    elif armor_present and pull_arm and room_puzzle[1] == False:
        print "You jostle the arm and work on it, the metal shrieking at"
        print "you as it resists and scrapes. With a final effort, you free"
        print "the appendage from the steel body. Congradulations, you now"
        print "have an arm."

        descriptions['ARMOR'] = """
        A medeival suit of armor held together by pins. It's missing an arm.
        """
        player_inventory.append('ARM')
        room_puzzle[1] = True

    else:
        print "You push, pull, and swear, but %s does not move." % player_input[1]

    return (room_puzzle, room_exits, descriptions)

# Player tries to hit something.
def hit(player_input, player_inventory, room_contents, room_inventory,
        room_puzzle, descriptions):

        target_skel = player_input[1] == "SKELETON"
        has_arm = "ARM" in player_inventory

        if has_arm and target_skel and "SKELETON" in room_contents:

            if room_puzzle[1] == False:

                print "You secure a two-handed grip on the metal arm and swing with"
                print "all of your might. The skull flies off, chips scattering"
                print "across the cold, gray floor. You swing again, shattering"
                print "the rib cage. A small metal object tumbles to the floor,"
                print "free from its cage of bones."

                room_inventory.append("LOCKET")
                descriptions["SKELETON"] = """
                Only about half of a skeleton lies here, the rest is strewn
                around the dungeon.
                """
            else:
                print "You pound on the Skeleton some more, happy now?"

        elif target_skel:

            print "You hit the skeleton, but all you end up with are bruises."
            print "You're going to need something else to hit it with."

        else:

            print "You hit %s, but it doesn't do anything." % player_input[1]
            print "Have you considered anger management classes?"

        return (room_puzzle, room_contents, descriptions)

# Handle fatal player actions
def player_death():

    # Kill player and game (placeholder)
    print "You have died. Your soul will forever haunt this place,"
    print "eternally tormented by the ghost. Sorry!"
    quit ("Goodbye!")
    return

# Break player input into words and return that list along with the
# number of words in the list.
def parse_input(player_input):
    parsed_words = player_input.split(' ')
    parsed_length = len(parsed_words)
    return parsed_words, parsed_length

# Parse two word commands
def parse_two(player_input, room_name, room_inventory,
player_inventory, room_contents, room_puzzle, room_exits, descriptions):

    ##########################################################################
    # Look for verbs used in two word commands. Commands that could see
    # a lot of use or do something that has an effect no matter where or
    # what the player is working with have their own functions.
    #########################################################################

    throw = (player_input[0] == 'THROW' or player_input[0] == 'HURL')

    inspect = (player_input[0] == "EXAMINE" or player_input[0] == "INSPECT")

    move = (player_input[0] == "PUSH" or player_input[0] == "MOVE"
    or player_input[0] == "PULL")

    strike = (player_input[0] == "HIT" or player_input[0] == "STRIKE"
    or player_input[0] == "ATTACK")

    drop = (player_input[0] == "DROP" or player_input[0] == "PLACE")

    fire = (player_input[1] == "FIRE" or player_input[1] == "FIREPLACE"
    or player_input[1] == "MATCH")

    show = (player_input[0] == "SHOW" or player_input[0] == "DISPLAY")

    draw = (player_input[0] == "DRAW" or player_input[0] == "INSCRIBE")

    lift = (player_input[0] == "LIFT" or player_input[0] == "RAISE")

    get = (player_input[0] == "GET" or player_input[0] == "GRAB")

    remove = (player_input[0] == "REMOVE" or player_input[0] == "DETACH")

    open_1 = (player_input[0] == "OPEN")

    basement_door = (player_input[1] == "DOOR" or player_input[1] == "BASEMENT DOOR")

    if (get):
        (player_inventory, room_inventory) = Pick_up(player_inventory,
        room_inventory, player_input[1])

    elif (throw):
        (player_inventory, room_inventory) = throw(player_inventory,
        room_inventory, player_input[1])

    elif (inspect):
        examine(player_input[1], player_inventory, room_inventory,
        room_contents, descriptions)

    elif (move):
        (room_puzzle, room_exits, descriptions) = move_object(player_input,
        room_contents, room_inventory, room_puzzle, room_exits, descriptions)

    elif (strike):
        (room_puzzle, room_contents, descriptions) = hit(player_input, player_inventory,
        room_contents, room_inventory, room_puzzle, descriptions)

    elif (drop):

        is_locket = player_input[1] == "LOCKET" and "LOCKET" in player_inventory
        diagram_drawn = "DIAGRAM" in room_contents

        if is_locket and diagram_drawn:

            print """
            You drop the locket into the center of the diagram. A howling wind
            whips up around you, threatening to push you down the hall. It
            starts to abate as the locket shakes. Soon, a warm light emminates
            from the locket and the wind ceases.
            """

            player_inventory.remove("LOCKET")
            room_inventory.append("BLESSED LOCKET")

        else:
            (player_inventory, room_inventory) = drop_item(player_inventory,
            room_inventory, player_input[1])

    elif (player_input[0] == "SEARCH"):

        coats = (player_input[1] == "COATS" or player_input[1] == "PILE" or player_input[1] == "COAT PILE")
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

        have_matches = ('MATCHES' in player_inventory)

        if (have_matches and room_name == "Coat Room"):

            print "There's a whiff of sulfur as you light a match."
            print "Something jostles you, causing you to drop it into"
            print "the moldy pile of coats. The mold combusts and flames"
            print "fill the room. Thick, black smoke overwhelms you and"
            print "you sink to the floor, choking as the world goes back."
            print "Years later, they find your charred remains, still"
            print "reaching for the door."

            player_death()

        elif (have_matches and "FIREPLACE" in room_contents and room_puzzle[1] == False):

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
            The pages are yellow with age and made of some material you can't
            quite place. One page is ripped out. The facing page details a
            ritual for exorcising ghosts. The details are fairly simple, you
            need something the ghost owned in life, and a smooth surface in
            its domain to draw a diagram on. The diagram must be drawn in
            charcoal produced at the place the ghost resides. All you need to
            do is place the object in the diagram and it will be blessed with
            the ability to eliminate the ghost. Of course, the page that was
            ripped out contained the diagram you need.
            """
        elif (page and page_present):
            print """
            The page contains an intricate, mindbending design that resembles
            Celtic art. Each line intersects a number of others, forming a
            complex basket-like image on the page. The longer you stare, the
            more disoriented you become, as if your brain is struggling to
            interpret what it's seeing. """

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
            room_contents.remove('GHOST')
            room_exits.append("SOUTH")
            room_exits.append("S")

        else:
            print "Nothing happens."
            print "You feel kind of stupid holding up this %s" % player_input[1]

    elif (draw and player_input[1] == "DIAGRAM"):
        page_present = ("PAGE" in room_inventory or "PAGE" in player_inventory)
        charcoal_present = ("CHARCOAL" in player_inventory)

        if (page_present and charcoal_present and room_name == "South Hall"):

            print """
            You work furiously, seemingly possessed by what's on the page.
            Once finished, you step back and are surprised to find you have
            copied the diagram exactly. Your hands are black with charcoal.
            """
            room_puzzle[1] = True
            room_contents.append("DIAGRAM")
            descriptions['DIAGRAM'] = """
            An impossibly intricate diagram is drawn in charcoal on the floor
            here.
            """

        elif (charcoal_present and room_name == "South Hall"):

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

    elif (lift):

        if (room_name == "Dining Room" and player_input[1] == "COVER"):

            print "Hesitantly, you reach for the pewter cover ..."
            print "The handle is slick in you hands, but you lift ..."
            print "As the cover clears the plate you are greeted with ..."
            print "A decaying, severed head. You drop the cover."

            room_puzzle[1] = True
            room_contents.append("SEVERED HEAD")
            descriptions["SERVING DISH"] = """
            On the dish lies a severed, male head. Old blood covers every inch
            of it's formerly white surface. The cover lies on the table."""

    elif (open_1 and player_input[1] == 'MOUTH'):

        if ('SEVERED HEAD' in room_contents and ('KEY' not in room_contents or 'KEY' not in player_inventory)):

            print "Gingerly, you pry open the mouth as it's rotted lips ooze"
            print "pustulence over your fingers. Your hands grasp something"
            print "cold and hard. Plucking it out, you are now holding a key."

            player_inventory.append('KEY')

        else:
            print "You open your mouth. You should close it before you eat a fly."

    elif (open_1 and basement_door):

        door_present = "BASEMENT DOOR" in room_contents
        key_present = "KEY" in player_inventory

        if door_present and key_present and room_puzzle[1] == False:
            print "You insert the heavy, metal key into the old fashioned"
            print "lock and twist. It resists at first, groaning as it"
            print "slowly turns. Eventually, it clicks and the door seems"
            print "to swing open of it's own volition."

            room_puzzle[1] = True
            room_exits.append("SOUTH")
            room_exits.append("S")

        elif key_present:
            print "The key doesn't fit any door in this room."

        else:
            print "I don't see the door here."


    return (player_inventory, room_inventory, room_contents,
            room_puzzle, room_exits, descriptions)

#############################################################################
# Most complicated part of game. Take player input and parse it, then
# compare actions to room contents, inventory, and puzzle and return
# the values of those.
#############################################################################

def parser (player_input, room_name, room_inventory,
player_inventory, room_contents, room_puzzle, room_exits, descriptions):

    # Break up player input with the parse_input function
    parsed_words, parsed_length = parse_input(player_input)

    # Store adjectives used in game as a list for comparison
    adjectives =  ['SERVING', 'SEVERED', 'HIDEBOUND', 'BLESSED',
    'STRANGE', 'BASEMENT', 'COAT']

    #######################################################################
    # Look for two word commands and send to parser. Return an
    # error message if player tries to use more (or less) words.
    #######################################################################

    if (parsed_length == 2):

        (player_inventory, room_inventory, room_contents,
        room_puzzle, room_exits, descriptions) = parse_two(parsed_words,
        room_name, room_inventory, player_inventory, room_contents, room_puzzle,
        room_exits, descriptions)

    ###########################################################################
    # Check to see if player has targeted one of the objects that is
    # described with two words in the game. If they have, combine the
    # two words and pass that to the parser along with the action.
    # The flow is as follows: "GET HIDEBOUND BOOK" is broken up into
    # "GET" "HIDEBOUND" "BOOK", since "HIDEBOUND" is an adjective used
    # by the game, the parser recombines the adjective/noun combo as one
    # element of the parsed_words list so it can be processed.
    ###########################################################################

    elif (parsed_length == 3 and parsed_words[1] in adjectives):

        parsed_words[1] = parsed_words[1] + ' ' + parsed_words[2]
        parsed_words.remove(parsed_words[2])

        (player_inventory, room_inventory, room_contents,
        room_puzzle, room_exits, descriptions) = parse_two(parsed_words,
        room_name, room_inventory, player_inventory, room_contents, room_puzzle,
        room_exits, descriptions)

    else:
        print "I don't understand what you are trying to say."

    return (player_inventory, room_inventory, room_contents,
           room_puzzle, room_exits, descriptions)


# Run the room indicated by player position
def room (room_desc, room_inventory, room_contents, room_puzzle, room_name,
player_inventory, player_pos_x, player_pos_y, room_exits, descriptions):

        #####################################################################
        # Takes room variables and provides handling for player action in
        # each specific room.
        #####################################################################

        print "\n****** %s ******" % room_name
        print room_desc
        print room_contents

        ######################################################################
        # Check to see if the room puzzle has been solved and display
        # the correct description.
        ######################################################################

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

    # Loop function while player remains in room or quits game.
        while True:

            # Prompt player for input. Capitalize input to standardize
            # it and make parsing easier.
            player_raw = str(raw_input(">>"))
            player_input = player_raw.upper()

            # Check to see if player wants to quit
            if (player_input == "QUIT"):
                quit("Goodbye and thanks for playing.")

            # Check to see if player wants to view inventory
            elif (player_input == "INVENTORY" or player_input == "I"):
                print "You are carrying:\n"
                print player_inventory

            # Player can refresh room description with Look command.
            elif (player_input == "LOOK" or player_input == "L"):
                return (player_pos_x, player_pos_y, player_inventory,
                room_inventory, room_contents, room_puzzle, descriptions)

            #Debugging code for tracking player location
            #print "Current location: x:%r, y:%r" % (player_pos_x,
            #player_pos_y)

            ##################################################################
            # Check to see if player wants to move. If so, move player
            # and go back to room selection. Note that south is positive
            # and North is negative in this game since the player is working
            # their way south toward the ultimate exit.
            ##################################################################

            elif (player_input in room_exits):

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
                room_puzzle, room_exits, descriptions) = parser(player_input,
                room_name, room_inventory, player_inventory, room_contents,
                room_puzzle, room_exits, descriptions)

# Function for player winning game and escaping.
def escape():

    print """
    You escape.
    """
    quit("You Win!")

    return

# Set up room variables and player defaults

############
# Entrance #
############
entrance_desc = """
Stone flooring radiates unforgiving cold and the gray walls seem to sap all
color from the room. The door behind you is shut tightly. """
entrance_exits = ['SOUTH', 'S', 'EAST', 'E']
entrance_inventory = []
entrance_contents = ['FIREPLACE']
entrance_puzzle = ['The fireplace is cold.', False,
'Fire crackles wildly in the fireplace.']

#############
# Coat Room #
#############
coat_room_desc = """
This room is almost a closet and moldy coats are piled haphazardly on the floor.
A large coat rack leans against the far wall. """
coat_room_exits = ['WEST', 'W']
coat_room_inventory = []
coat_room_contents = ['COAT PILE']
coat_room_puzzle = ['The pile of coats lies undisturbed', False,
'Coats are strewn across the room.']

##############
# North Hall #
##############
north_hall_desc = """Ancient suits of armor line the walls as the hallway
disappears into apparent darkness. There are no doors, only faded portraits
and crests. Dust is thick in the chill air."""
north_hall_exits = ['NORTH', 'N', 'SOUTH', 'S']
north_hall_inventory = []
north_hall_contents = ['ARMOR']
north_hall_puzzle = ['A strange suit of armor stands here.', False,
'A strange suit of armor, now missing an arm, stands here.']

##############
# South Hall #
##############
south_hall_desc = """The further in you go, the more the malevolence of this
place engulfs you. Doors lie at the end."""
south_hall_exits = ['NORTH', 'N', 'SOUTH', 'S', 'EAST', 'E', 'WEST', 'W']
south_hall_inventory = []
south_hall_contents = ['STRANGE PAINTING']
south_hall_puzzle = ['The floor is surprisingly smooth here.', False,
'An intricate design has been drawn on the floor in chalk.']

#########
# Study #
#########
study_desc = """There is a thick coating of dust on every surface here, pristine
and undisturbed. Bookshelves line the walls and a small reading table occupies
the far corner."""
study_exits = ['EAST', 'E']
study_inventory = ['HIDEBOUND BOOK']
study_contents = ['BOOKSHELF']
study_puzzle = ['The bookshelf is full of books.', False,
 'Books are piled on the floor.']

###########
# Bedroom #
###########
bedroom_desc = """A large, four poster bed dominates the center of the room. It
is flanked by a large vanity on one side and an immense chest of drawers on the
other side. The bed sheets are stained brown and brittle, soaked through with
old blood."""
bedroom_exits = ['WEST', 'W']
bedroom_inventory = []
bedroom_contents = ['DRESSER']
bedroom_puzzle = ['The room is undisturbed. ', False,
'The dresser has been moved from the wall, exposing a new door. ']

###########
# Dungeon #
###########
dungeon_desc = """The stink of this room hits you like a sledgehammer. Every
inch seems to be stained. The cold stone all but glows with malevolence."""
dungeon_exits = ['WEST', 'W']
dungeon_inventory = []
dungeon_contents = ['SHACKLES', 'SKELETON']
dungeon_puzzle = ['A female skeleton hangs, shackled to the wall.', False,
'The remains of a female skeleton litter the floor.']

###############
# Dining Room #
###############
dining_room_desc = """The last meal of whoever owned this house lies on the
table, green with mold and smelling strongly of decay."""
dining_room_exits = ['NORTH', 'N', 'SOUTH', 'S']
dining_room_inventory = []
dining_room_contents = ['SERVING DISH']
dining_room_puzzle = ['One serving dish remains covered.', False,
'A rotted head looks up at you from the table, eyes blank and ruined.']

###########
# Kitchen #
###########
kitchen_desc = """The kitchen is a wreck. It looks as if there was a fight here,
and someone came out the definite loser. Old bloodstains abound from counter to
floor."""
kitchen_exits = ['NORTH', 'N']
kitchen_inventory = []
kitchen_contents = ['BASEMENT DOOR']
kitchen_puzzle = ['The basement door is locked.', False,
 'The basement door is unlocked.']

############
# Basement #
############
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

###############################################################################
# Store descriptions in a dictionary for 'examine'
# Descriptions can be changed.
###############################################################################
descriptions = {
'FIREPLACE':
"""
The fireplace is old and soot covered. A loose brick
is visible above the mantle.""",

'DRESSER':
"""
An antique chest of drawers made from dark wood with a satin
finish.""",

'FLOOR':
"""
The floor is made of the same gray brick as the rest of the
house.""",

'COAT PILE':
"""
The coats are in various stages of decay. The smell of mold and mildew
is overwhelming.""",

'ARMOR': """
A medeival suit of armor held together by pins. One arm appears
to be loose.""",

'HIDEBOUND BOOK': """
An old, heavy tome wrapped in thin, almost paper-like leather.
Best not to ask what animal it came from.""",

'PAGE': """
This page has seen better days. There's an intricate diagram inscribed
on it.""",

'STRANGE PAINTING': """
It's a bedroom, swathed in silk and luxury. A four poster bed dominates the
room and a large vanity occupies one wall. There's a door on the other wall,
it looks seldom used.""",

'BOOKSHELF': """
Lined with tomes, these bookshelves sport intricate carvings on the dividers. It
would take forever to read all of these books.""",

'SHACKLES': """
These manacles are heavy, iron and nearly rusted through. They've long since
fallen off of the skeleton's hands.""",

'SKELETON': """
This slight skeleton is delicate looking and feminine. Mummified skin still
clings to bone, unable or unwilling to let go. Something sparkles from within
her chest cavity, but a rotted webwork of skin and bone keep you from getting
a good look.""",

'SERVING DISH': """
A mottled, gray pewter cover caps this dish. The edges are crusted with a
brownish dried blood.""",

'BASEMENT DOOR': """
This door is made from solid oak and banded with riveted iron. An oldfashioned
keyhole lies beneath the knob.""",

'GHOST': """
She was beautiful once, but malice has twisted her fine features into a rictus
of hate and anguish. Her spectral form is hidden in an elaborate dress, although
her face and hands appear mottled and corpselike. Wicked talons spring forth
from her finger tips.""",

'CHARCOAL': """
A well burnt piece of charred wood conveniently shaped like a pencil.""",

'LOCKET': """
Silver and heart shaped, this locket contains the portrait of a fine looking
woman dressed in antiquated, frilly clothing.""",

'BLESSED LOCKET': """
The locket now glows with an inner light. It is warm to the touch and it's very
presence comforts you.""",

'KEY': """
An old fashioned, iron key."""
}

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

    elif (room_name == 'Escape'):
        escape()

    else:
        print "You are in a nonexistant area. Goodbye!"
        print "Error: Player out of bounds."
        quit()
