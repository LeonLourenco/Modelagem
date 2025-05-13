CREATE SCHEMA IF NOT EXISTS `US_ACCIDENTS` DEFAULT CHARACTER SET utf8;
USE `US_ACCIDENTS`;

-- -----------------------------------------------------
-- Table `US_ACCIDENTS`.`WEATHER_CONDITIONS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `US_ACCIDENTS`.`WEATHER_CONDITIONS` (
  `id` VARCHAR(128) NOT NULL,
  `Description` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id` (`id` ASC)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `US_ACCIDENTS`.`DAY_PERIODS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `US_ACCIDENTS`.`DAY_PERIODS` (
  `id` VARCHAR(128) NOT NULL,
  `Sunrise_Sunset` VARCHAR(10) NOT NULL,
  `Civil_Twilight` VARCHAR(10) NOT NULL,
  `Nautical_Twilight` VARCHAR(10) NOT NULL,
  `Astronomical_Twilight` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id` (`id` ASC)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `US_ACCIDENTS`.`WEATHER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `US_ACCIDENTS`.`WEATHER` (
  `id` VARCHAR(128) NOT NULL,
  `Weather_Timestamp` TIMESTAMP NOT NULL,
  `Temperature` FLOAT NOT NULL,
  `Humidity` FLOAT NOT NULL,
  `Pressure` FLOAT NOT NULL,
  `Visibility` FLOAT NOT NULL,
  `Wind_Direction` VARCHAR(10) NOT NULL,
  `Wind_Speed` FLOAT NOT NULL,
  `Precipitation` FLOAT NOT NULL,
  `Weather_Condition_ID` VARCHAR(128) NOT NULL,
  `Day_Period_ID` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id` (`id` ASC),
  CONSTRAINT `fk_WEATHER_WEATHER_CONDITIONS`
    FOREIGN KEY (`Weather_Condition_ID`)
    REFERENCES `US_ACCIDENTS`.`WEATHER_CONDITIONS` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_WEATHER_DAY_PERIODS`
    FOREIGN KEY (`Day_Period_ID`)
    REFERENCES `US_ACCIDENTS`.`DAY_PERIODS` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `US_ACCIDENTS`.`AIRPORTS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `US_ACCIDENTS`.`AIRPORTS` (
  `Airport_Code` VARCHAR(3) NOT NULL,
  `Name` VARCHAR(125) NOT NULL,
  `Timezone` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`Airport_Code`),
  UNIQUE INDEX `Airport_Code` (`Airport_Code` ASC)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `US_ACCIDENTS`.`LOCATIONS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `US_ACCIDENTS`.`LOCATIONS` (
  `id` VARCHAR(128) NOT NULL,
  `Street` VARCHAR(45) NOT NULL,
  `City` VARCHAR(45) NOT NULL,
  `County` VARCHAR(45) NOT NULL,
  `State` VARCHAR(2) NOT NULL,
  `Zipcode` VARCHAR(10) NOT NULL,
  `Country` VARCHAR(2) NOT NULL,
  `Airport_Code` VARCHAR(3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id` (`id` ASC),
  CONSTRAINT `fk_LOCATIONS_AIRPORTS`
    FOREIGN KEY (`Airport_Code`)
    REFERENCES `US_ACCIDENTS`.`AIRPORTS` (`Airport_Code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `US_ACCIDENTS`.`ROAD_FEATURES`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `US_ACCIDENTS`.`ROAD_FEATURES` (
  `id` VARCHAR(128) NOT NULL,
  `Avenue` TINYINT NOT NULL,
  `Bump` TINYINT NOT NULL,
  `Crossing` TINYINT NOT NULL,
  `Give_Way` TINYINT NOT NULL,
  `Junction` TINYINT NOT NULL,
  `No_Exit` TINYINT NOT NULL,
  `Railway` TINYINT NOT NULL,
  `Roundabout` TINYINT NOT NULL,
  `Station` TINYINT NOT NULL,
  `Stop` TINYINT NOT NULL,
  `Traffic_Calming` TINYINT NOT NULL,
  `Traffic_Signal` TINYINT NOT NULL,
  `Turning_Loop` TINYINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id` (`id` ASC)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `US_ACCIDENTS`.`ACCIDENTS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `US_ACCIDENTS`.`ACCIDENTS` (
  `id` VARCHAR(128) NOT NULL,
  `Severity` INT NOT NULL,
  `Start_Time` TIMESTAMP NOT NULL,
  `End_Time` TIMESTAMP NOT NULL,
  `Distance` FLOAT NOT NULL,
  `Description` VARCHAR(255) NOT NULL,
  `Year` YEAR(4) NOT NULL,
  `Weather_ID` VARCHAR(128) NOT NULL,
  `Location_ID` VARCHAR(128) NOT NULL,
  `Feature_ID` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_ACCIDENTS_WEATHER`
    FOREIGN KEY (`Weather_ID`)
    REFERENCES `US_ACCIDENTS`.`WEATHER` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ACCIDENTS_LOCATIONS`
    FOREIGN KEY (`Location_ID`)
    REFERENCES `US_ACCIDENTS`.`LOCATIONS` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ACCIDENTS_ROAD_FEATURES`
    FOREIGN KEY (`Feature_ID`)
    REFERENCES `US_ACCIDENTS`.`ROAD_FEATURES` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;
