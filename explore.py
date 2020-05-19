import sys
import os
print(sys.path)
sys.path.append('C:\\program files\\python35\\lib\\site-packages')

import chess
import chess.pgn

def position(move):
    return "S"

output = open("boardstates.txt","w+")
output2 = open("gamebreakdown.txt","w+")

boardsForGame = []

def writeBoard(bird):
    output.write(bird.winner)
    output.write("-")
    output.write(bird.board)
    output.write(", ")

class Boardstate:
    board =  ""
    winner = "W"

    def __init__(self):

        self.board += "BRBNBBBQBKBBBNBR"
        self.board += "BPBPBPBPBPBPBPBP"
        for r in range(4):
            for c in range(8):
                self.board += "EE"
        self.board += "WRWNWBWQWKWBWNWR"
        self.board += "WPWPWPWPWPWPWPWP"

    def move(self, mv):
        return self


def parseGame(pgn, winner, welo, belo, tmc):

    temp = open("kasp.pgn")
    temp2 = open("temp.pgn","w+")
    temp2.write('[Event "IBM Man-Machine, New York USA"]\n[Site "01"]\n[Date "1997.??.??"]\n[EventDate "?"]\n[Round "?"]\n[Result "1-0"]\n[White "Garry Kasparov"]\n[Black "Deep Blue (Computer)"]\n[ECO "A06"]\n[WhiteElo "?"]\n[BlackElo "?"]\n[PlyCount "89"]')
    temp2.write('\n')
    temp2.write(pgn)
    temp2.write(' 1-0')
    temp2.close()
    temp2 = open("temp.pgn")
    #temp.write('[Event "London m5"]\n[Site "London"]\n[Date "1862.??.??"]\n[Round "?"]\n[White "Mackenzie, George Henry"]\n[Black "Paulsen, Louis"]\n[Result "1-0"]\n[WhiteElo ""]\n[BlackElo ""]\n[ECO "C51"]\n1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bxb4 5.c3 Bc5 6.O-O d6 7.d4 exd4 8.cxd4 Bb69.Nc3 Na5 10.Bd3 Ne7 11.e5 dxe5 12.dxe5 O-O 13.Qc2 h6 14.Ba3 c5 15.Rad1 Bd7 16.e6 fxe6 17.Bh7+ Kh8 18.Ne5 Nd5 19.Nxd5 exd5 20.Rxd5 Bf5 21.Rxd8 Bxc2 22.Rxf8+ Rxf8 23.Bxc2  1-0')

    first_game = chess.pgn.read_game(temp2)
    first_game.headers["Event"]
    #print(first_game)
    board = first_game.board()
    #print(board)
    tt = [0,0,0,0,0]
    mc = 0
    lc = 0

    output2.write(winner)
    output2.write(',')
    output2.write(str(welo))
    output2.write(',')
    output2.write(str(belo))
    output2.write(',')
    output2.write(str(tmc))
    output2.write(',')
    for move in first_game.mainline_moves():
        output.write(winner)
        output.write(',')
        output.write(str(welo))
        output.write(',')
        output.write(str(belo))
        output.write(',')
        output.write(str(tmc))
        output.write(',')
        output.write(str(mc+1))
        output.write(',')
        board.push(move)
        mc+=1
        pc = pieceCount(board)
        for n in range(len(tt)):
            tt[n] += pc[n]
        if mc == 10 or mc == 20 or mc == 30:
            lc += 1
            for n in range(len(tt)):
                output2.write(str(tt[n]))
                output2.write(',')
        for n in range(len(tt)):
            output.write(str(pc[n]))
            output.write(',')
        for n in range(len(tt)):
            output.write(str(tt[n]))
            output.write(',')
        output.write('0')
        output.write('\n')
    while lc < 3:
        lc += 1
        for n in range(len(tt)):
            output2.write('999')
            output2.write(',')
    for n in range(len(tt)):
        output2.write(str(tt[n]))
        output2.write(',')
    output2.write('\n')

    temp2.close()
    os.remove("temp.pgn")

def pieceCount(board):
    final = []
    final.append(len(board.pieces(chess.PAWN,chess.WHITE)) - len(board.pieces(chess.PAWN,chess.BLACK)))
    final.append(len(board.pieces(chess.KNIGHT,chess.WHITE)) - len(board.pieces(chess.KNIGHT,chess.BLACK)))
    final.append(len(board.pieces(chess.BISHOP,chess.WHITE)) - len(board.pieces(chess.BISHOP,chess.BLACK)))
    final.append(len(board.pieces(chess.ROOK,chess.WHITE)) - len(board.pieces(chess.ROOK,chess.BLACK)))
    final.append(len(board.pieces(chess.QUEEN,chess.WHITE)) - len(board.pieces(chess.QUEEN,chess.BLACK)))
    return final

def process_lines(stro):
    if (stro[0:1] == "#"):
        return
    #print(stro.find("###"))
    if (stro.find("###") > -1):
        movestring = stro[stro.find("###") + 4:]
        initial = stro[0:stro.find("###")].split(" ")
        #print(initial)
        moves = movestring.split(" ")
        #output.write(movestring)
        #print(moves)
        winner = "F"
        if (initial[2] == '1-0'): winner = "W"
        if (initial[2] == '0-1'): winner = "B"
        if (initial[2] == '1/2-1/2'): winner = "D"
        welo = 0
        belo = 0
        if (initial[8] == "welo_false"): welo = int(initial[3])
        if (initial[9] == "belo_false"): belo = int(initial[4])
        parseGame(movestring, winner, welo, belo, initial[5])
        #print(movestring)
    #output.write(stro)

test = 0
with open("chess.txt") as f:
    for n in range(24):
        output2.write("Col" + str(n + 1))
        output2.write(',')
    for n in range(15):
        output.write("Col" + str(n + 1))
        output.write(',')
    output.write("Col" + str(16 + 1))
    output.write('\n')
    output2.write("Col" + str(25 + 1))
    output2.write('\n')
    for line in f:
        process_lines(line)
        test += 1
        if (test > 10000):
            break



output.close()
