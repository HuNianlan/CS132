function trainNumberList = findAvaTransferTicket(int depStationID, int arrStationID)
	% return list of transfer train-pairs whose time and seat is available.
  % only when depStation and arrStation are on different lines do we need transfer.
  % return in order of departure time of first train (then second train)
  % For example, searching Huzhou-Jiaxing at 10:50 will return
  % trainNumberList = {222,215;222,217;223,218;224,217}   n × 2 cell array
  % if no available train-pair, return {} 0x0 empty cell array