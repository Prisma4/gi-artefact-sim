import random, asyncio, PIL
from PIL import Image, ImageFont, ImageDraw

async def actual_substats(main_stat):
    substat_start_amount = random.randint(3,4)
    actual_subs = {}
    for i in range(substat_start_amount):
        substat_name, substat = random.choice(list((await possible_substats()).items()))
        while substat_name in actual_subs.keys() or substat_name == main_stat:
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
    possible_substats['_Крит. урон'] = random.choice([5.4, 6.2, 7.1, 7.8])
    return possible_substats

async def artifact_image(artifact_level, current_substats, user_id, artifact_type, artefact_main_stat, start_stat):
    image = Image.open('artifactsim/pics/artifact_sample/universal_sample.png')
    artefact = Image.open(f'artifactsim/pics/artifacts/samples/{artifact_type}.png').resize((180, 180))
    draw = ImageDraw.Draw(image)
    gi_font = "artifactsim/fonts/gi_font.ttf"
    draw.text(
            (39,221),
            f'{artifact_level}',
            fill=('#ffffff'),
            font=ImageFont.truetype(gi_font, 15)
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
                (27,256+(n*25)),
                f'\u00B7 {substat_name} +{substat}{percent}',
                fill=('#4a5466'),
                font=ImageFont.truetype(gi_font, 17)
                )
    
    # лёгкие типы артефактов

    percent_main = ''
    if artifact_type == 'flower':
        artifact_name, artifact_sub_name, artifact_stat, start_stat, step = 'Ностальгия гладиатора', 'Цветок жизни', 'HP', 717, 203
    elif artifact_type == 'feather':
        artifact_name, artifact_sub_name, artifact_stat, start_stat, step = 'Судьба гладиатора', 'Перо смерти', 'Сила атаки', 47, 13
    else:
        step = ((start_stat * 6.7) - start_stat) / 20
        if '_' in artefact_main_stat:
            artefact_main_stat = artefact_main_stat.replace('_', '')
            percent_main = "%"

    # тяжёлые типы артефактов

    if artifact_type == 'clock':
        artifact_name, artifact_sub_name, artifact_stat, start_stat, step = 'Стремление гладиатора', 'Пески времени', artefact_main_stat, start_stat, step
    elif artifact_type == 'goblet':
        artifact_name, artifact_sub_name, artifact_stat, start_stat, step = 'Пьянство гладиатора', 'Кубок пространства', artefact_main_stat, start_stat, step
    elif artifact_type == 'crown':
        artifact_name, artifact_sub_name, artifact_stat, start_stat, step = 'Триумф гладиатора', 'Корона прозрения', artefact_main_stat, start_stat, step

    draw.text(
                (18,130),
                f'{round((start_stat + artifact_level*step), 1)}{percent_main}',
                fill=('#ffffff'),
                font=ImageFont.truetype(gi_font, 30)
                )
    image.paste(artefact, (180, 35), mask=artefact)
    draw.text(
            (22,8),
            artifact_name,
            fill=('#ffffff'),
            font=ImageFont.truetype(gi_font, 20)
            )
    draw.text(
            (22,50),
            artifact_sub_name,
            fill=('#ffffff'),
            font=ImageFont.truetype(gi_font, 15)
            )
    draw.text(
            (20,113),
            artifact_stat,
            fill=(255,255,255,64),
            font=ImageFont.truetype(gi_font, 15)
            )
    image.save(f'artifactsim/pics/artifacts/{user_id}-artifact.png')

async def artifact_level_up_four(artifact_level, current_substats, main_stat):
    if len(current_substats.keys()) <= 3:
        artifact_level += 4
        new_substat_name, new_substat = random.choice(list((await possible_substats()).items()))
        while new_substat_name in current_substats.keys() or new_substat_name == main_stat:
            new_substat_name, new_substat = random.choice(list((await possible_substats()).items()))
        current_substats[f'{new_substat_name}']=new_substat
    elif len(current_substats.keys()) == 4:
        artifact_level += 4
        new_substat_name, new_substat = random.choice(list((await possible_substats()).items()))
        while new_substat_name not in current_substats.keys():
            new_substat_name, new_substat = random.choice(list((await possible_substats()).items()))
        current_substats[f'{new_substat_name}'] += new_substat
    current_substats[f'{new_substat_name}'] = round(current_substats[f'{new_substat_name}'], 1)
    return current_substats, artifact_level

async def main_stat(artifact_type):
    possible_mainstat = {}
    possible_mainstat['_HP'] = 7
    possible_mainstat['_Сила атаки'] = 7
    possible_mainstat['_Защита'] = 8.3
    possible_mainstat['Мастерство стихий'] = 28
    if artifact_type == 'clock':
        possible_mainstat['_Восст. энергии'] = 7.8
    if artifact_type == 'goblet':
        element = random.choice(('пиро', 'анемо', 'крио', 'электро', 'дендро', 'гидро', 'гео'))
        possible_mainstat[f'_Бонус {element} урона'] = 7
        possible_mainstat['_Бонус физ. урона'] = 8.7
    if artifact_type == 'crown':
        possible_mainstat['_Крит. урон'] = 9.3
        possible_mainstat['_Крит. шанс'] = 4.7
        possible_mainstat['_Бонус лечения'] = 5.4
    selected_stat, start_stat = random.choice(list(possible_mainstat.items()))
    return selected_stat, start_stat