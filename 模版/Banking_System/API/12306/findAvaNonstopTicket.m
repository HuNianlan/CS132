function trainNumberList = findAvaNonstopTicket(int depStationID, int arrStationID)
	% return list of nonstop trains whose time and seat is available.
  % return in order of departure time
  % For example, searching Nanjing-Shanghai at 12:20 will return
  % trainNumberList = {114,218,116}   1 × n cell array
  % if no available train, return {} 0x0 empty cell array