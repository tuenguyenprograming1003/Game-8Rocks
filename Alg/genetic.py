import random

n = 8

def fitness(ind):
    """Tính fitness của cá thể cho 8 quân xe - fitness = số cột unique"""
    return len(set(ind))  # Với 8 quân xe, ta cần 8 cột khác nhau

def create_individual():
    """Tạo một cá thể ngẫu nhiên - permutation của [0,1,2,3,4,5,6,7]"""
    individual = list(range(n))
    random.shuffle(individual)
    return individual

def create_population(size):
    """Tạo quần thể ban đầu"""
    return [create_individual() for _ in range(size)]

def tournament_selection(pop, fit_scores, tournament_size=3):
    """Chọn lọc tournament"""
    selected = []
    for _ in range(len(pop)):
        # Chọn ngẫu nhiên tournament_size cá thể
        candidates = random.sample(list(zip(pop, fit_scores)), tournament_size)
        # Chọn cá thể có fitness cao nhất
        winner = max(candidates, key=lambda x: x[1])
        selected.append(winner[0])
    return selected

def crossover(parent1, parent2):
    """Order Crossover (OX) để duy trì tính chất permutation"""
    if random.random() < 0.8:  # Xác suất lai ghép
        # Chọn 2 điểm cắt ngẫu nhiên
        start, end = sorted(random.sample(range(n), 2))
        
        # Child 1
        child1 = [-1] * n
        child1[start:end] = parent1[start:end]
        pointer = end
        for val in parent2[end:] + parent2[:end]:
            if val not in child1:
                child1[pointer % n] = val
                pointer += 1
        
        # Child 2  
        child2 = [-1] * n
        child2[start:end] = parent2[start:end]
        pointer = end
        for val in parent1[end:] + parent1[:end]:
            if val not in child2:
                child2[pointer % n] = val
                pointer += 1
                
        return child1, child2
    return parent1.copy(), parent2.copy()

def mutate(ind, mutation_rate=0.1):
    """Swap mutation để duy trì tính chất permutation"""
    mutated = ind.copy()
    if random.random() < mutation_rate:
        # Swap 2 vị trí ngẫu nhiên
        i, j = random.sample(range(n), 2)
        mutated[i], mutated[j] = mutated[j], mutated[i]
    return mutated

def genetic_target(tg, pop_size=100, max_gen=200):
    """Genetic Algorithm để tìm đường đến target"""
    # Nếu target là [None]*8, tìm lời giải tổng quát
    if all(x is None for x in tg):
        return genetic_simple(pop_size, max_gen)
    
    # Tạo quần thể ban đầu với một số cá thể gần target
    pop = create_population(pop_size // 2)
    
    # Thêm một số cá thể được tạo bằng cách mutate từ target
    for _ in range(pop_size // 2):
        individual = tg.copy()
        # Mutate một vài lần để tạo diversity
        for _ in range(random.randint(1, 3)):
            individual = mutate(individual, 0.3)
        pop.append(individual)
    
    path = []
    best_individual = None
    best_distance = float('inf')
    stagnant_generations = 0
    
    for gen in range(max_gen):
        # Tính fitness dựa trên khoảng cách đến target
        distances = []
        for ind in pop:
            dist = sum(1 for i in range(n) if ind[i] != tg[i])
            distances.append(dist)
            
            # Theo dõi cá thể tốt nhất
            if dist < best_distance:
                best_distance = dist
                best_individual = ind.copy()
                stagnant_generations = 0  # Reset counter
                
        # Nếu đã tìm được target chính xác
        if best_distance == 0:
            break
            
        # Nếu không cải thiện trong nhiều generations, restart
        stagnant_generations += 1
        if stagnant_generations > 20:
            # Restart với population mới, giữ lại best individual
            pop = create_population(pop_size - 1)
            if best_individual:
                pop.append(best_individual.copy())
            stagnant_generations = 0
            
        # Chọn lọc với pressure cao hơn cho target cụ thể
        fit_scores = [(max_gen * 2) - dist for dist in distances]
        selected = tournament_selection(pop, fit_scores, tournament_size=5)
        
        # Lai ghép và đột biến với rate cao hơn
        new_pop = []
        for i in range(0, len(selected), 2):
            if i + 1 < len(selected):
                child1, child2 = crossover(selected[i], selected[i+1])
                child1 = mutate(child1, 0.15)  # Tăng mutation rate
                child2 = mutate(child2, 0.15)
                new_pop.extend([child1, child2])
            else:
                new_pop.append(mutate(selected[i], 0.15))
        
        pop = new_pop[:pop_size]
        
        # Lưu thế hệ tốt nhất vào path
        if best_individual:
            path.append(best_individual.copy())
    
    # Tạo step-by-step path từ solution cuối cùng
    if best_individual:
        step_path = []
        for i in range(n):
            step = [None] * n
            for j in range(i + 1):
                step[j] = best_individual[j]
            step_path.append(step)
        return step_path
    
    return path if path else [tg.copy()]

def genetic_simple(pop_size=50, max_gen=100):
    """Genetic Algorithm để giải bài toán 8 quân xe tổng quát"""
    # Tạo quần thể ban đầu
    pop = create_population(pop_size)
    path = []
    best_individual = None
    best_fitness = -1
    
    for gen in range(max_gen):
        # Tính fitness cho từng cá thể
        fit_scores = [fitness(ind) for ind in pop]
        
        # Tìm cá thể tốt nhất trong thế hệ này
        max_fit = max(fit_scores)
        if max_fit > best_fitness:
            best_fitness = max_fit
            best_idx = fit_scores.index(max_fit)
            best_individual = pop[best_idx].copy()
            path.append(best_individual.copy())
        
        # Nếu đã tìm được lời giải hoàn hảo (8 cột khác nhau)
        if best_fitness == n:
            break
            
        # Chọn lọc
        selected = tournament_selection(pop, fit_scores)
        
        # Lai ghép và đột biến
        new_pop = []
        for i in range(0, len(selected), 2):
            if i + 1 < len(selected):
                child1, child2 = crossover(selected[i], selected[i+1])
                child1 = mutate(child1)
                child2 = mutate(child2)
                new_pop.extend([child1, child2])
            else:
                new_pop.append(mutate(selected[i]))
        
        pop = new_pop[:pop_size]
    
    return path if path else [create_individual()]
