import board, pieces, ai
from move import Move
import pygame as p
import time



# Khai báo một số hằng số cho giao diện
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = {"WP", "WR", "WN", "WB", "WK", "WQ", "BP", "BR", "BN", "BB", "BK", "BQ"}
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def is_checkmate_or_stalemate(board, color):
    possible_moves = board.get_possible_moves(color)
    if not possible_moves:
        return True
    for possible_move in possible_moves:
        temp_board = board.clone(board)
        temp_board.perform_move(possible_move)
        if not temp_board.is_check(color):
            return False
    return True

def get_valid_user_move(board, user_move):
    possible_moves = board.get_possible_moves(pieces.Piece.WHITE)
    move = user_move

    for possible_move in possible_moves:
        if move.equals(possible_move):
            # Perform the move on a temporary board
            temp_board = board.clone(board)
            temp_board.perform_move(move)
            
            # Check if the move leads to a check
            if not temp_board.is_check(pieces.Piece.WHITE):
                return move
            else:
                print("Invalid move: Lead to checkmate")
                return 1
    print("Invalid move: This move is not valid")
    return 1

def get_ai_illegal_moves(board):
    illegal_moves = []
    possible_moves = board.get_possible_moves(pieces.Piece.BLACK)
    for move in possible_moves:
        temp_board = board.clone(board)
        temp_board.perform_move(move)
        if temp_board.is_check(pieces.Piece.BLACK):
            illegal_moves.append(move)
    return illegal_moves
        
def main():
    chessboard = board.Board.new()
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("white"))
    p.display.set_caption("ChessMaster")
    loadImages()
    clock = p.time.Clock()
    running = True
    sqSelected = ()
    playerClicks = []
    current_player_color = pieces.Piece.WHITE
    highlight_square = None
    first = 0
    gameover = False
    while running and not gameover:
        for event in p.event.get():
            if first == 0:
                current_player_color = "B"
                first = 1
                break
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                if current_player_color != "B":
                    highlight_previous = None
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if highlight_square == (row, col):
                        highlight_square = None
                    else:
                        highlight_square = (row, col)
                    if sqSelected == (row,col): #user clicked the same square twice
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = Move(playerClicks[0][1], playerClicks[0][0], playerClicks[1][1], playerClicks[1][0])
                        move = get_valid_user_move(chessboard, move)
                        if move != 1:
                            chessboard.perform_move(move)
                            current_player_color = pieces.Piece.BLACK
                            highlight_previous = (playerClicks[0][0], playerClicks[0][1])
                            drawGameState(screen, chessboard, highlight_square, highlight_previous)
                            # Update màn hình
                            p.display.flip()
                            check_black= is_checkmate_or_stalemate(chessboard, "B")
                            check_white = is_checkmate_or_stalemate(chessboard, "W")
                            if(check_black):
                                if (chessboard.is_check(pieces.Piece.BLACK)):
                                    print("Checkmate. White wins.")
                                else:
                                    print("Stalemate for black")
                                gameover = True
                            if(check_white):
                                if not chessboard.is_check(pieces.Piece.WHITE):
                                    print("Stalemate for white")
                                gameover = True
                            sqSelected = ()
                            playerClicks = []
                        elif move == 1:
                            sqSelected = (playerClicks[1][0], playerClicks[1][1])
                            playerClicks = []
                            playerClicks.append(sqSelected)
                            
        if current_player_color == "B" and not gameover:
            start = time.time()
            print("AI Turn")
            invalid_moves_ai = get_ai_illegal_moves(chessboard)
            ai_move = ai.AI.get_ai_move(chessboard, invalid_moves_ai)
            end = time.time()
            print("AI has moved")
            excution = end - start
            print("Took AI", excution, "seconds to make a move")
            chessboard.perform_move(ai_move)
            highlight_previous = (ai_move.get_xfrom_yfrom()[1], ai_move.get_xfrom_yfrom()[0])
            highlight_square = (ai_move.get_xto_yto()[1], ai_move.get_xto_yto()[0])
            current_player_color = "W"
            drawGameState(screen, chessboard, highlight_square, highlight_previous)
            # Update màn hình
            p.display.flip()
            check_black= is_checkmate_or_stalemate(chessboard, "B")
            check_white = is_checkmate_or_stalemate(chessboard, "W")
            if(check_white):
                if (chessboard.is_check(pieces.Piece.BLACK)):
                    print("Checkmate. Black wins.")
                else:
                    print("Stalemate for white")
                gameover = True
            if(check_black):
                if not chessboard.is_check(pieces.Piece.WHITE):
                    print("Stalemate for black")
                gameover = True
            
        # 4. Vẽ bàn cờ và các quân cờ lên màn hình
        drawGameState(screen, chessboard, highlight_square, highlight_previous)
            # Update màn hình
        p.display.flip()
        clock.tick(MAX_FPS)

def drawGameState(screen, chessboard, highlight_square, highlight_previous):
    drawBoard(screen, highlight_square, highlight_previous)
    drawPieces(screen, chessboard)
    
def drawBoard(screen, highlight_square, highlight_previous):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if highlight_square != None and highlight_square == (row, col):
                p.draw.rect(screen, p.Color("yellow"), p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if highlight_previous != None and highlight_previous == (row, col):
                p.draw.rect(screen, p.Color("yellow"), p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, chessboard):
    for row in range(DIMENSION):  
        for col in range(DIMENSION):
            piece = chessboard.chesspieces[row][col]  # Đảo ngược col và row ở đây
            if piece != 0:
                image = IMAGES[piece.to_string().strip()]  
                # Vẽ hình ảnh lên màn hình ở vị trí (col, row) với kích thước SQ_SIZE x SQ_SIZE
                screen.blit(image, p.Rect(row * SQ_SIZE, col * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # Đảo ngược row và col ở đây
                    
                    


if __name__ == "__main__":
    main()
    