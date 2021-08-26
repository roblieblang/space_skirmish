class Settings:

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = 'black'

        self.ship_limit = 3

        self.laser_width = 3
        self.laser_height = 15
        self.laser_color = 'red'
        self.lasers_allowed = 3
        self.fleet_drop_speed = 6
        self.speedup_scale = 1.3
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.8
        self.laser_speed = 3
        self.enemy_speed = 1.6
        self.fleet_direction = 1
        self.enemy_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.laser_speed *= self.speedup_scale
        self.enemy_speed *= self.speedup_scale
        self.enemy_points = int(self.enemy_points * self.score_scale)
