import chess
import random
import piece_square_tables as pst

board = chess.Board()

def piece_value(piece):
  if piece == None:
      return 0
  def absolute_value(piece):
    if piece.piece_type == chess.PAWN:
      return 100
    elif piece.piece_type == chess.KNIGHT:
      return 320
    elif piece.piece_type == chess.BISHOP:
      return 330
    elif piece.piece_type == chess.ROOK:
      return 500
    elif piece.piece_type == chess.QUEEN:
      return 900
    elif piece.piece_type == chess.KING:
      return 20000
  absolute_value = absolute_value(piece)
  return absolute_value if piece.color == True else -absolute_value
  
def evaluation(board):
  eval = 0
  for i in range(64):
    eval += piece_value(board.piece_at(i))
  return eval

def make_random_move(board):
  moves = list(board.legal_moves)
  random_move = random.choice(moves)
  board.push(random_move)

def calculate_best_move(board):
  moves = list(board.legal_moves)
  print(board.legal_moves)
  best_move = None
  best_value = -9999

  for move in moves:
    board.push(move)
    board_value = -evaluation(board)
    print(board_value)
    board.pop()
    if board_value > best_value:
      best_value = board_value
      best_move = move
  
  if best_move == None:
    return random.choice(moves)
  else:
    return best_move

alphabeta_position_count = 0
minimax_position_count = 0

def minimax(board, depth):
  global minimax_position_count
  minimax_position_count += 1

  if depth == 0:
    return -evaluation(board)
  
  moves = list(board.legal_moves)

  if board.turn == False: #black
    best_value = -9999
    for move in moves:
      board.push(move)
      best_value = max(best_value, minimax(board, depth - 1))
      board.pop()
    return best_value
  else: #white
    best_value = 9999
    for move in moves:
      board.push(move)
      best_value = min(best_value, minimax(board, depth - 1))
      board.pop()
    return best_value

def minimax_decision(board, depth):
  moves = list(board.legal_moves)
  best_move = None
  best_value = -9999

  for move in moves:
    #print("best", best_value, best_move)
    board.push(move)
    board_value = minimax(board, depth - 1)
    board.pop()
    #print("candidate", board_value, move)
    if board_value >= best_value:
      best_value = board_value
      best_move = move
  
  return best_move

def alpha_beta(board, depth, a, b):
  global alphabeta_position_count
  alphabeta_position_count += 1

  if depth == 0:
    return -evaluation(board)
  
  moves = list(board.legal_moves)

  if board.turn == False: #black
    best_value = -9999
    for move in moves:
      board.push(move)
      best_value = max(best_value, alpha_beta(board, depth - 1, a, b))
      board.pop()
      if best_value >= b:
        return best_value
      a = max(a, best_value)
    return best_value
  else: #white
    best_value = 9999
    for move in moves:
      board.push(move)
      best_value = min(best_value, alpha_beta(board, depth - 1, a, b))
      board.pop()
      if best_value <= a:
        return best_value
      b = min(b, best_value)
    return best_value

def alpha_beta_decision(board, depth):
  moves = list(board.legal_moves)
  best_move = None
  best_value = -9999

  for move in moves:
    #print(board.san(best_move), best_value)
    board.push(move)
    board_value = alpha_beta(board, depth - 1, -9999, 9999)
    board.pop()
    #print("candidate", board_value, move)
    if board_value >= best_value:
      best_value = board_value
      best_move = move
  
  return best_move


# board.set_fen("2r2b1k/2R2p2/5N1p/p1p2R2/P7/2P5/1P3PPP/2K5 b - - 0 30")
# #board.push_san("e4")
# print(board)
# # computer_move = minimax_decision(board, 2)
# # print("Minimax positions visited:", minimax_position_count)
# # print("Minimax best move", computer_move)
# computer_move2 = alpha_beta_decision(board, 3)
# print("Alpha-Beta positions visited:", alphabeta_position_count)
# print("Alpha-Beta best move", computer_move2)

def play():
  while not board.is_game_over():
    print(board)
    if(board.turn):
      print("Players turn")
      while True:
        try:
          move = input("Your move: ")
          board.push_san(move)
          break
        except ValueError:
          print("not correct san format")
    else:
      print("Computers turn")
      computer_move = alpha_beta_decision(board, 3)
      print("Computers move:", board.san(computer_move))
      board.push(computer_move)

# board.set_fen("r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3")
# move = alpha_beta_decision(board, 4)
# move2 = minimax_decision(board, 4)
# print(alphabeta_position_count)
# print(board.san(move))
# move2
# assert move == move2

play()