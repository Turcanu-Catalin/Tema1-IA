def is_blocked(box, map_obj):
    # Verifica daca o cutie este blocata intr-un colt sau langa pereti

    x, y = box
    walls = set(map_obj.obstacles)  # Set de pozitii cu ziduri

    # Daca cutia este deja pe o tinta, nu o consideram blocata
    if (x, y) in map_obj.targets:
        return False

    # Definim combinatii de colturi: doua ziduri adiacente
    corners = [
        ((-1, 0), (0, -1)),  # Sus si stanga
        ((-1, 0), (0, 1)),   # Sus si dreapta
        ((1, 0), (0, -1)),   # Jos si stanga
        ((1, 0), (0, 1))     # Jos si dreapta
    ]

    # Verificam daca exista doua ziduri adiacente pozitiei cutiei
    for (dx1, dy1), (dx2, dy2) in corners:
        if ((x + dx1, y + dy1) in walls) and ((x + dx2, y + dy2) in walls):
            return True  # Cutia este blocata

    return False  # Cutia nu este blocata

def ida_heuristic(map_obj):
    # Euristica folosita pentru IDA* bazata pe matching greedy cutii-tinte si penalizare pentru blocaje

    boxes = list(map_obj.positions_of_boxes.keys())  # Lista pozitii cutii
    goals = list(map_obj.targets)                   # Lista pozitii tinte
    total = 0                                        # Cost total euristic

    used_goals = set()  # Tintele deja asociate

    # Asociem fiecare cutie cu cea mai apropiata tinta libera
    for box in boxes:
        min_dist = float('inf')
        best_goal = None

        for goal in goals:
            if goal in used_goals:
                continue  # Evitam asocierea dubla a tintelor
            dist = abs(box[0] - goal[0]) + abs(box[1] - goal[1])  # Distanta Manhattan
            if dist < min_dist:
                min_dist = dist
                best_goal = goal

        if best_goal:
            total += min_dist
            used_goals.add(best_goal)

    # Penalizam starile in care cutiile sunt blocate
    penalty = sum(1000 for box in boxes if is_blocked(box, map_obj))
    return total + penalty  # Cost total + penalizari

def beam_search_heuristic(map_obj):
    # Euristica folosita pentru Beam Search, identica cu cea de la IDA* pentru uniformitate

    boxes = list(map_obj.positions_of_boxes.keys())  # Lista pozitii cutii
    goals = list(map_obj.targets)                   # Lista pozitii tinte
    total = 0                                        # Cost total euristic

    used_goals = set()  # Tintele deja asociate

    # Asociem fiecare cutie cu cea mai apropiata tinta libera
    for box in boxes:
        min_dist = float('inf')
        best_goal = None

        for goal in goals:
            if goal in used_goals:
                continue
            dist = abs(box[0] - goal[0]) + abs(box[1] - goal[1])  # Distanta Manhattan
            if dist < min_dist:
                min_dist = dist
                best_goal = goal

        if best_goal:
            total += min_dist
            used_goals.add(best_goal)

    # Penalizam cutiile blocate (identic cu IDA*)
    penalty = sum(1000 for box in boxes if is_blocked(box, map_obj))
    return total + penalty
