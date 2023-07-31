from queue import Queue
import copy

def read_input_file(input_file):
    with open(input_file, "r") as file:
        N, M = map(int, file.readline().split())
        graph = [list(map(int, file.readline().split())) for _ in range(N)]
        start_x, start_y = map(int, file.readline().split())

    return N, M, graph, start_x, start_y

def write_result_to_file(file_path, result):
    with open(file_path, 'w') as file:
        file.write(result)

def is_valid_move(x, y, N, M, graph):
    return 0 <= x < N and 0 <= y < M and graph[x][y] != 1

def get_adjacent_tiles(x, y, N, M, graph):
    adjacent_tiles = []
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    for i in range(4):
        new_x, new_y = x + dx[i], y + dy[i]
        if is_valid_move(new_x, new_y, N, M, graph):
            adjacent_tiles.append((new_x, new_y))

    return adjacent_tiles

def bfs(graph, start_x, start_y, target_x, target_y, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    queue = Queue()
    queue.put((start_x, start_y))
    visited[start_x][start_y] = True
    parent = {(start_x, start_y): None}

    while not queue.empty():
        x, y = queue.get()

        if x == target_x and y == target_y:
            path = []
            current = (x, y)
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for adj_x, adj_y in get_adjacent_tiles(x, y, N, M, graph):
            if not visited[adj_x][adj_y]:
                queue.put((adj_x, adj_y))
                visited[adj_x][adj_y] = True
                parent[(adj_x, adj_y)] = (x, y)

    return None  # No path to food

def find_nearest_food(graph, start_x, start_y, N, M):
    nearest_food = None
    min_distance = float('inf')

    for i in range(N):
        for j in range(M):
            if graph[i][j] == 2:
                distance = abs(i - start_x) + abs(j - start_y)
                if distance < min_distance:
                    min_distance = distance
                    nearest_food = (i, j)

    return nearest_food

def play_game_level_1(graph, start_x, start_y, N, M):
    game_points = 0

    while True:
        nearest_food = find_nearest_food(graph, start_x, start_y, N, M)
        if nearest_food is None:
            break

        path = bfs(graph, start_x, start_y, nearest_food[0], nearest_food[1], N, M)
        if path is None or len(path) < 2:
            print("No path to food!")
            return

        game_points += len(path) + 20 - len(path) - 1
        start_x, start_y = path[1]

        graph[start_x][start_y] = 0

    return game_points

def bfs_with_visibility_limit(graph, start_x, start_y, target_x, target_y, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    queue = Queue()
    queue.put((start_x, start_y, 0))
    visited[start_x][start_y] = True
    parent = {(start_x, start_y): None}

    while not queue.empty():
        x, y, visibility = queue.get()

        if x == target_x and y == target_y:
            path = []
            current = (x, y)
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        if visibility >= 3:
            continue

        for adj_x, adj_y in get_adjacent_tiles(x, y, N, M, graph):
            if not visited[adj_x][adj_y]:
                queue.put((adj_x, adj_y, visibility + 1))
                visited[adj_x][adj_y] = True
                parent[(adj_x, adj_y)] = (x, y)

    return None  # No path to food

def play_game_level_2(graph, start_x, start_y, N, M):
    game_points = 0

    while True:
        nearest_food = find_nearest_food(graph, start_x, start_y, N, M)
        if nearest_food is None:
            break

        path = bfs(graph, start_x, start_y, nearest_food[0], nearest_food[1], N, M)
        if path is None or len(path) < 2:
            print("No path to food!")
            return

        game_points += len(path) + 20 - len(path) - 1
        start_x, start_y = path[1]

        graph[start_x][start_y] = 0

    return game_points

def play_game_level_3(graph, start_x, start_y, N, M):
    game_points = 0

    while True:
        nearest_food = find_nearest_food(graph, start_x, start_y, N, M)
        if nearest_food is None:
            break

        path = bfs_with_visibility_limit(graph, start_x, start_y, nearest_food[0], nearest_food[1], N, M)
        if path is None or len(path) < 2:
            print("No path to food!")
            return

        game_points += len(path) + 20 - len(path) - 1
        start_x, start_y = path[1]

        graph[start_x][start_y] = 0

    return game_points

def main():
    input_file = "map1.txt"
    N, M, graph, start_x, start_y = read_input_file(input_file)

    result = f"Level 1:\n"
    result += "\n".join(" ".join(str(cell) for cell in row) for row in graph)
    result += "\n\n"

    game_points = play_game_level_1(copy.deepcopy(graph), start_x, start_y, N, M)

    if game_points is not None:
        result += f"Game points: {game_points}\n"

        output_file = "result1.txt"
        write_result_to_file(output_file, result)

    result += f"Level 2:\n"
    result += "\n".join(" ".join(str(cell) for cell in row) for row in graph)
    result += "\n\n"

    game_points = play_game_level_2(copy.deepcopy(graph), start_x, start_y, N, M)

    if game_points is not None:
        result += f"Game points: {game_points}\n"

        output_file = "result2.txt"
        write_result_to_file(output_file, result)

    result += f"Level 3:\n"
    result += "\n".join(" ".join(str(cell) for cell in row) for row in graph)
    result += "\n\n"

    game_points = play_game_level_3(copy.deepcopy(graph), start_x, start_y, N, M)

    if game_points is not None:
        result += f"Game points: {game_points}\n"

        output_file = "result3.txt"
        write_result_to_file(output_file, result)

if __name__ == "__main__":
    main()
