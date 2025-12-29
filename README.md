# Brief Description

Using React + Vite, I've created a custom AI to play 
infinite Tic-Tac-Toe (TTT) optimally. 

Infinite TTT is just like classical TTT but prevents draws by removing the 4th oldest
move of each player. 

I had to use a custom search implementation because infinite TTT does 
not have terminal end nodes, thus many simulation based
search techniques, and terminal node based search techniques do not work. 
This rules out classical minimax/negamax and Monte Carlo. Thus, the project uses a custom AI that only looks
1 move ahead and prioritizes the optimal outcome (draw). Since infinite TTT does not allow
for draws, the AI can either win, or the games keeps going on for infinity.

Also, because TTT is a relatively small board space,
and the AI is thinking only one move ahead, I've used copies
of the board rather than doing and undoing moves.

# Usage

At `inf-tic-tac-toe/api', run:
```aiignore
flask run
```

At the root, run:
```aiignore
npm run dev
```

# Troubleshooting

If error `'flask' not found`:
Run the virtual environment, in `inf-tic-tac-toe/api':
```aiignore
python3 -m venv venv
. venv/bin/activate
pip install flask python-dotenv 
```

# Potential Improvements

- make a slider for weakest to strongest AI player
- randomize AI to be either X or O
