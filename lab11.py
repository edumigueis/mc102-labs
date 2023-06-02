from dataclasses import dataclass, field


@dataclass
class Movable:
    """
    Represents a movable object.
    Implements movement in 4 directions for a constrained box.
    """
    position: tuple

    def move(self, dir, line_bounds=(0, 0), column_bounds=(0, 0)) -> None:
        line = self.position[0]
        col = self.position[1]
        match(dir):
            case "U":
                self.position = (line - 1
                                 if line > line_bounds[0] else line, col)
            case "D":
                self.position = (line + 1
                                 if line < line_bounds[1] else line, col)
            case "L":
                self.position = (line, col - 1
                                 if col > column_bounds[0] else col)
            case "R":
                self.position = (line, col + 1
                                 if col < column_bounds[1] else col)


@dataclass
class Monster(Movable):
    """
    Represents a single monster
    """
    health: int
    attack: int
    m_type: str

    def take_dmg(self, dmg: int) -> int:
        prev_health = self.health
        self.health = max(self.health - dmg, 0)
        return min(dmg, prev_health)

    def move_monster(self, line_bounds, column_bounds) -> None:
        if self.position:
            return super().move(self.m_type, line_bounds, column_bounds)

    def vanish(self) -> None:
        self.position = None


@dataclass
class Link(Movable):
    """
    Represents the main warrior in the battle
    and is responsible for tracking its stats
    """
    health: int
    strength: int

    def take_dmg_or_heal(self, value: int) -> int:
        prev_health = self.health
        self.health = max(self.health + value, 0)
        if value < 0:
            return min(prev_health, -value)
        return value

    def strengthen_or_weaken(self, value) -> None:
        self.strength = max(self.strength + value, 1)

    def attack(self, enemies: list[Monster]) -> None:
        for enemy in enemies:
            dmg_taken = enemy.take_dmg(self.strength)
            print(
                f"O Personagem deu {dmg_taken} de dano ao monstro na posicao {enemy.position}")
            if enemy.health != 0:
                link_dmg_taken = self.take_dmg_or_heal(-enemy.attack)
                print(
                    f"O Monstro deu {link_dmg_taken} de dano ao Personagem. Vida restante = {self.health}")
                if not self.health:
                    return
            else:
                enemy.vanish()

    def get_status(self) -> str:
        if self.health != 0:
            return "P"
        return "X"


@dataclass
class Artifact:
    """
    Represents a single artifact in the dungeon
    """
    name: str
    a_type: str
    position: tuple
    status: int

    def vanish(self) -> None:
        self.position = None
        print(
            f"[{self.a_type}]Personagem adquiriu o objeto {self.name} com status de {self.status}")


@dataclass
class Dungeon():
    size: tuple
    player: Link
    artifacts: list[Artifact]
    monsters: list[Monster]
    final_pos: tuple
    dungeon: list[list[str]] = field(init=False)

    def start(self) -> None:
        """
        Main dungeon loop. Responsible for tracking positions and next steps.
        """
        line_bound = (0, self.size[0] - 1)
        col_bound = (0, self.size[1] - 1)
        reaching_final_pos = True
        while (self.player.position != self.final_pos
               and self.player.get_status() != "X"):
            self.update(True)
            for monster in self.monsters:
                monster.move_monster(line_bound, col_bound)
            if not reaching_final_pos:
                if self.player.position[0] % 2 == 0:
                    if self.player.position[1] == col_bound[0]:
                        self.player.move("U", line_bound, col_bound)
                    self.player.move("L", line_bound, col_bound)
                else:
                    if self.player.position[1] == col_bound[1]:
                        self.player.move("U", line_bound, col_bound)
                    self.player.move("R", line_bound, col_bound)
            else:
                self.player.move("D", (0, self.size[0] - 1))
                reaching_final_pos = self.player.position != (
                    self.size[0] - 1, self.player.position[1])
            self.__handle_position_match()
        else:
            self.update(True)
            if self.player.position == self.final_pos:
                print("Chegou ao fim!")

    def __handle_position_match(self) -> None:
        """
        Handles events when two objects occupy the same position
        """
        artifact_matches = [
            obj for obj in self.artifacts
            if obj.position == self.player.position]
        monster_matches = [
            monster for monster in self.monsters
            if monster.position == self.player.position
            and monster.position != self.final_pos]
        if any(artifact_matches):
            for artif in artifact_matches:
                if artif.a_type == "v":
                    self.player.take_dmg_or_heal(artif.status)
                else:
                    self.player.strengthen_or_weaken(artif.status)
                artif.vanish()
        if any(monster_matches):
            self.player.attack(monster_matches)

    def update(self, do_print=False) -> None:
        """
        Updates the map with current positions stored in objects
        """
        self.dungeon = [["."] * self.size[1] for _ in range(self.size[0])]
        for artif in self.artifacts:
            if artif.position:
                self.dungeon[artif.position[0]
                             ][artif.position[1]] = artif.a_type
        for monster in self.monsters:
            if monster.position:
                self.dungeon[monster.position[0]
                             ][monster.position[1]] = monster.m_type
        self.dungeon[self.final_pos[0]][self.final_pos[1]] = "*"
        self.dungeon[self.player.position[0]
                     ][self.player.position[1]] = self.player.get_status()
        if do_print:
            self.print_map()

    def print_map(self) -> None:
        for i in range(self.size[0]):
            print(" ".join(self.dungeon[i]))
        print()


def main() -> None:
    Vp, Dp = map(int, input().split())
    N, M = map(int, input().split())
    Ix, Iy = map(int, input().split(","))
    Fx, Fy = map(int, input().split(","))
    monsters = []
    for _ in range(int(input())):
        health, attack, m_type, pos = input().split()
        monsters.append(Monster(tuple([int(p) for p in pos.split(",")]),
                                int(health), int(
            attack), m_type))
    artifacts = []
    for _ in range(int(input())):
        name, a_type, pos, status = input().split()
        artifacts.append(
            Artifact(name, a_type,
                     tuple([int(p) for p in pos.split(",")]), int(status)))
    Dungeon((N, M), Link((Ix, Iy), Vp, Dp),
            artifacts, monsters, (Fx, Fy)).start()


if __name__ == "__main__":
    main()
