import sys

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QPushButton, QLabel,
                               QDialog, QGridLayout, QMessageBox, QFrame)


class Position:  # Позиции на доске

    def __init__(self, x, y):
        self.x = x  # Координата X (столбец)
        self.y = y  # Координата Y (Строка)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):  # Проверка равенства 2ух позиций
        return isinstance(other, Position) and self.x == other.x and self.y == other.y


class CamelPiece:  # Верблюд
    def __init__(self, position):
        self.position = position  # Позиция фигуры на доске

    def get_attack_positions(self, board_size):  # Атаковвнные клетки
        attacks = set()
        x, y = self.position.x, self.position.y

        # Возможные ходы верблюда
        moves = [
            (3, 1), (3, -1), (-3, 1), (-3, -1),
            (1, 3), (1, -3), (-1, 3), (-1, -3)
        ]

        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < board_size and 0 <= new_y < board_size:
                attacks.add(Position(new_x, new_y))

        return attacks

    def can_attack(self, other_position, board_size):  # Проверка, может ли верблюд атаковать позицию
        return other_position in self.get_attack_positions(board_size)


class ChessBoard:  # Шахматная доска

    def __init__(self, size):
        self.size = size  # Размер доски
        self.placed_pieces = []  # Список установленных фигут

    def add_piece(self, position):  # Добавление фигур
        if not self.is_position_valid(position):
            return False

        new_piece = CamelPiece(position)

        # Проверка на то, может ли новая фигура атаковать уже существующие фигуры
        for existing_piece in self.placed_pieces:
            if (new_piece.can_attack(existing_piece.position, self.size) or
                    existing_piece.can_attack(new_piece.position, self.size)):
                return False

        self.placed_pieces.append(new_piece)
        return True

    def is_position_valid(self, position):  # Проверка не выходит ли фигура за пределы доски
        return (0 <= position.x < self.size and
                0 <= position.y < self.size and
                not self.is_position_occupied(position))

    def is_position_occupied(self, position):  # Проверка не занята ли клетка
        return any(piece.position == position for piece in self.placed_pieces)

    def get_all_attacked_positions(self):  # Возвращает клетки, которые атакуются
        attacked = set()
        for piece in self.placed_pieces:
            attacked.update(piece.get_attack_positions(self.size))
        return attacked

    def get_piece_positions(self):  # Возвращает позиции всех фигур на доске
        return [piece.position for piece in self.placed_pieces]

    def clear(self):  # Очищает доску
        self.placed_pieces.clear()


class CamelSolver:  # Решение задачи
    def __init__(self, board_size, existing_positions):
        self.board_size = board_size  # Размер доски
        self.existing_positions = existing_positions  # Существующие позиции
        self.solutions = []  # Решения

    def solve(self, additional_pieces):  # Поиск решений
        # Создаем доску с уже размещенными фигурами
        board = ChessBoard(self.board_size)
        for pos in self.existing_positions:
            board.add_piece(pos)

        # Свободные клетки
        free_positions = []
        attacked_positions = board.get_all_attacked_positions()

        for x in range(self.board_size):
            for y in range(self.board_size):
                pos = Position(x, y)
                if (not board.is_position_occupied(pos) and
                        pos not in attacked_positions):
                    free_positions.append(pos)

        # Находим все возможные комбинации для размещения дополнительных фигур
        self.solutions = []
        if additional_pieces == 0:
            self.solutions.append(self.existing_positions.copy())
        else:
            self._find_solutions(board.placed_pieces.copy(), free_positions, additional_pieces)

        return self.solutions

    def _find_solutions(self, current_pieces, available_positions, remaining):  # рекурсивно находим решения
        if remaining == 0:
            all_positions = [piece.position for piece in current_pieces]
            self.solutions.append(all_positions)
            return

        if len(available_positions) < remaining:
            return  # Недостаточно клеток

        # Возможные клетки для следующей фигуры
        for i in range(len(available_positions) - remaining + 1):
            pos = available_positions[i]

            new_piece = CamelPiece(pos)

            # Проверка можно ли разместить фигуру
            can_place = True
            for existing_piece in current_pieces:
                if (new_piece.can_attack(existing_piece.position, self.board_size) or
                        existing_piece.can_attack(new_piece.position, self.board_size)):
                    can_place = False
                    break

            if can_place:  # Размещение фигуры
                new_pieces = current_pieces + [new_piece]

                # Обновляем список доступных клеток
                new_available = []
                attacked_by_new = new_piece.get_attack_positions(self.board_size)

                for j in range(i + 1, len(available_positions)):
                    candidate_pos = available_positions[j]
                    if candidate_pos not in attacked_by_new:
                        # Проверка, что фигура не атакует новую фигуру
                        candidate_piece = CamelPiece(candidate_pos)
                        if not candidate_piece.can_attack(pos, self.board_size):
                            new_available.append(candidate_pos)

                self._find_solutions(new_pieces, new_available, remaining - 1)


class SolverWorker(QThread):  # Решение в отдельном потоке

    solution_found = Signal(list)  # Найденные решения

    def __init__(self, board_size, existing_positions, additional_pieces):
        super().__init__()
        self.board_size = board_size
        self.existing_positions = existing_positions
        self.additional_pieces = additional_pieces

    def run(self):  # Решение задачи в отдельном потоке
        solver = CamelSolver(self.board_size, self.existing_positions)
        solutions = solver.solve(self.additional_pieces)
        self.solution_found.emit(solutions)


class CoordinateInputDialog(QDialog):  # Ввод координат

    def __init__(self, parent, num_pieces, board_size):
        super().__init__(parent)
        self.num_pieces = num_pieces  # Кол-во вводимых фигур
        self.board_size = board_size  # Размер доски
        self.coordinate_inputs = []  # Поля ввода координат
        self.positions = []

        self.setWindowTitle("Ввод координат")
        self.setModal(True)
        self.setFixedSize(300, 150)

        self.setup_ui()
        self.update_ok_button_state()

    def setup_ui(self):  # Интерфейс
        layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel("Введите координаты:")
        layout.addWidget(title_label)

        # Поля ввода координат
        for i in range(self.num_pieces):
            coord_layout = QHBoxLayout()
            label = QLabel(f"№{i + 1}")
            coord_input = QLineEdit()
            coord_input.setPlaceholderText("x y")
            coord_input.textChanged.connect(self.validate_coordinates)

            coord_layout.addWidget(label)
            coord_layout.addWidget(coord_input)
            layout.addLayout(coord_layout)

            self.coordinate_inputs.append(coord_input)

        # Кнопки
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        self.ok_button.clicked.connect(self.accept_coordinates)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def validate_coordinates(self):  # Проверка введенных координат с подсветкой ошибок
        positions = []
        all_valid = True

        # Проверяем все поля ввода
        for i, input_field in enumerate(self.coordinate_inputs):
            text = input_field.text().strip()

            if not text:
                input_field.setStyleSheet("")
                all_valid = False
                continue

            try:
                parts = text.split()
                if len(parts) != 2:
                    raise ValueError("Неверные координаты")

                x, y = int(parts[0]), int(parts[1])

                if not (0 <= x < self.board_size and 0 <= y < self.board_size):
                    raise ValueError(f"Координаты должны быть от 0 до {self.board_size - 1}")

                positions.append(Position(x, y))
                # Правильный ввод - зеленая подсветка
                input_field.setStyleSheet("background-color: lightgreen;")

            except ValueError:
                # Неправильный ввод - красная подсветка
                input_field.setStyleSheet("background-color: lightcoral;")
                all_valid = False

        # Допольнительная проверка для заполнения полей
        if all_valid and len(positions) == self.num_pieces:
            # Проверка уникальность позиций
            if len(set(positions)) != len(positions):
                # Если есть дублирующиеся позиции, подсвечиваем все поля красным
                for input_field in self.coordinate_inputs:
                    if input_field.text().strip():
                        input_field.setStyleSheet("background-color: lightcoral;")
                all_valid = False
            else:
                # Проверяем, что фигуры не атакуют друг друга
                board = ChessBoard(self.board_size)
                for pos in positions:
                    if not board.add_piece(pos):
                        # Если фигуры атакуют друг друга, подсвечиваем все поля красным
                        for input_field in self.coordinate_inputs:
                            if input_field.text().strip():
                                input_field.setStyleSheet("background-color: lightcoral;")
                        all_valid = False
                        break

        if all_valid and len(positions) == self.num_pieces:
            self.positions = positions
        else:
            self.positions = []

        self.update_ok_button_state()  # обновление кнопки OK

    def update_ok_button_state(self):  # обновление кнопки OK
        all_filled = all(input_field.text().strip() for input_field in self.coordinate_inputs)
        valid_positions = len(self.positions) == self.num_pieces
        self.ok_button.setEnabled(all_filled and valid_positions)

    def accept_coordinates(self):  # Принимает координаты при OK
        if self.positions:
            self.accept()

    def get_positions(self):  # Возвращает позиции
        return self.positions


class BoardDisplayWindow(QDialog):  # Отображение шахматной доски

    def __init__(self, parent, board_size, user_positions, solution_positions, all_solutions):
        super().__init__(parent)
        self.board_size = board_size
        self.user_positions = user_positions
        self.solution_positions = solution_positions
        self.all_solutions = all_solutions
        self.setWindowTitle("Шахматная доска")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):  # Интерфейс окна шахматной доски
        layout = QVBoxLayout()

        # Создаем сетку для доски
        board_widget = QWidget()
        board_layout = QGridLayout()
        board_layout.setSpacing(1)

        # Создаем клетки доски
        for y in range(self.board_size):
            for x in range(self.board_size):
                cell = QFrame()
                cell.setFixedSize(40, 40)
                cell.setFrameStyle(QFrame.Box)
                pos = Position(x, y)

                # Цвета клеток
                if pos in self.user_positions:
                    cell.setStyleSheet("background-color: green;")  # Уже стоящие фигуры
                elif pos in self.solution_positions:
                    cell.setStyleSheet("background-color: red;")  # Найденные фигуры
                elif self.is_attacked_position(pos):
                    cell.setStyleSheet("background-color: blue;")  # Атакованные позиции
                else:
                    cell.setStyleSheet("background-color: white;")  # Пустые клетки

                board_layout.addWidget(cell, y, x)

        board_widget.setLayout(board_layout)
        layout.addWidget(board_widget)

        # Кнопочки
        button_layout = QHBoxLayout()

        save_button = QPushButton("Записать в файл")
        close_button = QPushButton("Выход")

        save_button.clicked.connect(self.save_to_file)
        close_button.clicked.connect(self.accept)

        button_layout.addWidget(save_button)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def is_attacked_position(self, position):  # Проверка, атакована ли клетка
        all_pieces = self.user_positions + self.solution_positions

        for piece_pos in all_pieces:
            piece = CamelPiece(piece_pos)
            if piece.can_attack(position, self.board_size):
                return True

        return False

    def save_to_file(self):  # Сохранение решений в файл
        try:
            with open("output.txt", "w", encoding="utf-8") as f:
                if self.all_solutions:
                    for solution in self.all_solutions:
                        line = " ".join(f"({pos.x},{pos.y})" for pos in solution)
                        f.write(line + "\n")
                else:
                    f.write("no solutions\n")

            QMessageBox.information(self, "Успех", "Данные записаны в файл output.txt")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка записи в файл: {str(e)}")


class MainWindow(QMainWindow):  # Главное окно

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Размещение верблюдов на шахматной доске")
        self.setFixedSize(400, 200)
        self.user_positions = []  # Существующие решения
        self.solutions = []  # Найденные решения
        self.setup_ui()
        self.update_button_states()

    def setup_ui(self):  # Настройка главного окна
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Поля ввода
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText("Размер доски (N)")
        self.size_input.textChanged.connect(self.update_button_states)

        self.additional_input = QLineEdit()
        self.additional_input.setPlaceholderText("Кол-во требуемых фигур (L)")
        self.additional_input.textChanged.connect(self.update_button_states)

        self.existing_input = QLineEdit()
        self.existing_input.setPlaceholderText("Кол-во размещённых фигур (K)")
        self.existing_input.textChanged.connect(self.update_button_states)

        layout.addWidget(QLabel("Размер доски (N)"))
        layout.addWidget(self.size_input)
        layout.addWidget(QLabel("Кол-во требуемых фигур (L)"))
        layout.addWidget(self.additional_input)
        layout.addWidget(QLabel("Кол-во размещённых фигур (K)"))
        layout.addWidget(self.existing_input)

        # Кнопочки
        button_layout = QHBoxLayout()
        self.coord_button = QPushButton("Создать доску")
        self.draw_button = QPushButton("Нарисовать доску")
        self.exit_button = QPushButton("Выход")
        self.coord_button.clicked.connect(self.open_coordinate_input)
        self.draw_button.clicked.connect(self.solve_and_display)
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.coord_button)
        button_layout.addWidget(self.draw_button)
        button_layout.addWidget(self.exit_button)
        layout.addLayout(button_layout)
        central_widget.setLayout(layout)

    def update_button_states(self):  # Обновляет кнопки
        try:
            size_text = self.size_input.text().strip()
            additional_text = self.additional_input.text().strip()
            existing_text = self.existing_input.text().strip()

            # Проверка, что все поля заполнены
            all_filled = size_text and additional_text and existing_text
            if all_filled:
                size = int(size_text)
                additional = int(additional_text)
                existing = int(existing_text)

                # Проверка допустимости значений
                valid_values = (1 <= size <= 20 and additional >= 0 and existing >= 0)
                if valid_values:
                    self.coord_button.setEnabled(True)

                    # Условия активации кнопки отрисовки
                    if existing == 0:
                        self.draw_button.setEnabled(True)
                    else:
                        self.draw_button.setEnabled(len(self.user_positions) == existing)
                else:
                    self.coord_button.setEnabled(False)
                    self.draw_button.setEnabled(False)
            else:
                self.coord_button.setEnabled(False)
                self.draw_button.setEnabled(False)

        except ValueError:
            self.coord_button.setEnabled(False)
            self.draw_button.setEnabled(False)

    def open_coordinate_input(self):  # Открывает окно ввода координат
        try:
            existing = int(self.existing_input.text().strip())
            size = int(self.size_input.text().strip())

            if existing == 0:
                self.user_positions = []
                self.update_button_states()
                return

            dialog = CoordinateInputDialog(self, existing, size)
            if dialog.exec() == QDialog.Accepted:
                self.user_positions = dialog.get_positions()
                self.update_button_states()

        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Неверные входные данные")

    def solve_and_display(self):  # Решение задачи и отображение результата
        try:
            size = int(self.size_input.text().strip())
            additional = int(self.additional_input.text().strip())
            existing = int(self.existing_input.text().strip())

            # Проверка соответствия количества введенных координат
            if len(self.user_positions) != existing:
                QMessageBox.critical(self, "Ошибка",
                                     f"Введено {len(self.user_positions)} координат, а должно быть {existing}")
                return

            # Поток решения задачи
            self.solver_thread = SolverWorker(size, self.user_positions, additional)
            self.solver_thread.solution_found.connect(self.on_solution_found)
            self.solver_thread.start()
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Неверные входные данные")

    def on_solution_found(self, solutions):  # Обработка решения
        self.solutions = solutions

        if not solutions:
            QMessageBox.information(self, "Результат", "Решение не найдено")
            return

        # Первое решение для отображения
        first_solution = solutions[0]
        additional_positions = [pos for pos in first_solution if pos not in self.user_positions]

        # Окно отображения шахматной доски
        try:
            size = int(self.size_input.text().strip())
            board_window = BoardDisplayWindow(
                self,
                size,
                self.user_positions,
                additional_positions,
                solutions
            )
            board_window.exec()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка отображения доски: {str(e)}")


def main():  # Запуск приложения
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()