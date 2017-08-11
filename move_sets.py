import chess_input_parser

Morphy = [['e2', 'e4'], ['e7', 'e5'], ['f2', 'f4'], [('e5'), ('f4')], [('g1'), ('f3')],
		  [('g7'), ('g5')],[('h2'), ('h4')],[('g5'), ('g4')], [('f3'), ('e5')], [('g8'), ('f6')],
		  [('e5'), ('g4')], [('f6'), ('e4')], [('d2'), ('d3')], [('e4'), ('g3')], [('c1'), ('f4')],
		  [('g3'), ('h1')], [('d1'), ('e2')], [('d8'), ('e7')], [('g4'), ('f6')], ['e8', 'd8'],
		  [('f4'), ('c7')], [('d8'), ('c7')], [('f6'), ('d5')], [('c7'), ('d8')], ['d5', 'e7'],
		  [('f8'), ('e7')], [('e2'), ('g4')], [('d7'), ('d6')], [('g4'), ('f4')], ['h8', 'g8'],
		  [('f4'), ('f7')], [('e7'), ('h4')], [('e1'), ('d2')], [('g8'), ('e8')], ['b1', 'a3'],
		  [('b8'), ('a6')], [('f7'), ('h5')], [('h4'), ('f6')], [('h5'), ('h1')], ['f6', 'b2'],
		  [('h1'), ('h4')], [('d8'), ('d7')], [('a1'), ('b1')], [('b2'), ('a3')], ['h4', 'a4']]
alg_not = "1. e4 d6 2. d4 Nf6 3. Nc3 g6 4. Be3 Bg7 5. Qd2 c6 6. f3 b5 7. " \
		  "Nge2 Nbd7 8. Bh6 Bxh6 9. Qxh6 Bb7 10. a3 e5 11. O-O-O Qe7 12. Kb1 a6 " \
		  "13. Nc1 O-O-O 14. Nb3 exd4 15. Rxd4 c5 16. Rd1 Nb6"
game_2 = "1.c4 e5 2.g3 d6 3.Bg2 g6 4.d4 Nd7 5.Nc3 Bg7 6.Nf3 Ngf6 7.O-O " \
		 "O-O 8.Qc2 Re8 9.Rd1 c6 10.b3 Qe7 11.Ba3 e4 12.Ng5 e3 13.f4 Nf8 " \
		 "14.b4 Bf5 15.Qb3 h6 16.Nf3 Ng4 17.b5 g5 18.bxc6 bxc6 19.Ne5 " \
		 "gxf4 20.Nxc6 Qg5 21.Bxd6 Ng6 22.Nd5 Qh5 23.h4 Nxh4 24.gxh4 " \
		 "Qxh4 25.Nde7+ Kh8 26.Nxf5 Qh2+ 27.Kf1 Re6 28.Qb7 Rg6 29.Qxa8+ " \
		 "Kh7 30.Qg8+ Kxg8 31.Nce7+ Kh7 32.Nxg6 fxg6 33.Nxg7 Nf2 34.Bxf4 " \
		 "Qxf4 35.Ne6 Qh2 36.Rdb1 Nh3 37.Rb7+ Kh8 38.Rb8+ Qxb8 39.Bxh3 " \
		 "Qg3 0-1"
game_3 = "1.d4 Nf6 2.c4 e6 3.Nc3 Bb4 4.e3 d5 5.a3 Bxc3+ 6.bxc3 c5 7.cxd5 " \
		 "exd5 8.Bd3 O-O 9.Ne2 b6 10.O-O Ba6 11.Bxa6 Nxa6 12.Bb2 Qd7 " \
		 "13.a4 Rfe8 14.Qd3 c4 15.Qc2 Nb8 16.Rae1 Nc6 17.Ng3 Na5 18.f3 " \
		 "Nb3 19.e4 Qxa4 20.e5 Nd7 21.Qf2 g6 22.f4 f5 23.exf6 Nxf6 24.f5 " \
		 "Rxe1 25.Rxe1 Re8 26.Re6 Rxe6 27.fxe6 Kg7 28.Qf4 Qe8 29.Qe5 Qe7 " \
		 "30.Ba3 Qxa3 31.Nh5+ gxh5 32.Qg5+ Kf8 33.Qxf6+ Kg8 34.e7 Qc1+ " \
		 "35.Kf2 Qc2+ 36.Kg3 Qd3+ 37.Kh4 Qe4+ 38.Kxh5 Qe2+ 39.Kh4 Qe4+ " \
		 "40.g4 Qe1+ 41.Kh5"
Aronian = "1.d4 Nf6 2.c4 e6 3.Nf3 b6 4.g3 Ba6 5.b3 Bb4+ 6.Bd2 Be7 7.Bg2 " \
		  "c6 8.Bc3 d5 9.Ne5 Nfd7 10.Nxd7 Nxd7 11.Nd2 O-O 12.O-O Nf6 " \
		  "13.e4 b5 14.exd5 exd5 15.Re1 Rb8 16.c5 Bc8 17.Nf3 Ne4 18.Rxe4 " \
		  "dxe4 19.Ne5 Qd5 20.Qe1 Bf5 21.g4 Bg6 22.f3 b4 23.fxe4 Qe6 " \
		  "24.Bb2 Bf6 25.Nxc6 Qxc6 26.e5 Qa6 27.exf6 Rfe8 28.Qf1 Qe2 " \
		  "29.Qf2 Qxg4 30.h3 Qg5 31.Bc1 Qh5 32.Bf4 Rbd8 33.c6 Be4 34.c7 " \
		  "Rc8 35.Re1 Qg6 36.Rxe4 Rxe4 37.d5 Rce8 38.d6 Re1+ 39.Kh2 Qf5 " \
		  "40.Qg3 g6 41.Qg5 Qxg5 42.Bxg5 Rd1 43.Bc6 Re2+ 44.Kg3"
Mcdonal = "1.d4 d5 2.c4 dxc4 3.e4 e5 4.d5 f5 5.Nc3 Nf6 6.Bxc4 Bc5 7.Nf3 " \
		  "Qe7 8.Bg5 Bxf2+ 9.Kf1 Bb6 10.Qe2 f4 11.Rd1 Bg4 12.d6 cxd6 " \
		  "13.Nd5 Nxd5 14.Bxe7 Ne3+ 15.Ke1 Kxe7 16.Qd3 Rd8 17.Rd2 Nc6 " \
		  "18.b3 Ba5 19.a3 Rac8 20.Rg1 b5 21.Bxb5 Bxf3 22.gxf3 Nd4 23.Bc4 " \
		  "Nxf3+ 24.Kf2 Nxd2 25.Rxg7+ Kf6 26.Rf7+ Kg6 27.Rb7 Ndxc4 " \
		  "28.bxc4 Rxc4 29.Qb1 Bb6 30.Kf3 Rc3 31.Qa2 Nc4 32.Kg4 Rg8 " \
		  "33.Rxb6 axb6 34.Kh4 Kf6 35.Qe2 Rg6 36.Qh5 Ne3"
Nezhmet_Kismet = "1. d4 Nf6 2. c4 d6 3. Nc3 e5 4. e4 exd4 5. Qxd4 Nc6 6. Qd2 g6 " \
				 "7. b3 Bg7 8. Bb2 O-O 9. Bd3 Ng4 10. Nge2 Qh4 11. Ng3 Nge5 " \
				 "12. O-O f5 13. f3 Bh6 14. Qd1 f4 15. Nge2 g5 16. Nd5 g4 17. g3 " \
				 "fxg3 18. hxg3 Qh3 19. f4 Be6 20. Bc2 Rf7 21. Kf2 Qh2+ 22. Ke3 " \
				 "Bxd5 23. cxd5 Nb4 24. Rh1 Rxf4 25. Rxh2 Rf3+ 26. Kd4 Bg7 " \
				 "27. a4 c5+ 28. dxc6 bxc6 29. Bd3 Nexd3+ 30. Kc4 d5+ 31. exd5 " \
				 "cxd5+ 32. Kb5 Rb8+ 33. Ka5 Nc6+"
scholars_mate = [['e2', 'e4'], ['e7', 'e5'], ['f1', 'c4'], ['f8','c5'], ['d1','h5'], ['g8', 'f6'], ['h5','f7'],['e8','e7']]
black_check = [['e2', 'e3'], ['f7', 'f6'], ['b2', 'b4'], ['d7', 'd6'],  ['d1', 'h5'], ['g7', 'g6'], ['a2','a3'], ['a7', 'a5']]
blackburne_shilling_mate = "1. e4 e5 2. Nf3 Nc6 3. Bc4 Nd4 4. Nxe5 Qg5 5. Nxf7 Qxg2 6. Rf1 Qxe4+ 7. Be2 Nf3"
blackburne_shilling_mate = chess_input_parser.convert(blackburne_shilling_mate)
black_check = [['e2', 'e3'], ['f7', 'f6'],  ['d1', 'h5'], ['g7', 'g6'], ['a2','a3'], ['a7', 'a5']]
black_check2 = [['e2', 'e3'], ['f7', 'f6'], ['b2', 'b4'], ['d7', 'd6'],  ['d1', 'h5'], ['g7', 'g6'], ['a2','a3'], ['a7', 'a5']]
white_check = [['f2', 'f3'],['e7', 'e6'],['e1', 'f2'],['d8', 'h4'],['f2', 'e3']]
white_check_pawn = [['f2', 'f3'],['e7', 'e6'],['e1', 'f2'],['g7', 'g5'],['c2', 'c4'], ['g5', 'g4'], ['c4', 'c5'], ['g4', 'g3'], ['f2', 'e3']]
white_check_pawn_backedup = [['f2', 'f3'],['e7', 'e6'],['e1', 'f2'],['g7', 'g5'],['c2', 'c4'], ['g5', 'g4'], ['c4', 'c5'], ['d8', 'g5'],['c5', 'c6'],['g4', 'g3'], ['f2', 'e3']]
Aronian = chess_input_parser.convert(Aronian)