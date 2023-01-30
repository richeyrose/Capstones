import math

# Use triple quotes to display a multi line string. Putting this inside the
# input() method would make the code difficult to read
print(
    """Choose either 'investment' or 'bond' fromn the menu below to proceed:

investment  -   to calculate the amount of interest you'll earn on your \
investment
bond        -   to calculate the amount you'll have to pay on a home loan"""
)

# convert to upper so we don't need to check for variants
investment_type = input().upper()
# exit if the user enters an invalid string
if investment_type != "INVESTMENT" and investment_type != "BOND":
    print("Invalid input. Exiting program.")
elif investment_type == "INVESTMENT":
    # make sure we show a currency sign in fron of the user input
    deposit = float(input("How much would you like to deposit?\n£ "))
    # convert to decimal
    rate = float(input("Please enter the interest rate as a number: ")) * 0.01
    years = int(input("Please enter the number of years you wish to invest \
for: "))
    interest = input(
        "Please choose either 'simple' or 'compound' interest:").upper()
    # check again for invalid input
    if interest != "SIMPLE" and interest != "COMPOUND":
        print("Invalid input. Exiting program.")
    # calculate and print total amount if simple interest is chosen
    elif interest == "SIMPLE":
        total_amount = round((deposit * (1 + rate * years)), 2)
        print(f"You will have £{total_amount} after {years} years.")
    else:
        # calculate and print total amount if compound interest is chosen
        total_amount = round((deposit * math.pow((1 + rate), years)), 2)
        print(f"You will have £{total_amount} after {years} years.")
else:
    house_value = float(
        # get value of house
        input("Please enter the present value of your house: £"))
    # get interest rate and convert to decimal
    yearly_rate = float(
        input("Please enter the interest rate as a number: ")) * 0.01
    # get number of months to pay back bond
    months = int(input(
        "Please enter the number of months you plan to repay the bond over:"))
    # calculate monthly rate
    monthly_rate = yearly_rate / 12
    # calculated monthly repayment amount
    repayment_amount = (monthly_rate * house_value) / (
        1 - math.pow((1 + monthly_rate), (-months))
    )
    print(f"You will need to repay £{round(repayment_amount, 2)} per month.")
