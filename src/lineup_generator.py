def load_players(filepath):
    """Load player data from a JSON file."""
    import json
    with open(filepath, 'r') as file:
        data = json.load(file)
        return data['players']  # Return the list of players

def load_game_prep(filepath):
    """Load game prep data from a JSON file."""
    import json
    with open(filepath, 'r') as file:
        data = json.load(file)
        return data

def load_player_innings(filepath):
    """Load player innings data from a CSV file."""
    import csv
    player_innings = {}
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            player_name = row['Player']
            player_innings[player_name] = {
                'Available Innings': int(row['Available Innings']),
                'P': int(row['P']),
                'C': int(row['C']),
                '1B': int(row['1B']),
                '2B': int(row['2B']),
                'SS': int(row['SS']),
                '3B': int(row['3B']),
                'LF': int(row['LF']),
                'CF': int(row['CF']),
                'RF': int(row['RF'])
            }
    return player_innings

def generate_lineups(players, innings=6, game_prep=None, player_innings=None):
    """
    Generate lineups for multiple innings.
    Assigns positions based on player capabilities and availability.

    Args:
        players (list): List of player dictionaries with their details.
        innings (int): Number of innings to generate lineups for.
        game_prep (dict): Pre-game preparation data, including pitching plans and inning availability.
        player_innings (dict): Historical data about player innings.

    Returns:
        tuple: A list of lineups (one for each inning) and a summary table.
    """
    if game_prep is None:
        game_prep = {}
    if player_innings is None:
        player_innings = {}

    # Extract pre-game data
    pitching_plan = game_prep.get("Pitching Plan", {})
    inactive_entire_game = set(game_prep.get("Inning Availability", {}).get("Inactive Entire Game", []))
    partial_inactivity = game_prep.get("Inning Availability", {}).get("Partial Inactivity", {})

    # Define available positions
    infield_positions = ['1B', '2B', '3B', 'SS', 'C', 'P']
    outfield_positions = ['LF', 'CF', 'RF']
    all_positions = infield_positions + outfield_positions

    # Initialize lineups for each inning
    lineups = []

    # Initialize summary table
    summary_table = {player['name']: {'Innings Played': 0, 'Infield': 0, 'Outfield': 0} for player in players}

    # Track player usage to enforce constraints
    player_usage = {player['name']: {'P': 0, 'C': 0, 'sits': 0, 'last_positions': []} for player in players}

    # Track total innings played by each player
    total_innings_played = {player['name']: 0 for player in players}

    for inning in range(1, innings + 1):
        print(f"Generating lineup for Inning {inning}...")  # Debugging
        used_positions = set()
        used_players = set()
        lineup = {position: None for position in all_positions}

        # Assign pitcher first based on the pitching plan
        inning_key = f"Inning {inning}"  # Match the key format in the Pitching Plan
        pitcher_name = pitching_plan.get(inning_key)
        if pitcher_name:
            # Find the pitcher in the players list
            pitcher = next((player for player in players if player['name'] == pitcher_name), None)
            if pitcher and pitcher_name not in inactive_entire_game and inning not in partial_inactivity.get(pitcher_name, []):
                lineup['P'] = pitcher_name
                used_positions.add('P')
                used_players.add(pitcher_name)
                player_usage[pitcher_name]['P'] += 1
                player_usage[pitcher_name]['last_positions'].append('P')
                summary_table[pitcher_name]['Innings Played'] += 1
                summary_table[pitcher_name]['Infield'] += 1
                total_innings_played[pitcher_name] += 1
                if len(player_usage[pitcher_name]['last_positions']) > 2:
                    player_usage[pitcher_name]['last_positions'].pop(0)
                print(f"Assigned {pitcher_name} as Pitcher for Inning {inning}")  # Debugging

        # Assign other positions
        for position in all_positions:
            if position in used_positions:
                continue

            # Sort players by total innings played (ascending) and use percentage of available innings as a tie-breaker
            eligible_players = [
                player for player in players
                if player['name'] not in inactive_entire_game
                and inning not in partial_inactivity.get(player['name'], [])
                and player['name'] not in used_players  # Ensure no duplicate assignments
                and position in player['positions']
                and position not in used_positions
            ]
            eligible_players.sort(key=lambda p: (
                total_innings_played[p['name']],
                player_innings.get(p['name'], {}).get('Total Innings', 0) /
                max(player_innings.get(p['name'], {}).get('Available Innings', 1), 1)
            ))

            for player in eligible_players:
                player_name = player['name']

                # Enforce constraints
                if position == 'P' and player_usage[player_name]['P'] >= 2:
                    continue
                if position == 'C' and player_usage[player_name]['C'] >= 2:
                    continue
                if len(player_usage[player_name]['last_positions']) >= 2 and \
                        player_usage[player_name]['last_positions'][-2:] == [position, position]:
                    # Skip if the player has played this position in the last 2 innings
                    continue

                # Assign the position
                lineup[position] = player_name
                used_positions.add(position)
                used_players.add(player_name)
                player_usage[player_name]['last_positions'].append(position)
                summary_table[player_name]['Innings Played'] += 1
                total_innings_played[player_name] += 1
                if position in infield_positions:
                    summary_table[player_name]['Infield'] += 1
                elif position in outfield_positions:
                    summary_table[player_name]['Outfield'] += 1
                if len(player_usage[player_name]['last_positions']) > 2:
                    player_usage[player_name]['last_positions'].pop(0)

                break

        # Add the lineup for this inning
        lineups.append(lineup)

    # Ensure all active players have played at least one inning
    for player_name, innings_played in total_innings_played.items():
        if player_name not in inactive_entire_game and innings_played == 0:
            print(f"Warning: {player_name} did not play any innings. Adjust the lineup logic.")

    return lineups, summary_table


from calculations import generate_player_innings_table
import pandas as pd

def main():
    """Main function to load players and generate the lineups."""
    players_filepath = 'c:/Users/jonat/OneDrive/Documents/GitHub/little-league-lineup/src/data/players.json'
    prep_filepath = 'c:/Users/jonat/OneDrive/Documents/GitHub/little-league-lineup/src/data/game_prep.json'
    innings_data_filepath = 'c:/Users/jonat/OneDrive/Documents/GitHub/little-league-lineup/src/data/positions_data_history.json'

    players = load_players(players_filepath)
    game_prep = load_game_prep(prep_filepath)

    # Generate the player innings table as a DataFrame
    player_innings_df = generate_player_innings_table(innings_data_filepath)

    # Convert the DataFrame to a dictionary for compatibility with existing code
    player_innings = player_innings_df.set_index('Player').to_dict('index')

    innings = 6
    lineups, summary_table = generate_lineups(players, innings, game_prep, player_innings)

    # Convert the lineups to a DataFrame
    lineup_df = pd.DataFrame(lineups)
    lineup_df.index = [f"Inning {i+1}" for i in range(innings)]

    # Transpose the lineup DataFrame
    lineup_df = lineup_df.transpose()

    # Sort the DataFrame by the desired order of positions
    position_order = ['P', 'C', '1B', '2B', 'SS', '3B', 'LF', 'CF', 'RF']
    lineup_df = lineup_df.reindex(position_order)

    # Convert the summary table to a DataFrame
    summary_df = pd.DataFrame.from_dict(summary_table, orient='index')
    summary_df.index.name = 'Player'
    summary_df.reset_index(inplace=True)

    # Return the DataFrames instead of printing
    return lineup_df, summary_df

if __name__ == "__main__":
    lineup_df, summary_df = main()

    # Display the DataFrames in the interactive window
    import pandas as pd
    from IPython.display import display  # For better formatting in interactive environments

    print("Lineup DataFrame:")
    display(lineup_df)  # Nicely formatted table in the interactive window

    print("\nSummary DataFrame:")
    display(summary_df)  # Nicely formatted table in the interactive window