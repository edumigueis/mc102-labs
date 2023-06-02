from math import floor
from dataclasses import dataclass, field


class BattleLogger:
    """
    Utility class to save logs and flush them when needed based on
    the battle's final results
    """
    logs: dict = {}
    current_log = 0

    @classmethod
    def flush_battle_result_log(cls, result: int) -> None:
        for i in range(cls.current_log):
            cls.flush_logs(cls.logs[i].get("basics", []))
            if ((result == 2 or result == 3)
                    and i < cls.current_log - 1) or result == 1:
                cls.flush_logs(cls.logs[i].get("arrows", []))
                cls.flush_logs(cls.logs[i].get("crits", []))
        else:
            if result == 1:
                print("Aloy provou seu valor e voltou para sua tribo.")
            elif result == 2:
                print("Aloy ficou sem flechas e recomeçará sua missão mais preparada.")
            else:
                print("Aloy foi derrotada em combate e não retornará a tribo.")

    @staticmethod
    def flush_logs(logs_to_flush: list[str]) -> None:
        for log in logs_to_flush:
            print(log)

    @classmethod
    def log(cls, log: str, log_type: str) -> None:
        cls.logs.setdefault(cls.current_log, {})
        cls.logs[cls.current_log].setdefault(log_type, []).append(log)


@dataclass
class Aloy:
    """
    Represents the main warrior in the battle
    and is responsible for tracking its stats
    """
    max_health: int
    health: int
    arrows: dict

    def heal(self) -> None:
        """
        Heals adding up to half of max health and not surpassing it
        """
        self.health = min(
            self.health + floor(0.5 * self.max_health),
            self.max_health)

    def take_dmg(self, dmg: int) -> None:
        self.health = max(self.health - dmg, 0)

    def replenish_arrows(self, used_arrows: dict) -> None:
        for arrow in self.arrows.keys():
            self.arrows[arrow] = used_arrows[arrow][1]


@dataclass
class Machine:
    """
    Represents a single machine in the fight
    """
    health: int
    strength: int
    parts: list

    def take_dmg(self, target_part, arrow_type, coord) -> None:
        """
        Damage calculated by the Manhattan distance
        (note that negative damage doesn't count)
        """
        dmg = target_part.max_dmg - (abs(target_part.coordinate[0] - coord[0])
                                     + abs(target_part.coordinate[1]
                                           - coord[1]))
        if dmg > 0:
            self.health = max(self.health - dmg
                              if (arrow_type ==
                                  target_part.weakness or
                                  target_part.weakness == "todas")
                              else self.health - dmg//2, 0)


@dataclass
class Part:
    """
    Represents a single machine part
    """
    name: str
    weakness: str
    max_dmg: int
    coordinate: tuple


@dataclass
class Battle:
    enemies: int
    remaining_enemies: int = field(init=False, repr=False)
    warrior: Aloy
    machines: list[Machine]
    used_arrows: dict[str, list[int]] = field(init=False, repr=False)
    crits: dict[int, dict[tuple, int]] = field(init=False, repr=False)

    def __post_init__(self):
        self.used_arrows = {
            arrow_type: [0, count] for arrow_type, count
            in self.warrior.arrows.items()}
        self.remaining_enemies = self.enemies

    def prepare_fight(self) -> None:
        """
        Reads inputs and starts up all fields for fight
        """
        current_machine_count = int(input())
        self.machines = []
        self.crits = {}
        for _ in range(current_machine_count):
            machine_stats = input().split(" ")
            self.machines.append(
                Machine(int(machine_stats[0]), int(machine_stats[1]), []))
            for _ in range(int(machine_stats[2])):
                part_stats = input().split(", ")
                part_to_add = Part(*(part_stats[0], part_stats[1],
                                     int(part_stats[2]),
                                     tuple(map(int, part_stats[3:]))))
                self.machines[len(
                    self.machines) - 1].parts.append(part_to_add)

    def start_fight(self) -> None:
        """
        Loop for each fight(runs while the attacks continue up to a result).
        """
        self.warrior.heal()
        self.warrior.replenish_arrows(self.used_arrows)
        BattleLogger.log(
            f"Combate {BattleLogger.current_log}, vida = {self.warrior.health}", "basics")
        attack_count = 1
        targets = set()
        while not self.__is_current_fight_over():
            attack_stats = input().split(", ")
            target = int(attack_stats[0])
            targets.add(target)
            self.__attack(target, attack_stats[1],
                          attack_stats[2], (int(attack_stats[3]),
                                            int(attack_stats[4])))
            if attack_count % 3 == 0:
                dmg = sum(m.strength for m in self.machines if m.health > 0)
                self.warrior.take_dmg(dmg)
            attack_count += 1
        else:
            BattleLogger.log("Vida após o combate = " +
                             str(self.warrior.health), "basics")
            self.handle_arrows()
            self.handle_crits(targets)

    def __attack(self, target: int, target_part: str,
                 arrow_type: str, coord: tuple) -> None:
        """_
        Responsible for resolving and tigger stats updates
        after a single attack(line of input)
        """
        target_part_obj = next(
            (part for part in self.machines[target].parts
             if part.name == target_part), None)
        self.machines[target].take_dmg(target_part_obj, arrow_type, coord)
        if target_part_obj and target_part_obj.coordinate == coord:
            self.crits.setdefault(target, {}).update(
                {coord: self.crits[target].get(coord, 0) + 1})
        if self.machines[target].health <= 0:
            self.remaining_enemies -= 1
            BattleLogger.log(f"Máquina {target} derrotada", "basics")
        self.warrior.arrows[arrow_type] -= 1
        self.used_arrows[arrow_type][0] += 1

    def __is_current_fight_over(self) -> bool:
        """
        Defines if entire battle ended
        """
        return (
            self.__all_dead()
            or self.warrior.health == 0
            or sum(self.warrior.arrows.values()) == 0
        )

    def is_battle_over(self) -> bool:
        """
        Defines if entire battle ended
        """
        return (
            self.__all_dead() and self.remaining_enemies == 0
            or self.warrior.health == 0
            or sum(self.warrior.arrows.values()) == 0
        )

    def handle_arrows(self) -> None:
        """
        Filter and log used arrows
        """
        BattleLogger.log("Flechas utilizadas:", "arrows")
        for arrow_type, arrow_type_tp in self.used_arrows.items():
            if arrow_type_tp[0] > 0:
                BattleLogger.log(
                    f"- {arrow_type}: {arrow_type_tp[0]}/{arrow_type_tp[1]}",
                    "arrows")
                self.used_arrows[arrow_type][0] = 0

    def handle_crits(self, targets: set[int]) -> None:
        """
        Reorder and log critial hits
        """
        if self.crits:
            BattleLogger.log("Críticos acertados:", "crits")
            for tg in sorted(targets):
                if tg in self.crits:
                    self.crits[tg] = {part.coordinate:
                                      self.crits[tg][part.coordinate]
                                      for part in self.machines[tg].parts
                                      if part.coordinate in self.crits[tg]}
                    BattleLogger.log(f"Máquina {tg}:", "crits")
                    for coord, count in self.crits[tg].items():
                        BattleLogger.log(f"- {coord}: {count}x", "crits")

    def __all_dead(self) -> bool:
        return sum(machine.health for machine in self.machines) == 0

    def result(self) -> int:
        """
        1: warrior won, 2: arrows ended, 3: warrior died
        """
        if self.warrior.health == 0:
            return 3
        return 2 if sum(list(self.warrior.arrows.values())) == 0 else 1


def main() -> None:
    input_health = int(input())
    input_arrows = input().split(" ")
    arrows = {input_arrows[i]: int(input_arrows[i + 1])
              for i in range(0, len(input_arrows), 2)}
    battle = Battle(int(input()), Aloy(input_health, input_health, arrows), [])
    while not battle.is_battle_over():
        battle.prepare_fight()
        battle.start_fight()
        BattleLogger.current_log += 1
    BattleLogger.flush_battle_result_log(battle.result())


if __name__ == "__main__":
    main()
