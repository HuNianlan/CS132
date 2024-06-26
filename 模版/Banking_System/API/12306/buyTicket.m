function orderID = buyTicket(int passengerID, int trainID, int depStationID, int arrStationID):
	% passenger can only buy one ticket per train, but can buy tickets of different trains without quantitative limitation.
  % we will setTime before call this function, so there no time parameter, just take system time
  % buying transfer ticket will call this function twice
  % return 0 when no ticket available 
  % return an arbitrary orderID, as long as no same ID even if refunding happens