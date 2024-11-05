def ask_question(prompt, options):
    """Utility function to ask a question and validate user input."""
    print(prompt)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input("Enter your choice (1-{}): ".format(len(options))))
            if 1 <= choice <= len(options):
                return choice
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def investment_risk_questionnaire():
    """Runs the questionnaire and calculates the risk score."""
    score = 0

    # Section 2: Investment Objectives
    score += ask_question(
        "What is your primary investment goal?",
        ["Wealth preservation", "Stable income generation",
         "Moderate capital growth", "Aggressive capital growth"]
    )

    score += ask_question(
        "How long do you plan to invest the majority of your funds?",
        ["Less than 1 year", "1 – 3 years", "3 – 5 years", "5 – 10 years", "10+ years"]
    )

    # Section 3: Attitudes Towards Risk
    score += ask_question(
        "How comfortable are you with market fluctuations in your investments?",
        ["I get anxious with any loss.",
         "I am uncomfortable with losses but willing to accept small risks.",
         "I am comfortable with moderate fluctuations to achieve growth.",
         "I can accept large losses for the potential of high returns."]
    )

    score += ask_question(
        "How would you react if your portfolio lost 20% of its value in a month?",
        ["Sell everything to avoid further losses.",
         "Sell some assets to reduce risk.",
         "Stay invested and wait for recovery.",
         "Buy more assets to take advantage of lower prices."]
    )

    score += ask_question(
        "What is the maximum percentage loss you could tolerate over a year?",
        ["0 – 5%", "5 – 10%", "10 – 20%", "More than 20%"]
    )

    # Section 4: Investment Experience and Preferences
    score += ask_question(
        "How experienced are you with investing?",
        ["Beginner (little or no experience)",
         "Intermediate (some experience with stocks or mutual funds)",
         "Advanced (comfortable managing diverse investments)"]
    )

    score += ask_question(
        "What types of investments are you most interested in?",
        ["Cash or Fixed Income (Savings, Bonds, CDs)",
         "Balanced Funds or ETFs (Mix of stocks and bonds)",
         "Equities (Stocks, Mutual Funds)",
         "High-risk Investments (Crypto, Options, Startups)"]
    )

    # Section 5: Portfolio Strategy Preferences
    score += ask_question(
        "How frequently do you plan to monitor your investments?",
        ["Daily", "Weekly", "Monthly", "Annually or less frequently"]
    )

    score += ask_question(
        "Would you prefer higher but unpredictable returns over stable and lower returns?",
        ["Strongly prefer stable returns",
         "Slightly prefer stable returns",
         "Slightly prefer higher returns",
         "Strongly prefer higher returns"]
    )

    score += ask_question(
        "How important is liquidity (ease of converting investments to cash) for you?",
        ["Very important – I may need quick access to my funds.",
         "Somewhat important – I prefer some liquidity but can wait.",
         "Not important – I am comfortable with long-term investments."]
    )

    # Calculate Risk Preference Based on Score
    if score <= 15:
        risk_profile = "Conservative Investor"
    elif 16 <= score <= 25:
        risk_profile = "Moderate Investor"
    else:
        risk_profile = "Aggressive Investor"
    return risk_profile

