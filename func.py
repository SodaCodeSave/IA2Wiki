import os
import yaml

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
    filename = f"./{namespace}.md"
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
                    file_handle.write(f'<img src="../static/{items[i].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: {46 + 36 * i}px; top:{34 + 36 * temp}px" />\n')
        file_handle.write("\n")
        temp += 1
    file_handle.write(f'<img src="../static/{name.split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 234px; top: 70px" />\n')
    file_handle.write('<img src="../static/1.png"></div>\n\n')
        
def write_smithing_recipe_to_file(file_handle, repice):
    file_handle.write('<div style="width:320px; height:160px; position: relative; margin-bottom: 10px;">')
    file_handle.write(f'<img src="../static/{repice["base"].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 39px; top: 99px" />\n')
    file_handle.write(f'<img src="../static/{repice["addition"].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 137px; top: 99px" />\n')
    file_handle.write(f'<img src="../static/{repice["result"]["item"].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 253px; top: 99px" />\n')
    file_handle.write('<img src="../static/404.png"></div>\n\n')
    
def write_cooking_recipe_to_file(file_handle, repice):
    file_handle.write('<div style="width:320px; height:180px; position: relative; margin-bottom: 10px;">')
    file_handle.write(f'<img src="../static/{repice["ingredient"]["item"].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 96px; top: 46px" />\n')
    file_handle.write(f'<img src="../static/coal.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 96px; top: 118px" />\n')
    file_handle.write(f'<img src="../static/{repice["result"]["item"].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 215px; top: 82px" />\n')
    file_handle.write('<img src="../static/2.png"></div>\n\n')
    
def write_p_recipe_to_file(file_handle, repice):
    temp = 0
    line = -1
    file_handle.write('<div style="width:320px; height:160px; position: relative; margin-bottom: 10px;">')
    for i in repice["ingredients"]:
        if temp % 3 == 0:
            line += 1
        file_handle.write(f'<img src="../static/{repice["ingredients"][i].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: {46 + 36 * temp}px; top:{34 + 36 * line}px" />\n')
        temp += 1
    file_handle.write(f'<img src="../static/{repice["result"]["item"].split(":")[-1]}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: 234px; top: 70px" />\n')
    file_handle.write('<img src="../static/1.png"></div>\n\n')
def process_item_recipes(config, namespace, item_key, file_handle):
    """处理单个物品的配方"""
    full_item_name = f"{namespace}:{item_key}"
    
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
        if "smithing" in config["recipes"]:
            # 查找匹配的配方
            for recipe_data in config["recipes"]["smithing"].values():
                if recipe_data.get("result", {}).get("item") == full_item_name:
                    repice_count += 1
                    write_smithing_recipe_to_file(file_handle, recipe_data)
                    file_handle.write("\n\n")
        if "cooking" in config["recipes"]:
            # 查找匹配的配方
            for recipe_data in config["recipes"]["cooking"].values():
                if recipe_data.get("result", {}).get("item") == full_item_name:
                    repice_count += 1
                    write_cooking_recipe_to_file(file_handle, recipe_data)
                    file_handle.write("\n\n")
    if repice_count <= 0:
        file_handle.write("暂无配方\n")

def process_yaml_file(file_path):
    """处理单个YAML配置文件"""
    config = load_yaml_file(file_path)
    if not config or "info" not in config or "namespace" not in config["info"]:
        return
    
    namespace = config["info"]["namespace"]
    namespace_file = create_namespace_file(namespace)
    
    # 处理每个物品
    if "items" in config:
        for item_key in config["items"]:
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
                process_item_recipes(config, namespace, item_key, f)

def scan_yml_files():
    """扫描并处理contents目录中的所有YAML文件"""
    # 定义contents文件夹路径（相对于脚本所在目录）
    contents_dir = os.path.join(os.path.dirname(__file__), 'contents')
    
    if not os.path.exists(contents_dir):
        print("contents文件夹不存在")
        return
    
    print("正在扫描contents文件夹中的yml文件...")
    for root, dirs, files in os.walk(contents_dir):
        for filename in files:
            if filename.endswith('.yml') or filename.endswith('.yaml'):
                file_path = os.path.join(root, filename)
                process_yaml_file(file_path)

if __name__ == "__main__":
    scan_yml_files()