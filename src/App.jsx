import {useEffect, useState} from 'react'
import './App.css'

function App() {
    const [board, setBoard] = useState(Array(9).fill(""))
    const [winner, setWinner] = useState(null)
    const [playAI, setPlayAI] = useState(false)
    const [thinking, setThinking] = useState(false)

    useEffect(() => {
    fetch("/api/state")
        .then(res => res.json())
        .then(data => {
            setBoard(data.board)
            setWinner(data.winner)
        });
    }, [])

    function handleClick(index) {
        if (thinking || winner) return;
        setThinking(true);
        fetch("/api/move", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({index})
        })
            .then(res => res.json())
            .then(data => {
                setBoard(data.board)
                setWinner(data.winner)

                if (playAI && !data.winner) {
                    setTimeout(makeAIMove, 300)
                } else {
                    setThinking(false);
                }
            })
    }

    function resetBoard() {
        setBoard(Array(9).fill(""));
        setWinner(null);
        setPlayAI(false);
        setThinking(false);
        fetch("/api/reset", {method: "POST", headers: {"Content-Type": "application/json"}})
    }

    function startAI() {
      setPlayAI(true);
      setWinner(null);
      setThinking(false);
        fetch("/api/reset", { method: "POST" })
            .then(() => {
                setBoard(Array(9).fill(""));
            });
    }

    function makeAIMove() {
        fetch("/api/negamax", {method: "POST", headers: {"Content-Type": "application/json"}})
        .then(res => res.json())
        .then(data => {
            setBoard(data.board)
            setWinner(data.winner)
            setThinking(false);
        });
    }

  return (
    <>
        <button
            className="resetButton"
            onClick={resetBoard}
            >
            Reset
        </button>
        <button
            className="aiButton"
            onClick={startAI}
            >
            Play AI
        </button>
      <h1>Tic Tac Toe</h1>
      <div className="board">
          {board.map((cell, index) => (
              <button
                  key={index}
                  className={`cell ${cell}`}
                  onClick={() => handleClick(index)}
                  disabled={cell !== "" || winner || thinking}
              >
                  {cell}
              </button>
          ))}
      </div>
        {winner && (
            <p className="winner">
                {winner === "draw" ? "Draw!" : `Winner: ${winner}`}
            </p>
        )}
    </>
  )
}



export default App
