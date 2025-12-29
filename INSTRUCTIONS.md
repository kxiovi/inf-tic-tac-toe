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

This project cannot simply use classical minimax/negamax, because there are no terminal 
end nodes unless there is a victory. Thus, project uses a custom AI that only looks 
1 move ahead and prioritizes the optimal outcome (draw).

Also, because TTT is a relatively small board space, 
and the AI is thinking only one move ahead, I've used the copy
of the board rather than doing and undoing moves.