function success = pressOutsideButton(floor, direction)
% @brief: Press a button at a certain floor.
% @param floor - int32: The floor of the button.
% @param direction - logical: Up if true, down otherwise.
% @return success - logical: True if success, False otherwise.
% @note: Index starts from 1, as it is in MATLAB's convention.
% @example: 
%  >> pressOutsideButton(1, false)
%     logical
%      0