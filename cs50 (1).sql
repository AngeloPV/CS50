-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 11/08/2024 às 22:16
-- Versão do servidor: 10.4.28-MariaDB
-- Versão do PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `cs50`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `buy`
--

CREATE TABLE `buy` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `criptocurrencies_id` int(11) NOT NULL,
  `amount` float NOT NULL,
  `cost` float NOT NULL,
  `created` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `criptocurrencies`
--

CREATE TABLE `criptocurrencies` (
  `id` int(11) NOT NULL,
  `cripto_name` text NOT NULL,
  `actual_value` float NOT NULL,
  `range_value` text NOT NULL,
  `transaction_volume` text NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `deposit`
--

CREATE TABLE `deposit` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `value_deposited` float NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `email_data`
--

CREATE TABLE `email_data` (
  `id` int(11) NOT NULL,
  `type` varchar(30) NOT NULL,
  `content_html` text NOT NULL,
  `content_text` text NOT NULL,
  `subject` varchar(50) DEFAULT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `email_sit`
--

CREATE TABLE `email_sit` (
  `id` int(11) NOT NULL,
  `email_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `email_sit` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `notification`
--

CREATE TABLE `notification` (
  `id` int(11) NOT NULL,
  `type` text NOT NULL,
  `content` text NOT NULL,
  `subject` varchar(50) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `reg_trade`
--

CREATE TABLE `reg_trade` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `cripto_sender_id` int(11) NOT NULL,
  `cripto_recepient_id` int(11) NOT NULL,
  `trade_sit` int(11) NOT NULL,
  `amount_min` float NOT NULL,
  `amount_max` float NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `sell`
--

CREATE TABLE `sell` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `criptocurrencies_id` int(11) NOT NULL,
  `amount_cripto` float NOT NULL,
  `value_amount` float NOT NULL,
  `created` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `trades`
--

CREATE TABLE `trades` (
  `id` int(11) NOT NULL,
  `cripto_sender_id` int(11) NOT NULL,
  `cripto_recipient_id` int(11) NOT NULL,
  `user_sender_id` int(11) NOT NULL,
  `user_recipient_id` int(11) NOT NULL,
  `reg_trade_id` int(11) NOT NULL,
  `amount_sender` float NOT NULL,
  `amount_recipient` float NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `trade_sit`
--

CREATE TABLE `trade_sit` (
  `id` int(11) NOT NULL,
  `situation` int(11) NOT NULL,
  `created` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `user_btc`
--

CREATE TABLE `user_btc` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `amount` float DEFAULT NULL,
  `value` float DEFAULT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `user_cash`
--

CREATE TABLE `user_cash` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `cash` float DEFAULT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `user_data`
--

CREATE TABLE `user_data` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(220) NOT NULL,
  `cpf` varchar(14) NOT NULL,
  `phone` varchar(13) NOT NULL,
  `password` text NOT NULL,
  `pass_4_digit` varchar(4) DEFAULT NULL,
  `img_name` text DEFAULT NULL,
  `created` datetime DEFAULT current_timestamp(),
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `user_data`
--

INSERT INTO `user_data` (`id`, `name`, `email`, `cpf`, `phone`, `password`, `pass_4_digit`, `img_name`, `created`, `modified`) VALUES
(1, 'felipe', 'felipe', '000.000.000-00', '(54)999999999', 'asd123!', '2345', 'name.png', '2024-08-10 17:58:53', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- Estrutura para tabela `user_eth`
--

CREATE TABLE `user_eth` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `amount` float DEFAULT NULL,
  `value` float DEFAULT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `user_notfication`
--

CREATE TABLE `user_notfication` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `notification_id` int(11) NOT NULL,
  `sit_notfication` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `buy`
--
ALTER TABLE `buy`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `criptocurrencies_id` (`criptocurrencies_id`);

--
-- Índices de tabela `criptocurrencies`
--
ALTER TABLE `criptocurrencies`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `deposit`
--
ALTER TABLE `deposit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Índices de tabela `email_data`
--
ALTER TABLE `email_data`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `email_sit`
--
ALTER TABLE `email_sit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `email_id` (`email_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Índices de tabela `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `reg_trade`
--
ALTER TABLE `reg_trade`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `cripto_sender_id` (`cripto_sender_id`),
  ADD KEY `cripto_recepient_id` (`cripto_recepient_id`),
  ADD KEY `trade_sit` (`trade_sit`);

--
-- Índices de tabela `sell`
--
ALTER TABLE `sell`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `criptocurrencies_id` (`criptocurrencies_id`);

--
-- Índices de tabela `trades`
--
ALTER TABLE `trades`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cripto_recipient_id` (`cripto_recipient_id`),
  ADD KEY `user_sender_id` (`user_sender_id`),
  ADD KEY `user_recipient_id` (`user_recipient_id`),
  ADD KEY `reg_trade_id` (`reg_trade_id`);

--
-- Índices de tabela `trade_sit`
--
ALTER TABLE `trade_sit`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `user_btc`
--
ALTER TABLE `user_btc`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Índices de tabela `user_cash`
--
ALTER TABLE `user_cash`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Índices de tabela `user_data`
--
ALTER TABLE `user_data`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `user_eth`
--
ALTER TABLE `user_eth`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Índices de tabela `user_notfication`
--
ALTER TABLE `user_notfication`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `notification_id` (`notification_id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `buy`
--
ALTER TABLE `buy`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `criptocurrencies`
--
ALTER TABLE `criptocurrencies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `deposit`
--
ALTER TABLE `deposit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `email_data`
--
ALTER TABLE `email_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `email_sit`
--
ALTER TABLE `email_sit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `notification`
--
ALTER TABLE `notification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `reg_trade`
--
ALTER TABLE `reg_trade`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `sell`
--
ALTER TABLE `sell`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `trades`
--
ALTER TABLE `trades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `trade_sit`
--
ALTER TABLE `trade_sit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `user_btc`
--
ALTER TABLE `user_btc`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `user_cash`
--
ALTER TABLE `user_cash`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `user_data`
--
ALTER TABLE `user_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `user_eth`
--
ALTER TABLE `user_eth`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `user_notfication`
--
ALTER TABLE `user_notfication`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `buy`
--
ALTER TABLE `buy`
  ADD CONSTRAINT `buy_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`id`),
  ADD CONSTRAINT `buy_ibfk_2` FOREIGN KEY (`criptocurrencies_id`) REFERENCES `criptocurrencies` (`id`);

--
-- Restrições para tabelas `deposit`
--
ALTER TABLE `deposit`
  ADD CONSTRAINT `deposit_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`id`);

--
-- Restrições para tabelas `email_sit`
--
ALTER TABLE `email_sit`
  ADD CONSTRAINT `email_sit_ibfk_1` FOREIGN KEY (`email_id`) REFERENCES `email_data` (`id`),
  ADD CONSTRAINT `email_sit_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`id`);

--
-- Restrições para tabelas `reg_trade`
--
ALTER TABLE `reg_trade`
  ADD CONSTRAINT `reg_trade_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`id`),
  ADD CONSTRAINT `reg_trade_ibfk_2` FOREIGN KEY (`cripto_sender_id`) REFERENCES `criptocurrencies` (`id`),
  ADD CONSTRAINT `reg_trade_ibfk_3` FOREIGN KEY (`cripto_recepient_id`) REFERENCES `criptocurrencies` (`id`),
  ADD CONSTRAINT `reg_trade_ibfk_4` FOREIGN KEY (`trade_sit`) REFERENCES `trade_sit` (`id`);

--
-- Restrições para tabelas `sell`
--
ALTER TABLE `sell`
  ADD CONSTRAINT `sell_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`id`),
  ADD CONSTRAINT `sell_ibfk_2` FOREIGN KEY (`criptocurrencies_id`) REFERENCES `criptocurrencies` (`id`);

--
-- Restrições para tabelas `trades`
--
ALTER TABLE `trades`
  ADD CONSTRAINT `trades_ibfk_1` FOREIGN KEY (`cripto_recipient_id`) REFERENCES `criptocurrencies` (`id`),
  ADD CONSTRAINT `trades_ibfk_2` FOREIGN KEY (`user_sender_id`) REFERENCES `user_data` (`id`),
  ADD CONSTRAINT `trades_ibfk_3` FOREIGN KEY (`user_recipient_id`) REFERENCES `user_data` (`id`),
  ADD CONSTRAINT `trades_ibfk_4` FOREIGN KEY (`reg_trade_id`) REFERENCES `reg_trade` (`id`);

--
-- Restrições para tabelas `user_btc`
--
ALTER TABLE `user_btc`
  ADD CONSTRAINT `user_btc_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`id`);

--
-- Restrições para tabelas `user_cash`
--
ALTER TABLE `user_cash`
  ADD CONSTRAINT `user_cash_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`id`);

--
-- Restrições para tabelas `user_eth`
--
ALTER TABLE `user_eth`
  ADD CONSTRAINT `user_eth_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`id`);

--
-- Restrições para tabelas `user_notfication`
--
ALTER TABLE `user_notfication`
  ADD CONSTRAINT `user_notfication_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_data` (`id`),
  ADD CONSTRAINT `user_notfication_ibfk_2` FOREIGN KEY (`notification_id`) REFERENCES `notification` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
