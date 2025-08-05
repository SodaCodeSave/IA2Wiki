import os
import yaml
import shutil

def load_yaml_file(file_path):
    """加载YAML文件并返回解析后的内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"加载文件 {file_path} 时出错: {e}")
        return None

def create_namespace_file(namespace):
    """创建命名空间Markdown文件"""
    filename = f"./wiki/{namespace}.md"
    # 确保wiki目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {namespace}\n\n")
    return filename

def process_recipe_pattern(recipe_data):
    """处理配方模式，将配方字符替换为实际物品"""
    if "pattern" not in recipe_data or "ingredients" not in recipe_data:
        return []
    
    pattern = recipe_data["pattern"].copy()  # 创建副本避免修改原始数据
    
    # 替换配方字符为实际物品
    for i in range(len(pattern)):
        # 创建一个新的行字符串
        new_line = ""
        for char in pattern[i]:
            if char in recipe_data["ingredients"]:
                # 将配方字符替换为实际物品
                new_line += f"{recipe_data['ingredients'][char]} "
            elif char == "X":
                # 将空位替换为O（空气）
                new_line += "O "
            else:
                # 保持其他字符（包括空格）
                new_line += f"{char} "
        # 去除末尾空格并保持格式
        pattern[i] = new_line.rstrip()
    
    return pattern

def write_recipe_to_file(file_handle, pattern, name):
    """将配方写入文件"""
    temp = 0
    file_handle.write('<div style="width:320px; height:160px; position: relative; margin-bottom: 10px;">')
    for pattern_line in pattern:
        items = pattern_line.split(" ")
        # 确保处理所有物品，而不仅仅是3个
        for i in range(len(items)):
            if items[i]:  # 如果物品不为空
                if items[i].split(":")[-1] != "O":
                    file_handle.write(f'<img src="./static/{items[i].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: {46 + 36 * i}px; top:{34 + 36 * temp}px" />\n')
        file_handle.write("\n")
        temp += 1
    file_handle.write(f'<img src="./static/{name.split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 234px; top: 70px" />\n')
    file_handle.write('<img src="./static/1.png"></div>\n\n')
        
def write_smithing_recipe_to_file(file_handle, repice):
    file_handle.write('<div style="width:320px; height:160px; position: relative; margin-bottom: 10px;">')
    file_handle.write(f'<img src="./static/{repice["base"].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 39px; top: 99px" />\n')
    file_handle.write(f'<img src="./static/{repice["addition"].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 137px; top: 99px" />\n')
    file_handle.write(f'<img src="./static/{repice["result"]["item"].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 253px; top: 99px" />\n')
    file_handle.write('<img src="./static/404.png"></div>\n\n')
    
def write_cooking_recipe_to_file(file_handle, repice):
    file_handle.write('<div style="width:320px; height:180px; position: relative; margin-bottom: 10px;">')
    file_handle.write(f'<img src="./static/{repice["ingredient"]["item"].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 96px; top: 46px" />\n')
    file_handle.write(f'<img src="./static/coal.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 96px; top: 118px" />\n')
    file_handle.write(f'<img src="./static/{repice["result"]["item"].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 215px; top: 82px" />\n')
    file_handle.write('<img src="./static/2.png"></div>\n\n')
    
def write_p_recipe_to_file(file_handle, repice):
    temp = 0
    line = -1
    file_handle.write('<div style="width:320px; height:160px; position: relative; margin-bottom: 10px;">')
    for i in repice["ingredients"]:
        if temp % 3 == 0:
            line += 1
        file_handle.write(f'<img src="./static/{repice["ingredients"][i].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: {46 + 36 * temp}px; top:{34 + 36 * line}px" />\n')
        temp += 1
    file_handle.write(f'<img src="./static/{repice["result"]["item"].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 234px; top: 70px" />\n')
    file_handle.write('<img src="./static/1.png"></div>\n\n')

def collect_item_ids_from_recipe(recipe_data, item_ids):
    """从配方数据中收集物品ID"""
    # 收集结果物品
    if "result" in recipe_data and "item" in recipe_data["result"]:
        item_ids.append(recipe_data["result"]["item"])
    
    # 收集合成材料
    if "ingredients" in recipe_data:
        for ingredient in recipe_data["ingredients"].values():
            if isinstance(ingredient, str):
                item_ids.append(ingredient)
    
    # 处理特定类型的配方
    if "base" in recipe_data:
        item_ids.append(recipe_data["base"])
    if "addition" in recipe_data:
        item_ids.append(recipe_data["addition"])
    if "ingredient" in recipe_data:
        if isinstance(recipe_data["ingredient"], dict) and "item" in recipe_data["ingredient"]:
            item_ids.append(recipe_data["ingredient"]["item"])
        elif isinstance(recipe_data["ingredient"], str):
            item_ids.append(recipe_data["ingredient"])

def process_item_recipes(config, namespace, item_key, file_handle, item_ids=None):
    """处理单个物品的配方"""
    full_item_name = f"{namespace}:{item_key}"
    
    if item_ids is not None:
        item_ids.append(full_item_name)
    
    repice_count = 0
    
    # 检查是否存在配方配置
    if "recipes" in config:
        if "crafting_table" in config["recipes"]:
            # 查找匹配的配方
            for recipe_data in config["recipes"]["crafting_table"].values():
                if recipe_data.get("result", {}).get("item") == full_item_name:
                    # 找到匹配配方，处理并写入
                    pattern = process_recipe_pattern(recipe_data)
                    if pattern:
                        repice_count += 1
                        write_recipe_to_file(file_handle, pattern, recipe_data.get("result", {}).get("item"))
                    else:
                        repice_count += 1
                        write_p_recipe_to_file(file_handle, recipe_data)
                    file_handle.write("\n\n")
                
                # 收集配方中的物品ID
                if item_ids is not None:
                    collect_item_ids_from_recipe(recipe_data, item_ids)
                    
        if "smithing" in config["recipes"]:
            # 查找匹配的配方
            for recipe_data in config["recipes"]["smithing"].values():
                if recipe_data.get("result", {}).get("item") == full_item_name:
                    repice_count += 1
                    write_smithing_recipe_to_file(file_handle, recipe_data)
                    file_handle.write("\n\n")
                
                # 收集配方中的物品ID
                if item_ids is not None:
                    collect_item_ids_from_recipe(recipe_data, item_ids)
                    
        if "cooking" in config["recipes"]:
            # 查找匹配的配方
            for recipe_data in config["recipes"]["cooking"].values():
                if recipe_data.get("result", {}).get("item") == full_item_name:
                    repice_count += 1
                    write_cooking_recipe_to_file(file_handle, recipe_data)
                    file_handle.write("\n\n")
                
                # 收集配方中的物品ID
                if item_ids is not None:
                    collect_item_ids_from_recipe(recipe_data, item_ids)
                    
    if repice_count <= 0:
        file_handle.write("暂无配方\n")

def process_yaml_file(file_path, all_item_ids=None):
    """处理单个YAML配置文件"""
    config = load_yaml_file(file_path)
    if not config or "info" not in config or "namespace" not in config["info"]:
        return []
    
    namespace = config["info"]["namespace"]
    namespace_file = create_namespace_file(namespace)
    
    local_item_ids = []
    local_item_names = []
    
    # 处理每个物品
    if "items" in config:
        for item_key in config["items"]:
            full_item_name = f"{namespace}:{item_key}"
            if full_item_name not in local_item_ids:
                local_item_ids.append(full_item_name)
            display_name = config["items"][item_key].get("display_name", item_key)
            if display_name not in local_item_names:
                local_item_names.append(display_name)
            if all_item_ids is not None and full_item_name not in all_item_ids:
                all_item_ids.append(full_item_name)
                
            item_display_name = config["items"][item_key].get("display_name", item_key)
            print(item_display_name)
            
            with open(namespace_file, "a", encoding="utf-8") as f:
                f.write(f"## {item_display_name}\n\n")
                try:
                    f.write(f"::: info\n食用后恢复饱食度{config["items"][item_key]["events"]["eat"]["feed"]["amount"]}点 饱和度{config["items"][item_key]["events"]["eat"]["feed"]["saturation"]}点\n:::\n")
                except:
                    pass
                try:
                    f.write(f"::: info\n食用后恢复饱食度{config["items"][item_key]["consumable"]["nutrition"]}点 饱和度{config["items"][item_key]["consumable"]["saturation"]}点\n:::\n")
                except:
                    pass
                try:
                    f.write(f"::: info\n饮用后恢复饱食度{config["items"][item_key]["events"]["drink"]["feed"]["amount"]}点 饱和度{config["items"][item_key]["events"]["drink"]["feed"]["saturation"]}点\n:::\n")
                except:
                    pass
                try:
                    f.write(f"::: info\n最大耐久{config["items"][item_key]["durability"]["max_custom_durability"]}\n:::\n")
                except:
                    pass
                try:
                    f.write(f"{config["items"][item_key]["lore"][0].replace("&7", "")}\n")
                except:
                    pass
                process_item_recipes(config, namespace, item_key, f, all_item_ids)
    
    return local_item_ids, local_item_names

def check_image_exists(image_name, static_dir="./wiki/static"):
    """检查图片是否存在"""
    image_path = os.path.join(static_dir, image_name + ".png")
    if image_name in ["1", "2", "404"]:  # 修改1: 直接比较名称部分
        os.makedirs(static_dir, exist_ok=True)
        # 复制static文件夹的图片到./wiki/static
        source_path = os.path.join("./static", image_name + ".png")
        target_path = os.path.join(static_dir, image_name + ".png")
        shutil.copy(source_path, target_path)  # 修改2: 正确的源和目标路径
        return True
    return os.path.exists(image_path)

def scan_yml_files(path):
    """扫描并处理contents目录中的所有YAML文件"""
    # 定义contents文件夹路径（相对于脚本所在目录）
    contents_dir = path
    static_dir = "./wiki/static"
    
    if not os.path.exists(contents_dir):
        print("contents文件夹不存在")
        return [], []
    
    # 必须存在的固定图片
    required_fixed_images = ["1", "2", "404", "coal"]
    missing_images = []
    
    # 检查固定图片是否存在
    for image_name in required_fixed_images:
        if not check_image_exists(image_name, static_dir):
            missing_image = f"{image_name}.png"
            if missing_image not in missing_images:
                missing_images.append(missing_image)
    
    all_item_ids = []
    all_item_names = []
    print("正在扫描contents文件夹中的yml文件...")
    for root, dirs, files in os.walk(contents_dir):
        for filename in files:
            if filename.endswith('.yml') or filename.endswith('.yaml'):
                file_path = os.path.join(root, filename)
                file_item_ids = process_yaml_file(file_path, all_item_ids)
                for item_id in file_item_ids[0]:
                    if item_id not in all_item_ids:
                        all_item_ids.append(item_id)
                for item_name in file_item_ids[1]:
                    if item_name not in all_item_names:
                        all_item_names.append(item_name)
    
    # 检查物品图片是否存在
    for item_id in all_item_ids:
        # 获取物品名称（去掉命名空间前缀）
        item_name = item_id.split(":")[-1]
        if not check_image_exists(item_name, static_dir):
            missing_image = f"{item_name}.png"
            if missing_image not in missing_images:
                missing_images.append(missing_image)
    
    return all_item_ids, missing_images, all_item_names