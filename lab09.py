class Robot:
    """
    Represents a robot and all of its atributions
    """

    def __init__(self, room):
        self.room = room
        self.prev_pos = (0, 0)
        self.current_pos = (0, 0)
        self.mode_switch_pos = (0, 0)
        self.mode = "scan"
        self.direction = "r"

    def start(self):
        """
        Main loop that takes care of matching modes and running them
        """
        self.__print()
        while self.mode != "end":
            match self.mode:
                case "scan":
                    self.scan()
                case "clean":
                    self.mode_switch_pos = self.current_pos
                    self.clean()
                case "back":
                    self.back_to_scanning()
                case "finish_up":
                    self.finish_up()

    def get_dirty_position(self):
        """
        Gets and returns next dirty position.
        Returns (-1,-1) if not found
        """
        if self.current_pos[1] > 0:
            if self.room[self.current_pos[0]][self.current_pos[1] - 1] == "o":
                return (self.current_pos[0], self.current_pos[1] - 1)
        if self.current_pos[0] > 0:
            if self.room[self.current_pos[0] - 1][self.current_pos[1]] == "o":
                return (self.current_pos[0] - 1, self.current_pos[1])
        if self.current_pos[1] < len(self.room[0]) - 1:
            if self.room[self.current_pos[0]][self.current_pos[1] + 1] == "o":
                return (self.current_pos[0], self.current_pos[1] + 1)
        if self.current_pos[0] < len(self.room) - 1:
            if self.room[self.current_pos[0] + 1][self.current_pos[1]] == "o":
                return (self.current_pos[0] + 1, self.current_pos[1])
        return (-1, -1)  # no dirty positions found

    def __print(self):
        for line in self.room:
            print(" ".join(line))
        print()

    def __update_and_print(self):
        """
        Updates the robot position and calls map printing
        """
        self.room[self.current_pos[0]][self.current_pos[1]] = "r"
        self.room[self.prev_pos[0]][self.prev_pos[1]] = "."
        self.__print()

    def move_to_next_pos(self):
        """
        Matches direction and then updates robot position
        """
        self.prev_pos = self.current_pos
        match self.direction:
            case "r":
                if self.current_pos[1] == len(self.room[0]) - 1:
                    self.current_pos = (
                        self.current_pos[0] + 1, self.current_pos[1])
                    self.direction = "l"
                else:
                    self.current_pos = (
                        self.current_pos[0], self.current_pos[1] + 1)
            case "l":
                if self.current_pos[1] == 0:
                    self.current_pos = (self.current_pos[0] + 1, 0)
                    self.direction = "r"
                else:
                    self.current_pos = (
                        self.current_pos[0], self.current_pos[1] - 1)
            case "u":
                self.current_pos = (
                    self.current_pos[0] - 1, self.current_pos[1])
            case "d":
                self.current_pos = (
                    self.current_pos[0] + 1, self.current_pos[1])
        self.__update_and_print()

    def __get_relative_direction(self, dirt_pos):
        if dirt_pos[0] < self.current_pos[0]:
            return "u"
        if dirt_pos[0] > self.current_pos[0]:
            return "d"
        if dirt_pos[1] < self.current_pos[1]:
            return "l"
        if dirt_pos[1] > self.current_pos[1]:
            return "r"

    def __is_dirt_on_the_way(self):
        """
        Verifies if there is dirt in the robot's path
        """
        if self.current_pos == (self.mode_switch_pos[0],
                                self.mode_switch_pos[1]
                                + 1) or self.current_pos == (
                self.mode_switch_pos[0],
                self.mode_switch_pos[1] - 1):
            return True
        if (self.current_pos[0] % 2 == 0
            and self.current_pos[0] == self.mode_switch_pos[0] + 1
            and (self.current_pos[1] == 0
                 and self.mode_switch_pos[1] == 0)):
            return True
        if (self.mode_switch_pos[0] % 2 == 0
            and self.current_pos[0] == self.mode_switch_pos[0] + 1
            and (self.current_pos[1] == len(self.room[0]) - 1
                 and self.mode_switch_pos[1] == len(self.room[0]) - 1)):
            return True
        return False

    def finish_up(self):
        """
        Last mode
        """
        if self.current_pos == (len(self.room) - 1, 0):
            self.direction = "r"
            self.scan()
        else:
            self.mode = "end"

    def clean(self):
        """
        Cleaning mode -> runs while there is dirt to clean
        """
        while True:
            dirt_pos = self.get_dirty_position()
            if dirt_pos == (-1, -1):
                self.mode = "back"
                break
            self.direction = self.__get_relative_direction(dirt_pos)
            self.move_to_next_pos()
            if self.__is_dirt_on_the_way():
                self.mode = "scan"
                break

    def scan(self):
        if self.mode == "scan":
            self.direction = "l"
            if self.current_pos[0] % 2 == 0:
                self.direction = "r"
        while True:
            if self.get_dirty_position() != (-1, -1):
                self.mode = "clean"
                break
            if self.current_pos[0] == len(self.room) - 1:
                if ((self.current_pos[1] == 0 and self.direction == "l")
                    or (self.current_pos[1] == len(self.room[0]) - 1
                        and self.direction == "r")):
                    self.mode = "finish_up"
                    break
            self.move_to_next_pos()

    def back_to_scanning(self):
        while self.current_pos[1] != self.mode_switch_pos[1]:
            if self.get_dirty_position() != (-1, -1):
                self.mode = "clean"
                return
            if self.current_pos[1] > self.mode_switch_pos[1]:
                self.direction = "l"
            else:
                self.direction = "r"
            self.move_to_next_pos()
        while self.current_pos[0] != self.mode_switch_pos[0]:
            if self.get_dirty_position() != (-1, -1):
                self.mode = "clean"
                return
            if self.current_pos[0] > self.mode_switch_pos[0]:
                self.direction = "u"
            else:
                self.direction = "d"
            self.move_to_next_pos()
        self.mode = "scan"


def main() -> None:
    num_lines = int(input())
    room = [input().split(" ") for _ in range(num_lines)]
    rob = Robot(room)
    rob.start()


if __name__ == "__main__":
    main()