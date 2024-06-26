function success = selectInsideButton(elevatorID, action)
% @brief: Press a button to a certain floor in a given elevator.
% @param elevatorID - int32: The id of the given elevator.
% @param action - int32 | string: The floor of the button to press, or 'open', 'close' the door.
% @return success - logical: True if success, False otherwise.
% @note: Index starts from 1, as it is in MATLAB's convention.
% @example: 
%  >> selectInsideButton(1, 'open')
%     logical
%      1