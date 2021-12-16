from testfixtures import compare

from day15.day15 import load_risks, get_path, score_path, embiggen_risks, get_path_astar

test_risks = [
    [1, 1, 6, 3, 7, 5, 1, 7, 4, 2, ],
    [1, 3, 8, 1, 3, 7, 3, 6, 7, 2, ],
    [2, 1, 3, 6, 5, 1, 1, 3, 2, 8, ],
    [3, 6, 9, 4, 9, 3, 1, 5, 6, 9, ],
    [7, 4, 6, 3, 4, 1, 7, 1, 1, 1, ],
    [1, 3, 1, 9, 1, 2, 8, 1, 3, 7, ],
    [1, 3, 5, 9, 9, 1, 2, 4, 2, 1, ],
    [3, 1, 2, 5, 4, 2, 1, 6, 3, 9, ],
    [1, 2, 9, 3, 1, 3, 8, 5, 2, 1, ],
    [2, 3, 1, 1, 9, 4, 4, 5, 8, 1, ],
]


test_shortest_path = [
    (0, 0),
    (1, 0),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (3, 6),
    (3, 7),
    (4, 7),
    (5, 7),
    (5, 8),
    (6, 8),
    (7, 8),
    (8, 8),
    (8, 9),
    (9, 9),
]


def test_load_risks():
    compare(load_risks("day15_test_data.txt"), expected=test_risks)


def test_find_path():
    path = get_path(test_risks)
    compare(path, expected=test_shortest_path)


def test_score_shortest_path():
    compare(score_path(test_shortest_path, test_risks), expected=40)


def test_embiggen_risks():
    expected = """\
11637517422274862853338597396444961841755517295286
13813736722492484783351359589446246169155735727126
21365113283247622439435873354154698446526571955763
36949315694715142671582625378269373648937148475914
74634171118574528222968563933317967414442817852555
13191281372421239248353234135946434524615754563572
13599124212461123532357223464346833457545794456865
31254216394236532741534764385264587549637569865174
12931385212314249632342535174345364628545647573965
23119445813422155692453326671356443778246755488935
22748628533385973964449618417555172952866628316397
24924847833513595894462461691557357271266846838237
32476224394358733541546984465265719557637682166874
47151426715826253782693736489371484759148259586125
85745282229685639333179674144428178525553928963666
24212392483532341359464345246157545635726865674683
24611235323572234643468334575457944568656815567976
42365327415347643852645875496375698651748671976285
23142496323425351743453646285456475739656758684176
34221556924533266713564437782467554889357866599146
33859739644496184175551729528666283163977739427418
35135958944624616915573572712668468382377957949348
43587335415469844652657195576376821668748793277985
58262537826937364893714847591482595861259361697236
96856393331796741444281785255539289636664139174777
35323413594643452461575456357268656746837976785794
35722346434683345754579445686568155679767926678187
53476438526458754963756986517486719762859782187396
34253517434536462854564757396567586841767869795287
45332667135644377824675548893578665991468977611257
44961841755517295286662831639777394274188841538529
46246169155735727126684683823779579493488168151459
54698446526571955763768216687487932779859814388196
69373648937148475914825958612593616972361472718347
17967414442817852555392896366641391747775241285888
46434524615754563572686567468379767857948187896815
46833457545794456865681556797679266781878137789298
64587549637569865174867197628597821873961893298417
45364628545647573965675868417678697952878971816398
56443778246755488935786659914689776112579188722368
55172952866628316397773942741888415385299952649631
57357271266846838237795794934881681514599279262561
65719557637682166874879327798598143881961925499217
71484759148259586125936169723614727183472583829458
28178525553928963666413917477752412858886352396999
57545635726865674683797678579481878968159298917926
57944568656815567976792667818781377892989248891319
75698651748671976285978218739618932984172914319528
56475739656758684176786979528789718163989182927419
67554889357866599146897761125791887223681299833479
"""
    actual = embiggen_risks(test_risks)
    stringy = ""
    for row in actual:
        stringy += ''.join([str(i) for i in row]) + "\n"
    compare(stringy, expected=expected)


def test_big_risks():
    big_risks = embiggen_risks(test_risks)
    path = get_path_astar(big_risks)
    compare(score_path(path, big_risks), expected=315)

def test_using_pathlib():
    from pathfinding.finder.a_star import AStarFinder
    from pathfinding.finder.dijkstra import DijkstraFinder
    from pathfinding.core.grid import Grid

    grid = Grid(matrix=test_risks)
    start = grid.node(0, 0)
    end = grid.node(len(test_risks)-1, len(test_risks)-1)
    finder = AStarFinder()
    path, runs = finder.find_path(start, end, grid)
    flipped_path = [(r, c) for c, r in path]
    compare(flipped_path, expected=test_shortest_path)
