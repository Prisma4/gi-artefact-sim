import random, asyncio, PIL
from PIL import Image, ImageFont, ImageDraw

async def actual_substats(rarity_level):
    substat_start_amount = random.randint(rarity_level-2,rarity_level-1)
    actual_subs = {}
    for i in range(substat_start_amount):
        substat_name, substat = random.choice(list((await possible_substats()).items()))
        while substat_name in actual_subs.keys():
            substat_name, substat = random.choice(list((await possible_substats()).items()))
        actual_subs[f'{substat_name}']=substat
    return actual_subs

async def possible_substats():
    possible_substats = {}

    possible_substats['HP'] = random.choice([209, 239, 268, 298])
    possible_substats['Сила атаки'] = random.choice([13, 15, 17, 19])
    possible_substats['Защита'] = random.choice([16, 18, 20, 23])
    possible_substats['Мастерство стихий'] = random.choice([16, 18, 20, 23])

    possible_substats['_Защита'] = random.choice([5, 5.8, 6.5, 7.2])
    possible_substats['_Восст. энергии'] = random.choice([4.5, 5.1, 5.8, 6.4])
    possible_substats['_Сила атаки'] = random.choice([4, 4.6, 5.2, 5.8])
    possible_substats['_HP'] = random.choice([4, 4.6, 5.2, 5.8])
    possible_substats['_Шанс крит. попадания'] = random.choice([2.7, 3.1, 3.5, 3.9])
    possible_substats['_Крит. урон'] = random.choice([5.4, 6.2, 7, 7.8])
    return possible_substats

async def artefact_image(artefact_level, current_substats, user_id, aftefact_type):
    image = Image.open('artefactsim/pics/artefact_sample/flower_sample.png')
    gi_font = ImageFont.truetype("artefactsim/fonts/gi_font.ttf", 15)
    draw = ImageDraw.Draw(image)
    draw.text(
            (41,220),
            f'{artefact_level}',
            fill=('#ffffff'),
            font=gi_font
            )
    n = -1
    for substat_name, substat in current_substats.copy().items():
        n+=1
        if '_' in substat_name:
            substat_name = substat_name.replace('_', '')
            percent = "%"
        else:
            percent = ''

        draw.text(
                (30,256+(n*20)),
                f'\u00B7 {substat_name} +{substat}{percent}',
                fill=('#4a5466'),
                font=gi_font
                )
    if aftefact_type == 'flower':
        draw.text(
                (18,130),
                f'{717 + artefact_level*213}',
                fill=('#ffffff'),
                font=ImageFont.truetype("artefactsim/fonts/gi_font.ttf", 30)
                )

    image.save(f'artefactsim/pics/artefacts/{user_id}-artefact.png')

async def artefact_level_up_four(artefact_level, current_substats):
    if len(current_substats.keys()) <= 3:
        artefact_level += 4
        new_substat_name, new_substat = random.choice(list((await possible_substats()).items()))
        while new_substat_name in current_substats.keys():
            new_substat_name, new_substat = random.choice(list((await possible_substats()).items()))
        current_substats[f'{new_substat_name}']=new_substat
    elif len(current_substats.keys()) == 4:
        artefact_level += 4
        new_substat_name, new_substat = random.choice(list((await possible_substats()).items()))
        while new_substat_name not in current_substats.keys():
            new_substat_name, new_substat = random.choice(list((await possible_substats()).items()))
        current_substats[f'{new_substat_name}'] += new_substat
    current_substats[f'{new_substat_name}'] = round(current_substats[f'{new_substat_name}'], 1)
    return current_substats, artefact_level
