#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IA2Wiki - ItemsAdder Wiki Generator

This module contains functions to automatically identify ItemsAdder files and generate item documentation.
It processes YAML configuration files, extracts item information, and generates Markdown documentation with recipes.
"""

import os
import yaml
import shutil


def get_nested_value(data, keys, default=None):
    """Safely get nested value from dictionary"""
    for key in keys:
        if not isinstance(data, dict) or key not in data:
            return default
        data = data[key]
    return data


def load_yaml_file(file_path):
    """Load YAML file and return parsed content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        error_msg = f"Error loading {file_path}: {e}"
        print(error_msg)
        return None


def create_namespace_file(namespace):
    """Create namespace Markdown file"""
    filename = f"./wiki/{namespace}.md"
    # Ensure wiki directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {namespace}\n\n")
    return filename


def process_recipe_pattern(recipe_data):
    """Process recipe pattern, replace recipe characters with actual items"""
    if "pattern" not in recipe_data or "ingredients" not in recipe_data:
        return []
    
    ingredients = recipe_data["ingredients"]
    processed_pattern = []
    
    # Replace recipe characters with actual items
    for line in recipe_data["pattern"]:
        # Process each character in the line
        processed_line = " ".join(
            ingredients[char] if char in ingredients else 
            "O" if char == "X" else 
            char for char in line if char.strip()
        )
        processed_pattern.append(processed_line)
    
    return processed_pattern


def write_image_tag(file_handle, item_id, left, top):
    """Write image tag to file"""
    item_name = item_id.split(":")[-1]
    if item_name != "O":  # Skip air blocks
        file_handle.write(f'<img src="./static/{item_name}.png" style="height: 32px;image-rendering: pixelated;position: absolute; left: {left}px; top:{top}px" />\n')


def write_recipe_container(file_handle, width="320px", height="160px"):
    """Write recipe container div start tag"""
    file_handle.write(f'<div style="width:{width}; height:{height}; position: relative; margin-bottom: 10px;">')


def write_recipe_background(file_handle, background_image):
    """Write recipe background image and close container"""
    file_handle.write(f'<img src="./static/{background_image}.png"></div>\n\n')


def write_recipe_to_file(file_handle, pattern, name):
    """Write recipe to file"""
    temp = 0
    write_recipe_container(file_handle)
    for pattern_line in pattern:
        items = pattern_line.split(" ")
        # Ensure all items are processed, not just 3
        for i in range(len(items)):
            if items[i]:  # If item is not empty
                write_image_tag(file_handle, items[i], 46 + 36 * i, 34 + 36 * temp)
        temp += 1
    write_image_tag(file_handle, name, 234, 70)
    write_recipe_background(file_handle, "1")
        
def write_smithing_recipe_to_file(file_handle, recipe):
    """Write smithing recipe to file"""
    write_recipe_container(file_handle)
    write_image_tag(file_handle, recipe["base"], 39, 99)
    write_image_tag(file_handle, recipe["addition"], 137, 99)
    write_image_tag(file_handle, recipe["result"]["item"], 253, 99)
    write_recipe_background(file_handle, "404")
    
def write_cooking_recipe_to_file(file_handle, recipe):
    """Write cooking recipe to file"""
    write_recipe_container(file_handle, height="180px")
    write_image_tag(file_handle, recipe["ingredient"]["item"], 96, 46)
    write_image_tag(file_handle, "minecraft:coal", 96, 118)
    write_image_tag(file_handle, recipe["result"]["item"], 215, 82)
    write_recipe_background(file_handle, "2")
    
def write_p_recipe_to_file(file_handle, recipe):
    """Write shaped recipe to file"""
    temp = 0
    line = -1
    write_recipe_container(file_handle)
    for i in recipe["ingredients"]:
        if temp % 3 == 0:
            line += 1
        write_image_tag(file_handle, recipe["ingredients"][i], 46 + 36 * temp, 34 + 36 * line)
        temp += 1
    write_image_tag(file_handle, recipe["result"]["item"], 234, 70)
    write_recipe_background(file_handle, "1")


def collect_item_ids_from_recipe(recipe_data, item_ids):
    """Collect item IDs from recipe data"""
    # Collect result item
    if "result" in recipe_data and "item" in recipe_data["result"]:
        item_ids.add(recipe_data["result"]["item"])
    
    # Collect crafting materials
    if "ingredients" in recipe_data:
        for ingredient in recipe_data["ingredients"].values():
            if isinstance(ingredient, str):
                item_ids.add(ingredient)
    
    # Handle specific recipe types
    if "base" in recipe_data:
        item_ids.add(recipe_data["base"])
    if "addition" in recipe_data:
        item_ids.add(recipe_data["addition"])
    if "ingredient" in recipe_data:
        if isinstance(recipe_data["ingredient"], dict) and "item" in recipe_data["ingredient"]:
            item_ids.add(recipe_data["ingredient"]["item"])
        elif isinstance(recipe_data["ingredient"], str):
            item_ids.add(recipe_data["ingredient"])


def process_item_recipes(config, namespace, item_key, file_handle, item_ids=None):
    """Process recipes for a single item"""
    full_item_name = f"{namespace}:{item_key}"
    
    if item_ids is not None:
        item_ids.add(full_item_name)
    
    recipe_count = 0
    
    # Check if recipe configuration exists
    if "recipes" in config:
        if "crafting_table" in config["recipes"]:
            # Find matching recipes
            for recipe_data in config["recipes"]["crafting_table"].values():
                if recipe_data.get("result", {}).get("item") == full_item_name:
                    # Found matching recipe, process and write
                    pattern = process_recipe_pattern(recipe_data)
                    if pattern:
                        recipe_count += 1
                        write_recipe_to_file(file_handle, pattern, recipe_data.get("result", {}).get("item"))
                    else:
                        recipe_count += 1
                        write_p_recipe_to_file(file_handle, recipe_data)
                    file_handle.write("\n\n")
                
                # Collect item IDs from recipe
                if item_ids is not None:
                    collect_item_ids_from_recipe(recipe_data, item_ids)
                    
        if "smithing" in config["recipes"]:
            # Find matching recipes
            for recipe_data in config["recipes"]["smithing"].values():
                if recipe_data.get("result", {}).get("item") == full_item_name:
                    recipe_count += 1
                    write_smithing_recipe_to_file(file_handle, recipe_data)
                    file_handle.write("\n\n")
                
                # Collect item IDs from recipe
                if item_ids is not None:
                    collect_item_ids_from_recipe(recipe_data, item_ids)
                    
        if "cooking" in config["recipes"]:
            # Find matching recipes
            for recipe_data in config["recipes"]["cooking"].values():
                if recipe_data.get("result", {}).get("item") == full_item_name:
                    recipe_count += 1
                    write_cooking_recipe_to_file(file_handle, recipe_data)
                    file_handle.write("\n\n")
                
                # Collect item IDs from recipe
                if item_ids is not None:
                    collect_item_ids_from_recipe(recipe_data, item_ids)
                    
    if recipe_count <= 0:
        file_handle.write("No recipes available\n")


def process_yaml_file(file_path, all_item_ids=None):
    """Process a single YAML configuration file"""
    config = load_yaml_file(file_path)
    if not config or "info" not in config or "namespace" not in config["info"]:
        return set(), set()
    
    namespace = config["info"]["namespace"]
    namespace_file = create_namespace_file(namespace)
    
    local_item_ids = set()
    local_item_names = set()
    
    # Process each item
    if "items" in config:
        for item_key in config["items"]:
            item_config = config["items"][item_key]  # Cache item config
            full_item_name = f"{namespace}:{item_key}"
            local_item_ids.add(full_item_name)
            display_name = item_config.get("display_name", item_key)
            local_item_names.add(display_name)
            if all_item_ids is not None:
                all_item_ids.add(full_item_name)
                
            print(display_name)
            
            with open(namespace_file, "a", encoding="utf-8") as f:
                f.write(f"## {display_name}\n\n")
                
                # Check for eat events
                eat_amount = get_nested_value(item_config, ["events", "eat", "feed", "amount"])
                eat_saturation = get_nested_value(item_config, ["events", "eat", "feed", "saturation"])
                if eat_amount is not None and eat_saturation is not None:
                    f.write(f"::: info\nRestores {eat_amount} hunger points and {eat_saturation} saturation points when eaten\n:::\n")
                
                # Check for consumable nutrition
                nutrition = get_nested_value(item_config, ["consumable", "nutrition"])
                saturation = get_nested_value(item_config, ["consumable", "saturation"])
                if nutrition is not None and saturation is not None:
                    f.write(f"::: info\nRestores {nutrition} hunger points and {saturation} saturation points when eaten\n:::\n")
                
                # Check for drink events
                drink_amount = get_nested_value(item_config, ["events", "drink", "feed", "amount"])
                drink_saturation = get_nested_value(item_config, ["events", "drink", "feed", "saturation"])
                if drink_amount is not None and drink_saturation is not None:
                    f.write(f"::: info\nRestores {drink_amount} hunger points and {drink_saturation} saturation points when drunk\n:::\n")
                
                # Check for durability
                max_durability = get_nested_value(item_config, ["durability", "max_custom_durability"])
                if max_durability is not None:
                    f.write(f"::: info\nMax durability: {max_durability}\n:::\n")
                
                # Check for lore
                lore = get_nested_value(item_config, ["lore"])
                if isinstance(lore, list) and lore:
                    f.write(f"{lore[0].replace("&7", "")}\n")
                
                process_item_recipes(config, namespace, item_key, f, all_item_ids)
    
    return local_item_ids, local_item_names


def check_image_exists(image_name, static_dir="./wiki/static"):
    """Check if image exists"""
    image_path = os.path.join(static_dir, f"{image_name}.png")
    
    # Handle required fixed images
    if image_name in {"1", "2", "404"}:
        os.makedirs(static_dir, exist_ok=True)
        source_path = os.path.join("./static", f"{image_name}.png")
        
        if os.path.exists(source_path):
            try:
                # Only copy if target doesn't exist or is different
                if not os.path.exists(image_path) or not os.path.samefile(source_path, image_path):
                    shutil.copy2(source_path, image_path)  # Use copy2 to preserve metadata
                return True
            except Exception as e:
                print(f"Error copying {source_path} to {image_path}: {e}")
        else:
            print(f"Warning: Required image source not found - {source_path}")
    
    return os.path.exists(image_path)


def scan_yml_files(path):
    """Scan and process all YAML files in the contents directory"""
    # Define contents folder path (relative to script directory)
    contents_dir = path
    static_dir = "./wiki/static"
    
    if not os.path.exists(contents_dir):
        print("Contents folder does not exist")
        return set(), set(), set()
    
    # Required fixed images
    required_fixed_images = {"1", "2", "404", "coal"}
    missing_images = set()
    
    # Check if fixed images exist
    for image_name in required_fixed_images:
        if not check_image_exists(image_name, static_dir):
            missing_images.add(f"{image_name}.png")
    
    all_item_ids = set()
    all_item_names = set()
    print("Scanning YAML files in contents folder...")
    for root, dirs, files in os.walk(contents_dir):
        for filename in files:
            if filename.endswith('.yml') or filename.endswith('.yaml'):
                file_path = os.path.join(root, filename)
                file_item_ids, file_item_names = process_yaml_file(file_path, all_item_ids)
                all_item_ids.update(file_item_ids)
                all_item_names.update(file_item_names)
    
    # Check if item images exist
    for item_id in all_item_ids:
        # Get item name (remove namespace prefix)
        item_name = item_id.split(":")[-1]
        if not check_image_exists(item_name, static_dir):
            missing_images.add(f"{item_name}.png")
    
    return all_item_ids, missing_images, all_item_names
