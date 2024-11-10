class TicTacToe:
    GAME_OVER_REASON_NONE = 0
    GAME_OVER_REASON_OUT_OF_BOUNCE = 1
    GAME_OVER_REASON_PLAYER_QUIT = 2
    GAME_OVER_REASON_PLAYER_WINS = 3
    BUTTON_QUIT = 'q'
    MAX_ROUNDS = 9

    def __init__(self):
        self.playground = {'a1': 0, 'a2': 0, 'a3': 0, 'b1': 0, 'b2': 0, 'b3': 0, 'c1': 0, 'c2': 0, 'c3': 0, }
        self.active_player_id = 1
        self.round = 1
        self.was_last_move_accepted = True
        self.game_over = False
        self.game_over_reason = self.GAME_OVER_REASON_NONE
        self.coord_input = ''

    def run(self) -> None:
        print('Welcome to Tic Tac Toe')
        while not self.game_over:
            self.__play()
        print('Game Over!')
        self.__print_game_over_reason(self.game_over_reason, self.active_player_id, self.playground)

    def handle_max_rounds_reached(self) -> None:
        if self.round > self.MAX_ROUNDS:
            self.__set_game_over_reason(self.GAME_OVER_REASON_OUT_OF_BOUNCE)
            self.__activate_game_over()

    def handle_player_wins_or_not(self) -> None:
        if not self.__is_player_winner(self.active_player_id, self.playground):
            self.active_player_id = self.__get_next_player(self.active_player_id)
            self.round = self.__get_next_round(self.round)
            self.handle_max_rounds_reached()

        else:
            self.__set_game_over_reason(self.GAME_OVER_REASON_PLAYER_WINS)
            self.__activate_game_over()
            self.__print_winner(self.active_player_id, self.round, self.playground)

    def handle_abort_by_input_or_continue(self, coord: str) -> None:
        if not self.__is_allowed_input(coord, self.playground) or not self.__is_move_possible(coord, self.playground):
            self.__set_last_move_accepted(False)

        else:
            self.__set_last_move_accepted(True)
            self.__save_move(coord, self.active_player_id, self.playground)
            self.handle_player_wins_or_not()

    def handle_quit_or_not(self, coord: str) -> None:
        if not self.__is_quit_by_input(coord):
            self.handle_abort_by_input_or_continue(coord)

        else:
            self.__set_game_over_reason(self.GAME_OVER_REASON_PLAYER_QUIT)
            self.__activate_game_over()

    def __play(self) -> None:
        self.__print_game_info(self.round, self.active_player_id)
        self.__print_last_move_not_accepted(self.was_last_move_accepted)
        self.__print_playground(self.playground)
        self.__get_input_from_interface()
        self.handle_quit_or_not()

    def __print_playground(self, pg: dict) -> None:
        print('  1|2|3')
        print(f'a {self.__get_pg_marker(pg['a1'])}|{self.__get_pg_marker(pg['a2'])}|{self.__get_pg_marker(pg['a3'])}')
        print(f'b {self.__get_pg_marker(pg['b1'])}|{self.__get_pg_marker(pg['b2'])}|{self.__get_pg_marker(pg['b3'])}')
        print(f'c {self.__get_pg_marker(pg['c1'])}|{self.__get_pg_marker(pg['c2'])}|{self.__get_pg_marker(pg['c3'])}')

    def __print_winner(self, player_id: int, round_num: int, pg: dict) -> None:
        print(f'And The Winner, after {str(round_num)} is:')
        print(f'Player {str(player_id)}')
        print('\n')
        self.__print_playground(pg)

    def __print_round_limit_reached(self, pg: dict) -> None:
        print('Round Limit reached!')
        self.__print_playground(pg)

    def __print_game_over_reason(self, reason_id: int, player_id: int, pg: dict) -> None:
        if reason_id == self.GAME_OVER_REASON_OUT_OF_BOUNCE:
            self.__print_round_limit_reached(pg)
            return
        if reason_id == self.GAME_OVER_REASON_PLAYER_QUIT:
            self.__print_game_quit_by_player(player_id)
            return
        if reason_id == self.GAME_OVER_REASON_PLAYER_WINS:
            self.__print_winner(player_id, self.round, pg)

    def __get_input_from_interface(self) -> str:
        return input(f'Insert Coordinates for your Move (i.e. "a1") or "{self.BUTTON_QUIT}" to give up: ')

    def __set_coord_input(self, value: str):
        self.coord_input = value

    def __is_allowed_input(self, coord: str, pg: dict) -> bool:
        return self.__is_quit_by_input(coord) or coord in pg

    def __is_player_winner(self, player_id: int, pg: dict) -> bool:
        if self.__is_winner_by_coords('a1', 'a2', 'a3', player_id, pg):
            return True

        if self.__is_winner_by_coords('b1', 'b2', 'b3', player_id, pg):
            return True

        if self.__is_winner_by_coords('c1', 'c2', 'c3', player_id, pg):
            return True

        if self.__is_winner_by_coords('a1', 'b1', 'c1', player_id, pg):
            return True

        if self.__is_winner_by_coords('a2', 'b2', 'c2', player_id, pg):
            return True

        if self.__is_winner_by_coords('a3', 'b3', 'c3', player_id, pg):
            return True

        if self.__is_winner_by_coords('a1', 'b2', 'c3', player_id, pg):
            return True

        if self.__is_winner_by_coords('a3', 'b2', 'c1', player_id, pg):
            return True

        return False

    def __is_quit_by_input(self, coord: str) -> bool:
        return coord.lower() == self.BUTTON_QUIT

    def __activate_game_over(self):
        self.game_over = True

    def __set_game_over_reason(self, reason_id: int) -> None:
        self.game_over_reason = reason_id

    def __set_last_move_accepted(self, value: bool) -> None:
        self.was_last_move_accepted = value

    @staticmethod
    def __get_pg_marker(pg_value: int) -> str:
        if pg_value == 1:
            return 'X'
        if pg_value == 2:
            return 'O'
        return '-'

    @staticmethod
    def __get_next_player(player_id: int) -> int:
        if player_id == 1:
            return 2
        return 1

    @staticmethod
    def __get_next_round(round_num: int) -> int:
        return round_num + 1

    @staticmethod
    def __is_move_possible(coord: str, pg: dict) -> bool:
        return pg[coord] == 0

    @staticmethod
    def __print_game_info(round_num: int, player_id: int) -> None:
        print(f'Round {str(round_num)}: Player {str(player_id)}')

    @staticmethod
    def __print_last_move_not_accepted(accepted: bool) -> None:
        if not accepted:
            print('Your last move was not accepted. Please try again')

    @staticmethod
    def __print_game_quit_by_player(player_id: int) -> None:
        print(f'Game has been Quit by Player {player_id}')

    @staticmethod
    def __save_move(coord, player_id: int, pg: dict) -> None:
        pg[coord] = player_id

    @staticmethod
    def __is_winner_by_coords(coord1: str, coord2: str, coord3: str, player_id: int, pg: dict) -> bool:
        return pg[coord1] == player_id and pg[coord2] == player_id and pg[coord3] == player_id


if __name__ == "__main__":
    game = TicTacToe()
    game.run()
