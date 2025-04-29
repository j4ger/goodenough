import json

def extract_enemy_data(database_path, enemies_list_path, output_path):
    """
    从敌方数据库中提取参赛角色信息，并进行扁平化处理。
    增加了未匹配条目检测和特定条目保留。

    Args:
        database_path (str): enemy_database.json 文件的路径.
        enemies_list_path (str): enemies.txt 文件的路径.
        output_path (str): 输出 JSON 文件的路径.
    """

    # 1. 读取所有角色数据
    with open(database_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_enemies = data['enemies']
    enemy_name_to_data = {}
    for enemy_entry in all_enemies:
        enemy_key = enemy_entry['Key']
        enemy_data_list = enemy_entry['Value']
        for enemy_data_entry in enemy_data_list:
            enemy_data = enemy_data_entry['enemyData']
            enemy_name = enemy_data['name']['m_value']
            enemy_name_to_data[enemy_name] = enemy_data

    # 2. 读取参赛角色名称
    with open(enemies_list_path, 'r', encoding='utf-8') as f:
        participating_enemies = [line.strip() for line in f]

    # 3. 筛选并提取关键属性
    extracted_data = []
    unmatched_enemies = []
    for index, enemy_name in enumerate(participating_enemies):
        if enemy_name in enemy_name_to_data:
            enemy_data = enemy_name_to_data[enemy_name]
            attributes = enemy_data['attributes']

            # 提取关键属性，并添加存在性检查
            extracted_enemy = {
                'id': index,
                'name': enemy_name,
                'maxHp': attributes.get('maxHp', {}).get('m_value', None),
                'atk': attributes.get('atk', {}).get('m_value', None),
                'def': attributes.get('def', {}).get('m_value', None),
                'magicResistance': attributes.get('magicResistance', {}).get('m_value', None),
                'blockCnt': attributes.get('blockCnt', {}).get('m_value', None),
                'moveSpeed': attributes.get('moveSpeed', {}).get('m_value', None),
                'attackSpeed': attributes.get('attackSpeed', {}).get('m_value', None),
                'baseAttackTime': attributes.get('baseAttackTime', {}).get('m_value', None),
                'respawnTime': attributes.get('respawnTime', {}).get('m_value', None),
                'hpRecoveryPerSec': attributes.get('hpRecoveryPerSec', {}).get('m_value', None),
                'tauntLevel': attributes.get('tauntLevel', {}).get('m_value', None),
                'epDamageResistance': attributes.get('epDamageResistance', {}).get('m_value', None),
                'epResistance': attributes.get('epResistance', {}).get('m_value', None),
                'damageHitratePhysical': attributes.get('damageHitratePhysical', {}).get('m_value', None),
                'damageHitrateMagical': attributes.get('damageHitrateMagical', {}).get('m_value', None),
                'stunImmune': attributes.get('stunImmune', {}).get('m_value', None),
                'silenceImmune': attributes.get('silenceImmune', {}).get('m_value', None),
                'sleepImmune': attributes.get('sleepImmune', {}).get('m_value', None),
                'frozenImmune': attributes.get('frozenImmune', {}).get('m_value', None),
                'rangeRadius': enemy_data.get('rangeRadius', {}).get('m_value', None)
            }
            extracted_data.append(extracted_enemy)
        else:
            unmatched_enemies.append(enemy_name)

    # 4. 保存为 JSON 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=2)

    print(f"已提取 {len(extracted_data)} 个参赛角色信息，并保存到 {output_path}")

    # 5. 输出未匹配的条目
    if unmatched_enemies:
        print("以下角色在数据库中未找到：")
        for enemy_name in unmatched_enemies:
            print(f"- {enemy_name}")

# 使用示例
database_path = 'enemy_database.json'  # 替换为你的 enemy_database.json 文件路径
enemies_list_path = 'enemies.txt'  # 替换为你的 enemies.txt 文件路径
output_path = 'db.json'  # 输出文件路径

extract_enemy_data(database_path, enemies_list_path, output_path)
