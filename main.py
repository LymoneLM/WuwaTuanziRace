import tuanzi

if __name__ == "__main__":
    tuanzi_list = [tuanzi.jinhsi,
                   tuanzi.changli,
                   tuanzi.calcharo,
                   tuanzi.shorekeeper,
                   tuanzi.camellya,
                   tuanzi.carlotta
                   ]
    score_list = [0 for i in range(len(tuanzi_list))]
    num = 10000
    print(score_list)
    for i in range(num):
        race_map = tuanzi.RaceMap(tuanzi_list)
        score_list[race_map.run_match()] += 1
        print(score_list)
    for i in range(len(tuanzi_list)):
        print(f"{tuanzi_list[i].name}:{score_list[i] / num:.2%}")