from arbit import check_sports  # Import the check_sports function from arbit.py

# Main execution
if __name__ == "__main__":
    try:
        # Call the function that checks sports for arbitrage opportunities
        check_sports()
    except Exception as e:
        # If an error occurs, send a critical failure email
        import traceback
        from arbit import send_email  # Import the send_email function from arbit.py
        error_message = f"Critical error: {str(e)}\n{traceback.format_exc()}"
        send_email("Arbitrage Bot Critical Failure", error_message)
