DB_NAME = 'uomi'

TABLES = {}
TABLES['debt'] = (
    "CREATE TABLE `debt` ("
    "  `debt_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `date` date NOT NULL,"
    "  `name` varchar(30) NOT NULL,"
    "  `type` enum('cash','barter','other') NOT NULL,"
    "  `value` int(11) NULL,"
    "  `barter` varchar(128) NULL,"
    "  `other` varchar(128) NULL,"
    "  `pay_date` date NOT NULL,"
    "  PRIMARY KEY (`debt_no`)"
    ") ENGINE=MyISAM")

TABLES['credit'] = (
    "CREATE TABLE `credit` ("
    "  `credit_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `date` date NOT NULL,"
    "  `name` varchar(30) NOT NULL,"
    "  `type` enum('cash','barter','other') NOT NULL,"
    "  `value` int(11) NULL,"
    "  `barter` varchar(128) NULL,"
    "  `other` varchar(128) NULL,"
    "  `pay_date` date NOT NULL,"
    "  PRIMARY KEY (`credit_no`)"
    ") ENGINE=MyISAM")

