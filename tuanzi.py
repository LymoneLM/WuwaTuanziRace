import random
from enum import Enum, auto


def log(string):
    print(f"[TuanziLog]{string}")


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
        if now == self.check_chance:
            self.check_func(self.race_map, self.tuanzi_id)


"""Note
起始处为0
4+2+3+1+6+3+3+1(完赛) = 23
>=23
"""


class RaceMap:
    def __init__(self, tuanzi: list[Tuanzi], rank: list[int] = None, length=23):
        # 转存
        self.tuanzi = tuanzi
        self.length = length
        # 生成
        self.flag = []
        self.num_tuanzi = len(tuanzi)
        self.step = [0 for _ in range(self.num_tuanzi)]
        self.order = [n for n in range(self.num_tuanzi)]
        self.track = [[] for _ in range(self.length + self.num_tuanzi + 3)]
        for i in range(self.num_tuanzi):
            self.tuanzi[i].set_map(self, i)
        self.dice = [0 for _ in range(self.num_tuanzi)]
        self.roll_dice()  # 第一骰
        # 处理初始位次
        if rank is None:
            for i in range(self.num_tuanzi):
                self.track[0].append(self.order[i])
        else:
            for i in range(self.num_tuanzi):
                self.step[i] = rank[i]
                self.track[rank[i]].append(i)

    def roll_dice(self):
        dice12 = lambda: random.randint(1, 3)
        random.shuffle(self.order)
        self.dice = [dice12() for _ in range(self.num_tuanzi)]

    def run_match(self) -> int:
        while True:
            out = self.run_round()
            self.roll_dice()  # 后置Roll点以适应不同起点
            if out != -1:
                log(f"{self.tuanzi[out].name}获胜")
                return out

    def run_round(self):
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
        source = self.track[self.step[tuanzi_id]]
        diff_step = self.dice[tuanzi_id]
        target = self.track[self.step[tuanzi_id] + diff_step]
        current = source.index(tuanzi_id)
        n = len(source) - current
        for i in range(n):
            tuanzi = source.pop(current)
            self.step[tuanzi] += diff_step
            target.append(tuanzi)
        return self.check_win(tuanzi_id)

    def check_win(self, tuanzi_id):
        if self.step[tuanzi_id] < self.length:
            return -1
        winner_list = self.track[self.step[tuanzi_id]]
        winner = winner_list.pop()
        return winner


# ======Tuanzi======
# jinhsi
def jinhsi_check(race_map, tuanzi_id):
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


# roccia
def roccia_check(race_map, tuanzi_id):
    if race_map.order[race_map.num_tuanzi - 1] == tuanzi_id:
        race_map.dice[tuanzi_id] += 2
        log("洛可可发动技能")


roccia = Tuanzi("洛可可", CheckChance.BEFORE_RUN, roccia_check)


# brant
def brant_check(race_map, tuanzi_id):
    if race_map.order[0] == tuanzi_id:
        race_map.dice[tuanzi_id] += 2
        log("布兰特发动技能")


brant = Tuanzi("布兰特", CheckChance.BEFORE_RUN, brant_check)


# cantarella
def cantarella_check(race_map, tuanzi_id):
    if "cantarella" in race_map.flag:
        return
    diff = race_map.dice[tuanzi_id]
    for i in range(1, diff + 1):
        if race_map.track[race_map.step[tuanzi_id] + i]:
            log("坎大雷发动技能")
            race_map.dice[tuanzi_id] = diff
            race_map.flag.append("cantarella")
            break


cantarella = Tuanzi("坎特雷拉", CheckChance.BEFORE_RUN, cantarella_check)


# zani
def zani_check(race_map, tuanzi_id):
    # 技能1
    if race_map.dice[tuanzi_id] == 2:
        race_map.dice[tuanzi_id] += 1 if random.random() > 0.5 else -1
    # 技能2
    if "zani" in race_map.flag:
        race_map.flag.remove("zani")
        if random.random() <= 0.4:
            log("赞妮发动技能")
            race_map.dice[tuanzi_id] += 2
    if len(race_map.track[race_map.step[tuanzi_id]]) > 1:
        race_map.flag.append("zani")


zani = Tuanzi("赞妮", CheckChance.BEFORE_RUN, zani_check)


# cartethyia
# 某些人的机制能不能不要这么复杂啊！学学菲比好不好
def cartethyia_check(race_map, tuanzi_id):
    if "cartethyia" in race_map.flag:
        if random.random() <= 0.6:
            log("卡提希娅发动技能")
            race_map.dice[tuanzi_id] += 2
    else:
        # 模拟本次移动，以免卡提有两个不同时机的判定函数
        diff = race_map.dice[tuanzi_id]
        cp_step = race_map.step.copy()
        cp_step[tuanzi_id] += diff
        if min(cp_step) == cp_step[tuanzi_id]:
            # 堆叠的情况，最下层是最后一名，显然后来者不会在最下
            if cp_step.count(cp_step[tuanzi_id]) == 1:
                log("卡提希娅启动超级变换形态")
                race_map.flag.append("cartethyia")


cartethyia = Tuanzi("卡提希娅", CheckChance.BEFORE_RUN, cartethyia_check)


# phoebe
def phoebe_check(race_map, tuanzi_id):
    if random.random() <= 0.5:
        log("菲比发动技能")
        race_map.dice[tuanzi_id] += 1


phoebe = Tuanzi("菲比", CheckChance.ROLL, phoebe_check)
# ======Test======
if __name__ == "__main__":
    print("直接运行tuanzi.py是无效的，请运行main.py")
