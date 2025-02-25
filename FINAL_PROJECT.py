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
            print("IRR not found in the range. Please check your inputs.")
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

def tic_tac_toe_game():
    print("Welcome to the Tic Tac Toe game"
          "\nThis game will serve as a base for the football-inspired multiplayer versions")
    print("In this game, a single player will play against the computer")
    print("We recommend making the output screen bigger for better visibility")
    print("-------------------------------------------------------------")
    print("-------------------------------------------------------------")

    Numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    gameBoard = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rows = 3
    columns = 3

    def printboard():
        for x in range(rows):
            print("\n______________")
            print(" |", end="")
            for y in range(columns):
                print("", gameBoard[x][y], end=" |")
        print("\n______________")

    def modgameboard(num, turn):
        num -= 1
        if num == 0:
            gameBoard[0][0] = turn
        elif num == 1:
            gameBoard[0][1] = turn
        elif num == 2:
            gameBoard[0][2] = turn
        elif num == 3:
            gameBoard[1][0] = turn
        elif num == 4:
            gameBoard[1][1] = turn
        elif num == 5:
            gameBoard[1][2] = turn
        elif num == 6:
            gameBoard[2][0] = turn
        elif num == 7:
            gameBoard[2][1] = turn
        elif num == 8:
            gameBoard[2][2] = turn

    endloop = False
    Count_Turns = 0

    def checkwin(gameBoard):
        nonlocal endloop
        # Check rows
        if gameBoard[0][0] == gameBoard[0][1] == gameBoard[0][2] == 'X':
            print("Player wins!")
            endloop = True
        elif gameBoard[1][0] == gameBoard[1][1] == gameBoard[1][2] == 'X':
            print("Player wins!")
            endloop = True
        elif gameBoard[2][0] == gameBoard[2][1] == gameBoard[2][2] == 'X':
            print("Player wins!")
            endloop = True
        elif gameBoard[0][0] == gameBoard[0][1] == gameBoard[0][2] == 'O':
            print("Python wins!")
            endloop = True
        elif gameBoard[1][0] == gameBoard[1][1] == gameBoard[1][2] == 'O':
            print("Python wins!")
            endloop = True
        elif gameBoard[2][0] == gameBoard[2][1] == gameBoard[2][2] == 'O':
            print("Python wins!")
            endloop = True
        # Check columns
        if gameBoard[0][0] == gameBoard[1][0] == gameBoard[2][0] == 'X':
            print("Player wins!")
            endloop = True
        elif gameBoard[0][0] == gameBoard[1][0] == gameBoard[2][0] == 'O':
            print("Python wins!")
            endloop = True
        elif gameBoard[0][1] == gameBoard[1][1] == gameBoard[2][1] == 'X':
            print("Player wins!")
            endloop = True
        elif gameBoard[0][1] == gameBoard[1][1] == gameBoard[2][1] == 'O':
            print("Python wins!")
            endloop = True
        elif gameBoard[0][2] == gameBoard[1][2] == gameBoard[2][2] == 'X':
            print("Player wins!")
            endloop = True
        elif gameBoard[0][2] == gameBoard[1][2] == gameBoard[2][2] == 'O':
            print("Python wins!")
            endloop = True
        # Check diagonals
        if gameBoard[0][0] == gameBoard[1][1] == gameBoard[2][2] == 'X':
            print("Player wins!")
            endloop = True
        elif gameBoard[0][0] == gameBoard[1][1] == gameBoard[2][2] == 'O':
            print("Python wins!")
            endloop = True
        elif gameBoard[2][0] == gameBoard[1][1] == gameBoard[0][2] == 'X':
            print("Player wins!")
            endloop = True
        elif gameBoard[2][0] == gameBoard[1][1] == gameBoard[0][2] == 'O':
            print("Python wins!")
            endloop = True

    while not endloop:
        if Count_Turns % 2 == 1:
            printboard()
            picknumber = int(input("\nChoose a number from 1 to 9: "))
            if 1 <= picknumber <= 9 and picknumber in Numbers:
                modgameboard(picknumber, 'X')
                Numbers.remove(picknumber)
                checkwin(gameBoard)
            else:
                print("Invalid input, please enter an available integer between 1 and 9")
            Count_Turns += 1
        else:
            if Numbers:
                ChoicePython = random.choice(Numbers)
                print("\nCPU chose:", ChoicePython)
                modgameboard(ChoicePython, 'O')
                Numbers.remove(ChoicePython)
                checkwin(gameBoard)
                Count_Turns += 1
            else:
                break

def tenaball():
    barcelona_signings = ["Philippe Coutinho", "Ousmane Dembele", "Antoine Griezmann",
                          "Neymar Jr", "Frenkie de Jong", "Luis Suarez", "Zlatan Ibrahimovic"]
    degea_app = ["Marcus Rashford", "Chris Smalling", "Anthony Martial", "Juan Mata",
                 "Antonio Valencia", "Ashley Young", "Luke Shaw", "Wayne Rooney", "Phil Jones", "Victor Lindelof"]
    juve_real = ["Cristiano Ronaldo", "Zinedine Zidane", "Gonzalo Higuain", "Alvaro Morata",
                 "Sami Khedira", "Danilo", "Fabio Cannavaro", "Angel Di Maria", "Emereson", "Micheal Laudrup"]
    spain_app = ["Sergio Ramos", "Iker Casillas", "Sergio Busquets", "Xavi", "Andres Iniesta",
                 "Andoni Zubizarreta", "David Silva", "Xabi Alonso", "Fernando Torres", "Cesc Fabregas"]
    top_goals = ["Cristiano Ronaldo", "Lionel Messi", "Pele", "Romario", "Ferenc Puskas",
                 "Josef Bican", "Robert Lewandowski", "Jimmy Jones", "Gerd Muller", "Joe Bambrick"]

    random_tenaball, category = random.choice([
        (barcelona_signings, "most expensive barça signings"),
        (degea_app, "most appearances with teammate David de Gea"),
        (juve_real, "players with the most combined appearances for Juventus and Real Madrid"),
        (spain_app, "players with the most caps for the Spanish National Team"),
        (top_goals, "all time goalscorers")
    ])

    correct_answer = []
    lives = 3

    print("Welcome to our Tenaball game mode")
    play = input("Do you want to play or exit? ").strip().lower()
    if play == "exit":
        print("Bye!")
        return
    else:
        print(f"Find the top 10 {category}")

        while lives > 0 and len(correct_answer) < 10:
            print(f"\nYou have {lives} lives left")
            player = input("Enter a player's full name: ").strip()
            if player in random_tenaball and player not in correct_answer:
                position = random_tenaball.index(player) + 1
                print(f"You guessed {player} correctly, he is number {position} on the list")
                correct_answer.append(player)
                lives = 3
            elif player in correct_answer:
                print("You already guessed that player")
            else:
                print(f"{player} is not on the list")
                lives -= 1

        if len(correct_answer) == 10:
            print("\nYou beat the Tenaball")
        else:
            print("\nThe Tenaball beat you")
            print("The correct players were:")
            for pos, player in enumerate(random_tenaball, start=1):
                print(f"{pos}. {player}")

def footynator():
    print("Welcome to Footynator Bond Price Calculator")


def missing11():
    print("Welcome to Missing 11")


# --------------------- MAIN MENU ---------------------

def main_menu():
    print("Welcome to the BIEBIR assistant!")
    print("Choose a mode:")
    print("1: Play Games")
    print("2: Bond Calculations")
    print("3: Corporate Finance & Accounting")
    mode = input("Enter 1, 2, or 3: ").strip()

    if mode == "1":
        print("\nSelect a game:")
        print("1: Tic Tac Toe")
        print("2: Footynator Bond Price")
        print("3: Tenaball")
        print("4: Missing 11")
        game_choice = input("Enter a number from 1 to 4: ").strip()
        if game_choice == "1":
            tic_tac_toe_game()
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
