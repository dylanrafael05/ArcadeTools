"""

    Created by Floofer++

    Uses the "math" library built-in to python

    -----------------------------------------

        ###  ####  #####  ###  ####  #####
       #   # #   # #     #   # #   # #
       ##### ####  #     ##### #   # ###
       #   # #   # #     #   # #   # #
       #   # #   # ##### #   # ####  #####

       #####  ###   ###  #      ####
         #   #   # #   # #     #
         #   #   # #   # #      ###
         #   #   # #   # #         #
         #    ###   ###  ##### ####

    -----------------------------------------

    Arcade Tools does not intend to infringe upon the rights
    of lowiro (c), nor is it intended to be used to break their
    terms of service or to modify their game and creation,
    Arcaea. Do not use this script to violate any terms which
    lowiro (c) has put forth.

    Any correlation to other scripts of the same general purpose,
    including any created by lowiro (c), the rightful creators of
    Arcaea, are purely coincedental. This script was created
    without the usage of any resources other than those which
    explain or provide aid with the Python language.

"""

# IMPORT STATEMENTS #
from math import sin, cos, pi, floor


# ARC MATH METHODS #
# Taking in a float, usually between 0 and 1, these methods
# return the relative position; defined as the x-position at
# a time (relative*100)% through an arc which begins at [0,a]
# and ends at [1,b]
def b_arc(relative):
    return sin(relative * pi - pi / 2) / 2 - 0.5


def si_arc(relative):
    return sin(relative * pi / 2)


def so_arc(relative):
    return 1 - cos(relative * pi / 2)


# ROUNDING #
# Rounds "num" to the nearest multiple of the float "to"
def round_to(num, to):
    return round(num / to) * to


# INHERITANCE #
# Checks to see if "inst" is of a type which inherits "cls"
def is_inherited(inst, cls):
    return issubclass(type(inst), cls)


# TIMING LIST MANAGEMENT #
# Gets the correct timing used for any note at time "time"
# from a list of provided timings "timings"
def get_nearest_timing(time, timings):
    for i, timing in enumerate(timings):

        if timing.time < time:
            return timings[i - 1 if i > 0 else 0]

    return timings[-1]


# ADD LINE MARKERS #
# Adds numerical line markers within a string
def add_line_markers(val):
    return "\n".join(f"{i}\t| {l}" for i, l in val.splitlines())


# TIMING CLASS #
class Timing:

    # CONSTRUCTION #
    # Calculate the millisecond length of one beat
    # upon construction in order to decrease overhead
    def __init__(self, time, bpm, timesig):
        self.time = time
        self.bpm = bpm
        self.ms_elapse = 60000 / bpm
        self.timesig = timesig

    # TIMING READING #
    # Attempt to create a Timing instance from
    # provided text of .aff standard formatting
    @classmethod
    def parse_str(cls, val: str):

        if not val[0:7] == "timing(":
            return None

        if not val[-2:] == ");":
            return None

        spl = val[7:-2].split(",")

        try:
            tm = int(spl[0])
            bp = float(spl[1])
            ts = float(spl[2])
            return cls(tm, bp, ts)
        except ValueError and IndexError:
            return None

    # TIMING REPR #
    # Format a Timing instance as .aff standard
    # text. No need for __eq__ here, as no content
    # checking will be required for Timings
    def __repr__(self):
        return f"timing({self.time},{'{:.2f}'.format(self.bpm)}," \
               f"{'{:.2f}'.format(self.timesig)});"


# NOTE CLASSES #
# Base class for all notes, used to simplify type-checking
# by use of is_inherited
class Note:

    def __init__(self, time):
        self.time = time


# Class for all Tap notes
class Tap(Note):

    # CONSTRUCTION #
    # Tap inherits Note, and therefore can call
    # the "super" constructor to set time
    def __init__(self, time, lane):
        super().__init__(time)
        self.lane = lane

    # TAP READING #
    # Attempt to create a Tap instance from
    # provided text of .aff standard formatting
    @classmethod
    def parse_str(cls, val: str):

        if not val[0] == "(":
            return None

        if not val[-2:] == ");":
            return None

        spl = val[1:-2].split(",")

        try:
            tm = int(spl[0])
            ln = int(spl[1])
            return cls(tm, ln)
        except ValueError and IndexError:
            return None

    # MAGIC METHODS #
    # Enable comparison, content-checking,
    # and string formatting
    def __eq__(self, other):
        if not isinstance(other, Tap):
            return False
        return (self.time, self.lane) == (other.time, other.lane)

    def __repr__(self):
        return f"({self.time},{self.lane});"


# Class for all Hold notes
class Hold(Note):

    # CONSTRUCTION #
    # Hold inherits Note, and therefore can call
    # the "super" constructor to set time
    def __init__(self, time, end, lane):
        super().__init__(time)
        self.end = end
        self.lane = lane

    # HOLD READING #
    # Attempt to create a Hold instance from
    # provided text of .aff standard formatting
    @classmethod
    def parse_str(cls, val: str):

        if not val[0:5] == "hold(":
            return None

        if not val[-2:] == ");":
            return None

        spl = val[5:-2].split(",")

        try:
            tm = int(spl[0])
            nd = int(spl[1])
            ln = int(spl[2])
            return cls(tm, nd, ln)
        except ValueError and IndexError:
            return None

    # MAGIC METHODS #
    # Enable comparison, content-checking,
    # and string formatting
    def __eq__(self, other):
        if not isinstance(other, Hold):
            return False
        return (self.time, self.end, self.lane) == (other.time, other.end, other.lane)

    def __repr__(self):
        return f"hold({self.time},{self.end},{self.lane});"


# Class for all Arc notes
class Arc(Note):

    # CONSTRUCTION #
    # Arc inherits Note, and therefore can call
    # the "super" constructor to set time
    def __init__(self, time, end, x1, x2, arctype, y1, y2, color, void, arctaps):
        super().__init__(time)
        self.end = end
        self.x1 = x1
        self.x2 = x2
        self.arctype = arctype
        self.y1 = y1
        self.y2 = y2
        self.color = color
        self.void = void
        self.arctaps = arctaps

    # ARC READING #
    # Attempt to create an Arc instance from
    # provided text of .aff standard formatting
    @classmethod
    def parse_str(cls, val: str):

        if not val[0:4] == "arc(":
            return None

        end_idx = val.find(")")
        if not end_idx == -1:
            return None

        spl = val[4:end_idx + 1].split(",")
        end = val[end_idx:]

        try:
            tm = int(spl[0])
            nd = int(spl[1])
            x1 = float(spl[2])
            x2 = float(spl[3])
            tp = spl[4]
            y1 = float(spl[5])
            y2 = float(spl[6])
            col = int(spl[7])
            void = spl[9] == "true"
            ctp = []
            if len(end) > 1:
                for arctap in end[1:-2].split(","):
                    ctp.append(int(arctap))

            return cls(tm, nd, x1, x2, tp, y1, y2, col, void, ctp)
        except ValueError and IndexError:
            return None

    # ARC POSITION CALCULATION #
    # Get the position of the arc at a given
    # time (usually within the bounds of the arc)
    def get_pos(self, time):
        relative = (time - self.time) / (self.end - self.time)
        x_rel, y_rel = 0, 0
        if self.arctype == "s":
            x_rel, y_rel = relative, relative
        elif self.arctype == "b":
            x_rel, y_rel = b_arc(relative)
        elif self.arctype == "si":
            x_rel = si_arc(relative)
            y_rel = relative
        elif self.arctype == "so":
            x_rel = so_arc(relative)
            y_rel = relative
        elif self.arctype == "sisi":
            x_rel = si_arc(relative)
            y_rel = x_rel
        elif self.arctype == "soso":
            x_rel = so_arc(relative)
            y_rel = x_rel
        elif self.arctype == "siso":
            x_rel = si_arc(relative)
            y_rel = so_arc(relative)
        elif self.arctype == "sosi":
            x_rel = so_arc(relative)
            y_rel = si_arc(relative)
        return self.x1 + (self.x2 - self.x1) * x_rel, self.y1 + (self.y2 - self.y1) * y_rel

    # MAGIC METHODS #
    # Enable comparison, content-checking,
    # and string formatting
    def __eq__(self, other):
        if not isinstance(other, Arc):
            return False
        return (self.time, self.end, self.x1, self.x2, self.arctype, self.y1, self.y2, self.color,
                self.void, self.arctaps) == (
                other.time, other.end, other.x1, other.x2, other.arctype, other.y1, other.y2,
                other.color, other.void, other.arctaps)

    def __repr__(self):
        return f"arc({self.time},{self.end},{'{:.2f}'.format(self.x1)}," \
               f"{'{:.2f}'.format(self.x2)},{self.arctype},{'{:.2f}'.format(self.y1)}," \
               f"{'{:.2f}'.format(self.y2)},{self.color},none," \
               f"{'true' if self.void else 'false'}" + \
               f"[{','.join(self.arctaps)}];" if len(self.arctaps) > 0 else ");"


# MAIN CLASSES #
class TimingGroup:

    # CONSTRUCTION #
    def __init__(self, notes, timings):
        self.notes = notes
        self.timings = timings

    # FACTORY METHODS #
    @classmethod
    def blank(cls):
        return cls([], [])

    @classmethod
    def from_timing(cls, timing):
        return cls([], [timing])


class Aff:

    # AFF BASICS #
    quantize_snaps = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 16]

    def __init__(self, audio_offset):

        self.audioOffset = audio_offset
        self.tgs = [TimingGroup.blank()]

    # AFF READER #
    # Convert human-readable or .aff standard
    # data into an Aff instance
    @classmethod
    def read(cls, data: str):

        # Separate all lines
        contents = data.splitlines()

        # If the file does not have more than 2 lines,
        # refuse to parse
        if len(contents) < 3:
            raise ValueError("Invalid AFF file. Not enough data.")

        # If there is no specified audio offset, refuse
        # to parse
        if not contents[0].startswith("AudioOffset:"):
            raise ValueError("Invalid AFF file. No present audio offset.")

        a_o_temp = int(contents[0][12:])
        aff_ret = Aff(a_o_temp)

        tg_index = 0
        tg_counter = 0

        start_t = Timing.parse_str(contents[2].strip())

        # If there is no valid timing on line 3, cry like
        # a small infant
        if not start_t:
            raise ValueError("Invalid AFF file. No timing found on line 3.")

        aff_ret.tgs[0] = TimingGroup.from_timing(start_t)

        # Enumerate over following lines
        i = 3
        while i < len(contents):

            line = contents[i]

            # If the line is the start of a timinggroup,
            # proceed with caution
            if line.startswith("timinggroup(){"):

                tg_index += 1
                tg_counter += 1

                start_t = Timing.parse_str(contents[i + 1].strip())

                # If there is not a valid timing one line after
                # the beggining of the timinggroup, piss yourself
                if not start_t:
                    raise ValueError(f"Invalid AFF file. Improper start of timinggroup at line {i}.")

                aff_ret.tgs.append(TimingGroup.from_timing(start_t))

                i += 2

            # Handle the end of a timinggroup
            elif line == "};":

                tg_counter -= 1
                i += 1

            # Handle all other line types
            else:

                aff_ret.parse_line(line, i, tg_index if tg_counter > 0 else 0)
                i += 1

        # Sort all timings
        aff_ret.sort_timings()

        # Return the built aff
        return aff_ret

    # AFF LOADER #
    # Load and then read from a valid .aff file
    @classmethod
    def load(cls, filepath: str):

        # Only accept .aff files
        if not filepath.endswith(".aff"):
            raise TypeError("Not an AFF file.")

        # Read all contents
        with open(filepath) as file:
            data = file.read()
            file.close()

        # If an error occurred, scream loudly at the user
        if not data:
            raise BaseException("Could not load file.")

        # Send data to "read"
        return cls.read(data)

    # LINE PARSER #
    # Parse a single line of the .aff, assumed
    # to contain a note of some kind, or a timing.
    def parse_line(self, line: str, linenum: int, tg: int):

        # Parse Tap notes
        if line.startswith("("):

            val = Tap.parse_str(line)
            if val:
                self.tgs[tg].notes.append(val)

        # Parse Hold notes
        elif line.startswith("hold("):

            val = Hold.parse_str(line)
            if val:
                self.tgs[tg].notes.append(val)

        # Parse Arc notes
        elif line.startswith("arc("):

            val = Arc.parse_str(line)
            if val:
                self.tgs[tg].notes.append(val)

        # Parse Timings
        elif line.startswith("timing("):
            val = Timing.parse_str(line)
            if val:
                self.tgs[tg].timings.append(val)

        # Pretend that any other note type is non-existent
        elif line.startswith("camera(") or line.startswith("special("):
            self.tgs[tg].notes.append(line)

        # Raise an error if the note is none of these types
        else:
            raise ValueError(f'Invalid AFF File: improper line at: {linenum};\n"{line}"')

    # TIMING SORTER #
    # Sorting the timings of each timinggroup
    # by time of effect decreases time it takes to
    # find the nearest valid timing for any given
    # note
    def sort_timings(self):
        for tg in self.tgs:
            tg.timings = sorted(tg.timings, key=lambda t: t.time, reverse=True)

    # AFF REPRESENTATION #
    # Convert the Aff instance into human-readable
    # or .aff standard data
    def __repr__(self):

        # Start with the header
        val = f"AudioOffset:{self.audioOffset}\n-\n"

        # Enumerate everything else
        for i, tg in enumerate(self.tgs):

            # Create timinggroup tag if required
            if not i == 0:
                val += "timinggroup(){\n"

            # Append all timings
            for timing in tg.timings:
                val += repr(timing) + '\n'

            # Append all notes
            for note in tg.notes:
                val += repr(note) + '\n'

            # Close timinggroup if necessary
            if not i == 0:
                val += "};\n"

        return val

    # SAVING AFF TO FILE #
    # Saves the .aff standard representation given by
    # the above __repr__() function to a file at (filename)
    def save(self, filename):
        with open(filename, "w") as file:
            file.write(repr(self))

    # STATIC FUNCTIONS #
    # Return arithmetic or note-based data created
    # using inputs not requiring an instance of Aff
    @staticmethod
    def fix_quantize_single(time, tg):

        timing = get_nearest_timing(time, tg.timings)

        for snap in Aff.quantize_snaps:

            snapped_time = round_to(time, timing.ms_elapse / snap)

            if abs(time - snapped_time) <= 1.5:
                return floor(snapped_time)

        return time

    # MODIFIER FUNCTIONS #
    # Modify or remove current notes in order
    # to correct specified issues or to meet
    # provided criteria
    def fix_quantizing_errors(self, exemptions):

        for i, tg in enumerate(self.tgs):

            if f"gr{i}" in exemptions:
                continue

            for j, note in enumerate(tg.notes):

                if not is_inherited(note, Note):
                    continue

                self.tgs[i].notes[j].time = self.fix_quantize_single(note.time, tg)

                if type(note) == Hold:

                    self.tgs[i].notes[j].end = self.fix_quantize_single(note.end, tg)

                elif type(note) == Arc:

                    self.tgs[i].notes[j].end = self.fix_quantize_single(note.end, tg)

                    for k, arctap in enumerate(note.arctaps):
                        self.tgs[i].notes[j].arctaps[k] = self.fix_quantize_single(arctap, tg)

    def remove_zero_length_holds(self, exemptions):

        for i, tg in enumerate(self.tgs):

            if f"gr{i}" in exemptions:
                continue

            tg.notes = \
                [x for x in tg.notes if not isinstance(x, Hold) or not
                 x.time == x.end and f"tm{x.time}" not in exemptions]

    def remove_duplicate_notes(self, exemptions):

        for i, tg in enumerate(self.tgs):

            if i in exemptions:
                continue

            tg.notes = \
                [x for idx, x in enumerate(tg.notes) if x not in
                 tg.notes[idx + 1:] and f"tm{x.time}" not in exemptions]

            for j, n in enumerate(tg.notes):

                if not isinstance(n, Arc):
                    continue

                n.arctaps = \
                    [x for idx, x in enumerate(n.arctaps) if x
                     not in n.arctaps[idx + 1:] and f"tm{x.time}"
                     not in exemptions]

    def remove_invalid_arcs(self, exemptions):

        for i, tg in enumerate(self.tgs):

            if f"gr{i}" in exemptions:
                continue

            tg.notes = \
                [x for x in tg.notes if not isinstance(x, Arc) or not
                 x.time == x.end and x.x1 == x.x2 and x.y1 == x.y2 and
                 f"tm{x.time}" not in exemptions]

    # GENERATOR FUNCTIONS #
    # Create a group of new notes from an existing note, or
    # from user provided data
    def create_segmented_arc(self, tg, target_idx, snap, stair):

        if tg not in range(len(self.tgs)):
            raise ValueError("Not a valid timing group")

        if target_idx not in range(len(self.tgs[tg])):
            raise ValueError("Not a valid note")

        arc = self.tgs[tg].notes[target_idx]

        if not isinstance(arc, Arc):
            raise ValueError("Not a valid arc")

        timing = get_nearest_timing(arc.time, self.tgs[tg].timings)

        cnt = 0
        c_time = arc.time
        new_arcs = []

        while c_time / snap < arc.end:

            c_time = floor(arc.time + cnt * timing.ms_elapse)
            n_time = floor(arc.time + (cnt + 1) * timing.ms_elapse)
            c_pos = arc.get_pos(c_time)
            n_pos = arc.get_pos(n_time)

            if stair:
                new_arcs.append(Arc(c_time, min(n_time, arc.end), c_pos[0],
                                n_pos[0], "s", c_pos[1], n_pos[1] - 0.01,
                                arc.color, arc.void, arc.arctaps))
            else:
                new_arcs.append(Arc(c_time, min(n_time, arc.end), c_pos[0],
                                n_pos[0], "s", c_pos[0], n_pos[0],
                                arc.color, arc.void, arc.arctaps))

                if n_time < arc.end:
                    new_arcs.append(Arc(n_time, n_time, c_pos[0],
                                        n_pos[0], "s", c_pos[1],
                                        n_pos[1], arc.color,
                                        arc.void, arc.arctaps))

            cnt += 1

        if len(new_arcs) < 1:
            raise Exception("Error while creating new arcs")

        del self.tgs[tg].notes[target_idx]
        self.tgs[tg].notes.append(new_arcs)


# GLOBAL VARIABLES #
aff = Aff(0)  # Aff data
currentNavigation = True  # Current menu navigation command
tempNavigation = True  # Previous menu navigation
currentState = "FILE"  # Current menu state
tgIdx = 0  # Tracks timinggroup choices

intro_txt = """              Welcome to...
.---------------------------------------.
|                                       |
|   ###  ####  #####  ###  ####  #####  |
|  #   # #   # #     #   # #   # #      |
|  ##### ####  #     ##### #   # ###    |
|  #   # #   # #     #   # #   # #      |
|  #   # #   # ##### #   # ####  #####  |
|                                       |
|  #####  ###   ###  #      ####  #  #  |
|    #   #   # #   # #     #      #  #  |
|    #   #   # #   # #      ###   #  #  |
|    #   #   # #   # #         #        |
|    #    ###   ###  ##### ####   #  #  |
|                                       |
`---------------------------------------'

Designed and Created by Floofer++ :)
Type "EXIT" at any time to quit the console.
Type "BACK" at any time after entering your .aff file to return
to the main menu."""

main_txt = """What would you like to do with your .aff? 
(Type the corresponding number and enter to choose)
0: Read back my .aff
1: Save my .aff to a new location
2: Fix quantization errors
3: Remove all zero-length hold notes
4: Remove all duplicate taps and arc-taps
5: Remove all arcs with the same start and end time
   and the same start and end position
6: Turn an arc into a stair-arc
7: Turn an arc into a segmented (amygdata) arc
8: Load another .aff
"""

exemption_txt = """Type out any exemptions to this command that you would like
Exemptions are not effected by any command. There are two types of exemptions,
timinggroup, and note. Any timinggroups listed in the exemptions are ignored in
full. timinggroup exemptions are formatted as gr#. Note exemptions are formatted
as tm# where # is the time of the note. Separate exemptions by a comma."""


# MAIN METHOD #
def main():

    global aff, currentNavigation, currentState, tempNavigation, tgIdx

    print(intro_txt)

    while not currentNavigation == "EXIT":

        if currentState == "FILE":

            currentNavigation = input("Please enter the full path to a valid .aff file: ")

            if currentNavigation == "EXIT":
                break

            try:

                aff = Aff.load(currentNavigation)
                currentState = "MAIN"
                print("\nYour .aff file has been loaded!")

            except ValueError and TypeError and BaseException as e:

                print("Error: " + str(e) + "\n")

        elif currentState == "MAIN":

            print(main_txt)
            currentNavigation = input("> ")

            if currentNavigation == "0":
                print(f"\n{repr(aff)}\n")
            elif currentNavigation == "1":
                currentState = "SAVE"
            elif currentNavigation in ["2", "3", "4", "5"]:
                currentState = "MOD"
            elif currentNavigation == "6":
                currentState = "STR"
            elif currentNavigation == "7":
                currentState = "STR"
            elif currentNavigation == "8":
                currentState = "FILE"
            elif currentNavigation == "EXIT":
                break
            else:
                print("That is not a valid choice!")

        elif currentState == "SAVE":

            currentNavigation = input("Please enter the full path where you would like to save to:")

            if currentNavigation == "BACK":
                currentState = "MAIN"
                continue
            elif currentNavigation == "EXIT":
                break

            try:

                aff.save(currentNavigation)
                currentState = "MAIN"
                print("\nYour .aff file has been saved!")

            except BaseException as e:

                print("Error: " + str(e) + "\n")

        elif currentState == "MOD":

            tempNavigation = currentNavigation

            print(exemption_txt)
            currentNavigation = input("> ")

            if currentNavigation == "BACK":
                currentState = "MAIN"
                continue
            if currentNavigation == "EXIT":
                break

            print("\nWorking...")
            exem = [x.strip() for x in currentNavigation.split(",")]

            if tempNavigation == "2":
                aff.fix_quantizing_errors(exem)
            elif tempNavigation == "3":
                aff.remove_zero_length_holds(exem)
            elif tempNavigation == "4":
                aff.remove_duplicate_notes(exem)
            elif tempNavigation == "5":
                aff.remove_invalid_arcs(exem)

            print("Finished!")
            currentState = "MAIN"

        elif currentState == "STR":

            tempNavigation = currentNavigation

            while True:

                currentNavigation = input("""Enter the number of the timing which the arc you want to
                transform belongs to: """)

                if currentNavigation == "BACK":
                    break

                try:
                    tgIdx = int(currentNavigation)
                    assert tgIdx in range(len(aff.tgs))
                    break
                except AssertionError and ValueError as e:
                    print(f"Not a valid timinggroup: {e}")

            if currentNavigation == "BACK":
                currentState = "MAIN"
                continue
            if currentNavigation == "EXIT":
                break

            idx = -1

            while True:

                print("\n" + add_line_markers('\n'.join(repr(x) for x in aff.tgs[tgIdx].notes)))

                currentNavigation = input("Enter the line number of the arc you wish to modify: ")

                if currentNavigation == "BACK" or currentNavigation == "EXIT":
                    break

                try:
                    idx = int(currentNavigation)
                    assert idx in range(len(aff.tgs[tgIdx].notes))
                    break
                except AssertionError and ValueError as e:
                    print(f"Not a valid note: {e}")

            if currentNavigation == "BACK":
                currentState = "MAIN"
                continue
            if currentNavigation == "EXIT":
                break

            snap = 1

            while True:

                currentNavigation = input("Enter the beat divisor to snap to: ")

                if currentNavigation == "BACK" or currentNavigation == "EXIT":
                    break

                try:
                    snap = float(currentNavigation)
                    break
                except ValueError:
                    print("Not a valid float!")

            if currentNavigation == "BACK":
                currentState = "MAIN"
                continue
            if currentNavigation == "EXIT":
                break

            aff.create_segmented_arc(tgIdx, idx, snap, tempNavigation == "7")


# EXECUTION #
if __name__ == '__main__':
    main()
