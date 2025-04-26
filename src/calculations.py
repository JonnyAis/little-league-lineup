import json
import pandas as pd

def generate_player_innings_table(input_filepath):
    """
    Generate a table with player innings data and return it as a DataFrame.

    Args:
        input_filepath (str): Path to the input JSON file with position data.

    Returns:
        pd.DataFrame: DataFrame containing the player innings table.
    """
    # Load the position data
    with open(input_filepath, 'r') as file:
        position_data = json.load(file)

    # Initialize a dictionary to store the summary
    player_summary = {}

    # Define all positions
    all_positions = ['P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']

    # Calculate total innings per game
    total_innings_per_game = {
        game: max(sum(players.values()) for position, players in positions.items() if position != "Inactive")
        for game, positions in position_data.items()
    }

    # Process each game
    for game, positions in position_data.items():
        inactive_players = positions.get("Inactive", [])
        for position, players in positions.items():
            if position == "Inactive":
                continue
            for player, innings in players.items():
                if player not in player_summary:
                    # Initialize all positions and totals for the player
                    player_summary[player] = {pos: 0 for pos in all_positions}
                    player_summary[player].update({
                        'Total Innings': 0,
                        'Available Innings': 0
                    })
                # Update the player's innings based on the position
                if position in all_positions:
                    player_summary[player][position] += innings
                # Update the total innings
                player_summary[player]['Total Innings'] += innings

    # Correctly calculate available innings for each player
    for player in player_summary.keys():
        player_summary[player]['Available Innings'] = sum(
            total_innings_per_game[game]
            for game, positions in position_data.items()
            if player not in positions.get("Inactive", [])
        )

    # Convert the summary to a DataFrame
    df = pd.DataFrame.from_dict(player_summary, orient='index')
    df.index.name = 'Player'
    df.reset_index(inplace=True)

    # Add a column for the percentage of total innings played
    df['Percentage Played'] = (df['Total Innings'] / df['Available Innings'] * 100).round(2)

    return df


# File paths
input_file = 'c:/Users/jonat/OneDrive/Documents/GitHub/little-league-lineup/src/data/positions_data_history.json'

# Generate the table
df = generate_player_innings_table(input_file)

# Print the DataFrame to verify
print("Player innings table generated:")
print(df)