function success = inputInitialState(locations)
% @brief: Set the elevator to a given state.
% @param locations - cell{int32}: The location of each elevator.
% @return success - logical: True if success, False otherwise.
% @note: Index starts from 1, as it is in MATLAB's convention.
% @example: 
%  >> inputInitialState({1, 1})
%     logical
%      1
