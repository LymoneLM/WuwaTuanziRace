import random
from enum import Enum, auto


def log(str):
    print(f"[TuanziLog]{str}")


class CheckChance(Enum):
    ROLL = auto(),
    BEFORE_RUN = auto(),


class Tuanzi:
    def __init__(self, name: str, check_chance, check_func):
        self.race_map = None
        self.tuanzi_id = None
        self.name = name
        self.check_chance = check_chance
        self.check_func = check_func

    def set_map(self, race_map, tuanzi_id):
        self.race_map = race_map
        self.tuanzi_id = tuanzi_id

    def check(self, now):
        self.check_func(self.race_map, self.tuanzi_id)


"""Note
起始处为0
4+2+3+1+6+3+3+1(完赛) = 23
>=23
"""


class RaceMap:
    def __init__(self, tuanzi: list[Tuanzi], length=23):
        self.tuanzi = tuanzi
        self.num_tuanzi = len(tuanzi)
        self.order = [n for n in range(self.num_tuanzi)]
        self.dice = [0 for n in range(self.num_tuanzi)]
        self.step = [0 for n in range(self.num_tuanzi)]
        self.length = length
        self.track = [[] for n in range(self.length * 2)]
        for i in range(self.num_tuanzi):
            self.tuanzi[i].set_map(self, i)

    def roll_dice(self):
        dice12 = lambda: random.randint(1, 3)
        random.shuffle(self.order)
        self.dice = [dice12() for n in range(self.num_tuanzi)]

    def run_match(self) -> int:
        while True:
            out = self.run_round()
            if out != -1:
                return out

    def run_round(self):
        self.roll_dice()
        for n in self.tuanzi:
            n.check(CheckChance.ROLL)
        for n in range(len(self.order)):
            th = self.tuanzi[self.order[n]]
            th.check(CheckChance.BEFORE_RUN)
            out = self.move(self.order[n])
            if out != -1:
                return out
        return -1

    def move(self, tuanzi_id):
        if self.step[tuanzi_id] == 0:
            self.track[self.step[tuanzi_id] + self.dice[tuanzi_id]].append(tuanzi_id)
            self.step[tuanzi_id] += self.dice[tuanzi_id]
            return -1
        source = self.track[self.step[tuanzi_id]]
        diff_step = self.dice[tuanzi_id]
        target = self.track[self.step[tuanzi_id] + diff_step]
        current = source.index(tuanzi_id)
        n = len(source) - (current + 1)
        for i in range(n):
            tuanzi = source.pop(current)
            self.step[tuanzi] += diff_step
            target.append(tuanzi)
        return self.check_win(tuanzi_id)

    def check_win(self, tuanzi_id):
        if self.step[tuanzi_id] >= self.length:
            return -1
        winner_list = self.track[self.step[tuanzi_id]]
        winner = winner_list.pop()
        log(f"{self.tuanzi[winner].name}获胜")
        return winner


# ======Tuanzi======
# jinhsi
def jinhsi_check(race_map, tuanzi_id):
    if race_map.step[tuanzi_id] == 0:  # 特殊情况刚起步
        return
    now_list = race_map.track[race_map.step[tuanzi_id]]
    pos = now_list.index(tuanzi_id)
    if pos + 1 != len(now_list):  # 不在最顶
        if random.random() > 0.40:
            return
        log("今汐发动技能")
        now_list.remove(tuanzi_id)
        now_list.append(tuanzi_id)


jinhsi = Tuanzi("今汐", CheckChance.ROLL, jinhsi_check)


# changli
def changli_check(race_map, tuanzi_id):
    if race_map.step[tuanzi_id] == 0:  # 特殊情况刚起步
        return
    now_list = race_map.track[race_map.step[tuanzi_id]]
    pos = now_list.index(tuanzi_id)
    if len(now_list) != 1 and pos != 0:
        if random.random() > 0.65:
            return
        log("长离发动技能")
        race_map.order.remove(tuanzi_id)
        race_map.order.append(tuanzi_id)


changli = Tuanzi("长离", CheckChance.ROLL, changli_check)


# calcharo
def calcharo_check(race_map, tuanzi_id):
    step = race_map.step[tuanzi_id]
    flag = True
    for s in race_map.step:
        if s < step:
            flag = False
    if flag:
        log("卡卡罗发动技能")
        race_map.dice[tuanzi_id] += 3


calcharo = Tuanzi("卡卡罗", CheckChance.ROLL, calcharo_check)


# shorekeeper
def shorekeeper_check(race_map, tuanzi_id):
    if race_map.dice[tuanzi_id] == 1:
        log("守岸人发动技能")
        race_map.dice[tuanzi_id] = random.randint(2, 3)


shorekeeper = Tuanzi("守岸人", CheckChance.ROLL, shorekeeper_check)


# camellya
def camellya_check(race_map, tuanzi_id):
    if race_map.step[tuanzi_id] == 0:  # 特殊情况刚起步
        return
    if random.random() > 0.5:
        return
    log("椿发动技能")
    now_list = race_map.track[race_map.step[tuanzi_id]]
    race_map.dice[tuanzi_id] += (len(now_list) - 1)
    # 等效为移动到团子顶层
    now_list.remove(tuanzi_id)
    now_list.append(tuanzi_id)


camellya = Tuanzi("椿", CheckChance.BEFORE_RUN, camellya_check)


# carlotta
def carlotta_check(race_map, tuanzi_id):
    if random.random() > 0.28:
        return
    log("土豆地雷发动技能")
    race_map.dice[tuanzi_id] *= 2


carlotta = Tuanzi("柯莱塔", CheckChance.ROLL, carlotta_check)

# ======Test======
if __name__ == "__main__":
    print("直接运行tuanzi.py是无效的，请运行main.py")
