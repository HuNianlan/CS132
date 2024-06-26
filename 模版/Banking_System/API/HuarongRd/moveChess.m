function [chessboard_done,is_valid,is_win]=moveChess(chessboard,obj,action)
% Move the chess
% Input:
% chessboard:(ceil) the customized situation.
%									e.g. chessboard={"曹操","曹操","张飞","赵云";
%																   "曹操","曹操","张飞","赵云";
%																   "关羽","关羽","马超","黄忠";
%																   "卒1","卒2","马超","黄忠";
%																   "卒3","卒4","",""}
% obj:(str) the Object that exists in the grid. e.g. "曹操"/"关羽"/"张飞"/"赵云"/"马超"/"黄忠"/"卒1"/"卒2"/"卒3"/"卒4"
% action:(int) 0:Up/1:Down/2:Left/3:Right									
% Output:
% chessboard_done:(struct) the Updated situation.
% is_valid:(bool) Whether the obj can be moved according to the action.
% is_win:(bool) Whether the game has been cleared.