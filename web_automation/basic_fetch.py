from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

from pprint import pprint

def main():
    # Initialize the HfApiModel
    # This will use the Hugging Face API with the default model
    model = HfApiModel()
    
    # Print the model ID being used
    print("Using model:")
    pprint(model.model_id)
    
    # Initialize the agent with tools
    # Using both DuckDuckGo search and web browser capabilities
    agent = CodeAgent(
        tools=[
            DuckDuckGoSearchTool(),
        ],
        model=model
    )
    
    # Example queries
    queries = [
        "How long does it take to get to the moon with a Saturn 5 rocket?",
        "What are the main features of Python 3.10?",
        "Find the latest news about artificial intelligence."
    ]
    
    # Run the agent with each query
    for query in queries:
        print("\n" + "="*50)
        print(f"QUERY: {query}")
        print("="*50)
        
        response = agent.run(query)
        
        print("\nRESPONSE:")
        print(response)

if __name__ == "__main__":
    main()