# Little League Lineup Generator

This project is designed to help coaches generate optimal lineups for little league baseball teams. It takes into account player capabilities, preferred positions, and time spent in the infield versus outfield throughout the season.

## Project Structure

```
little-league-lineup
├── src
│   ├── lineup_generator.py       # Main logic for generating the optimal lineup
│   ├── data
│   │   └── players.json          # Player data in JSON format
│   ├── utils
│   │   └── calculations.py        # Utility functions for calculations
├── tests
│   └── test_lineup_generator.py   # Unit tests for lineup generation
├── requirements.txt               # Python dependencies
├── .gitignore                     # Files to ignore in version control
└── README.md                      # Project documentation
```

## Setup

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using:

   ```
   pip install -r requirements.txt
   ```

## Usage

To generate an optimal lineup, run the `lineup_generator.py` script located in the `src` directory. Ensure that the `players.json` file is populated with player data before running the script.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License.