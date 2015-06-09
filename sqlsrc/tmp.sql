CREATE TABLE `testoption1` (
  `underlying_symbol` varchar(10) NOT NULL,
  `option_symbol` varchar(50) NOT NULL,
  `strike` float NOT NULL,
  `expiry` date NOT NULL,
  `option_type` varchar(4) NOT NULL,
  `quote_date` date NOT NULL,
  `last` float NOT NULL,
  `bid` float NOT NULL,
  `ask` float NOT NULL,
  `vol` int(11) NOT NULL,
  `open_int` int(11) NOT NULL,
  `IV` varchar(50) NOT NULL,
  `underlying_price` float NOT NULL
);
