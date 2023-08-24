import tkinter as tk
from tkinter import messagebox
import random


class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku App")
        self.solution = None  # Add this attribute to store the solution
        self.create_ui()

    def create_ui(self):
        self.cells = []
        self.solution = [[0] * 9 for _ in range(9)]

        for i in range(9):
            row = []
            for j in range(9):
                cell = tk.Entry(
                    self.root, width=2, font=("Arial", 18), justify="center"
                )
                cell.grid(row=i, column=j, padx=1, pady=1)
                row.append(cell)
            self.cells.append(row)

        generate_button = tk.Button(
            self.root, text="Generate", command=self.generate_puzzle
        )
        generate_button.grid(row=9, column=0, columnspan=3, padx=10, pady=5)

        solve_button = tk.Button(self.root, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=9, column=3, columnspan=3, padx=10, pady=5)

        verify_button = tk.Button(
            self.root, text="Verify", command=self.verify_solution
        )
        verify_button.grid(row=9, column=6, columnspan=3, padx=10, pady=5)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_grid)
        clear_button.grid(row=10, column=0, columnspan=9, padx=10, pady=5)

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Easy")
        difficulty_menu = tk.OptionMenu(
            self.root, self.difficulty_var, "Easy", "Medium", "Hard"
        )
        difficulty_menu.grid(row=11, column=0, columnspan=9, padx=10, pady=5)

    def generate_puzzle(self):
        self.clear_grid()

        self.solution = self.generate_sudoku_solution()  # Store the solution
        self.solution_backup = [
            row[:] for row in self.solution
        ]  # Store a backup of the solution

        difficulty = self.difficulty_var.get()
        if difficulty == "Medium":
            num_to_remove = 40
        elif difficulty == "Hard":
            num_to_remove = 50
        else:
            num_to_remove = 30

        self.fill_cells(num_to_remove)
        self.update_grid_with_solution()

    def update_grid_with_solution(self):
        for i in range(9):
            for j in range(9):
                value = self.solution[i][j]
                if value != 0:
                    self.cells[i][j].insert(0, str(value))
                    self.cells[i][j].config(state="disabled")

    def generate_sudoku_solution(self):
        n = 9

        def is_valid(board, row, col, num):
            for i in range(n):
                if board[row][i] == num or board[i][col] == num:
                    return False

            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(3):
                for j in range(3):
                    if board[start_row + i][start_col + j] == num:
                        return False
            return True

        def solve(board):
            for row in range(n):
                for col in range(n):
                    if board[row][col] == 0:
                        nums = list(range(1, n + 1))
                        random.shuffle(nums)
                        for num in nums:
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                if solve(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        board = [[0 for _ in range(n)] for _ in range(n)]
        solve(board)
        return board

    def fill_cells(self, num_to_remove):
        cells_to_remove = set()

        while len(cells_to_remove) < num_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if (row, col) not in cells_to_remove and self.solution[row][col] != 0:
                cells_to_remove.add((row, col))

        for row, col in cells_to_remove:
            self.solution[row][col] = 0
            self.cells[row][col].delete(0, tk.END)
            self.cells[row][col].config(state="normal")

    def solve_sudoku(self):
        if self.solution_backup:
            for i in range(9):
                for j in range(9):
                    if self.cells[i][j].get() == "":
                        self.cells[i][j].delete(0, tk.END)
                        self.cells[i][j].insert(0, str(self.solution_backup[i][j]))

    def verify_solution(self):
        user_solution = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[i][j].get()
                if value == "":
                    row.append(0)
                else:
                    try:
                        int_value = int(value)
                        row.append(int_value)
                    except ValueError:
                        messagebox.showerror(
                            "Verification", "Please enter integers in all cells."
                        )
                        return
            user_solution.append(row)

        if self.is_valid_solution(user_solution):
            messagebox.showinfo(
                "Verification", "Congratulations! You've solved the puzzle."
            )
        else:
            messagebox.showerror(
                "Verification", "Sorry, the puzzle solution is incorrect."
            )

    def is_valid_solution(self, solution):
        def is_valid_unit(unit):
            unit_numbers = [num for num in unit if num != 0]
            return (
                len(unit_numbers) == len(set(unit_numbers))
                and all(1 <= num <= 9 for num in unit_numbers)
                and sum(unit_numbers) == sum(range(1, 10))
            )

        # Check rows
        for row in solution:
            if not is_valid_unit(row):
                return False

        # Check columns
        for col in range(9):
            column = [solution[row][col] for row in range(9)]
            if not is_valid_unit(column):
                return False

        # Check subgrids (3x3 boxes)
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subgrid = [
                    solution[row][col]
                    for row in range(i, i + 3)
                    for col in range(j, j + 3)
                ]
                if not is_valid_unit(subgrid):
                    return False

        return True

    def clear_grid(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].config(state="normal")
                self.solution[i][j] = 0
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].config(state="normal")
                self.solution[i][j] = 0


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.resizable(width=False, height=False)
    root.mainloop()
