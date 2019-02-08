main_statistics = [
    {
        'name': 'strength',
        'parent_name': None,
        'multiplier': 1.0,
    },
    {
        'name': 'agility',
        'parent_name': None,
        'multiplier': 1.0,
    },
    {
        'name': 'intelligence',
        'parent_name': None,
        'multiplier': 1.0,
    },
    {
        'name': 'vitality',
        'parent_name': None,
        'multiplier': 1.0,
    },
]

derivative_statistics = [
    {
        'name': 'physical_damage',
        'parent_name': 'strength',
        'multiplier': 2.0,
    },
    {
        'name': 'defense',
        'parent_name': 'strength',
        'multiplier': 1.5,
    },
    # TODO probably dodge and critic multipliers are too big
    {
        'name': 'dodge_chance',
        'parent_name': 'agility',
        'multiplier': 0.01, # 1%
    },
    {
        'name': 'critic_chance',
        'parent_name': 'agility',
        'multiplier': 0.005, # 0.5% (half of a percent)
    },
    {
        'name': 'magic_attack',
        'parent_name': 'intelligence',
        'multiplier': 2.0,
    },
    {
        'name': 'magic_resist',
        'parent_name': 'intelligence',
        'multiplier': 1.5,
    },
    {
        'name': 'health',
        'parent_name': 'vitality',
        'multiplier': 3,
    },
]