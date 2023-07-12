"""Спасибо за ревью!"""

from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: int
    distance: float
    speed: float
    calories: float

    INFO_TRAINING = ('Тип тренировки: {training_type}; '
                     'Длительность: {duration:.3f} ч.; '
                     'Дистанция: {distance:.3f} км; '
                     'Ср. скорость: {speed:.3f} км/ч; '
                     'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """ Возврат сообщения """
        return self.INFO_TRAINING.format(**asdict(self))


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

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    """Константы для бега"""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        average_speed: float = self.get_mean_speed()
        return ((
            self.CALORIES_MEAN_SPEED_MULTIPLIER * average_speed
            + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weigth / self.M_IN_KM
            * (self.duration * self.HOURS_IN_MINUTE))


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
        return ((
            self.CALORIE_RATIO_1_WALK * self.weigth
            + (new_speed ** 2 / (self.height / self.CONSTANTA_HEIGHT_SM))
            * self.CALORIE_RATIO_2_WALK * self.weigth)
            * (self.duration * self.HOURS_IN_MINUTE))


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
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Формула рассчёта ккал"""
        average_speed: float = self.get_mean_speed()
        return ((
            average_speed + self.CALORIE_RATIO_1_SWIM)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weigth * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings = {'RUN': Running, 'SWM': Swimming, 'WLK': SportsWalking}
    try:
        if workout_type in trainings:
            return trainings[workout_type](*data)
    except KeyError:
        raise KeyError
    except ValueError:
        raise ValueError


"""Если честно не до конца понимаю,
что делаю. Почему нельзя передавать текст?
Потому что функция 'main' не принимает строку?"""


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
