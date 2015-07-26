-- CREATE DATABASE testoption;

USE testoption;


CREATE TABLE `AAPL` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `AXP` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `BA` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `CAT` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `CSCO` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `CVX` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `DD` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `DIS` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `GE` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `GS` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `HD` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `IBM` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `INTC` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `JNJ` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `JPM` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `KO` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `MCD` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `MMM` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `MRK` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `MSFT` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `NKE` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `PFE` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `PG` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `TRV` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `UNH` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `UTX` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `V` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `VZ` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `WMT` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);

CREATE TABLE `XOM` (
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
  `IV` float NOT NULL,
  `underlying_price` float NOT NULL
);
