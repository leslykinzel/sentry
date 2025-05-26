from dataclasses import dataclass


@dataclass
class DotaHero:
    id:               int
    name:             str
    primary_attr:     str
    attack_type:      str
    roles:            list[str]
    base_hp:          int
    base_hp_regen:    float
    base_mana:        int
    base_mana_regen:  float
    base_armor:       int
    base_mr:          int
    base_attack_min:  int
    base_attack_max:  int
    base_str:         int
    base_agi:         int
    base_int:         int
    str_gain:         float
    agi_gain:         float
    int_gain:         float
    attack_range:     int
    projectile_speed: int
    attack_rate:      float
    base_attack_time: float
    attack_point:     float
    move_speed:       int
    turn_rate:        float
    cm_enabled:       bool
    legs:             int
    day_vision:       int
    night_vision:     int
    localized_name:   str
