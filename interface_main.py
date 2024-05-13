import board, pieces, ai
from move import Move
import pygame as p



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
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
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
                        drawGameState(screen, chessboard)
                        # Update màn hình
                        p.display.flip()
                        check_black= is_checkmate_or_stalemate(chessboard, "B")
                        check_white = is_checkmate_or_stalemate(chessboard, "W")
                        if(check_black):
                            if (chessboard.is_check(pieces.Piece.BLACK)):
                                print("Checkmate. White wins.")
                                break
                            else:
                                print("Stalemate for black")
                                break
                        if(check_white):
                            if not chessboard.is_check(pieces.Piece.WHITE):
                                print("Stalemate for white")
                    sqSelected = ()
                    playerClicks = []
        if current_player_color == "B":
            print("AI Turn")
            invalid_moves_ai = get_ai_illegal_moves(chessboard)
            ai_move = ai.AI.get_ai_move(chessboard, invalid_moves_ai)
            chessboard.perform_move(ai_move)
            current_player_color = "W"
            drawGameState(screen, chessboard)
            # Update màn hình
            p.display.flip()
            check_black= is_checkmate_or_stalemate(chessboard, "B")
            check_white = is_checkmate_or_stalemate(chessboard, "W")
            if(check_white):
                if (chessboard.is_check(pieces.Piece.BLACK)):
                    print("Checkmate. Black wins.")
                    break
                else:
                    print("Stalemate for white")
                    break
            if(check_black):
                if not chessboard.is_check(pieces.Piece.WHITE):
                    print("Stalemate for black")

            
        # 4. Vẽ bàn cờ và các quân cờ lên màn hình
        drawGameState(screen, chessboard)
            # Update màn hình
        p.display.flip()
        clock.tick(MAX_FPS)

def drawGameState(screen, chessboard):
    drawBoard(screen)
    drawPieces(screen, chessboard)
    
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

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
    