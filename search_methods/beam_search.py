from heapq import heappush, heappop

def beam_search(map, heuristic, beam_width):
    # beam_search cauta o solutie folosind o frontiera limitata (beam width)
    
    # Cel mai bun drum gasit pana acum
    best_path_found = None
    # Scorul euristic al celui mai bun drum
    best_heuristic_score = float("inf")

    # Multimea starilor vizitate
    explored = set()
    explored.add(str(map))

    # Coada de prioritati: (heuristic, cost pana acum, harta, drumul parcurs)
    queue = [(heuristic(map), 0, map.copy(), [])]

    # Numarul de stari explorate (pentru masurare performanta)
    explored_count = 0

    while queue:
        # Sortam frontiera dupa valoarea euristicii si pastram doar cei mai buni beam_width candidati
        queue = sorted(queue, key=lambda elem: elem[0])[:beam_width]
        
        # Coada pentru iteratia urmatoare
        next_round = []

        for h_value, cost_so_far, current_state, current_moves in queue:
            # Daca am ajuns intr-o stare finala unde toate cutiile sunt pe pozitii corecte
            if current_state.is_solved():
                return current_moves, explored_count

            # Expandeaza succesorii starii curente
            for action in current_state.filter_possible_moves():
                # Copiem harta curenta
                candidate = current_state.copy()
                # Aplicam mutarea
                candidate.apply_move(action)
                # Codificam noua stare
                candidate_id = str(candidate)

                # Daca am vizitat deja aceasta stare o ignoram
                if candidate_id in explored:
                    continue

                # Marcam starea ca vizitata 
                explored.add(candidate_id)
                explored_count += 1

                # Actualizam lista de miscari
                new_moves = current_moves + [action]
                # Calculam scorul euristic al noului nod
                score = heuristic(candidate)

                # Adaugam candidatul in urmatoarea frontiera
                heappush(next_round, (score, cost_so_far + 1, candidate, new_moves))

                # Daca am ajuns la solutie si scorul este mai bun o retinem
                if candidate.is_solved() and score < best_heuristic_score:
                    best_path_found = new_moves
                    best_heuristic_score = score

        # Actualizam frontiera pentru urmatorul pas
        queue = next_round

    # Daca am gasit un drum valid il returnam
    return best_path_found, explored_count
