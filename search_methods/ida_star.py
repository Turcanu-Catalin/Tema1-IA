def successors(map_obj):
    # Pentru fiecare mutare valida a jucatorului
    for move in map_obj.filter_possible_moves():
        # Cream o copie a starii curente
        next_map = map_obj.copy()
        # Aplicam mutarea pe copia hartii
        next_map.apply_move(move)
        # Returnam noua stare si mutarea efectuata
        yield next_map, move

def dfs_search(path, g, bound, visited, move_path, heuristic, explored_count):
    # Selectam ultimul nod din cale
    node = path[-1]
    # Calculam functia f(n) = g(n) + h(n)
    f = g + heuristic(node)

    # Daca f depaseste pragul actual intoarcem f pentru a actualiza limita
    if f > bound:
        return f

    # Daca nodul curent reprezinta o stare finala
    if node.is_solved():
        return "Found"

    # Initializam costul minim ca infinit
    min_cost = float("inf")

    # Iteram prin toate starile succesor generate
    for succ_map, move in successors(node):
        # Codificam starea succesor
        succ_state = str(succ_map)

        # Daca am vizitat deja aceasta stare, o sarim
        if succ_state in visited:
            continue

        # Cresterea contorului de stari explorate
        explored_count[0] += 1

        # Adaugam succesorul la calea parcursa
        path.append(succ_map)
        # Adaugam mutarea corespunzatoare
        move_path.append(move)
        # Marcam succesorul ca vizitat
        visited.add(succ_state)

        # Apelam recursiv cautarea din succesor
        t = dfs_search(path, g + 1, bound, visited, move_path, heuristic, explored_count)

        # Daca am gasit solutia, o propagam inapoi
        if t == "Found":
            return "Found"

        # Actualizam costul minim pentru iteratia urmatoare
        if t < min_cost:
            min_cost = t

        # Daca nu am gasit solutie pe aceasta ramura, facem backtracking
        path.pop()
        move_path.pop()
        visited.remove(succ_state)

    # Returnam cel mai mic prag depasit
    return min_cost

def ida_star(start_map, heuristic=None):
    # Functia principala pentru lansarea algoritmului IDA*

    # Daca nu avem o euristica furnizata, folosim euristica nula
    if heuristic is None:
        heuristic = lambda m: 0

    # Initializam pragul cu valoarea euristicii pentru starea initiala
    bound = heuristic(start_map)

    # Calea curenta contine doar harta initiala
    path = [start_map.copy()]

    # Lista mutarilor efectuate
    move_path = []

    # Numar de stari explorate (folosim lista pentru a modifica in recursie)
    explored_count = [0]

    # Repetam pana gasim solutia sau confirmam ca nu exista
    while True:
        # Resetam starile vizitate pentru fiecare iteratie
        visited = set()
        visited.add(str(start_map))

        # Apelam cautarea limitata de prag
        t = dfs_search(path, 0, bound, visited, move_path, heuristic, explored_count)

        # Daca am gasit solutie, o returnam impreuna cu numarul de stari
        if t == "Found":
            return move_path, explored_count[0]

        # Daca nu mai exista solutie, returnam None
        if t == float("inf"):
            return None, explored_count[0]

        # Actualizam pragul pentru urmatoarea iteratie
        bound = t
