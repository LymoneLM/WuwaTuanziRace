import tuanzi


rounds = 100000

def run(tuanzi_list, **kw):
    rank = None
    if "rank" in kw:
        rank = kw["rank"]
    length = 23
    if length in kw:
        length = kw["length"]
    score_list = [0 for _ in range(len(tuanzi_list))]
    for i in range(rounds):
        race_map = tuanzi.RaceMap(tuanzi_list, rank, length)
        score_list[race_map.run_match()] += 1
        print(score_list)
    for i in range(len(tuanzi_list)):
        print(f"{tuanzi_list[i].name:<4}\t: {score_list[i] / rounds:.2%}")

def day1():
    tuanzi_list = [
        tuanzi.jinhsi,
        tuanzi.changli,
        tuanzi.calcharo,
        tuanzi.shorekeeper,
        tuanzi.camellya,
        tuanzi.carlotta,
    ]
    run(tuanzi_list)


def day2():
    tuanzi_list = [
        tuanzi.shorekeeper,
        tuanzi.camellya,
        tuanzi.jinhsi,
        tuanzi.changli,
        tuanzi.carlotta,
        tuanzi.calcharo,
    ]
    rank = [0, 1, 1, 2, 2, 3]
    run(tuanzi_list, rank=rank, length=23+4)


def day3():
    tuanzi_list = [
        tuanzi.roccia,
        tuanzi.brant,
        tuanzi.cantarella,
        tuanzi.zani,
        tuanzi.cartethyia,
        tuanzi.phoebe,
    ]
    run(tuanzi_list)


if __name__ == "__main__":
    day3()
