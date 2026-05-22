"""One-off generator: writes product_images.py with per-product image URLs."""
from __future__ import annotations

# Wikimedia Commons 400px thumbnails (stable, product-relevant)
IMG = {
    "chia": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Chia_seeds.jpg/400px-Chia_seeds.jpg",
    "pumpkin_seed": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Pumpkin_seeds_closeup.jpg/400px-Pumpkin_seeds_closeup.jpg",
    "quinoa": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Quinoa.jpg/400px-Quinoa.jpg",
    "sunflower_seed": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Sunflower_seeds.jpg/400px-Sunflower_seeds.jpg",
    "flax_seed": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Flax_seeds.jpg/400px-Flax_seeds.jpg",
    "basil_seed": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Basil_seeds.jpg/400px-Basil_seeds.jpg",
    "watermelon_seed": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Watermelon_seeds.jpg/400px-Watermelon_seeds.jpg",
    "moringa_powder": "https://img.drz.lazcdn.com/static/np/p/8118f5d263b4ef4ae98ef9dc261d1b00.jpg_720x720q80.jpg",
    "moringa": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Moringa_oleifera_leaves.jpg/400px-Moringa_oleifera_leaves.jpg",
    "ashwagandha": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Ashwagandha_plant.jpg/400px-Ashwagandha_plant.jpg",
    "spirulina": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Spirulina_tablets.jpg/400px-Spirulina_tablets.jpg",
    "turmeric": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Turmeric_powder.jpg/400px-Turmeric_powder.jpg",
    "aloe": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Aloe_vera.jpg/400px-Aloe_vera.jpg",
    "black_seed": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Nigella_sativa_seeds.jpg/400px-Nigella_sativa_seeds.jpg",
    "coconut_oil": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Coconut_oil.jpg/400px-Coconut_oil.jpg",
    "lavender": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Lavandula_angustifolia_flowers.jpg/400px-Lavandula_angustifolia_flowers.jpg",
    "honey": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Honey_comb.jpg/400px-Honey_comb.jpg",
    "wild_honey": "https://sarafoods.co.in/wp-content/uploads/2023/07/01-HONEY-500-250-120-GM.jpg",
    "shilajit": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Shilajit.jpg/400px-Shilajit.jpg",
    "rose_water": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Rose_water.jpg/400px-Rose_water.jpg",
    "henna": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Henna_powder.jpg/400px-Henna_powder.jpg",
    "neem_soap": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Neem_soap.jpg/400px-Neem_soap.jpg",
    "rudraksha": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Rudraksha_beads.jpg/400px-Rudraksha_beads.jpg",
    "dragon_fruit": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Pitaya.jpg/400px-Pitaya.jpg",
    "almonds": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Badems.jpg/400px-Badems.jpg",
    "walnuts": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Walnuts.jpg/400px-Walnuts.jpg",
    "cashew": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Cashew_nuts.jpg/400px-Cashew_nuts.jpg",
    "pistachio": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Pistachio_nuts.jpg/400px-Pistachio_nuts.jpg",
    "raisins": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Raisins.jpg/400px-Raisins.jpg",
    "dates": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Dates.jpg/400px-Dates.jpg",
    "figs": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Dried_figs.jpg/400px-Dried_figs.jpg",
    "blueberries": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Blueberries.jpg/400px-Blueberries.jpg",
    "cranberries": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Cranberries.jpg/400px-Cranberries.jpg",
    "banana_dried": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Banana-Slice.jpg/400px-Banana-Slice.jpg",
    "papaya": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Papaya.jpg/400px-Papaya.jpg",
    "pineapple": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Pineapple.jpg/400px-Pineapple.jpg",
    "apple": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Red_Apple.jpg/400px-Red_Apple.jpg",
    "pear": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Pears.jpg/400px-Pears.jpg",
    "kiwi": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Kiwi_aka.jpg/400px-Kiwi_aka.jpg",
    "broccoli": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Broccoli_DSC00874.jpg/400px-Broccoli_DSC00874.jpg",
    "tomato": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Tomato_je.jpg/400px-Tomato_je.jpg",
    "potato": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Patates.jpg/400px-Patates.jpg",
    "carrot": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Carrots.jpg/400px-Carrots.jpg",
    "spinach": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Spinacia_oleracea_Spinach.jpg/400px-Spinacia_oleracea_Spinach.jpg",
    "cucumber": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Uncoiled_cucumber.jpg/400px-Uncoiled_cucumber.jpg",
    "cabbage": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Cabbage_in_market.jpg/400px-Cabbage_in_market.jpg",
    "cauliflower": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Cauliflower_head.jpg/400px-Cauliflower_head.jpg",
    "kale": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Kale-Bundle.jpg/400px-Kale-Bundle.jpg",
    "celery": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Celery_1.jpg/400px-Celery_1.jpg",
    "beetroot": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Beetroot_jm26647.jpg/400px-Beetroot_jm26647.jpg",
    "mushroom": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Mushrooms.jpg/400px-Mushrooms.jpg",
    "garlic": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Garlic.jpg/400px-Garlic.jpg",
    "onion": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Onion_on_white.jpg/400px-Onion_on_white.jpg",
    "peas": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Peas_in_pods.jpg/400px-Peas_in_pods.jpg",
    "corn": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Maize.jpg/400px-Maize.jpg",
    "squash": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Cucurbita_pepo_002.JPG/400px-Cucurbita_pepo_002.JPG",
    "bitter_gourd": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Bitter_gourd.jpg/400px-Bitter_gourd.jpg",
    "sweet_potato": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Sweet_potatoes.jpg/400px-Sweet_potatoes.jpg",
    "microgreens": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Microgreens.jpg/400px-Microgreens.jpg",
    "millet": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Foxtail_millet.jpg/400px-Foxtail_millet.jpg",
    "rice_brown": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Brown_rice.jpg/400px-Brown_rice.jpg",
    "rice_red": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Red_rice.jpg/400px-Red_rice.jpg",
    "rice_black": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Black_rice.jpg/400px-Black_rice.jpg",
    "pink_salt": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Himalayan_salt.jpg/400px-Himalayan_salt.jpg",
    "cinnamon": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Cinnamon_sticks.jpg/400px-Cinnamon_sticks.jpg",
    "ginseng": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Ginseng_roots.jpg/400px-Ginseng_roots.jpg",
    "cordyceps": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Cordyceps_sinensis.jpg/400px-Cordyceps_sinensis.jpg",
    "vinegar": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Apple_cider_vinegar.jpg/400px-Apple_cider_vinegar.jpg",
    "molasses": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Molasses.jpg/400px-Molasses.jpg",
    "jaggery": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Jaggery.jpg/400px-Jaggery.jpg",
    "sugar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Brown_sugar.jpg/400px-Brown_sugar.jpg",
    "protein": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Whey_protein_powder.jpg/400px-Whey_protein_powder.jpg",
    "mint": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Mint-leaves.jpg/400px-Mint-leaves.jpg",
    "tulsi": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Holy_basil_ocimum_tenuiflorum.jpg/400px-Holy_basil_ocimum_tenuiflorum.jpg",
    "neem": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Neem_leaves.jpg/400px-Neem_leaves.jpg",
    "hibiscus": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Hibiscus_rosa-sinensis_flower.jpg/400px-Hibiscus_rosa-sinensis_flower.jpg",
    "rose": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Rosa_rubiginosa_1.jpg/400px-Rosa_rubiginosa_1.jpg",
    "jasmine": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Jasminum_sambac.jpg/400px-Jasminum_sambac.jpg",
    "clove": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Cloves.jpg/400px-Cloves.jpg",
    "peppermint": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Mentha_piperita.jpg/400px-Mentha_piperita.jpg",
    "rosemary": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Rosmarinus_officinalis.jpg/400px-Rosmarinus_officinalis.jpg",
    "tea_tree": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Tea_tree_oil.jpg/400px-Tea_tree_oil.jpg",
    "mustard_oil": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Mustard_oil.jpg/400px-Mustard_oil.jpg",
    "castor": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Castor_oil.jpg/400px-Castor_oil.jpg",
    "sesame": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Sesame_seeds.jpg/400px-Sesame_seeds.jpg",
    "hemp": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Hemp_seeds.jpg/400px-Hemp_seeds.jpg",
    "fenugreek": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Fenugreek_seeds.jpg/400px-Fenugreek_seeds.jpg",
    "fennel": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Fennel_seeds.jpg/400px-Fennel_seeds.jpg",
    "grape_seed": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Grape_seed_oil.jpg/400px-Grape_seed_oil.jpg",
    "orange_peel": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Orange_peel.jpg/400px-Orange_peel.jpg",
    "lemongrass": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Lemongrass.jpg/400px-Lemongrass.jpg",
    "camphor": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Camphor.jpg/400px-Camphor.jpg",
    "herbal_powder": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Turmeric_powder.jpg/400px-Turmeric_powder.jpg",
    "herbal_tea": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Chamomile_tea.jpg/400px-Chamomile_tea.jpg",
    "amla": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Phyllanthus_emblica_fruits.jpg/400px-Phyllanthus_emblica_fruits.jpg",
    "soapnut": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Soapnuts.jpg/400px-Soapnuts.jpg",
    "indigo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Indigo_fera.jpg/400px-Indigo_fera.jpg",
    "multani": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Multani_mitti.jpg/400px-Multani_mitti.jpg",
    "sandalwood": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Sandalwood.jpg/400px-Sandalwood.jpg",
    "perfume": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Perfume_bottle.jpg/400px-Perfume_bottle.jpg",
    "gem": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Gemstones.jpg/400px-Gemstones.jpg",
    "crystal": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Quartz_crystal.jpg/400px-Quartz_crystal.jpg",
    "shivling": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Shiva_Lingam.jpg/400px-Shiva_Lingam.jpg",
    "idol": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Ganesha_idol.jpg/400px-Ganesha_idol.jpg",
    "coin": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Gold_coins.jpg/400px-Gold_coins.jpg",
    "guava": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Guava_fruit.jpg/400px-Guava_fruit.jpg",
    "mango": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Mangoes.jpg/400px-Mangoes.jpg",
    "lemon": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Lemon.jpg/400px-Lemon.jpg",
    "litchi": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Lychee.jpg/400px-Lychee.jpg",
    "custard_apple": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Custard_apple.jpg/400px-Custard_apple.jpg",
    "apple_ber": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Red_Apple.jpg/400px-Red_Apple.jpg",
    "insulin_plant": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Moringa_oleifera_leaves.jpg/400px-Moringa_oleifera_leaves.jpg",
    "mosquito": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Insect_repellent.jpg/400px-Insect_repellent.jpg",
    "massage_oil": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Coconut_oil.jpg/400px-Coconut_oil.jpg",
    "hair_oil": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Coconut_oil.jpg/400px-Coconut_oil.jpg",
    "barley": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Barley_grains.jpg/400px-Barley_grains.jpg",
    "buckwheat": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Buckwheat.jpg/400px-Buckwheat.jpg",
    "amaranth": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Amaranth_grain.jpg/400px-Amaranth_grain.jpg",
    "radish": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Radish.jpg/400px-Radish.jpg",
    "arugula": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Arugula.jpg/400px-Arugula.jpg",
    "thyme": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Thyme.jpg/400px-Thyme.jpg",
    "mustard_greens": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Mustard_plant.jpg/400px-Mustard_plant.jpg",
    "swiss_chard": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Chard.jpg/400px-Chard.jpg",
    "bell_pepper": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Green_Bell_Pepper.jpg/400px-Green_Bell_Pepper.jpg",
    "beans": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Green_beans.jpg/400px-Green_beans.jpg",
    "coconut_flakes": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Coconut_shreds.jpg/400px-Coconut_shreds.jpg",
    "noni": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Noni_fruit.jpg/400px-Noni_fruit.jpg",
    "giloy": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Tinospora_cordifolia.jpg/400px-Tinospora_cordifolia.jpg",
    "jamun": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Jamun_fruit.jpg/400px-Jamun_fruit.jpg",
    "isabgol": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Psyllium_husk.jpg/400px-Psyllium_husk.jpg",
    "maca": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Maca_root.jpg/400px-Maca_root.jpg",
    "licorice": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Liquorice_root.jpg/400px-Liquorice_root.jpg",
    "senna": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Senna_plant.jpg/400px-Senna_plant.jpg",
    "stevia": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Stevia_plant.jpg/400px-Stevia_plant.jpg",
    "asparagus": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Asparagus.jpg/400px-Asparagus.jpg",
    "vetiver": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Vetiver_grass.jpg/400px-Vetiver_grass.jpg",
    "oud": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Oud_perfume.jpg/400px-Oud_perfume.jpg",
    "musk": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Perfume_bottle.jpg/400px-Perfume_bottle.jpg",
}


def pick(name: str, cat: str, sub: str) -> str:
    n = name.lower()
    s = sub.lower()
    c = cat.lower()

    # ── Exact / high-priority combos ──
    if "wild honey" in n:
        return IMG["wild_honey"]
    if "moringa honey" in n or "jamun honey" in n:
        return IMG["wild_honey"]
    if "moringa powder" in n:
        return IMG["moringa_powder"]
    if name == "Chia" or name == "Chia seed":
        return IMG["chia"]
    if "shilajit" in n:
        return IMG["shilajit"]
    if "rudraksha" in n:
        return IMG["rudraksha"]
    if "dragon fruit" in n:
        return IMG["dragon_fruit"]

    # ── Subcategory-driven (short/ambiguous names) ──
    if s in ("seeds",) or "seed" in s and "oil" not in s:
        if "chia" in n:
            return IMG["chia"]
        if "pumpkin" in n:
            return IMG["pumpkin_seed"]
        if "quinoa" in n:
            return IMG["quinoa"]
        if "sunflower" in n:
            return IMG["sunflower_seed"]
        if "flax" in n:
            return IMG["flax_seed"]
        if "basil" in n:
            return IMG["basil_seed"]
        if "watermelon" in n:
            return IMG["watermelon_seed"]
        return IMG["chia"]

    if "mosquito" in s or n in ("spray", "cream", "oils") and "mosquito" in c:
        return IMG["mosquito"]

    if s in ("soaps",):
        return IMG["neem_soap"]
    if s in ("colours", "hair care", "hair colours"):
        if "henna" in n or "indigo" in n:
            return IMG["henna"] if "henna" in n else IMG["indigo"]
        if "shikakai" in n or "ritha" in n:
            return IMG["soapnut"]
        return IMG["henna"]
    if s in ("water",):
        if "rose" in n:
            return IMG["rose_water"]
        if "jasmine" in n:
            return IMG["jasmine"]
        if "neem" in n:
            return IMG["neem"]
        if "sandal" in n:
            return IMG["sandalwood"]
        if "vetiver" in n:
            return IMG["vetiver"]
        return IMG["rose_water"]
    if s in ("attars", "perfumes"):
        if "oud" in n:
            return IMG["oud"]
        if "musk" in n:
            return IMG["musk"]
        if "rose" in n:
            return IMG["rose"]
        if "jasmine" in n:
            return IMG["jasmine"]
        if "lavender" in n:
            return IMG["lavender"]
        return IMG["perfume"]
    if s in ("spirituals",):
        if "rudraksha" in n:
            return IMG["rudraksha"]
        if "sphatik" in n or "crystal" in n:
            return IMG["crystal"]
        if "gem" in n or "stone" in n:
            return IMG["gem"]
        if "shivalinga" in n or "shaligram" in n:
            return IMG["shivling"]
        if "coin" in n:
            return IMG["coin"]
        if "idol" in n:
            return IMG["idol"]
        return IMG["rudraksha"]

    # ── Dehydrated / dried ──
    if "dehydrated" in n or "dried" in n:
        if "cabbage" in n:
            return IMG["cabbage"]
        if "potato" in n:
            return IMG["potato"]
        if "kale" in n:
            return IMG["kale"]
        if "onion" in n:
            return IMG["onion"]
        if "carrot" in n:
            return IMG["carrot"]
        if "spinach" in n:
            return IMG["spinach"]
        if "tomato" in n:
            return IMG["tomato"]
        if "bean" in n:
            return IMG["beans"]
        if "bell pepper" in n or "pepper" in n:
            return IMG["bell_pepper"]
        if "celery" in n:
            return IMG["celery"]
        if "beet" in n:
            return IMG["beetroot"]
        if "bitter" in n:
            return IMG["bitter_gourd"]
        if "gourd" in n or "squash" in n:
            return IMG["squash"]
        if "pea" in n:
            return IMG["peas"]
        if "sweet potato" in n:
            return IMG["sweet_potato"]
        if "brussels" in n:
            return IMG["cabbage"]
        if "mushroom" in n:
            return IMG["mushroom"]
        if "corn" in n:
            return IMG["corn"]
        if "garlic" in n:
            return IMG["garlic"]
        if "blueberr" in n:
            return IMG["blueberries"]
        if "cranberr" in n:
            return IMG["cranberries"]
        if "banana" in n:
            return IMG["banana_dried"]
        if "papaya" in n:
            return IMG["papaya"]
        if "pineapple" in n:
            return IMG["pineapple"]
        if "apple" in n:
            return IMG["apple"]
        if "pear" in n:
            return IMG["pear"]
        if "kiwi" in n:
            return IMG["kiwi"]
        if "amala" in n or "rhita" in n or "shikakai" in n:
            return IMG["amla"] if "amala" in n else IMG["soapnut"]
        if "almond" in n:
            return IMG["almonds"]
        if "walnut" in n:
            return IMG["walnuts"]
        if "cashew" in n:
            return IMG["cashew"]
        if "pistachio" in n:
            return IMG["pistachio"]
        if "raisin" in n:
            return IMG["raisins"]
        if "fig" in n:
            return IMG["figs"]
        if "coconut" in n:
            return IMG["coconut_flakes"]
        if "date" in n:
            return IMG["dates"]
        return IMG["mushroom"]

    # ── Keyword rules (longest logic via order) ──
    rules = [
        ("moringa honey", "wild_honey"), ("jamun honey", "wild_honey"), ("wild honey", "wild_honey"),
        ("moringa powder", "moringa_powder"), ("moringa plant", "moringa"), ("moringa seed", "moringa"),
        ("moringa neem", "neem_soap"), ("moringa multani", "neem_soap"), ("moringa", "moringa"),
        ("ashwagandha", "ashwagandha"), ("spirulina", "spirulina"), ("turmeric", "turmeric"),
        ("black turmeric", "turmeric"), ("wild turmeric", "turmeric"),
        ("shilajit", "shilajit"), ("yarsagumba", "cordyceps"), ("ginseng", "ginseng"),
        ("honey", "honey"), ("pink salt", "pink_salt"), ("cinnamon", "cinnamon"),
        ("red rice", "rice_red"), ("brown rice", "rice_brown"), ("black rice", "rice_black"),
        ("chia seed", "chia"), ("chiaseed", "chia"), ("pumpkin seed", "pumpkin_seed"),
        ("quinoa", "quinoa"), ("sunflower seed", "sunflower_seed"), ("flax seed", "flax_seed"),
        ("flaxseed", "flax_seed"), ("basil seed", "basil_seed"), ("watermelon seed", "watermelon_seed"),
        ("black seed", "black_seed"), ("coconut oil", "coconut_oil"), ("coconut", "coconut_oil"),
        ("lavender oil", "lavender"), ("lavender", "lavender"),
        ("rose water", "rose_water"), ("rose oil", "rose"), ("rose", "rose"),
        ("henna", "henna"), ("indigo", "indigo"), ("shikakai", "soapnut"), ("ritha", "soapnut"),
        ("multani", "multani"), ("sandal", "sandalwood"), ("aloevera", "aloe"), ("aloe", "aloe"),
        ("aleovera", "aloe"), ("amala", "amla"), ("giloy", "giloy"), ("giloya", "giloy"),
        ("noni", "noni"), ("apple cider", "vinegar"), ("molasses", "molasses"),
        ("jaggery", "jaggery"), ("brown sugar", "sugar"), ("protein powder", "protein"),
        ("almond oil", "almonds"), ("almond", "almonds"), ("walnut", "walnuts"),
        ("castor", "castor"), ("sesame", "sesame"), ("hemp", "hemp"), ("fenugreek", "fenugreek"),
        ("fennel", "fennel"), ("mustard oil", "mustard_oil"), ("mustard", "mustard_greens"),
        ("grapeseed", "grape_seed"), ("orange peel", "orange_peel"),
        ("tea tree", "tea_tree"), ("peppermint", "peppermint"), ("rosemary", "rosemary"),
        ("clove", "clove"), ("lemongrass", "lemongrass"), ("camphor", "camphor"),
        ("jasmine", "jasmine"), ("jojoba", "coconut_oil"), ("hibiscus", "hibiscus"),
        ("mint", "mint"), ("tulsi", "tulsi"), ("neem", "neem"), ("brahmi", "herbal_powder"),
        ("triphala", "herbal_powder"), ("baheda", "herbal_powder"), ("harad", "herbal_powder"),
        ("licorice", "licorice"), ("senna", "senna"), ("stevia", "stevia"), ("isabgol", "isabgol"),
        ("maca", "maca"), ("milk thistle", "herbal_powder"), ("gymnema", "herbal_powder"),
        ("arjuna", "herbal_powder"), ("beet root", "beetroot"), ("mucuna", "herbal_powder"),
        ("broccoli", "broccoli"), ("radish", "radish"), ("kale", "kale"), ("spinach", "spinach"),
        ("carrot", "carrot"), ("tomato", "tomato"), ("potato", "potato"), ("cucumber", "cucumber"),
        ("cauliflower", "cauliflower"), ("cabbage", "cabbage"), ("celery", "celery"),
        ("beetroot", "beetroot"), ("arugula", "arugula"), ("thyme", "thyme"), ("flax", "flax_seed"),
        ("pea shoot", "peas"), ("microgreen", "microgreens"), ("sunflower", "sunflower_seed"),
        ("swiss chard", "swiss_chard"), ("bell pepper", "bell_pepper"), ("sweet potato", "sweet_potato"),
        ("yellow squash", "squash"), ("millet", "millet"), ("jowar", "millet"), ("barley", "barley"),
        ("buckwheat", "buckwheat"), ("amaranth", "amaranth"), ("foxtail", "millet"),
        ("finger millet", "millet"), ("kodo", "millet"), ("pearl millet", "millet"),
        ("barnyard", "millet"), ("little millet", "millet"), ("proso", "millet"),
        ("mushroom", "mushroom"), ("gucche", "mushroom"), ("red mushroom", "mushroom"),
        ("pain relief", "massage_oil"), ("body massage", "massage_oil"), ("hair growth", "hair_oil"),
        ("mosquito", "mosquito"), ("guava", "guava"), ("papaya", "papaya"), ("mango", "mango"),
        ("lemon", "lemon"), ("litchi", "litchi"), ("custard apple", "custard_apple"),
        ("apple ber", "apple_ber"), ("insulin plant", "insulin_plant"), ("dragon", "dragon_fruit"),
        ("rudraksha", "rudraksha"), ("sphatik", "crystal"), ("shivalinga", "shivling"),
        ("shaligram", "shivling"), ("gem", "gem"), ("stone", "gem"), ("coin", "coin"),
        ("idol", "idol"), ("religious", "idol"), ("vetiver", "vetiver"), ("kewada", "jasmine"),
        ("oud", "oud"), ("musk", "musk"), ("perfume", "perfume"), ("soap", "neem_soap"),
        ("spray", "mosquito"), ("cream", "mosquito"),
        ("gastric", "herbal_tea"), ("diabetes", "herbal_tea"), ("sugar control", "herbal_tea"),
        ("healthy drink", "herbal_tea"), ("good sleep", "herbal_tea"), ("jamun", "jamun"),
        ("asparagus", "asparagus"), ("pistachio", "pistachio"), ("raisin", "raisins"),
        ("fig", "figs"), ("date palm", "dates"), ("cashew", "cashew"),
        ("bhringraj", "herbal_powder"), ("punarnava", "herbal_powder"), ("chirayata", "herbal_powder"),
        ("shankhapushpi", "herbal_powder"), ("budhachitta", "rudraksha"),
    ]
    for kw, key in rules:
        if kw in n:
            return IMG[key]

    # ── Category fallbacks ──
    if "food" in c:
        return IMG["millet"]
    if "cosmetic" in c:
        return IMG["rose_water"]
    if "spiritual" in c:
        return IMG["rudraksha"]
    if "nursery" in c:
        return IMG["moringa"]
    return IMG["millet"]


def _clean_product_name(name: str) -> str:
    import html
    import re

    s = html.unescape(name or "")
    s = re.sub(r"&#\d+;", " ", s)
    return " ".join(s.split())


def _norm_product_name(name: str) -> str:
    import re

    return re.sub(r"[^a-z0-9]+", " ", _clean_product_name(name).lower()).strip()


# Catalog name -> saraworldwide.com.np product title (when titles differ)
CATALOG_WP_ALIASES = {
    "Aleovera gel": "Jasmin Aloe Vera Gel",
    "Aleovera powder": "ALOE VERA Powder",
    "Aloevera fresh juice": "Aloe Vera Fresh Juice",
    "Aloeveraamala fresh juice": "Fresh Amala & Aloe vera juice",
    "Amala fresh juice": "Amla Fresh Juice",
    "Apple cider vinegar": "APPLE CIDER VINEGAR",
    "Ashwagandha powder": "Ashwagandha Powder",
    "Bahedapowder": "Baheda Powder",
    "Black grapeseed oil": "Black Grape Seed Oil ( कालो अंगुर को तेल )",
    "Black Strap Molasses": "BLACKSTRAP MOLASSES",
    "Brahmi Powder": "BRAHMI POWDER",
    "Castorseed oil": "Castor Oil",
    "Chia seed": "Chia Seed",
    "Chiaseed oil": "Chia seed oil",
    "Clove oil": "Clove Oil",
    "Coconut oil": "Extra virgin coconut",
    "Fennelseed oil": "Fennel seed oil – सौफ को तेल",
    "Fenugreekseed oil": "Fenugreek seed oil – मेथी को तेल",
    "Flaxseed oil": "Flax Seed Oil ( आलस को तेल )",
    "Giloypowder": "Gilloy Powder",
    "Gucche Mushroom": "गुच्चे च्याउ",
    "GymnemaSylvestre powder": "Gymnema Sylvestre powder",
    "Hibiscus powder": "HIBISCUS FLOWER POWDER",
    "Jamun Seed powder": "Jamun Seed Powder",
    "Lavender oil": "Lavender Oil",
    "Maca powder": "American Maca Root",
    "Moringa powder": "Moringa Powder",
    "Mucuna powder": "Mucuna Powder",
    "Neemseed oil": "Neem Oil",
    "Orange peel oil": "Orange peel powder",
    "Protein powder": "Protein Powder",
    "Pumpkin seed oil": "Pumpkin Seed Oil",
    "Quinoa seed": "Qunioa",
    "Red Mushroom": "रातो च्याउ – Rato chyau",
    "Saw palmetto powder": "Saw Palmetto",
    "Sesameseed oil": "Sesame oil – 100ml ( तिल को तेल)",
    "Shilajit": "Pure Shilajit – शिलाजीत",
    "Spirulina powder": "Spirulina Powder",
    "Stevia powder": "Stevia Powder",
    "Triphalapowder": "Triphala Powder",
    "Wild Honey": "Himalaya Apiary",
    "Wild turmeric": "Wild Turmeric",
    "Neem Plant": "Neem Oil",
    "Moringa Plant": "Moringa Powder",
    "Asparagus": "Asparagus powder",
    "Insulin Plant": "Moringa Powder",
    "Sindur Plant": "Hibiscus powder",
    "Chirayata": "Triphala Powder",
    "Serpentine": "Moringa Powder",
    "Pumpkin seed": "Pumpkin Seed Oil",
    "Sunflower seed": "Sunflower Seed Kernels",
    "Flax seed": "Flax seed Roasted Powder",
    "Basil seed": "Basil Seeds",
    "Honey": "Himalaya Apiary",
    "Turmeric powder": "Wild Turmeric",
    "Mint": "Mint Dry Leaves",
    "Tulsi": "Tulsi Dry Leaves",
    "Rose water": "Rose Water",
    "Rose oil": "Rose Essential Oil",
    "Jasmine oil": "Jasmin Natural Oil",
    "Jasmine water": "Jasmine Water",
    "Neem water": "Neem Oil",
    "Pink Salt": "Pink Salt",
    "Cinnamon Stick": "Cinnamon Stick (Sri Lanka)",
    "Spirulina powder": "Spirulina Powder",
    "Milk thistle powder": "Milk Thistle Powder",
    "Isabgol": "Isabgol ( Psyllium Husk )",
    "Stevia powder": "Stevia Powder",
    "Licorice powder": "Licorice Powder",
    "Senna powder": "Senna Powder",
    "Beet root powder": "Beet Root Powder – ( चुकन्दर को जरा पाउडर )",
    "Orange peel powder": "Orange peel powder",
    "Henna powder": "Henna Powder",
    "Indigo powder": "Indigo Powder",
    "Sandal powder": "Sandal Powder",
    "Shikakai powder": "Harad Powder",
    "Ritha powder": "Harad Powder",
    "MultaniMutti powder": "Multani Mitti",
    "Tea Tree oil": "Tea Tree Oil",
    "Peppermint oil": "Lemon Grass Oil",
    "Lemon grass oil": "Lemon Grass Oil",
    "Clove oil": "Clove Oil",
    "Black seed oil": "Black Seed Oil",
    "Hemp seed oil": "HEMP SEED OIL",
    "Mustard oil": "Virgin Coconut Oil",
    "Almond oil": "Almond oil – बदाम को तेल",
    "Walnut oil": "Walnut oil",
    "Onion seed oil": "Onion Seed Oil",
    "Moringa seed oil": "Moringa Oil",
    "Jamun Honey": "Moringa Honey",
    "Moringa Honey": "Moringa Honey",
    "Yarsagumba": "Yarsagumba",
    "Shilajit": "Pure Shilajit – शिलाजीत",
    "Dried blueberries": "Dried Blue Berry",
    "Dried Cranberries": "Dried Cran Berry",
    "Dried Wild Garlic": "Wild Garlic ( जंगली लसुन )",
    "Dried Kasmiri Garlic": "Wild Garlic ( जंगली लसुन )",
    "Gucche Mushroom": "गुच्चे च्याउ",
    "Red Mushroom": "रातो च्याउ – Rato chyau",
    "Ginseng": "Korean Ginseng",
    "Noni fresh juice": "Noni fresh juice",
    "Giloy fresh juice": "Giloya Fresh Juice",
    "Aloeveraamala fresh juice": "Fresh Amala & Aloe vera juice",
    "Apple cider vinegar": "APPLE CIDER VINEGAR",
    "Black Strap Molasses": "BLACKSTRAP MOLASSES",
    "Jaggery powder": "Organic Jaggery Powder",
    "Protein powder": "Protein Powder",
    "Wild Honey": "Himalaya Apiary",
}


def fetch_saraworldwide_images():
    """Pull all product images from https://saraworldwide.com.np WooCommerce API."""
    import httpx

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }
    wp: dict[str, str] = {}
    all_entries: list[dict[str, str]] = []
    seen_urls: set[str] = set()

    with httpx.Client(headers=headers, timeout=30, follow_redirects=True) as client:
        for page in range(1, 20):
            r = client.get(
                "https://saraworldwide.com.np/wp-json/wc/store/products",
                params={"per_page": 100, "page": page},
            )
            if r.status_code != 200:
                break
            batch = r.json()
            if not batch:
                break
            for p in batch:
                name = _clean_product_name(p.get("name") or "")
                imgs = p.get("images") or []
                for idx, img in enumerate(imgs):
                    src = (img or {}).get("src")
                    if not src or "saraworldwide.com.np" not in src:
                        continue
                    if name and idx == 0:
                        wp.setdefault(name, src)
                    if src in seen_urls:
                        continue
                    seen_urls.add(src)
                    title = name if idx == 0 else f"{name} — photo {idx + 1}"
                    link = p.get("permalink") or "https://saraworldwide.com.np/"
                    all_entries.append(
                        {"title": title or "Product", "url": src, "link": link}
                    )

    fetch_saraworldwide_images.last_all = all_entries  # type: ignore[attr-defined]
    return wp


def match_wp_image(name: str, wp: dict) -> str | None:
    from difflib import SequenceMatcher

    alias = CATALOG_WP_ALIASES.get(name)
    if alias and alias in wp:
        return wp[alias]

    clean = _clean_product_name(name)
    if clean in wp:
        return wp[clean]

    n = _norm_product_name(clean)
    if len(n) < 2:
        return None

    wp_norm: dict[str, str] = {}
    for k, url in wp.items():
        nk = _norm_product_name(k)
        if len(nk) >= 2:
            wp_norm[nk] = url

    if n in wp_norm:
        return wp_norm[n]

    best_url = None
    best_score = 0.0
    tokens = set(n.split())

    for wk, url in wp_norm.items():
        ratio = SequenceMatcher(None, n, wk).ratio()
        if ratio >= 0.92 and ratio > best_score:
            best_score = ratio
            best_url = url
            continue

        w_tokens = set(wk.split())
        overlap = tokens & w_tokens
        if not overlap:
            continue
        if not any(len(t) >= 3 for t in overlap):
            continue

        overlap_ratio = len(overlap) / max(len(tokens), len(w_tokens))
        if overlap_ratio < 0.55:
            continue
        if len(overlap) < min(2, len(tokens)):
            continue

        score = ratio * 0.45 + overlap_ratio * 0.55
        if score > best_score:
            best_score = score
            best_url = url

    if best_score >= 0.62:
        return best_url
    return None


def best_fuzzy_wp_match(name: str, wp: dict) -> str | None:
    """Pick closest saraworldwide.com.np product title by similarity."""
    from difflib import SequenceMatcher

    n = _norm_product_name(name)
    if len(n) < 2:
        return None

    tokens = set(n.split())
    best_url = None
    best_score = 0.0

    for title, url in wp.items():
        wk = _norm_product_name(title)
        if len(wk) < 2:
            continue

        ratio = SequenceMatcher(None, n, wk).ratio()
        w_tokens = set(wk.split())
        overlap = tokens & w_tokens
        overlap_score = (len(overlap) / max(len(tokens), 1)) if tokens else 0.0
        if n in wk or wk in n:
            ratio = max(ratio, 0.85)

        score = max(ratio, overlap_score * 0.92)
        if score > best_score:
            best_score = score
            best_url = url

    min_score = 0.38 if len(tokens) <= 1 else 0.48
    return best_url if best_score >= min_score else None


_MATCH_STOP_WORDS = frozenset(
    {
        "dehydrated",
        "dried",
        "organic",
        "natural",
        "fresh",
        "whole",
        "plant",
        "plants",
        "powder",
        "seed",
        "seeds",
        "oil",
        "juice",
        "gel",
        "water",
        "tea",
        "soap",
        "cream",
        "spray",
        "flakes",
        "care",
        "relief",
        "growth",
        "repellent",
        "massage",
        "extra",
        "virgin",
        "wild",
        "red",
        "green",
        "black",
        "brown",
        "pink",
        "little",
        "naked",
        "pear",
        "proso",
        "finger",
        "foxtail",
        "barnyard",
    }
)


def keyword_wp_match(name: str, wp: dict) -> str | None:
    """Match catalog name tokens to saraworldwide product titles."""
    tokens = [
        t
        for t in _norm_product_name(name).split()
        if len(t) >= 3 and t not in _MATCH_STOP_WORDS
    ]
    if not tokens:
        return None

    best_url = None
    best_score = 0.0
    for title, url in wp.items():
        wk = _norm_product_name(title)
        if len(wk) < 2:
            continue
        hits = sum(1 for t in tokens if t in wk)
        if not hits:
            continue
        score = hits / len(tokens)
        if score > best_score:
            best_score = score
            best_url = url

    return best_url if best_score >= 0.34 else None


# Subcategory -> preferred saraworldwide product (must exist on live store)
SUBCATEGORY_SARA_HINTS = {
    "Seeds": "Chia Seed",
    "Powder": "Moringa Powder",
    "Oil": "Black Seed Oil",
    "Essential Oil": "Lavender Oil",
    "Medicinal Herbs": "Holy Basil",
    "Himali Products": "Himalaya Apiary",
    "Juices & Detox Water": "Aloe Vera Fresh Juice",
    "Microgreens": "Wheat Grass Powder",
    "Dehydrated Fruits & Vegs": "Dried Blue Berry",
    "Millets & More": "Qunioa",
    "Oils": "Neem Oil",
    "Soaps": "Aloe Vera Gel",
    "Colours": "Henna Powder",
    "Hair Care": "Onion Seed Oil",
    "Water": "Rose Water",
    "Attars": "Rose Essential Oil",
    "Perfumes": "Jasmin Natural Oil",
    "Spirituals": "Yarsagumba",
    "Herbal and Medicinal Pants": "Neem Oil",
    "Fruit Plants": "Wild Garlic ( जंगली लसुन )",
}


def load_facebook_images() -> dict[str, str]:
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parent / "sara_fb_images.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    try:
        from fetch_facebook_images import fetch_facebook_product_images

        data = fetch_facebook_product_images()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return data
    except Exception:
        return {}


def match_fb_image(name: str, fb: dict) -> str | None:
    if not fb:
        return None
    alias = CATALOG_WP_ALIASES.get(name) or name
    if alias in fb:
        return fb[alias]
    clean = _clean_product_name(alias)
    if clean in fb:
        return fb[clean]

    tokens = [
        t
        for t in _norm_product_name(name).split()
        if len(t) >= 3 and t not in _MATCH_STOP_WORDS
    ]
    if not tokens:
        return None

    best_url = None
    best_score = 0.0
    for title, url in fb.items():
        wk = _norm_product_name(title)
        if len(wk) < 2:
            continue
        hits = sum(1 for t in tokens if t in wk)
        if not hits:
            continue
        score = hits / len(tokens)
        if score > best_score:
            best_score = score
            best_url = url
    return best_url if best_score >= 0.5 else None


def _build_subcategory_pools(wp: dict) -> dict[str, list[str]]:
    """Group saraworldwide product titles into subcategory pools (unique images)."""
    pools: dict[str, list[str]] = {sub: [] for sub in SUBCATEGORY_SARA_HINTS}
    for title in wp:
        nt = _norm_product_name(title)
        for sub, hint in SUBCATEGORY_SARA_HINTS.items():
            hint_n = _norm_product_name(hint)
            if hint_n in nt or any(t in nt for t in hint_n.split() if len(t) >= 4):
                pools[sub].append(title)
    for sub, titles in pools.items():
        if not titles and sub in SUBCATEGORY_SARA_HINTS:
            hint = SUBCATEGORY_SARA_HINTS[sub]
            if hint in wp:
                pools[sub] = [hint]
    return pools


def _choose_least_used(
    candidates: list[tuple[float, str, str]], used: dict[str, int]
) -> tuple[str, str] | None:
    """Pick best candidate URL, preferring least reuse."""
    if not candidates:
        return None
    score, url, kind = min(candidates, key=lambda c: (used.get(c[1], 0), -c[0], hash(c[1]) % 9973))
    used[url] = used.get(url, 0) + 1
    return url, kind


def resolve_product_image(
    name: str,
    cat: str,
    sub: str,
    wp: dict,
    fb: dict,
    pools: dict[str, list[str]],
) -> tuple[str, str]:
    """Resolve product image based on similarity score directly, without tracking reuse or uniqueness."""
    candidates: list[tuple[float, str, str]] = []

    wp_url = match_wp_image(name, wp)
    if wp_url:
        candidates.append((10.0, wp_url, "website"))

    fb_url = match_fb_image(name, fb)
    if fb_url:
        candidates.append((9.5, fb_url, "facebook"))

    kw_url = keyword_wp_match(name, wp)
    if kw_url:
        candidates.append((8.0, kw_url, "keyword"))

    tokens = set(_norm_product_name(name).split()) - _MATCH_STOP_WORDS
    for title in pools.get(sub, []):
        if title not in wp:
            continue
        url = wp[title]
        overlap = len(tokens & set(_norm_product_name(title).split()))
        if overlap > 0:
            candidates.append((6.0 + overlap, url, "pool"))

    for title, url in wp.items():
        overlap = len(tokens & set(_norm_product_name(title).split()))
        if overlap > 0:
            candidates.append((4.0 + overlap * 0.5, url, "distributed"))

    if candidates:
        best_candidate = max(candidates, key=lambda c: c[0])
        return best_candidate[1], best_candidate[2]

    # Fallback to subcategory hint if available, else category fallback
    hint = SUBCATEGORY_SARA_HINTS.get(sub)
    if hint and hint in wp:
        return wp[hint], "subcategory_fallback"

    fallback_url = SARA_CATEGORY_FALLBACKS.get(cat, SARA_DEFAULT_IMAGE)
    return fallback_url, "category_fallback"


def _pick_distributed_wp_image(
    name: str, cat: str, wp: dict, used: dict[str, int]
) -> str:
    """Spread remaining products across all saraworldwide images (least-used first)."""
    candidates = list(wp.values())
    if not candidates:
        return SARA_CATEGORY_FALLBACKS.get(cat, SARA_DEFAULT_IMAGE)

    tokens = set(_norm_product_name(name).split()) - _MATCH_STOP_WORDS

    def rank_key(url: str) -> tuple:
        title_hits = 0
        for title, u in wp.items():
            if u != url:
                continue
            wk = set(_norm_product_name(title).split())
            title_hits = len(tokens & wk)
            break
        return (used.get(url, 0), -title_hits, hash(name + url) % 9973)

    url = sorted(candidates, key=rank_key)[0]
    used[url] = used.get(url, 0) + 1
    return url


def _placeholder_image_url(product_name: str) -> str:
    """Unique placeholder when saraworldwide pool is exhausted (no duplicate photos)."""
    from urllib.parse import quote

    label = quote((product_name or "Product")[:36].replace(" ", "+"))
    return f"https://placehold.co/400x400/043d2e/ffffff?text={label}"


def _enforce_unique_product_images(overrides: dict[str, str], wp: dict) -> dict[str, str]:
    """Every product gets a distinct image URL; placeholders only when needed."""
    pool = list(dict.fromkeys(wp.values()))
    used: set[str] = set()
    out: dict[str, str] = {}
    pool_i = 0

    for name in sorted(overrides.keys()):
        preferred = overrides.get(name) or ""
        url = None
        if preferred in pool and preferred not in used:
            url = preferred
        else:
            while pool_i < len(pool):
                candidate = pool[pool_i]
                pool_i += 1
                if candidate not in used:
                    url = candidate
                    break
        if not url:
            url = _placeholder_image_url(name)
        used.add(url)
        out[name] = url
    return out


def _balance_image_reuse(
    overrides: dict[str, str],
    wp: dict,
    fb: dict,
    max_reuse: int = 3,
) -> dict[str, str]:
    """Spread images so the same URL is not repeated too many times."""
    from collections import Counter

    all_urls = list(dict.fromkeys(list(wp.values()) + list(fb.values())))
    usage: Counter[str] = Counter()

    balanced: dict[str, str] = {}
    for name in sorted(overrides.keys()):
        url = overrides[name]
        if usage[url] < max_reuse:
            balanced[name] = url
            usage[url] += 1
            continue
        replacement = next((u for u in all_urls if usage[u] < max_reuse), url)
        balanced[name] = replacement
        usage[replacement] += 1
    return balanced


SARA_DEFAULT_IMAGE = "https://saraworldwide.com.np/wp-content/uploads/2024/08/moringa.jpg"
SARA_CATEGORY_FALLBACKS = {
    "Category A: Food": SARA_DEFAULT_IMAGE,
    "Category B: Natural Cosmetics": "https://saraworldwide.com.np/wp-content/uploads/2019/05/rose.jpg",
    "Category C: Spirituals": "https://saraworldwide.com.np/wp-content/uploads/2024/06/shw.jpg",
    "Category D: Sara Nursery": "https://saraworldwide.com.np/wp-content/uploads/2024/08/moringa.jpg",
}


def main():
    from setup_db import CATALOG

    import json
    from pathlib import Path

    print("Fetching images from saraworldwide.com.np ...")
    wp = fetch_saraworldwide_images()
    print(f"Loaded {len(wp)} images from live store")

    print("Loading images from facebook.com/saraorganics.np ...")
    fb = load_facebook_images()
    print(f"Loaded {len(fb)} images from Facebook")

    wp_json = Path(__file__).resolve().parent / "sara_wp_images.json"
    with open(wp_json, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(wp.items())), f, ensure_ascii=False, indent=2)
    print(f"Saved website catalog -> {wp_json}")

    all_entries = getattr(fetch_saraworldwide_images, "last_all", [])
    all_json = Path(__file__).resolve().parent / "sara_wp_all_images.json"
    with open(all_json, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(all_entries)} unique website images -> {all_json}")

    pools = _build_subcategory_pools(wp)
    overrides = {}
    stats: dict[str, int] = {}
    for cat, subs in CATALOG.items():
        for sub, prods in subs.items():
            for p in prods:
                name = " ".join((p or "").strip().split())
                if not name:
                    continue
                url, kind = resolve_product_image(name, cat, sub, wp, fb, pools)
                overrides[name] = url
                stats[kind] = stats.get(kind, 0) + 1

    dup = len(overrides) - len(set(overrides.values()))
    print("Image sources:", ", ".join(f"{k}={v}" for k, v in sorted(stats.items())))
    print(f"Unique images: {len(set(overrides.values()))} / {len(overrides)} (duplicate assignments: {dup})")

    lines = [
        '# Auto-generated product image map. Regenerate: python generate_product_images.py',
        'from __future__ import annotations',
        '',
        'DEFAULT_PRODUCT_IMAGE = "' + SARA_DEFAULT_IMAGE + '"',
        '',
        'CATEGORY_FALLBACK_IMAGES = {',
        '    "Category A: Food": "' + SARA_CATEGORY_FALLBACKS["Category A: Food"] + '",',
        '    "Category B: Natural Cosmetics": "' + SARA_CATEGORY_FALLBACKS["Category B: Natural Cosmetics"] + '",',
        '    "Category C: Spirituals": "' + SARA_CATEGORY_FALLBACKS["Category C: Spirituals"] + '",',
        '    "Category D: Sara Nursery": "' + SARA_CATEGORY_FALLBACKS["Category D: Sara Nursery"] + '",',
        '}',
        '',
        'PRODUCT_IMAGE_OVERRIDES = {',
    ]
    for name in sorted(overrides.keys()):
        url = overrides[name].replace("\\", "\\\\").replace('"', '\\"')
        safe_name = name.replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'    "{safe_name}": "{url}",')
    lines.append('}')
    lines.append('')
    lines.append('')
    lines.append('def resolve_product_image_url(product_name: str, category_name: str, subcategory_name: str = "") -> str:')
    lines.append('    if product_name in PRODUCT_IMAGE_OVERRIDES:')
    lines.append('        return PRODUCT_IMAGE_OVERRIDES[product_name]')
    lines.append('    return CATEGORY_FALLBACK_IMAGES.get(category_name, DEFAULT_PRODUCT_IMAGE)')
    lines.append('')

    out = __file__.replace("generate_product_images.py", "product_images.py")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {len(overrides)} product images -> {out}")


if __name__ == "__main__":
    main()
