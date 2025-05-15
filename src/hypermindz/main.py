from hypermindz.crew import InvestmentCrew

def run():
    query = "I want to target 2 million people with a budget of $10 million over 12 months. \
            How would changing the 'Flight (months)' affect my overall budget?"
    result = InvestmentCrew().crew().kickoff(inputs={"query": query})
    print(result)
    print(result.raw)
    print(type(result.raw))
