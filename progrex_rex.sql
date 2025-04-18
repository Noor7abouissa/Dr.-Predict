USE progrex_rex;
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 18, 2025 at 11:26 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `progrex_rex`
--

-- --------------------------------------------------------

--
-- Table structure for table `predictions`
--

CREATE TABLE `predictions` (
  `id` int(11) NOT NULL,
  `patient_name` varchar(100) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `chronic_disease` varchar(50) DEFAULT NULL,
  `smoker` varchar(5) DEFAULT NULL,
  `num_medications` int(11) DEFAULT NULL,
  `prev_admissions` int(11) DEFAULT NULL,
  `bmi` float DEFAULT NULL,
  `days_since_last` int(11) DEFAULT NULL,
  `predicted_risk` varchar(20) DEFAULT NULL,
  `predicted_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `predictions`
--

INSERT INTO `predictions` (`id`, `patient_name`, `age`, `gender`, `chronic_disease`, `smoker`, `num_medications`, `prev_admissions`, `bmi`, `days_since_last`, `predicted_risk`, `predicted_at`) VALUES
(1, 'Jackson', 25, 'Male', 'Heart Disease', 'Yes', 3, 1, 24, 17, 'Low', '2025-04-17 20:36:42'),
(2, 'tom', 34, 'Male', 'Diabetes', 'No', 3, 1, 20, 5, 'No', '2025-04-17 20:38:38'),
(3, 'Jackson', 23, 'Male', 'No Chronic Disease', 'Yes', 3, 2, 22, 4, 'No', '2025-04-17 20:40:12'),
(4, 'tom', 23, 'Male', 'Hypertension', 'No', 3, 3, 23, 5, 'No', '2025-04-17 20:40:40'),
(5, 'Jackson', 63, 'Female', 'Heart Disease', 'Yes', 5, 3, 35, 20, 'High', '2025-04-17 22:41:36'),
(6, 'Jackson', 63, 'Female', 'Heart Disease', 'Yes', 5, 3, 35, 20, 'High', '2025-04-17 22:42:02'),
(7, 'Jackson', 63, 'Female', 'Heart Disease', 'Yes', 5, 3, 35, 20, 'High', '2025-04-17 22:42:48'),
(8, 'Jackson', 67, 'Female', 'Heart Disease', 'Yes', 5, 3, 28, 20, 'High', '2025-04-17 22:48:54'),
(9, 'Nolan', 70, 'Female', 'Heart Disease', 'Yes', 9, 5, 28, 1, 'High', '2025-04-17 22:58:14'),
(10, 'ali', 78, 'Female', 'Heart Disease', 'Yes', 7, 5, 26, 7, 'High', '2025-04-18 05:46:03');

-- --------------------------------------------------------

--
-- Table structure for table `progrex_rex`
--

CREATE TABLE `progrex_rex` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `progrex_rex`
--

INSERT INTO `progrex_rex` (`id`, `name`, `email`, `password`, `created_at`) VALUES
(7, 'umar', 'umar@gmail.com', 'pbkdf2:sha256:1000000$CZQI2tBFQFosRYph$ca2ab153874cf50cd48f96b7557b929c55bac2d065675af8d714adad8d22a5bc', '2025-04-17 13:09:30');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `predictions`
--
ALTER TABLE `predictions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `progrex_rex`
--
ALTER TABLE `progrex_rex`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `predictions`
--
ALTER TABLE `predictions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `progrex_rex`
--
ALTER TABLE `progrex_rex`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
