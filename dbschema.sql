--
-- Database: `fileassessment`
--
CREATE DATABASE IF NOT EXISTS `fileassessment` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `fileassessment`;

-- --------------------------------------------------------

--
-- Table structure for table `filestatus`
--

CREATE TABLE `filestatus` (
  `id` int(10) UNSIGNED NOT NULL COMMENT 'unique id as per entry',
  `filename` varchar(100) NOT NULL COMMENT 'name of file',
  `status` enum('0','1') NOT NULL DEFAULT '0' COMMENT 'status 0 if not processed, stats 1 if processed'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Table created as a part of an assessment given';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `filestatus`
--
ALTER TABLE `filestatus`
  ADD PRIMARY KEY (`id`),
  ADD KEY `filename` (`filename`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `filestatus`
--
ALTER TABLE `filestatus`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'unique id as per entry';
