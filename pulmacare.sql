-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 24, 2019 at 06:41 AM
-- Server version: 10.3.16-MariaDB
-- PHP Version: 7.3.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pulmacare`
--

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `d_id` int(11) NOT NULL,
  `h_id` int(11) NOT NULL DEFAULT 1,
  `u_id` int(11) NOT NULL,
  `total_stars` int(11) NOT NULL DEFAULT 40,
  `total_ratings` int(11) NOT NULL DEFAULT 8,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `doctors`
--

INSERT INTO `doctors` (`d_id`, `h_id`, `u_id`, `total_stars`, `total_ratings`, `timestamp`) VALUES
(1, 1, 27, 40, 8, '2019-11-10 07:17:22');

-- --------------------------------------------------------

--
-- Table structure for table `hospitals`
--

CREATE TABLE `hospitals` (
  `h_id` int(11) NOT NULL,
  `u_id` int(11) NOT NULL,
  `time_stamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `hospitals`
--

INSERT INTO `hospitals` (`h_id`, `u_id`, `time_stamp`) VALUES
(1, 26, '2019-11-10 07:10:01');

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `p_id` int(11) NOT NULL,
  `u_id` int(11) NOT NULL,
  `h_id` int(11) NOT NULL DEFAULT 1,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`p_id`, `u_id`, `h_id`, `timestamp`) VALUES
(3, 28, 1, '2019-11-10 07:23:43'),
(4, 29, 1, '2019-11-10 07:24:36'),
(5, 30, 1, '2019-11-10 07:27:58'),
(6, 31, 1, '2019-11-10 07:28:37'),
(7, 32, 1, '2019-11-10 07:29:24'),
(8, 33, 1, '2019-11-10 07:30:22');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `u_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` varchar(1) NOT NULL,
  `pic_url` varchar(50) NOT NULL,
  `location` text NOT NULL DEFAULT 'mg road',
  `time_stamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`u_id`, `name`, `email`, `password`, `role`, `pic_url`, `location`, `time_stamp`) VALUES
(26, 'Ramaiah Hospital', 'hos1@gmail.com', '5f4dcc3b5aa765d61d8327deb882cf99', '1', 'static/pro_pics/hospital.jpg', 'mg road', '2019-11-10 07:10:00'),
(27, 'VIjay Mallya', 'doc1@gmail.com', '5f4dcc3b5aa765d61d8327deb882cf99', '3', 'static/pro_pics/mallya.jpg', 'mg road', '2019-11-10 07:17:21'),
(28, 'Manish M', 'pat1@gmail.com', '5f4dcc3b5aa765d61d8327deb882cf99', '2', 'static/pro_pics/pat1.jpg', 'mg road', '2019-11-10 07:23:43'),
(29, 'Kaustubh DS', 'pat2@gmail.com', '5f4dcc3b5aa765d61d8327deb882cf99', '2', 'static/pro_pics/pat2.jpg', 'mg road', '2019-11-10 07:24:36'),
(30, 'Jayanth Vikram', 'pat3@gmail.com', '5f4dcc3b5aa765d61d8327deb882cf99', '2', 'static/pro_pics/pat3.jpg', 'mg road', '2019-11-10 07:27:58'),
(31, 'Keerthana', 'pat4@gmail.com', '5f4dcc3b5aa765d61d8327deb882cf99', '2', 'static/pro_pics/pat4.jpg', 'mg road', '2019-11-10 07:28:37'),
(32, 'Sai Sumanth', 'pat5@gmail.com', '5f4dcc3b5aa765d61d8327deb882cf99', '2', 'static/pro_pics/pat5.jpg', 'mg road', '2019-11-10 07:29:24'),
(33, 'Manoja U', 'pat6@gmail.com', '5f4dcc3b5aa765d61d8327deb882cf99', '2', 'static/pro_pics/pat6.jpg', 'mg road', '2019-11-10 07:30:22');

-- --------------------------------------------------------

--
-- Table structure for table `xrays`
--

CREATE TABLE `xrays` (
  `x_id` int(11) NOT NULL,
  `h_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `xray_url` varchar(50) NOT NULL,
  `predict` varchar(10) NOT NULL,
  `stage` varchar(10) NOT NULL,
  `time_stamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xrays`
--

INSERT INTO `xrays` (`x_id`, `h_id`, `p_id`, `xray_url`, `predict`, `stage`, `time_stamp`) VALUES
(7, 1, 3, 'static/xrays/demo1.jpeg', '0.9999993', '0', '2019-11-10 08:02:02'),
(8, 1, 4, 'static/xrays/demo2.jpeg', '1.49516e-9', '3', '2019-11-10 08:02:15'),
(9, 1, 5, 'static/xrays/demo3.jpeg', '0.9945253', '0', '2019-11-10 08:02:25'),
(10, 1, 6, 'static/xrays/demo4.jpeg', '1.0602e-7', '3', '2019-11-10 08:02:35'),
(11, 1, 7, 'static/xrays/demo5.jpeg', '0.9962212', '0', '2019-11-10 08:02:47'),
(12, 1, 8, 'static/xrays/demo6.jpeg', '3.8882e-10', '3', '2019-11-10 08:02:55'),
(13, 1, 3, 'static/xrays/person1_bacteria_2.jpeg', '0.00234741', '3', '2019-11-10 08:48:49'),
(14, 1, 7, 'static/xrays/person3_bacteria_13.jpeg', '0.03039671', '3', '2019-11-10 08:49:12'),
(16, 1, 4, 'static/xrays/person1946_bacteria_4874.jpeg', '1.24086e-7', '3', '2019-11-10 08:55:44'),
(17, 1, 4, 'static/xrays/person1946_bacteria_4874.jpeg', '1.24086e-7', '3', '2019-11-10 10:44:51');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`d_id`),
  ADD KEY `u_id` (`u_id`),
  ADD KEY `h_id` (`h_id`);

--
-- Indexes for table `hospitals`
--
ALTER TABLE `hospitals`
  ADD PRIMARY KEY (`h_id`),
  ADD KEY `u_id` (`u_id`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`p_id`),
  ADD KEY `u_id` (`u_id`),
  ADD KEY `h_id` (`h_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`u_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `xrays`
--
ALTER TABLE `xrays`
  ADD PRIMARY KEY (`x_id`),
  ADD KEY `p_id` (`p_id`),
  ADD KEY `h_id` (`h_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `d_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `hospitals`
--
ALTER TABLE `hospitals`
  MODIFY `h_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `p_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `u_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `xrays`
--
ALTER TABLE `xrays`
  MODIFY `x_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `doctors`
--
ALTER TABLE `doctors`
  ADD CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`u_id`) REFERENCES `users` (`u_id`),
  ADD CONSTRAINT `doctors_ibfk_2` FOREIGN KEY (`h_id`) REFERENCES `hospitals` (`h_id`);

--
-- Constraints for table `hospitals`
--
ALTER TABLE `hospitals`
  ADD CONSTRAINT `hospitals_ibfk_1` FOREIGN KEY (`u_id`) REFERENCES `users` (`u_id`);

--
-- Constraints for table `patients`
--
ALTER TABLE `patients`
  ADD CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`u_id`) REFERENCES `users` (`u_id`),
  ADD CONSTRAINT `patients_ibfk_2` FOREIGN KEY (`h_id`) REFERENCES `hospitals` (`h_id`);

--
-- Constraints for table `xrays`
--
ALTER TABLE `xrays`
  ADD CONSTRAINT `xrays_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `patients` (`p_id`),
  ADD CONSTRAINT `xrays_ibfk_2` FOREIGN KEY (`h_id`) REFERENCES `hospitals` (`h_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
