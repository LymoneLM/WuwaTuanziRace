import tuanzi

def day1():
    tuanzi_list = [
        tuanzi.jinhsi,
        tuanzi.changli,
        tuanzi.calcharo,
        tuanzi.shorekeeper,
        tuanzi.camellya,
        tuanzi.carlotta,
    ]
    score_list = [0 for _ in range(len(tuanzi_list))]
    num = 100000
    for i in range(num):
        race_map = tuanzi.RaceMap(tuanzi_list)
        score_list[race_map.run_match()] += 1
        print(score_list)
    for i in range(len(tuanzi_list)):
        print(f"{tuanzi_list[i].name:<4}\t: {score_list[i] / num:.2%}")

def day2():
    tuanzi_list = [
        tuanzi.shorekeeper,
        tuanzi.camellya,
        tuanzi.jinhsi,
        tuanzi.changli,
        tuanzi.carlotta,
        tuanzi.calcharo,
    ]
    rank = [0,1,1,2,2,3]
    score_list = [0 for _ in range(len(tuanzi_list))]
    num = 100000
    for i in range(num):
        race_map = tuanzi.RaceMap(tuanzi_list, rank, 23+4)
        score_list[race_map.run_match()] += 1
        print(score_list)
    for i in range(len(tuanzi_list)):
        print(f"{tuanzi_list[i].name:<4}\t: {score_list[i] / num:.2%}")

if __name__ == "__main__":
    day2()

