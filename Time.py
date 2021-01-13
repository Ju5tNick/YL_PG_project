import pygame


size = width, height = 1440, 960
screen = pygame.display.set_mode(size)


class Time:  # игровые сутки = 12 мин
    def __init__(self):
        self.hours = 0
        self.minutes = 0
        self.days_in_game = 0
        self.time_of_day = ""

    def calculate_time(self, miliseconds):
        # игровое время
        self.minutes = str(int(miliseconds / 500 % 60))
        self.hours = str(int(miliseconds / 30000 % 24))
        if len(self.hours) == 1:
            self.hours = "0" + self.hours
        if len(self.minutes) == 1:
            self.minutes = "0" + self.minutes

        # время суток
        night_hours = ["22", "23", "00", "01", "02", "03", "04", "05"]  # часы, которые считаются ночными
        if self.hours in night_hours:
            self.time_of_day = "Ночь"
        else:
            self.time_of_day = "День"

        # Дней в игре
        self.days_in_game = str(int(miliseconds // 720000))

    def get_time(self):
        return self.hours + ":" + self.minutes

    def get_time_of_day(self):
        return self.time_of_day

    def print_time(self):  # отрисовка времениd
        font = pygame.font.Font(None, 50)
        text_time = font.render(self.hours + ":" + self.minutes + ", " + self.time_of_day, True, (0, 0, 0))
        text_days_in_game = font.render("Дней в игре:" + " " + self.days_in_game, True, (0, 0, 0))
        screen.blit(text_time, (1100, 50))
        screen.blit(text_days_in_game, (1100, 0))

if __name__ == "__main__":
    game_time = Time()
    time = pygame.time.Clock()
    pygame.init()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        miliseconds = pygame.time.get_ticks() + 30000 * 6  # отсчет игрового времени начинается с 06:00
        game_time.calculate_time(miliseconds)
        game_time.print_time()
        pygame.display.flip()