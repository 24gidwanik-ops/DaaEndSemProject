import streamlit as st

def is_safe(maze, x, y, n):
    return 0 <= x < n and 0 <= y < n and maze[x][y] == 1

def solve_maze_util(maze, x, y, n, solution):
    if x == n - 1 and y == n - 1 and maze[x][y] == 1:
        solution[x][y] = 1
        return True
    if is_safe(maze, x, y, n):
        solution[x][y] = 1

        # Move Down
        if solve_maze_util(maze, x + 1, y, n, solution):
            return True
        # Move Right
        if solve_maze_util(maze, x, y + 1, n, solution):
            return True
        # Move Up
        if solve_maze_util(maze, x - 1, y, n, solution):
            return True
        # Move Left
        if solve_maze_util(maze, x, y - 1, n, solution):
            return True

        # Backtrack
        solution[x][y] = 0
        return False
    return False

def solve_maze(maze):
    n = len(maze)
    solution = [[0]*n for _ in range(n)]
    if solve_maze_util(maze, 0, 0, n, solution):
        return solution
    else:
        return None

def main():
    st.title("🐭 Rat in a Maze - Streamlit Edition")

    n = st.number_input("Enter Maze Size (n x n)", min_value=2, max_value=10, value=4, step=1)

    # Initialize maze matrix input
    st.write("Enter maze values (0 for blocked, 1 for open):")

    maze = []
    cols = st.columns(n)
    # Use session state to store the inputs
    if "maze_values" not in st.session_state:
        st.session_state.maze_values = [[1]*n for _ in range(n)]

    for i in range(n):
        row_values = []
        for j in range(n):
            with cols[j]:
                val = st.number_input(
                    label=f"Cell ({i+1},{j+1})",
                    min_value=0,
                    max_value=1,
                    value=st.session_state.maze_values[i][j],
                    key=f"cell_{i}_{j}"
                )
                row_values.append(val)
        maze.append(row_values)

    # Save inputs to session state
    st.session_state.maze_values = maze

    if st.button("Solve Maze"):
        # Validate start and end positions
        if maze[0][0] == 0 or maze[n-1][n-1] == 0:
            st.error("Start or end cell is blocked! Maze unsolvable.")
            return

        solution = solve_maze(maze)
        if solution:
            st.success("✅ Path Found:")
            for row in solution:
                st.write(" ".join(str(cell) for cell in row))
        else:
            st.error("❌ No path found in the maze.")

if __name__ == "__main__":
    main()
