class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
            self,
            training_type: str,
            duration: int,
            distance: float,
            speed: float,
            calories: float,) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """ Возврат сообщения """
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    """Константа для перевода из часы в минуты"""
    HOURS_IN_MINUTE: int = 60
    # Один шаг
    LEN_STEP: float = 0.65

    # константа для перевода значений из метров в километры.
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weigth = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    """Константы для бега"""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        new_fun: float = self.get_mean_speed()
        new_duration: float = ((
            self.CALORIES_MEAN_SPEED_MULTIPLIER * new_fun
            + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weigth / self.M_IN_KM
            * (self.duration * self.HOURS_IN_MINUTE))
        return new_duration


class SportsWalking(Training):
    """Константы для спортивной SportsWalking"""
    CALORIE_RATIO_1_WALK: float = 0.035
    CALORIE_RATIO_2_WALK: float = 0.029
    CONSTANTA = 0.278
    CONSTANTA_HEIGHT_SM = 100
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """ Функция рассчёта ккал """

        new_speed = self.get_mean_speed() * self.CONSTANTA
        calculate_kcal: float = ((
            self.CALORIE_RATIO_1_WALK * self.weigth
            + (new_speed ** 2 / (self.height / self.CONSTANTA_HEIGHT_SM))
            * self.CALORIE_RATIO_2_WALK * self.weigth)
            * (self.duration * self.HOURS_IN_MINUTE))
        return calculate_kcal


class Swimming(Training):
    """Тренировка: плавание."""
    """Константа для расчета"""
    CALORIE_RATIO_1_SWIM: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Формула рассчёта средней скорости при плавании"""
        average_swimming_speed: float = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)
        return average_swimming_speed

    def get_spent_calories(self) -> float:
        """Формула рассчёта ккал"""
        new_fun: float = self.get_mean_speed()
        calculate_kcal: float = ((
            new_fun + self.CALORIE_RATIO_1_SWIM)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weigth * self.duration)
        return calculate_kcal


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings = {'RUN': Running, 'SWM': Swimming, 'WLK': SportsWalking}
    return trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
