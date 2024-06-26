function paths = checkElevatorPaths()
% @brief: Check the history destinations of the elevators.
% @return paths - cell{cell{int32}}: lists of the destinations where the elevator had stopped in the order of 
% time. The first element of the tuple is the elevator id, and the second is the destination.
% @note: Index starts from 1, as it is in MATLAB's convention.
% @example: 
%  >> checkElevatorPaths()
%     1×2 cell 数组
%      {1×2 cell}    {1×2 cell}
%  >> % {{1, 2}, {2, 3}}