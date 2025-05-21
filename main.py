import sys
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
    print(f"{rounds}回合模拟团子胜率：")
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
    return tuanzi_list, run(tuanzi_list)


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
    return tuanzi_list, run(tuanzi_list, rank=rank, length=23+4)


def day3():
    tuanzi_list = [
        tuanzi.roccia,
        tuanzi.brant,
        tuanzi.cantarella,
        tuanzi.zani,
        tuanzi.cartethyia,
        tuanzi.phoebe,
    ]
    return tuanzi_list, run(tuanzi_list)


def day4():
    tuanzi_list = [
        tuanzi.phoebe,
        tuanzi.zani,
        tuanzi.brant,
        tuanzi.cartethyia,
        tuanzi.roccia,
        tuanzi.cantarella,
    ]
    rank = [0, 1, 1, 2, 2, 3]
    return tuanzi_list, run(tuanzi_list, rank=rank, length=23+4)


def day5():
    tuanzi_list = [
        tuanzi.jinhsi,
        tuanzi.changli,
        tuanzi.calcharo,
        tuanzi.shorekeeper,
    ]
    return tuanzi_list, run(tuanzi_list)


def day6():
    tuanzi_list = [
        tuanzi.shorekeeper,
        tuanzi.jinhsi,
        tuanzi.calcharo,
        tuanzi.changli,
    ]
    rank = [0, 1, 2, 3]
    return tuanzi_list, run(tuanzi_list, rank=rank, length=23+4)


def day7():
    tuanzi_list = [
        tuanzi.roccia,
        tuanzi.brant,
        tuanzi.zani,
        tuanzi.phoebe,
    ]
    return tuanzi_list, run(tuanzi_list)


def day8():
    tuanzi_list = [
        tuanzi.roccia,
        tuanzi.brant,
        tuanzi.phoebe,
        tuanzi.zani,
    ]
    rank = [0, 1, 2, 3]
    return tuanzi_list, run(tuanzi_list, rank=rank, length=23 + 4)

def day9():
    tuanzi_list = [
        tuanzi.shorekeeper,
        tuanzi.calcharo,
        tuanzi.brant,
        tuanzi.zani,
    ]
    return tuanzi_list, run(tuanzi_list)


def repechage():
    tuanzi_list = [
        tuanzi.camellya,
        tuanzi.carlotta,
        tuanzi.jinhsi,
        tuanzi.changli,
        tuanzi.cantarella,
        tuanzi.cartethyia,
        tuanzi.phoebe,
        tuanzi.roccia,
    ]
    run(tuanzi_list)


def repechage_a():
    tuanzi_list = [
        tuanzi.camellya,
        tuanzi.carlotta,
        tuanzi.jinhsi,
        tuanzi.changli,

    ]
    run(tuanzi_list)


def repechage_b():
    tuanzi_list = [
        tuanzi.cantarella,
        tuanzi.cartethyia,
        tuanzi.phoebe,
        tuanzi.roccia,
    ]
    run(tuanzi_list)


def all():
    tuanzi_list = [
        tuanzi.jinhsi,
        tuanzi.changli,
        tuanzi.calcharo,
        tuanzi.shorekeeper,
        tuanzi.camellya,
        tuanzi.carlotta,
        tuanzi.roccia,
        tuanzi.brant,
        tuanzi.cantarella,
        tuanzi.zani,
        tuanzi.cartethyia,
        tuanzi.phoebe,
    ]
    run(tuanzi_list,length=47)

if __name__ == "__main__":
    all()
