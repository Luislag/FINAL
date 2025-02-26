import random

# --------------------- BOND CALCULATIONS ---------------------

# Bond Price (Present Value) Calculator
def bond_calculator():
    try:
        face_value = float(input("Enter the face value of the bond ($): "))
        coupon_rate = float(input("Enter the coupon rate (as %): ")) / 100
        market_rate = float(input("Enter the market interest rate (as %): ")) / 100
        years_to_maturity = int(input("Enter the number of years until maturity: "))

        coupon_payment = face_value * coupon_rate
        coupon_pv = sum(coupon_payment / (1 + market_rate) ** t for t in range(1, years_to_maturity + 1))
        face_value_pv = face_value / (1 + market_rate) ** years_to_maturity

        bond_price = coupon_pv + face_value_pv
        print(f"\nThe present value (price) of the bond is: ${bond_price:.2f}")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

# Perpetuity Price Calculator
def perpetuity_price(payment, discount_rate_percent):
    """
    Calculate the price of a perpetuity:
         Price = Payment / (discount_rate_percent / 100)
    """
    if discount_rate_percent <= 0:
        raise ValueError("Discount rate must be greater than zero.")
    return payment / (discount_rate_percent / 100)

# Bond Maturity (Future Value) Calculator
def bond_maturity():
    """
    Calculate the maturity (future) value of a bond with reinvested coupon payments.

    Formula:
        FV_coupons = coupon_payment * [((1 + r)^n - 1) / r]   if r != 0
        Total Maturity Value = FV_coupons + face_value
    """
    try:
        face_value = float(input("Enter the face value of the bond ($): "))
        coupon_rate = float(input("Enter the coupon rate (as %): "))
        years_to_maturity = int(input("Enter the number of years until maturity: "))
        reinvestment_rate = float(input("Enter the reinvestment rate (as %): "))

        coupon_payment = face_value * (coupon_rate / 100)

        if reinvestment_rate != 0:
            fv_coupons = coupon_payment * (((1 + reinvestment_rate / 100) ** years_to_maturity - 1) / (reinvestment_rate / 100))
        else:
            fv_coupons = coupon_payment * years_to_maturity

        total_value = fv_coupons + face_value
        print(f"\nThe total maturity value of the bond is: ${total_value:.2f}")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

# Current Yield Calculator
def current_yield():
    try:
        face_value = float(input("Enter the face value of the bond ($): "))
        coupon_rate = float(input("Enter the coupon rate (as %): "))
        current_price = float(input("Enter the current market price of the bond ($): "))
        coupon_payment = face_value * (coupon_rate / 100)
        cy = (coupon_payment / current_price) * 100
        print(f"\nThe current yield of the bond is: {cy:.2f}%")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

# Yield to Maturity (YTM) Calculator using bisection method
def yield_to_maturity():
    try:
        bond_price = float(input("Enter the current bond price ($): "))
        face_value = float(input("Enter the face value of the bond ($): "))
        coupon_rate = float(input("Enter the coupon rate (as %): "))
        years_to_maturity = int(input("Enter the number of years until maturity: "))
        coupon_payment = face_value * (coupon_rate / 100)

        # Define the function f(y) = Present Value at yield y - bond_price
        def f(y):
            total = sum(coupon_payment / ((1 + y) ** t) for t in range(1, years_to_maturity + 1))
            total += face_value / ((1 + y) ** years_to_maturity)
            return total - bond_price

        # Bisection method settings
        low = 0.0001
        high = 1.0
        tolerance = 1e-6
        iteration = 0

        if f(low) * f(high) > 0:
            print("YTM not found in the range. Please check your inputs.")
            return

        while high - low > tolerance and iteration < 10000:
            mid = (low + high) / 2
            if f(mid) == 0:
                break
            elif f(mid) * f(low) < 0:
                high = mid
            else:
                low = mid
            iteration += 1

        ytm = (low + high) / 2
        print(f"\nThe approximate Yield to Maturity is: {ytm * 100:.2f}%")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

# Duration Calculation (Macaulay and Modified Duration)
def duration_calculation():
    try:
        face_value = float(input("Enter the face value of the bond ($): "))
        coupon_rate = float(input("Enter the coupon rate (as %): "))
        years_to_maturity = int(input("Enter the number of years until maturity: "))
        yield_rate_percent = float(input("Enter the yield/market interest rate (as %): "))
        y = yield_rate_percent / 100
        coupon_payment = face_value * (coupon_rate / 100)

        # Calculate bond price using cash flows:
        price = sum(coupon_payment / ((1 + y) ** t) for t in range(1, years_to_maturity)) \
                + (coupon_payment + face_value) / ((1 + y) ** years_to_maturity)

        weighted_sum = sum(t * (coupon_payment / ((1 + y) ** t)) for t in range(1, years_to_maturity)) \
                       + years_to_maturity * ((coupon_payment + face_value) / ((1 + y) ** years_to_maturity))

        macaulay_duration = weighted_sum / price
        modified_duration = macaulay_duration / (1 + y)
        print(f"\nThe Macaulay Duration is: {macaulay_duration:.2f} years")
        print(f"The Modified Duration is: {modified_duration:.2f} years")
    except ValueError:
        print("Invalid input! Please enter numeric values.")

# --------------------- CORPORATE FINANCE & ACCOUNTING ---------------------

# Internal Rate of Return (IRR) Calculator
def irr_calculation():
    try:
        cash_flow_str = input("Enter cash flows separated by commas (e.g., -1000, 300, 400, 500): ")
        cashflows = [float(cf.strip()) for cf in cash_flow_str.split(",")]
        # Define NPV function for a given rate r
        def npv(r):
            return sum(cashflows[t] / ((1 + r) ** t) for t in range(len(cashflows)))
        # Set search bounds for IRR
        low = -0.99
        high = 1.0
        tolerance = 1e-6
        iteration = 0

        if npv(low) * npv(high) > 0:
            print("IRR not found in the range -99% to 100%. Please check your cash flows.")
            return

        while high - low > tolerance and iteration < 10000:
            mid = (low + high) / 2
            if npv(mid) == 0:
                break
            elif npv(mid) * npv(low) < 0:
                high = mid
            else:
                low = mid
            iteration += 1

        irr = (low + high) / 2
        print(f"\nThe IRR is approximately: {irr * 100:.2f}%")
    except Exception as e:
        print("Error:", e)

# Payback Period Calculator
def payback_period():
    try:
        cash_flow_str = input("Enter cash flows separated by commas (start with the initial investment as a negative number, e.g., -1000, 300, 400, 500): ")
        cashflows = [float(cf.strip()) for cf in cash_flow_str.split(",")]
        cumulative = 0
        for i, cf in enumerate(cashflows):
            previous_cum = cumulative
            cumulative += cf
            if cumulative >= 0:
                # Fraction of period required
                if cf != 0:
                    fraction = abs(previous_cum) / cf
                else:
                    fraction = 0
                payback = i + fraction  # i is zero-indexed (period 0 is initial investment)
                print(f"\nThe payback period is approximately: {payback:.2f} periods")
                return
        print("\nThe investment is not recovered within the given periods.")
    except Exception as e:
        print("Error:", e)

# Recovery Value Calculator
def recovery_value():
    try:
        salvage_value = float(input("Enter the estimated salvage value ($): "))
        selling_cost = float(input("Enter the selling cost percentage (as %): "))
        tax_rate = float(input("Enter the tax rate on capital gains (as %): "))
        net_value = salvage_value * (1 - selling_cost / 100) * (1 - tax_rate / 100)
        print(f"\nThe net recovery value is: ${net_value:.2f}")
    except Exception as e:
        print("Error:", e)

# --------------------- GAMES ---------------------

def Footy_tictactoe():
    print("Welcome to the Tic Tac Toe game"
          """
             This function will play a game of Tic-Tac-Toe based on football. The idea of the game is the same as a normal
             Tic-Tac-Toe, but with a catch, for each cell, there are conditions that have to be satisfied with a football player.
             For further simplicity of the game, four categories have been added that can be used in the grid, they are the
             following: Country, Club, League, Ballon D'or Winner and Champions League winner. There are four sets to play the game,
             increasing in difficulty. From set one to four, the logic and programming behind the game is the same as used in
             the preliminary versions, just adding the use of dictionaries to assign players to their respective cells, through
             using the numbers. The maximum pool of players for each condition is 6, the most famous players will be included or
             the most influential for that specific category, the input might not be always wrong, just not included within the conditions,
             try and think about the basic answers, the most influential ones (e.g. for Liverpool and Spain Xabi Alonso, not Iago Aspas).
             Finally, it is important to note that special characters are not supported in player names, therefore the name must be
             introduced in the following way: "Firstname Lastname" or just "Lastname" making García an invalid name, Garcia would be valid.
             :return: The Footy Tic-Tac-Toe game. (Football inspired version of a Tic-Tac-Toe game)
             """)
    # DIFFERENT CONFIGURATIONS FOR THE TIC TAC TOE GAME

    def config_game1():
        """
        First configuration for the game, only including the conditions for countries and clubs. Maximum of 6 players
        are valid for each category, the most famous ones will be included, categories are ideated for having no more than
        5 options generally. It is important to note that the player will be included for the team he was most influential
        for in case of being available for multiple options, Nazario and Figo are considered Real Madrid players, not
        Barcelona players for this game and configurations.
        :return: The game board configuration with the following labels and the players that can be assigned to each cell.
        """
        # Configuration for Game 1
        row_labels = ["REAL MADRID", "BARÇA", "ATLETI"]
        col_labels = ["PORTUGAL", "HOLLAND", "BRAZIL"]
        player_to_cell = {
            "Cristiano Ronaldo": 1, "Cristiano": 1, "Luis Figo": 1, "Figo": 1, "Pepe": 1, "Ricardo Carvalho": 1,
            "Carvalho": 1, "Fabio Coentrao": 1, "Coentrao": 1,
            "Clarence Seedorf": 2, "Seedorf": 2, "Ruud van Nistelrooy": 2, "Van Nistelrooy": 2, "Arjen Robben": 2,
            "Robben": 2, "Wesley Sneijder": 2, "Sneijder": 2, "Rafael van der Vaart": 2, "Van der Vaart": 2,
            "Klaas-Jan Huntelaar": 2, "Huntelaar": 2,
            "Roberto Carlos": 3, "Ronaldo Nazario": 3, "Ronaldo": 3, "Kaka": 3, "Marcelo Vieira": 3, "Marcelo": 3,
            "Casemiro": 3, "Vinicius Junior": 3, "Vinicius": 3,
            "Deco": 4, "Baia": 4, "Simao Sabrosa": 4, "Andre Gomes": 4, "Nelson Semedo": 4, "Semedo": 4,
            "Johan Cruyff": 5, "Cruyff": 5, "Ronald Koeman": 5, "Koeman": 5, "Patrick Kluivert": 5, "Kluivert": 5,
            "Marc Overmars": 5, "Overmars": 5, "Frenkie de Jong": 5, "De Jong": 5, "Edgar Davids": 5, "Davids": 5,
            "Romario": 6, "Rivaldo": 6, "Ronaldinho Gaucho": 6, "Ronaldinho": 6, "Dani Alves": 6, "Alves": 6,
            "Raphinha": 6, "Vitor Roque": 6,
            "Jorge Alberto Mendonça": 7, "Mendonça": 7, "Paulo Futre": 7, "Futre": 7, "Hugo Leal": 7, "Leal": 7,
            "Pizzi": 7, "Diogo Jota": 7, "Jota": 7, "Gelson Martins": 7, "Martins": 7,
            "Jimmy Hasselbaink": 8, "Hasselbaink": 8, "John Heitinga": 8, "Heitinga": 8, "Kizito Musampa": 8,
            "Musampa": 8, "Memphis Depay": 8, "Depay": 8, "Merel van Dongen": 8, "Van Dongen": 8,
            "Sari van Veenedaal": 8, "Van Veenedaal": 8,
            "Diego Costa": 9, "Filipe Luis": 9, "João Miranda": 9, "Miranda": 9, "Matheus Cunha": 9, "Cunha": 9
        }
        return row_labels, col_labels, player_to_cell

    def config_game2():
        """
        Second configuration of the game now introducing the new conditions Ballon D'or Winner and Champions League winner,
        players that have done both are only counted for one category, in this case Zinedine Zidane is considered for Ballon D'or Winner
        as he has more than Benzema, as he is now considered as UCL winner for this game, the player will not lose the turn when introducing
        an invalid input.
        :return: The game board configuration and game configuration according to the conditions below.
        """
        # Configuration for Game 2
        row_labels = ["UCL WINNER", "DORTMUND", "BALLON D'OR"]
        col_labels = ["CZECHIA", "FRANCE", "ENGLAND"]
        player_to_cell = {
            "Milan Baros": 1, "Baros": 1, "Vladimir Smicer": 1, "Smicer": 1, "Marek Jankulovski": 1, "Jankulovski": 1,
            "Petr Cech": 1, "Cech": 1,
            "Karim Benzema": 2, "Benzema": 2, "Didier Deschamps": 2, "Deschamps": 2, "Bixente Lizarazu": 2,
            "Lizarazu": 2, "Christophe Dugarry": 2, "Dugarry": 2, "Kingsley Coman": 2, "Coman": 2,
            "Steven Gerrard": 3, "Gerrard": 3, "Frank Lampard": 3, "Lampard": 3, "Wayne Rooney": 3, "Rooney": 3,
            "Rio Ferdinand": 3, "Ferdinand": 3, "David Beckham": 3, "Beckham": 3, "Paul Scholes": 3, "Scholes": 3,
            "Jan Koller": 4, "Koller": 4, "Tomas Rosicky": 4, "Rosicky": 4, "Patrik Berger": 4, "Berger": 4,
            "Ousmane Dembele": 5, "Dembele": 5, "Axel Zagadou": 5, "Zagadou": 5, "Anthony Modeste": 5, "Modeste": 5,
            "Damien Le Tallec": 5, "Le Tallec": 5, "Soumaila Coulibaly": 5, "Coulibaly": 5,
            "Jadon Sancho": 6, "Sancho": 6, "Jude Bellingham": 6, "Bellingham": 6, "Jamie Bynoe Gittens": 6,
            "Bynoe Gittens": 6, "Carney Chukwuemeka": 6, "Chukwuemeka": 6,
            "Josef Masopust": 7, "Masopust": 7, "Pavel Nedved": 7, "Nedved": 7,
            "Raymond Kopa": 8, "Kopa": 8, "Michel Platini": 8, "Platini": 8, "Jean Pierre Papin": 8, "Papin": 8,
            "Zinedine Zidane": 8, "Zidane": 8,
            "Stanley Matthews": 9, "Matthews": 9, "Bobby Charlton": 9, "Charlton": 9, "Kevin Keegan": 9, "Keegan": 9,
            "Michael Owen": 9, "Owen": 9
        }
        return row_labels, col_labels, player_to_cell

    def config_game3():
        """
        Third configuration of the game, first mixing all the conditions freely, players that have done both are only counted for one category,
        In the case of Cristiano Ronaldo he is counted for the Ballon D'or only, not for Manchester UDT and Portugal.
        :return: The third variety of the game board with its respective inputs.
        """
        # Configuration for Game 3
        row_labels = ["MANCHESTER UDT", "LIVERPOOL", "BALLON D'OR"]
        col_labels = ["PORTUGAL", "MAN CITY", "BARÇA"]
        player_to_cell = {
            "Nani": 1, "Luis Nani": 1, "Bebe": 1, "Tiago Bebe": 1, "Joel Pereira": 1, "Pereira": 1, "Diogo Dalot": 1,
            "Dalot": 1, "Bruno Fernandes": 1, "Fernandes": 1,
            "Denis Law": 2, "Law": 2, "Brian Kidd": 2, "Kidd": 2, "Peter Schmeichel": 2, "Schmeichel": 2,
            "Andy Cole": 2, "Cole": 2, "Carlos Tevez": 2, "Tevez": 2, "Owen Hargreaves": 2, "Hargreaves": 2,
            "Mark Hughes": 3, "Hughes": 3, "Jordi Cruyff": 3, "Laurent Blanc": 3, "Blanc": 3, "Henrik Larsson": 3,
            "Larsson": 3, "Victor Valdes": 3, "Valdes": 3, "Zlatan Ibrahimovic": 3, "Ibrahimovic": 3, "Gerard Pique": 3,
            "Pique": 3,
            "Diogo Jota": 4, "Jota": 4, "Fabio Carvalho": 4, "Carvalho": 4, "Raul Meireles": 4, "Meireles": 4,
            "Joao Carlos Teixeira": 4, "Teixeira": 4, "Tiago Ilori": 4, "Ilori": 4, "Rafael Camacho": 4, "Camacho": 4,
            "James Milner": 5, "Milner": 5, "Raheem Sterling": 5, "Sterling": 5, "Robbie Fowler": 5, "Fowler": 5,
            "Steve McManaman": 5, "McManaman": 5, "Dietmar Hamann": 5, "Hamann": 5, "Craig Bellamy": 5, "Bellamy": 5,
            "Luis Suarez": 6, "Suarez": 6, "Javier Mascherano": 6, "Mascherano": 6, "Philippe Coutinho": 6,
            "Coutinho": 6, "Pepe Reina": 6, "Reina": 6, "Luis Garcia": 6, "Garcia": 6, "Boudewijn Zenden": 6,
            "Zenden": 6,
            "Eusebio": 7, "Eusebio da Silva Ferreira": 7, "Luis Figo": 7, "Figo": 7, "Cristiano Ronaldo": 7,
            "Cristiano": 7,
            "Rodrigo Hernandez": 8, "Rodri": 8,
            "Johan Cruyff": 9, "Cruyff": 9, "Hristo Stoichkov": 9, "Stoichkov": 9, "Rivaldo": 9, "Ronaldinho Gaucho": 9,
            "Ronaldinho": 9, "Lionel Messi": 9, "Messi": 9
        }
        return row_labels, col_labels, player_to_cell

    def config_game4():
        """
        Fourth configuration for the game, the difficulty lies on the scarcity of possible answers for each condition
        but either way the players available for those slots are well and widely known, for the Spanish row, I have decided
        to go for a mix between influence and the best players and most influential for those teams overall
        :return: The fourth variety of the game board with its respective inputs.
        """
        # Configuration for Game 4
        row_labels = ["UKRAINE", "SPAIN", "RUSSIA"]
        col_labels = ["BALLON D'OR", "REAL MADRID", "ARSENAL"]
        player_to_cell = {
            "Andriy Shevchenko": 1, "Shevchenko": 1,
            "Andriy Lunin": 2, "Lunin": 2, "Oleh Luzhnyi": 2, "Luzhnyi": 2,
            "Oleksandr Zinchenko": 3,
            "Luis Suarez": 4, "Suarez": 4, "Rodrigo Hernandez": 4, "Rodri": 4,
            "Sergio Ramos": 5, "Ramos": 5, "Iker Casillas": 5, "Casillas": 5, "Dani Carvajal": 5, "Carvajal": 5,
            "Xabi Alonso": 5, "Alonso": 5, "Lucas Vazquez": 5, "Vazquez": 5, "Asier Illarramendi": 5, "Illarramendi": 5,
            "Nacho": 5, "Marco Asensio": 5, "Asensio": 5,
            "Cesc Fabregas": 6, "Santi Cazorla": 6, "Cazorla": 6, "Mikel Arteta": 6, "Arteta": 6, "Mikel Merino": 6,
            "Merino": 6, "Hector Bellerin": 6, "Bellerin": 6, "Cesar Azpilicueta": 6, "Azpilicueta": 6,
            "Nacho Monreal": 6, "Monreal": 6,
            "Lev Yashin": 7, "Yashin": 7,
            "Denis Cheryshev": 8, "Cheryshev": 8,
            "Andrei Arshavin": 9, "Arshavin": 9,
        }
        return row_labels, col_labels, player_to_cell

    def play_game(Team_1, Team_2, row_labels, col_labels, player_to_cell):
        """
        Allows for the game to actually be played. It sets up the game board and the values inside each cell, that
        will later be changed with another function.
        :param Team_1: Home team, the team that will be assigned the symbol "X" on the board.
        :param Team_2: Away team, the team that will be assigned the symbol "O" on the board.
        :param row_labels: According to the different configurations of the game, the labels with the row conditions for the game
        :param col_labels: According to the different configurations of the game, the labels with the column conditions for the game
        :param player_to_cell: The dictionary that allows for that specific configuration to be used and have the players assigned
        to a certain cell on the board, allowing for the game to be played
        :return: The logic of the game board and the possible inputs for each category and respective cell.
        """
        # Basic game setup
        gameBoard = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        rows = 3
        columns = 3
        available_positions = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        home_team = "X"
        away_team = "O"
        endloop = False
        Count_Turns = 0

        # PRINT THE GAME BOARD
        def printboard():
            """
            Function that prints the game board, allowing for the visual representation of every step of the game, it
            prints the board after every turn with its updated version. The labels are also printed for every cell and category
            :return: Prints the game board with its respective labels and cells at any given moment during the game, the current
            state of the game board at that moment during the game .
            """
            print(" " * 20, end="")
            for header in col_labels:
                print(f"{header:^15}", end=" ")
            print("\n" + "-" * 70)
            for i in range(rows):
                print(f"{row_labels[i]:<15}", end="|")
                for j in range(columns):
                    print(f"{str(gameBoard[i][j]):^15}", end="|")
                print("\n" + "-" * 70)

        # CREATE A FUNCTION THAT MODIFIES THE CURRENT STATE OF THE GAME BOARD
        def modgameboard(num, symbol):
            """
            Allows for the game board to be modified after each input, adjusting for the 0 based indexing that python uses
            for lists and arrays. It will substitute the cell with its current value with the symbol that made the move and
            introduced a valid input for one of the categories.
            :param num: Number in the array (from 1 to 9) that will be modified according to the player to cell dictionary.
            :param symbol: 'X' or 'O' depending on the team that made the move and introduced a valid input for one of the category.
            :return: The updated game board with the modified cell after each move, but it does not print the current state of the board
            after it has been modified by this function.
            """
            nonlocal gameBoard  # Imports the Game board into this specific function
            num -= 1  # Adjust for 0-based indexing
            if num == 0:
                gameBoard[0][0] = symbol
            elif num == 1:
                gameBoard[0][1] = symbol
            elif num == 2:
                gameBoard[0][2] = symbol
            elif num == 3:
                gameBoard[1][0] = symbol
            elif num == 4:
                gameBoard[1][1] = symbol
            elif num == 5:
                gameBoard[1][2] = symbol
            elif num == 6:
                gameBoard[2][0] = symbol
            elif num == 7:
                gameBoard[2][1] = symbol
            elif num == 8:
                gameBoard[2][2] = symbol

        # CREATE A FUNCTION THAT PRINTS THE RESULT OF THE GAME
        def declare_winner(symbol):
            """
            This function declares the winner of the game, it severs a complementary purpose to the checkwin function.
            :param symbol: 'X' or 'O' depending on the team that won the game.
            :return: A f string with the team that has won the game of tic-tac-toe
            """
            nonlocal endloop  # Imports endloop into this specific function
            if symbol == home_team:
                print(f"Incredible! {Team_1} has scored a game winning goal!")
                print(f"{Team_1} has won the championship with an incredible performance!")
            elif symbol == away_team:
                print(f"Incredible! {Team_2} has scored a game winning goal!")
                print(f"{Team_2} has won the championship with an incredible performance!")
            endloop = True
            printboard()

        # CREATE A COMPLEMENTARY FUNCTION TO THE PREVIOUS ONE THAT RUNS THE WHOLE LOGIC OF WHO HAS WON
        def checkwin(board):
            """
            Creates the logic behind checking the winner of the game, this functions analyzes the current state of the
            game board and determines if there is a winner and who it is or if the game is a tie. It checks for that condition
            by comparing the cells to each other and seeing the symbol that they have assigned, if there are three of the same
            symbol in a straight line, it declares the winner. This is a simplified version of the function from the preliminary
            versions, as it now checks for the content of the cells and lets other function handle the result of the game, it does
            not check for every single possibility that there is for both players to determine the winner
            :param board: The current state of the tic-tac-toe game board.
            :return: The result of the game, but it does not print the team that won or if there was a tie
            """
            nonlocal endloop  # Imports endloop into the function
            # Check rows
            if board[0][0] == board[0][1] == board[0][2]:
                declare_winner(board[0][0])
            elif board[1][0] == board[1][1] == board[1][2]:
                declare_winner(board[1][0])
            elif board[2][0] == board[2][1] == board[2][2]:
                declare_winner(board[2][0])
            # Check columns
            elif board[0][0] == board[1][0] == board[2][0]:
                declare_winner(board[0][0])
            elif board[0][1] == board[1][1] == board[2][1]:
                declare_winner(board[0][1])
            elif board[0][2] == board[1][2] == board[2][2]:
                declare_winner(board[0][2])
            # Check diagonals
            elif board[0][0] == board[1][1] == board[2][2]:
                declare_winner(board[0][0])
            elif board[2][0] == board[1][1] == board[0][2]:
                declare_winner(board[2][0])

        # CREATE THE TURN LOGIC FOR THE GAME
        while endloop == False and Count_Turns < 9:
            # Logic for knowing which is the team in control of the turn
            printboard()
            if Count_Turns % 2 == 0:
                current_team = Team_1  # Sets the team that is in charge during that turn
                symbol = home_team
            else:
                current_team = Team_2
                symbol = away_team
            player_name = input(f"\n{current_team}, pick a player to try and score: ").strip()# The function strip eliminates all the useless spaces to be able to compare the names directly to the dictionary
            if player_name.lower() == "exit":
                print("Exiting game. Goodbye!")
                endloop = True
                break
            # Check if the player picked is within the options in the dictionary
            if player_name not in player_to_cell:
                print("That player is not available for the game!. Choose another option")
                continue
            # Check that the player is picking an available cell, one that has not been used by the opponent
            chosen_cell = player_to_cell[player_name]
            if chosen_cell not in available_positions:
                print(
                    f"That position {player_name} is already taken, a player has been used from there. Choose another cell.")
                continue
            # Modify the current state of the game board according to the input received, also checks if there has been a winning goal
            modgameboard(chosen_cell, symbol)
            available_positions.remove(chosen_cell)
            print(f"Incredible! {player_name} has scored an amazing goal for {current_team}!")
            checkwin(gameBoard)
            Count_Turns += 1

        if not endloop:
            print("It's a tie!")
            printboard()

    # MAIN MENU for choosing the games

    print("Choose a game configuration:")
    print("1: Game 1")
    print("2: Game 2")
    print("3: Game 3")
    print("4: Game 4")
    choice = input("Enter the number of the game you want to play: ").strip()
    if choice == "1":
        row_labels, col_labels, player_to_cell = config_game1()
    elif choice == "2":
        row_labels, col_labels, player_to_cell = config_game2()
    elif choice == "3":
        row_labels, col_labels, player_to_cell = config_game3()
    elif choice == "4":
        row_labels, col_labels, player_to_cell = config_game4()
    else:
        print("Invalid choice. Defaulting to Game 1.")
        row_labels, col_labels, player_to_cell = config_game1()
    Team_1 = input("Team 1's name is: ")
    Team_2 = input("Team 2's name is: ")
    print(f"Let the championship final between {Team_1} and {Team_2} begin!")
    play_game(Team_1, Team_2, row_labels, col_labels, player_to_cell)

def tenaball():
    barcelona_signings = ["Philippe Coutinho", "Ousmane Dembele", "Antoine Griezmann", "Neymar Jr", "Frenkie de Jong",
                          "Luis Suarez", "Zlatan Ibrahimovic", "Miralem Pjanic", "Raphinha", "Dani Olmo"]

    # most appearances with keeper David de Gea

    degea_app = ["Marcus Rashford", "Chris Smalling", "Anthony Martial", "Juan Mata", "Antonio Valencia",
                 "Ashley Young", "Luke Shaw", "Wayne Rooney", "Phil Jones", "Victor Lindelof"]

    # most combined games for Real Madrid and Juventus

    juve_real = ["Cristiano Ronaldo", "Zinedine Zidane", "Gonzalo Higuain", "Alvaro Morata", "Sami Khedira", "Danilo",
                 "Fabio Cannavaro", "Di Maria", "Emerson", "Micheal Laudrup"]

    # most spanish national team appearances

    spain_app = ["Sergio Ramos", "Iker Casillas", "Sergio Busquets", "Xavi", "Andres Iniesta", "Andoni Zubizarreta",
                 "David Silva", "Xabi Alonso", "Fernando Torres", "Cesc Fabregas"]

    # highest alltime goalscorers

    top_goals = ["Cristiano Ronaldo", "Lionel Messi", "Pele", "Romario", "Ferenc Puskas", "Josef Bican",
                 "Robert Lewandowski", "Jimmy Jones", "Gerd Muller", "Joe Bambrick"]

    # most appearances with teammate Antony

    antony_app = ["Lisandro Martinez", "Bruno Fernandes", "Dusan Tadic", "Andre Onana", "Diogo Dalot",
                  "Ryan Gravenberch", "Casemiro", "Davy Klaassen", "Daley Blind", "Edson Alvarez"]

    # most used players by coach Carlo Ancelotti at Real Madrid

    ancelotti_used = ["Luka Modric", "Dani Carvajal", "Karim Benzema", "Federico Valverde", "Toni Kroos",
                      "Vinicius Junior", "Thibaut Courtois", "Rodrygo", "Antonio Rudiger", "Nacho Fernandez"]

    # most used players by coach Luis Suarez at Fc Barcelona

    lEnrique_used = ["Lionel Messi", "Luis Suarez", "Neymar Jr", "Sergio Busquets", "Gerard Pique", "Javier Mascherano",
                     "Ivan Rakitic", "Jordi Alba", "Andres Iniesta", "Ter Stegen"]

    manu_managers = ["Ruben Amorim", "Ruud Van Nistelrooy", "Ten Hag", "Ralf Rangnick", "Michael Carrick",
                     "Ole Gunnar Solskjaer", "Jose Mourinho", "Louis Van Gaal", "Ryan Giggs", "David Moyes"]

    ronaldo_assist = ["Karim Benzema", "Mesut Ozil", "Gareth Bale", "Di Maria", "Marcelo", "Ryan Giggs",
                      "Gonzalo Higuain", "Isco", "Kaka", "Lucas Vazquez"]

    # Code to randomly choose the tenaball category and its list for the game

    random_tenaball, category = random.choice([
        (barcelona_signings, "most expensive barça signings"),
        (degea_app, "most appearances with teammate David de Gea"),
        (juve_real, "players with the most combined appearances for Juventus and Real Madrid"),
        (spain_app, "players with the most caps for the Spanish National Team"),
        (top_goals, "all time goalscorers"),
        (antony_app, "players with most appearances with teammate Antony"),
        (ancelotti_used, "most used players by coach Ancelotti at Real Madrid"),
        (lEnrique_used, "most used players by coach lEnrique at Fc Barcelona"),
        (manu_managers, "managers to have coached Manchester United after Sir Alex Ferguson"),
        (ronaldo_assist, "players that have provided the most assists to teammate Cristiano Ronaldo"),
    ])

    # so that we can track how many the player has guessed
    correct_answer = []

    # object that defines the amount of lives you
    lives = 3

    # Scoreboard object so to substitute the name of the player by the question mark
    reveal_ans = ["?" for _ in random_tenaball]

    # starting the game
    print("Welcome to our Tenaball game mode")
    play = input("Do you want to play or exit?")
    # if player types exit it will. not run
    if play == "exit":
        print("Bye!")
        return

    # anything else will start the game
    else:
        # will start a loop that will keep going as long as lives are not 0 or the amount of player guessed is less than 10
        while lives > 0 and len(correct_answer) < 10:
            print(f"\nYou have {lives} lives left")

            # will print the tenaball tower which will allows the player to later see what position of the players he guessed
            print("tenaball tower:")
            for i, name in enumerate(reveal_ans, start=1):
                print(f"{i}. {name}")
            print(f"find the top 10 {category}")

            player = input("Enter a player's full name: ")

            # check if guessed player is in the top 10
            if player in random_tenaball and player not in correct_answer:
                # will define what position in the top 10 the player is in
                position = random_tenaball.index(player) + 1
                # will print what position in the top 10 the player is in
                print(f"You guessed {player} correctly, he is number {position} on the list")
                # will then add the correct player to the list by removing the question mark by the player name
                reveal_ans[position - 1] = player
                # adds the player in the list of correct answers so that we can see how many right players
                # the user has guessed
                correct_answer.append(player)
                lives = 3

                # if player has already been guessed
            elif player in correct_answer:
                print("You already guessed that player")
                # lives == lives

                # if player is not on the list
            else:
                print(f"{player} is not on the list")
                # removes a life
                lives -= 1

        # conditionalities for the code to see if it should stop
        # stops if the length of players is the top 10 given
        if len(correct_answer) == 10:
            print("\nYou beat the Tenaball")

        # or it will also stop if lives reach zero

        else:
            print("\nThe Tenaball beat you")
            print(f"The correct players were:")
            for position, player in enumerate(random_tenaball, start=1):
                print(f"{position}. {player}")


def filter_players(players, attribute, value):
    """
    Filters the list of players based on the given attribute value.
    The comparison is case-insensitive.
    """
    return [player for player in players if player[attribute].lower() == value.lower()]

def footynator():
    print("Welcome to Footynator: Football Player Guesser!")
    players = [
        {"name": "Lionel Messi", "league": "MLS", "team": "Inter Miami", "position": "Forward", "age": "37",
         "nationality": "Argentina"},
        {"name": "Cristiano Ronaldo", "league": "Saudi Pro League", "team": "Al Nassr", "position": "Forward",
         "age": "40", "nationality": "Portugal"},
        {"name": "Neymar Jr", "league": "Brasilian Serie A", "team": "Santos Futebol", "position": "Forward",
         "age": "33", "nationality": "Brazil"},
        {"name": "Kevin De Bruyne", "league": "Premier League", "team": "Manchester City", "position": "Midfielder",
         "age": "33", "nationality": "Belgium"},
        {"name": "Luka Modrić", "league": "La Liga", "team": "Real Madrid", "position": "Midfielder", "age": "39",
         "nationality": "Croatia"},
        {"name": "Kylian Mbappe", "league": "La Liga", "team": "Real Madrid", "position": "Forward", "age": "26",
         "nationality": "France"},
        {"name": "Mohamed Salah", "league": "Premier League", "team": "Liverpool", "position": "Forward", "age": "32",
         "nationality": "Egypt"},
        {"name": "Robert Lewandowski", "league": "La Liga", "team": "Barcelona", "position": "Forward", "age": "36",
         "nationality": "Poland"},
        {"name": "Virgil van Dijk", "league": "Premier League", "team": "Liverpool", "position": "Defender",
         "age": "33", "nationality": "Netherlands"},
        {"name": "Sergio Ramos", "league": "La Liga", "team": "Sevilla", "position": "Defender", "age": "38",
         "nationality": "Spain"},
        {"name": "Sadio Mané", "league": "Bundesliga", "team": "Bayern Munich", "position": "Forward", "age": "32",
         "nationality": "Senegal"},
        {"name": "Karim Benzema", "league": "Saudi Pro League", "team": "Al-Ittihad", "position": "Forward",
         "age": "37", "nationality": "France"},
        {"name": "Erling Haaland", "league": "Premier League", "team": "Manchester City", "position": "Forward",
         "age": "24", "nationality": "Norway"},
        {"name": "Harry Kane", "league": "Bundesliga", "team": "Bayern Munich", "position": "Forward", "age": "31",
         "nationality": "England"},
        {"name": "Paulo Dybala", "league": "Serie A", "team": "AS Roma", "position": "Forward", "age": "31",
         "nationality": "Argentina"},
        {"name": "Antoine Griezmann", "league": "La Liga", "team": "Atlético Madrid", "position": "Forward",
         "age": "33", "nationality": "France"},
        {"name": "N’Golo Kanté", "league": "Premier League", "team": "Chelsea", "position": "Midfielder", "age": "33",
         "nationality": "France"},
        {"name": "Jan Oblak", "league": "La Liga", "team": "Atlético Madrid", "position": "Goalkeeper", "age": "32",
         "nationality": "Slovenia"},
        {"name": "Manuel Neuer", "league": "Bundesliga", "team": "Bayern Munich", "position": "Goalkeeper", "age": "38",
         "nationality": "Germany"},
        {"name": "Marc-André ter Stegen", "league": "La Liga", "team": "Barcelona", "position": "Goalkeeper",
         "age": "32", "nationality": "Germany"},
        {"name": "Son Heung-min", "league": "Premier League", "team": "Tottenham", "position": "Forward", "age": "32",
         "nationality": "South Korea"},
        {"name": "Raheem Sterling", "league": "Premier League", "team": "Chelsea", "position": "Forward", "age": "30",
         "nationality": "England"},
        {"name": "Bernardo Silva", "league": "Premier League", "team": "Manchester City", "position": "Midfielder",
         "age": "30", "nationality": "Portugal"},
        {"name": "Joshua Kimmich", "league": "Bundesliga", "team": "Bayern Munich", "position": "Midfielder",
         "age": "30", "nationality": "Germany"},
        {"name": "Alisson Becker", "league": "Premier League", "team": "Liverpool", "position": "Goalkeeper",
         "age": "32", "nationality": "Brazil"},
        {"name": "Thibaut Courtois", "league": "La Liga", "team": "Real Madrid", "position": "Goalkeeper", "age": "32",
         "nationality": "Belgium"},
        {"name": "Casemiro", "league": "Premier League", "team": "Manchester United", "position": "Midfielder",
         "age": "33", "nationality": "Brazil"},
        {"name": "Frenkie de Jong", "league": "Premier League", "team": "Manchester United", "position": "Midfielder",
         "age": "27", "nationality": "Netherlands"},
        {"name": "Jadon Sancho", "league": "Premier League", "team": "Manchester United", "position": "Winger",
         "age": "24", "nationality": "England"},
        {"name": "Bruno Fernandes", "league": "Premier League", "team": "Manchester United", "position": "Midfielder",
         "age": "30", "nationality": "Portugal"},
        {"name": "Romelu Lukaku", "league": "Serie A", "team": "Roma", "position": "Forward", "age": "31",
         "nationality": "Belgium"},
        {"name": "Luis Suárez", "league": "Brasileiro Série A", "team": "Grêmio", "position": "Forward", "age": "38",
         "nationality": "Uruguay"},
        {"name": "Thomas Müller", "league": "Bundesliga", "team": "Bayern Munich", "position": "Midfielder",
         "age": "35", "nationality": "Germany"},
        {"name": "Vinicius Junior", "league": "La Liga", "team": "Real Madrid", "position": "Forward", "age": "24",
         "nationality": "Brazil"},
        {"name": "Nico Williams", "league": "La Liga", "team": "Athletico Bilbao", "position": "Forward", "age": "22",
         "nationality": "Spain"},
        {"name": "Lamine Yamal", "league": "La Liga", "team": "Barcelona", "position": "Forward", "age": "17",
         "nationality": "Spain"},
        {"name": "Pau Cubarsi", "league": "La Liga", "team": "Barcelona", "position": "Defender", "age": "18",
         "nationality": "Spain"},
        {"name": "Ferran Torres", "league": "La Liga", "team": "Barcelona", "position": "Midfielder", "age": "24",
         "nationality": "Spain"},
        {"name": "Sergio Ramos", "league": "La Liga", "team": "Sevilla", "position": "Defender", "age": "38",
         "nationality": "Spain"},
        {"name": "Antony", "league": "Premier League", "team": "Manchester United", "position": "Forward", "age": "25",
         "nationality": "Brazil"},
        {"name": "Jude Bellingham", "league": "La Liga", "team": "Real Madrid", "position": "Midfielder", "age": "21",
         "nationality": "England"},
        {"name": "Antonio Rüdiger", "league": "La Liga", "team": "Real Madrid", "position": "Defencer", "age": "31",
         "nationality": "Germany"},
        {"name": "Dani Olmo", "league": "La Liga", "team": "Barcelona", "position": "Midfielder", "age": "26",
         "nationality": "Spain"},
        {"name": "Dani Carvajal", "league": "La Liga", "team": "Real Madrid", "position": "Defender", "age": "33",
         "nationality": "Spain"},
        {"name": "Gonzalo Garcia", "league": "La Liga", "team": "Real Madrid", "position": "Forward", "age": "20",
         "nationality": "Spain"},
    ]

    print("Think of a football player, and I'll try to guess who it is by asking a few questions.")
    print("At any point, type 'exit' to quit the game.")

    candidates = players.copy()

    questions = [
        ("league", "Which league does he play in?"),
        ("position", "What is his position?"),
        ("nationality", "What is his nationality?"),
        ("team", "Which team does he play for?"),
        ("age", "What is his age?")
    ]

    for attribute, question in questions:
        if len(candidates) == 1:
            break

        answer = input(question + " ").strip()
        if answer.lower() == "exit":
            print("Exiting the game.")
            return

        candidates = filter_players(candidates, attribute, answer)

        if not candidates:
            print("No player matches that description. Please try again.")
            return

    if len(candidates) == 1:
        guessed_player = candidates[0]["name"]
        print("The player you are thinking of is:", guessed_player)
        correct = input("Was I correct? (yes/no) ").strip().lower()
        if correct in ("yes", "y"):
            print("Great! Thanks for playing!")
        else:
            correct_name = input("Oh no, what player were you thinking of? ").strip()
            correct_league = input("Which league does he play in? ").strip()
            correct_position = input("What position does he play in? ").strip()
            correct_nationality = input("What is his nationality? ").strip()
            correct_team = input("Which team does he play for? ").strip()
            correct_age = input("How old is he? ").strip()
            print(f"Thanks for letting me know! I'll add {correct_name} to my records")
            print("Thanks for playing!")
            return
    else:
        print("I couldn't guess with certainty. The players that match are:")
        for player in candidates:
            print("- " + player["name"])

def missing11():
    teams = {
        "Liverpool (2019 Champions League)": [
            ("GK", "Becker"),
            ("LB", "Robertson"),
            ("CB", "Van Dijk"),
            ("CB", "Matip"),
            ("RB", "Alexander-Arnold"),
            ("CM", "Fabinho"),
            ("CM", "Wijnaldum"),
            ("CM", "Milner"),
            ("LW", "Mane"),
            ("RW", "Salah"),
            ("ST", "Firmino")
        ],
        "Bayern Munich (2020 Champions League)": [
            ("GK", "Neuer"),
            ("LB", "Davies"),
            ("CB", "Boateng"),
            ("CB", "Alaba"),
            ("RB", "Pavard"),
            ("CM", "Kimmich"),
            ("CM", "Goretzka"),
            ("CM", "Muller"),
            ("LW", "Coman"),
            ("RW", "Gnabry"),
            ("ST", "Lewandowski")
        ],
        "Chelsea (2021 Champions League)": [
            ("GK", "Mendy"),
            ("LB", "Azpilicueta"),
            ("CB", "Thiago Silva"),
            ("CB", "Rudiger"),
            ("RB", "James"),
            ("CM", "Jorginho"),
            ("CM", "Kante"),
            ("CM", "Mount"),
            ("LW", "Pulisic"),
            ("RW", "Havertz"),
            ("ST", "Werner")
        ],
        "Real Madrid (2022 Champions League)": [
            ("GK", "Courtois"),
            ("LB", "Mendy"),
            ("CB", "Militao"),
            ("CB", "Alaba"),
            ("RB", "Carvajal"),
            ("CM", "Casemiro"),
            ("CM", "Modric"),
            ("CM", "Kroos"),
            ("LW", "Vinicius"),
            ("RW", "Asensio"),
            ("ST", "Benzema")
        ],
        "Manchester City (2023 Champions League)": [
            ("GK", "Ederson"),
            ("LB", "Stones"),
            ("CB", "Dias"),
            ("CB", "Laporte"),
            ("RB", "Walker"),
            ("CM", "Rodri"),
            ("CM", "De Bruyne"),
            ("CM", "Silva"),
            ("LW", "Foden"),
            ("RW", "Mahrez"),
            ("ST", "Haaland")
        ],
        "Italy (2006 World Cup)": [
            ("GK", "Buffon"),
            ("LB", "Zambrotta"),
            ("CB", "Cannavaro"),
            ("CB", "Materazzi"),
            ("RB", "Grosso"),
            ("CM", "Pirlo"),
            ("CM", "Gattuso"),
            ("CM", "De Rossi"),
            ("LW", "Del Piero"),
            ("RW", "Totti"),
            ("ST", "Toni")
        ],
        "Spain (2010 World Cup)": [
            ("GK", "Casillas"),
            ("LB", "Capdevila"),
            ("CB", "Ramos"),
            ("CB", "Pique"),
            ("RB", "Puyol"),
            ("CM", "Alonso"),
            ("CM", "Xavi"),
            ("CM", "Iniesta"),
            ("LW", "David Villa"),
            ("RW", "Fabregas"),
            ("ST", "Torres")
        ],
        "Germany (2014 World Cup)": [
            ("GK", "Neuer"),
            ("LB", "Lahm"),
            ("CB", "Hummels"),
            ("CB", "Boateng"),
            ("RB", "Howedes"),
            ("CM", "Schweinsteiger"),
            ("CM", "Kroos"),
            ("CM", "Ozil"),
            ("LW", "Götze"),
            ("RW", "Muller"),
            ("ST", "Klose")
        ],
        "France (2018 World Cup)": [
            ("GK", "Lloris"),
            ("LB", "Hernandez"),
            ("CB", "Varane"),
            ("CB", "Umtiti"),
            ("RB", "Pavard"),
            ("CM", "Kante"),
            ("CM", "Pogba"),
            ("CM", "Matuidi"),
            ("LW", "Griezmann"),
            ("RW", "Mbappe"),
            ("ST", "Giroud")
        ],
        "Argentina (2022 World Cup)": [
            ("GK", "Martinez"),
            ("LB", "Acuña"),
            ("CB", "Romero"),
            ("CB", "Otamendi"),
            ("RB", "Molina"),
            ("CM", "De Paul"),
            ("CM", "Paredes"),
            ("CM", "Mac Allister"),
            ("LW", "Di Maria"),
            ("RW", "Messi"),
            ("ST", "Martínez")
        ]
    }
    # Randomly select a team.
    team_name, lineup = random.choice(list(teams.items()))
    print(f"Guess the starting 11 for {team_name}!")
    print("Enter player names one by one. (Type 'quit' to exit)\n")

    guessed = set()
    attempts = 0
    while len(guessed) < 11:
        guess = input("Your guess: ").strip()
        if guess.lower() == "quit":
            print("Game exited.")
            return
        attempts += 1
        normalized_guess = guess.lower()
        found = False

        # Check the guess against each player's name.
        for pos, player in lineup:
            if player.lower() == normalized_guess:
                if player in guessed:
                    print(f"You already guessed {player}.")
                else:
                    guessed.add(player)
                    print(f"Correct! {player} plays as {pos}.")
                found = True
                break

        if not found:
            print("Incorrect guess.")

        # Display the full lineup with positions, showing "???" for unguessed players.
        print("\nCurrent lineup:")
        for pos, player in lineup:
            if player in guessed:
                print(f"{pos}: {player}")
            else:
                print(f"{pos}: ???")
        print(f"\n{len(guessed)}/11 players found.\n")

    print(f"Congratulations! You completed the lineup in {attempts} guesses.")
    print("\nThe full starting 11 was:")
    for pos, player in lineup:
        print(f"{pos}: {player}")

# --------------------- MAIN MENU ---------------------

def main_menu():
    print("Welcome to the BIEBIR HUB")
    print("Choose a mode:")
    print("1: Play Games")
    print("2: Bond Calculations")
    print("3: Corporate Finance & Accounting")
    mode = input("Enter 1, 2, or 3: ").strip()

    if mode == "1":
        print("\nSelect a game:")
        print("1: Tic Tac Toe")
        print("2: Footynator")
        print("3: Tenaball")
        print("4: Missing 11")
        game_choice = input("Enter a number from 1 to 4: ").strip()
        if game_choice == "1":
            Footy_tictactoe()
        elif game_choice == "2":
            footynator()
        elif game_choice == "3":
            tenaball()
        elif game_choice == "4":
            missing11()
        else:
            print("Invalid game choice!")
    elif mode == "2":
        print("\nSelect a bond calculation:")
        print("1: Calculate Bond Maturity Value")
        print("2: Calculate Bond Price")
        print("3: Calculate Perpetuity Price")
        print("4: Calculate Current Yield")
        print("5: Calculate Yield to Maturity (YTM)")
        print("6: Calculate Duration")
        bond_choice = input("Enter a number from 1 to 6: ").strip()
        if bond_choice == "1":
            bond_maturity()
        elif bond_choice == "2":
            bond_calculator()
        elif bond_choice == "3":
            try:
                payment = float(input("Enter the periodic payment: "))
                discount_rate_percent = float(input("Enter the discount rate (as a percentage): "))
                price = perpetuity_price(payment, discount_rate_percent)
                print(f"The price of the perpetuity is: ${price:.2f}")
            except ValueError as e:
                print("Error:", e)
        elif bond_choice == "4":
            current_yield()
        elif bond_choice == "5":
            yield_to_maturity()
        elif bond_choice == "6":
            duration_calculation()
        else:
            print("Invalid bond calculation choice!")
    elif mode == "3":
        print("\nSelect a corporate finance calculation:")
        print("1: Calculate IRR")
        print("2: Calculate Payback Period")
        print("3: Calculate Recovery Value")
        cf_choice = input("Enter 1, 2, or 3: ").strip()
        if cf_choice == "1":
            irr_calculation()
        elif cf_choice == "2":
            payback_period()
        elif cf_choice == "3":
            recovery_value()
        else:
            print("Invalid corporate finance calculation choice!")
    else:
        print("Invalid mode selected. Please restart and choose 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
