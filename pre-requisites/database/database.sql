-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema gas_detection_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema gas_detection_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `gas_detection_db` DEFAULT CHARACTER SET utf8 ;
USE `gas_detection_db` ;

-- -----------------------------------------------------
-- Table `gas_detection_db`.`accounts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gas_detection_db`.`accounts` (
  `acc_id` INT NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `password` TEXT NOT NULL,
  `fname` VARCHAR(255) NULL,
  `lname` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `contact_num` VARCHAR(45) NULL,
  PRIMARY KEY (`acc_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gas_detection_db`.`devices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gas_detection_db`.`devices` (
  `device_id` INT NOT NULL,
  `room` VARCHAR(255) NOT NULL,
  `acc_id` INT NULL,
  `accounts_acc_id` INT NOT NULL,
  PRIMARY KEY (`device_id`),
  CONSTRAINT `fk_devices_accounts1`
    FOREIGN KEY (`accounts_acc_id`)
    REFERENCES `gas_detection_db`.`accounts` (`acc_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gas_detection_db`.`notifications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gas_detection_db`.`notifications` (
  `notif_id` INT NOT NULL,
  `device_id` INT NOT NULL,
  `room` VARCHAR(255) NULL,
  `gas` VARCHAR(255) NOT NULL,
  `reading` VARCHAR(255) NOT NULL,
  `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `devices_device_id` INT NOT NULL,
  `accounts_acc_id` INT NOT NULL,
  PRIMARY KEY (`notif_id`),
  CONSTRAINT `fk_notifications_devices`
    FOREIGN KEY (`devices_device_id`)
    REFERENCES `gas_detection_db`.`devices` (`device_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_notifications_accounts1`
    FOREIGN KEY (`accounts_acc_id`)
    REFERENCES `gas_detection_db`.`accounts` (`acc_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
