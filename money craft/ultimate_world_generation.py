# 🌍 ABSOLUTELY INSANE ULTIMATE WORLD GENERATION - Mountains, Volcanoes, Caves, and MORE! 🚀
# This is the most EPIC world generation system EVER CREATED! 💎⛏️🌋

import pygame
import random
import math
from enum import Enum
try:
    import noise
except ImportError:
    # Fallback if noise library isn't available
    noise = None

# 🌈 INSANE COLOR PALETTE - The most vibrant colors ever!
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
RUBY_RED = (220, 20, 60)
EMERALD_GREEN = (0, 100, 0)
DIAMOND_BLUE = (185, 242, 255)
SAPPHIRE_BLUE = (15, 82, 186)
AMETHYST_PURPLE = (153, 102, 204)
CRYSTAL_WHITE = (255, 255, 255)
BITCOIN_ORANGE = (247, 147, 26)
BITCOIN_GOLD = (255, 203, 0)
GOLD = (255, 215, 0)
LIME = (50, 205, 50)
GRASS_GREEN = (34, 139, 34)
MOUNTAIN_BROWN = (139, 90, 43)
WATER_BLUE = (64, 164, 223)
SNOW_WHITE = (255, 250, 250)
SWAMP_GREEN = (85, 107, 47)
MYSTICAL_PURPLE = (147, 112, 219)
CRYSTAL_PINK = (255, 182, 193)
VOLCANO_RED = (178, 34, 34)
LAVA_GLOW = (255, 69, 0)
DESERT_SAND = (238, 203, 173)
OCEAN_DEEP = (0, 119, 190)
FOREST_DARK = (34, 100, 34)
CAVE_DARK = (47, 47, 47)
ICE_BLUE = (176, 224, 230)
COSMIC_PURPLE = (75, 0, 130)
DRAGON_SCALE = (139, 69, 19)
RAINBOW_GOLD = (255, 215, 0)
UNDERWORLD_FIRE = (255, 69, 0)
SKY_ISLAND_BLUE = (173, 216, 230)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)

# � RAINBOW COLORS for bridges and effects!
RAINBOW_COLORS = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

# �🌟 INSANE BIOME TYPES - More biomes than any game ever!
class BiomeType(Enum):
    FOREST = 0
    DESERT = 1
    SNOW = 2
    MOUNTAINS = 3
    VOLCANIC = 4
    SWAMP = 5
    MYSTICAL = 6
    CRYSTAL_CAVES = 7
    UNDERWORLD = 8
    SKY_ISLANDS = 9
    OCEAN = 10
    JUNGLE = 11
    TUNDRA = 12
    CORRUPTED = 13
    HOLY = 14
    DRAGON_LAIRS = 15
    RAINBOW_VALLEYS = 16
    BITCOIN_MINES = 17
    TIME_DISTORTED = 18
    QUANTUM_FIELDS = 19
    COSMIC_REALMS = 20

# 🏔️ INSANE TERRAIN TYPES - More terrain than imaginable!
class TerrainType(Enum):
    AIR = 0
    GRASS = 1
    DIRT = 2
    STONE = 3
    SAND = 4
    SNOW = 5
    LAVA = 6
    ICE = 7
    CRYSTAL = 8
    OBSIDIAN = 9
    BEDROCK = 10
    MYSTICAL_ORE = 11
    VOLCANIC_ROCK = 12
    MOUNTAIN_STONE = 13
    # 🌟 INSANE ORE TYPES!
    RUBY_ORE = 14
    EMERALD_ORE = 15
    DIAMOND_ORE = 16
    CRYSTAL_ORE = 17
    DRAGON_ORE = 18
    QUANTUM_ORE = 19
    BITCOIN_ORE = 20
    RAINBOW_ORE = 21
    COSMIC_ORE = 22
    TIME_ORE = 23
    SOUL_ORE = 24
    BLOOD_ORE = 25
    STAR_ORE = 26
    VOID_ORE = 27
    INFINITY_ORE = 28

# 🏰 INSANE STRUCTURE TYPES - More structures than reality!
class StructureType(Enum):
    HOUSE = 0
    SHOP = 1
    CASTLE = 2
    TEMPLE = 3
    MINE = 4
    VOLCANO = 5
    MOUNTAIN_PEAK = 6
    CAVE_ENTRANCE = 7
    DUNGEON = 8
    TREASURE_CHEST = 9
    ANCIENT_RUINS = 10
    WIZARD_TOWER = 11
    DRAGON_LAIR = 12
    RAINBOW_BRIDGE = 13
    BITCOIN_EXCHANGE = 14
    QUANTUM_PORTAL = 15
    COSMIC_OBSERVATORY = 16
    TIME_TEMPLE = 17
    SOUL_ALTAR = 18
    STAR_GATE = 19
    VOID_ANCHOR = 20
    INFINITY_FORGE = 21
    BLOOD_ALTAR = 22
    ELEMENTAL_SHRINE = 23
    DIMENSIONAL_RIFT = 24

# 💎 INSANE GEM TYPES - More gems than the universe!
class GemType(Enum):
    RUBY = 0
    EMERALD = 1
    DIAMOND = 2
    GOLD = 3
    SAPPHIRE = 4
    AMETHYST = 5
    CRYSTAL = 6
    RARE_CRYSTAL = 7
    ANCIENT_GEM = 8
    RAINBOW_GEM = 9
    DRAGON_GEM = 10
    COSMIC_GEM = 11
    QUANTUM_GEM = 12
    INFINITY_GEM = 13
    BITCOIN = 14
    TIME_GEM = 15
    SOUL_GEM = 16
    BLOOD_GEM = 17
    STAR_GEM = 18
    VOID_GEM = 19
    ELEMENTAL_GEM = 20
    DIMENSIONAL_GEM = 21

# 🌊 INSANE NOISE FUNCTIONS - Better than real physics!
def pnoise1(x, octaves=1):
    """Fallback Perlin noise function"""
    if noise:
        return noise.pnoise1(x, octaves=octaves)
    else:
        # Super advanced sine wave fallback
        value = 0
        amplitude = 1
        frequency = 1
        for _ in range(octaves):
            value += amplitude * math.sin(x * frequency)
            amplitude *= 0.5
            frequency *= 2
        return value / 2

def pnoise2(x, y, octaves=1):
    """2D Perlin noise for insane terrain"""
    if noise:
        return noise.pnoise2(x, y, octaves=octaves)
    else:
        # Epic 2D sine wave fallback
        value = 0
        amplitude = 1
        freq_x = 1
        freq_y = 1
        for _ in range(octaves):
            value += amplitude * (math.sin(x * freq_x) + math.cos(y * freq_y))
            amplitude *= 0.5
            freq_x *= 2
            freq_y *= 2
        return value / 4

def ridged_noise(x, y):
    """Ridged multifractal noise for insane mountains"""
    if noise:
        return abs(noise.pnoise2(x, y, octaves=6))
    else:
        # Fallback ridged noise
        base = pnoise2(x, y, octaves=4)
        return 1.0 - abs(base)

# 🚀 THE MOST INSANE WORLD GENERATOR EVER CREATED! 🌍
class WorldGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.blocks = [[0 for _ in range(height)] for _ in range(width)]
        self.biomes = [[BiomeType.FOREST for _ in range(height)] for _ in range(width)]
        self.structures = []
        self.cave_systems = []
        self.ore_deposits = []
        self.treasure_chests = []
        self.dungeons = []
        self.volcanoes = []
        self.mountains = []
        self.rainbow_bridges = []
        self.quantum_portals = []
        self.cosmic_observatories = []
        self.time_temples = []
        self.soul_altars = []
        self.star_gates = []
        self.void_anchors = []
        self.infinity_forges = []
        self.blood_altars = []
        self.elemental_shrines = []
        self.dimensional_rifts = []
        self.dragon_lairs = []
        self.bitcoin_exchanges = []
        self.rainbow_valleys = []
        self.time_distorted_areas = []
        self.quantum_fields = []
        self.cosmic_realms = []
        
        # 🌟 INSANE WORLD GENERATION PARAMETERS!
        self.terrain_height = height // 2
        self.mountain_height_variation = 50  # INSANE MOUNTAINS!
        self.cave_density = 0.2  # MORE CAVES!
        self.ore_rarity = 0.1  # MORE ORES!
        self.structure_density = 0.15  # MORE STRUCTURES!
        self.volcano_frequency = 0.05  # MORE VOLCANOES!
        self.rainbow_frequency = 0.02  # RAINBOWS!
        self.quantum_frequency = 0.01  # QUANTUM STUFF!
        self.cosmic_frequency = 0.005  # COSMIC POWER!
        
        print("🚀 INITIALIZING THE MOST INSANE WORLD GENERATOR EVER! 🌍")
        
    def generate_world(self):
        """Generate the most insane world ever created!"""
        print("🌍 Generating ABSOLUTELY INSANE World...")
        
        # Generate base terrain with INSANE complexity!
        self.generate_terrain()
        
        # Generate INSANE biomes!
        self.generate_biomes()
        
        # Generate INSANE mountains!
        self.generate_mountains()
        
        # Generate INSANE volcanoes!
        self.generate_volcanoes()
        
        # Generate INSANE cave systems!
        self.generate_cave_systems()
        
        # Generate INSANE ore deposits!
        self.generate_ore_deposits()
        
        # Generate INSANE structures!
        self.generate_structures()
        
        # Generate INSANE dungeons!
        self.generate_dungeons()
        
        # Generate INSANE treasure chests!
        self.generate_treasure_chests()
        
        # Generate INSANE rainbow bridges!
        self.generate_rainbow_bridges()
        
        # Generate INSANE quantum portals!
        self.generate_quantum_portals()
        
        # Generate INSANE cosmic observatories!
        self.generate_cosmic_observatories()
        
        # Generate INSANE time temples!
        self.generate_time_temples()
        
        # Generate INSANE soul altars!
        self.generate_soul_altars()
        
        # Generate INSANE star gates!
        self.generate_star_gates()
        
        # Generate INSANE void anchors!
        self.generate_void_anchors()
        
        # Generate INSANE infinity forges!
        self.generate_infinity_forges()
        
        # Generate INSANE blood altars!
        self.generate_blood_altars()
        
        # Generate INSANE elemental shrines!
        self.generate_elemental_shrines()
        
        # Generate INSANE dimensional rifts!
        self.generate_dimensional_rifts()
        
        # Generate INSANE dragon lairs!
        self.generate_dragon_lairs()
        
        # Generate INSANE bitcoin exchanges!
        self.generate_bitcoin_exchanges()
        
        # Generate INSANE rainbow valleys!
        self.generate_rainbow_valleys()
        
        # Generate INSANE time distorted areas!
        self.generate_time_distorted_areas()
        
        # Generate INSANE quantum fields!
        self.generate_quantum_fields()
        
        # Generate INSANE cosmic realms!
        self.generate_cosmic_realms()
        
        print("✅ ABSOLUTELY INSANE World Generation Complete! 🚀")
        
    def generate_terrain(self):
        """Generate INSANE terrain with multiple noise layers!"""
        for x in range(self.width):
            # 🌟 MULTI-LAYER NOISE FOR INSANE TERRAIN!
            height = self.terrain_height
            
            # Main terrain with multiple octaves
            height += int(pnoise1(x * 0.02, octaves=8) * 20)
            
            # Secondary terrain variation
            height += int(pnoise1(x * 0.05, octaves=4) * 10)
            
            # Tertiary detail noise
            height += int(pnoise1(x * 0.1, octaves=2) * 5)
            
            # INSANE mountain ranges with ridged noise
            mountain_noise = ridged_noise(x * 0.01, x * 0.01)
            if mountain_noise > 0.4:
                height += int(mountain_noise * 60)
                self.mountains.append({"x": x, "height": height, "type": "insane"})
                
            # INSANE valley carving
            valley_noise = pnoise1(x * 0.03, octaves=3)
            if valley_noise < -0.3:
                height -= int(abs(valley_noise) * 30)
                
            # INSANE plateau generation
            plateau_noise = pnoise1(x * 0.015, octaves=2)
            if 0.2 < plateau_noise < 0.4:
                plateau_height = int(plateau_noise * 40)
                for px in range(max(0, x - 3), min(self.width, x + 4)):
                    if abs(px - x) <= 3:
                        self.blocks[px][plateau_height] = TerrainType.STONE
                        
            # Ensure terrain stays within bounds
            height = max(5, min(self.height - 5, height))
            
            # Fill terrain blocks with INSANE layers!
            for y in range(height, self.height):
                if y < height + 2:
                    self.blocks[x][y] = TerrainType.GRASS
                elif y < height + 5:
                    self.blocks[x][y] = TerrainType.DIRT
                elif y < height + 15:
                    self.blocks[x][y] = TerrainType.STONE
                else:
                    # DEEP UNDERGROUND with special blocks!
                    deep_noise = pnoise2(x * 0.1, y * 0.1, octaves=2)
                    if deep_noise > 0.5:
                        self.blocks[x][y] = TerrainType.MYSTICAL_ORE
                    elif deep_noise < -0.5:
                        self.blocks[x][y] = TerrainType.BEDROCK
                    else:
                        self.blocks[x][y] = TerrainType.STONE
                        
            # Surface block variations
            if height < self.height:
                surface_noise = pnoise1(x * 0.2, octaves=1)
                if surface_noise > 0.3:
                    self.blocks[x][height] = TerrainType.STONE  # Rocky surface
                elif surface_noise < -0.3:
                    self.blocks[x][height] = TerrainType.SAND  # Sandy patches
                else:
                    self.blocks[x][height] = TerrainType.GRASS
                    
    def generate_biomes(self):
        """Generate INSANE biomes with complex patterns!"""
        for x in range(self.width):
            for y in range(self.height):
                # 🌟 MULTI-DIMENSIONAL BIOME GENERATION!
                biome_value_x = pnoise1(x * 0.008, octaves=3)
                biome_value_y = pnoise1(y * 0.008, octaves=3)
                biome_value_2d = pnoise2(x * 0.01, y * 0.01, octaves=2)
                
                # Combine multiple noise sources for INSANE biome variation
                combined_value = (biome_value_x + biome_value_y + biome_value_2d) / 3
                
                # Height-based biome modification
                surface_y = self.get_surface_level(x)
                height_factor = (y - surface_y) / 20  # Depth factor
                
                # INSANE biome selection with 21 different biomes!
                if combined_value < -0.7:
                    if height_factor < 0:
                        biome = BiomeType.OCEAN
                    else:
                        biome = BiomeType.UNDERWORLD
                elif combined_value < -0.5:
                    biome = BiomeType.TUNDRA
                elif combined_value < -0.3:
                    biome = BiomeType.SNOW
                elif combined_value < -0.1:
                    biome = BiomeType.FOREST
                elif combined_value < 0.1:
                    biome = BiomeType.JUNGLE
                elif combined_value < 0.3:
                    biome = BiomeType.DESERT
                elif combined_value < 0.4:
                    biome = BiomeType.SWAMP
                elif combined_value < 0.5:
                    biome = BiomeType.MOUNTAINS
                elif combined_value < 0.6:
                    biome = BiomeType.VOLCANIC
                elif combined_value < 0.65:
                    biome = BiomeType.MYSTICAL
                elif combined_value < 0.7:
                    biome = BiomeType.CRYSTAL_CAVES
                elif combined_value < 0.75:
                    biome = BiomeType.SKY_ISLANDS
                elif combined_value < 0.8:
                    biome = BiomeType.DRAGON_LAIRS
                elif combined_value < 0.85:
                    biome = BiomeType.RAINBOW_VALLEYS
                elif combined_value < 0.9:
                    biome = BiomeType.BITCOIN_MINES
                elif combined_value < 0.93:
                    biome = BiomeType.TIME_DISTORTED
                elif combined_value < 0.96:
                    biome = BiomeType.QUANTUM_FIELDS
                else:
                    biome = BiomeType.COSMIC_REALMS
                    
                # Special biome overrides
                if random.random() < 0.02:  # 2% chance for special biomes
                    special_biomes = [BiomeType.CORRUPTED, BiomeType.HOLY]
                    biome = random.choice(special_biomes)
                    
                self.biomes[x][y] = biome
                
    def get_surface_level(self, x):
        """Get surface level at given X position"""
        if 0 <= x < self.width:
            for y in range(self.height):
                if self.blocks[x][y] != 0:
                    return y
        return self.height // 2
        
    # 🏔️ INSANE MOUNTAIN GENERATION!
    def generate_mountains(self):
        """Generate INSANE mountain ranges!"""
        num_mountain_ranges = random.randint(8, 15)
        for _ in range(num_mountain_ranges):
            center_x = random.randint(10, self.width - 10)
            range_width = random.randint(15, 30)
            peak_height = random.randint(25, 45)
            
            for x in range(max(0, center_x - range_width), min(self.width, center_x + range_width)):
                distance = abs(x - center_x)
                mountain_height = peak_height - (distance * peak_height // range_width)
                
                if mountain_height > 10:
                    for y in range(mountain_height, min(self.height, mountain_height + 20)):
                        if y < mountain_height + 3:
                            self.blocks[x][y] = TerrainType.MOUNTAIN_STONE
                        else:
                            self.blocks[x][y] = TerrainType.STONE
                            
                    # Snow cap on high peaks
                    if mountain_height > 35:
                        self.blocks[x][mountain_height] = TerrainType.SNOW
                        
    # 🌋 INSANE VOLCANO GENERATION!
    def generate_volcanoes(self):
        """Generate INSANE volcanoes!"""
        num_volcanoes = random.randint(5, 10)
        for _ in range(num_volcanoes):
            center_x = random.randint(20, self.width - 20)
            center_y = random.randint(15, 30)
            crater_size = random.randint(5, 12)
            
            # Build volcano cone
            for x in range(max(0, center_x - crater_size * 3), min(self.width, center_x + crater_size * 3)):
                for y in range(max(0, center_y - crater_size * 2), min(self.height, center_y + crater_size)):
                    distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                    
                    if distance <= crater_size * 3:
                        if distance <= crater_size:
                            # Crater with lava
                            self.blocks[x][y] = TerrainType.LAVA
                        else:
                            # Volcano slopes
                            self.blocks[x][y] = TerrainType.VOLCANIC_ROCK
                            
            self.volcanoes.append({
                "x": center_x,
                "y": center_y,
                "crater_size": crater_size,
                "active": True,
                "eruption_timer": random.randint(200, 600)
            })
            
    # 🕳️ INSANE CAVE SYSTEMS!
    def generate_cave_systems(self):
        """Generate INSANE cave systems!"""
        num_cave_systems = random.randint(15, 25)
        for _ in range(num_cave_systems):
            start_x = random.randint(5, self.width - 5)
            start_y = random.randint(10, self.height - 5)
            cave_length = random.randint(30, 80)
            cave_width = random.randint(3, 8)
            
            current_x, current_y = start_x, start_y
            cave_path = [(current_x, current_y)]
            
            for step in range(cave_length):
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                
                if step < cave_length // 3 and random.random() < 0.7:
                    direction = (0, 1)
                    
                new_x = current_x + direction[0]
                new_y = current_y + direction[1]
                
                if 0 <= new_x < self.width and 5 <= new_y < self.height - 2:
                    current_x, current_y = new_x, new_y
                    cave_path.append((current_x, current_y))
                    
                    # Clear cave area
                    for dx in range(-cave_width // 2, cave_width // 2 + 1):
                        for dy in range(-cave_width // 2, cave_width // 2 + 1):
                            cave_x = current_x + dx
                            cave_y = current_y + dy
                            
                            if (0 <= cave_x < self.width and 0 <= cave_y < self.height and
                                abs(dx) + abs(dy) <= cave_width // 2):
                                self.blocks[cave_x][cave_y] = 0
                                
            # Add branches
            for branch_point in range(8, len(cave_path), 15):
                if random.random() < 0.4:
                    branch_x, branch_y = cave_path[branch_point]
                    branch_length = random.randint(10, 25)
                    
                    for _ in range(branch_length):
                        branch_direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                        branch_x += branch_direction[0]
                        branch_y += branch_direction[1]
                        
                        if (0 <= branch_x < self.width and 5 <= branch_y < self.height - 2):
                            for dx in range(-1, 2):
                                for dy in range(-1, 2):
                                    if 0 <= branch_x + dx < self.width and 0 <= branch_y + dy < self.height:
                                        self.blocks[branch_x + dx][branch_y + dy] = 0
                                        
            self.cave_systems.append({
                "path": cave_path,
                "width": cave_width,
                "type": random.choice(["normal", "crystal", "lava", "ice", "mystical", "quantum"]),
                "treasure": random.random() < 0.4
            })
            
    # 💎 INSANE ORE DEPOSITS!
    def generate_ore_deposits(self):
        """Generate INSANE ore deposits!"""
        ore_types = [
            (TerrainType.STONE, GemType.RUBY, 0.15, "ruby_vein"),
            (TerrainType.STONE, GemType.EMERALD, 0.12, "emerald_vein"),
            (TerrainType.STONE, GemType.DIAMOND, 0.08, "diamond_vein"),
            (TerrainType.MOUNTAIN_STONE, GemType.RARE_CRYSTAL, 0.05, "crystal_vein"),
            (TerrainType.VOLCANIC_ROCK, GemType.DRAGON_GEM, 0.03, "dragon_vein"),
            (TerrainType.MYSTICAL_ORE, GemType.QUANTUM_GEM, 0.02, "quantum_vein"),
            (TerrainType.BEDROCK, GemType.INFINITY_GEM, 0.01, "infinity_vein"),
            (TerrainType.STONE, GemType.BITCOIN, 0.005, "bitcoin_vein"),
            (TerrainType.STONE, GemType.TIME_GEM, 0.003, "time_vein"),
            (TerrainType.STONE, GemType.SOUL_GEM, 0.002, "soul_vein"),
            (TerrainType.STONE, GemType.STAR_GEM, 0.001, "star_vein"),
            (TerrainType.STONE, GemType.VOID_GEM, 0.001, "void_vein")
        ]
        
        for stone_type, gem_type, rarity, vein_type in ore_types:
            num_veins = int(self.width * self.height * rarity)
            
            for _ in range(num_veins):
                center_x = random.randint(3, self.width - 4)
                center_y = random.randint(10, self.height - 4)
                vein_size = random.randint(4, 12)
                
                for x in range(max(0, center_x - vein_size), min(self.width, center_x + vein_size)):
                    for y in range(max(0, center_y - vein_size), min(self.height, center_y + vein_size)):
                        distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                        
                        if distance <= vein_size and self.blocks[x][y] == stone_type:
                            # Convert to ore block
                            if vein_type == "ruby_vein":
                                self.blocks[x][y] = TerrainType.RUBY_ORE
                            elif vein_type == "emerald_vein":
                                self.blocks[x][y] = TerrainType.EMERALD_ORE
                            elif vein_type == "diamond_vein":
                                self.blocks[x][y] = TerrainType.DIAMOND_ORE
                            elif vein_type == "crystal_vein":
                                self.blocks[x][y] = TerrainType.CRYSTAL_ORE
                            elif vein_type == "dragon_vein":
                                self.blocks[x][y] = TerrainType.DRAGON_ORE
                            elif vein_type == "quantum_vein":
                                self.blocks[x][y] = TerrainType.QUANTUM_ORE
                            elif vein_type == "infinity_vein":
                                self.blocks[x][y] = TerrainType.INFINITY_ORE
                            elif vein_type == "bitcoin_vein":
                                self.blocks[x][y] = TerrainType.BITCOIN_ORE
                            elif vein_type == "time_vein":
                                self.blocks[x][y] = TerrainType.TIME_ORE
                            elif vein_type == "soul_vein":
                                self.blocks[x][y] = TerrainType.SOUL_ORE
                            elif vein_type == "star_vein":
                                self.blocks[x][y] = TerrainType.STAR_ORE
                            elif vein_type == "void_vein":
                                self.blocks[x][y] = TerrainType.VOID_ORE
                                
                self.ore_deposits.append({
                    "type": vein_type,
                    "center": (center_x, center_y),
                    "size": vein_size,
                    "gem_type": gem_type
                })
                
    # 🏰 INSANE STRUCTURES!
    def generate_structures(self):
        """Generate INSANE structures!"""
        structure_types = [
            (StructureType.HOUSE, 0.04),
            (StructureType.SHOP, 0.02),
            (StructureType.CASTLE, 0.005),
            (StructureType.TEMPLE, 0.008),
            (StructureType.WIZARD_TOWER, 0.003),
            (StructureType.ANCIENT_RUINS, 0.002),
            (StructureType.RAINBOW_BRIDGE, 0.001),
            (StructureType.QUANTUM_PORTAL, 0.001),
            (StructureType.COSMIC_OBSERVATORY, 0.0005),
            (StructureType.TIME_TEMPLE, 0.0005),
            (StructureType.STAR_GATE, 0.0003),
            (StructureType.INFINITY_FORGE, 0.0002)
        ]
        
        for struct_type, frequency in structure_types:
            num_structures = int(self.width * self.height * frequency)
            
            for _ in range(num_structures):
                x = random.randint(5, self.width - 5)
                y = random.randint(5, self.height - 5)
                
                structure = {
                    "type": struct_type,
                    "x": x,
                    "y": y,
                    "width": random.randint(3, 8),
                    "height": random.randint(3, 10),
                    "loot": random.random() < 0.6
                }
                
                self.structures.append(structure)
                
    # 🏰 INSANE DUNGEONS!
    def generate_dungeons(self):
        """Generate INSANE dungeons!"""
        num_dungeons = random.randint(5, 10)
        
        for _ in range(num_dungeons):
            center_x = random.randint(15, self.width - 15)
            center_y = random.randint(20, self.height - 20)
            dungeon_size = random.randint(10, 20)
            
            rooms = []
            for _ in range(random.randint(5, 10)):
                room_x = center_x + random.randint(-dungeon_size, dungeon_size)
                room_y = center_y + random.randint(-dungeon_size, dungeon_size)
                room_width = random.randint(4, 8)
                room_height = random.randint(4, 8)
                
                for x in range(room_x, room_x + room_width):
                    for y in range(room_y, room_y + room_height):
                        if (0 <= x < self.width and 0 <= y < self.height):
                            self.blocks[x][y] = 0
                            
                rooms.append({
                    "x": room_x,
                    "y": room_y,
                    "width": room_width,
                    "height": room_height
                })
                
            self.dungeons.append({
                "rooms": rooms,
                "boss_room": rooms[-1] if rooms else None,
                "loot_level": random.randint(1, 10),
                "cleared": False
            })
            
    # 📦 INSANE TREASURE CHESTS!
    def generate_treasure_chests(self):
        """Generate INSANE treasure chests!"""
        num_chests = random.randint(25, 40)
        
        for _ in range(num_chests):
            x = random.randint(2, self.width - 3)
            y = random.randint(5, self.height - 3)
            
            if self.blocks[x][y] == 0:
                chest_rarity = random.choice(["common", "uncommon", "rare", "epic", "legendary", "mythic", "cosmic"])
                
                self.treasure_chests.append({
                    "x": x,
                    "y": y,
                    "rarity": chest_rarity,
                    "opened": False,
                    "loot": self.generate_treasure_loot(chest_rarity)
                })
                
    def generate_treasure_loot(self, rarity):
        """Generate INSANE treasure loot!"""
        loot_multipliers = {
            "common": 1.0,
            "uncommon": 2.0,
            "rare": 5.0,
            "epic": 10.0,
            "legendary": 25.0,
            "mythic": 50.0,
            "cosmic": 100.0
        }
        
        multiplier = loot_multipliers[rarity]
        
        return {
            "wealth": random.randint(100, 5000) * int(multiplier),
            "gems": random.randint(1, 10) * int(multiplier // 2),
            "items": random.choice(["pickaxe", "sword", "armor", "magic_staff"]) if rarity in ["legendary", "mythic", "cosmic"] else None
        }
        
    # 🌈 INSANE RAINBOW BRIDGES!
    def generate_rainbow_bridges(self):
        """Generate INSANE rainbow bridges!"""
        num_bridges = random.randint(2, 5)
        
        for _ in range(num_bridges):
            start_x = random.randint(10, self.width // 2)
            end_x = random.randint(self.width // 2, self.width - 10)
            y = random.randint(5, 20)
            
            self.rainbow_bridges.append({
                "start_x": start_x,
                "end_x": end_x,
                "y": y,
                "colors": RAINBOW_COLORS
            })
            
    # ⚛️ INSANE QUANTUM PORTALS!
    def generate_quantum_portals(self):
        """Generate INSANE quantum portals!"""
        num_portals = random.randint(1, 3)
        
        for _ in range(num_portals):
            x = random.randint(10, self.width - 10)
            y = random.randint(5, 30)
            
            self.quantum_portals.append({
                "x": x,
                "y": y,
                "active": True,
                "destination": random.choice(["quantum_realm", "time_space", "void_dimension"])
            })
            
    # 🔭 INSANE COSMIC OBSERVATORIES!
    def generate_cosmic_observatories(self):
        """Generate INSANE cosmic observatories!"""
        num_observatories = random.randint(1, 2)
        
        for _ in range(num_observatories):
            x = random.randint(15, self.width - 15)
            y = random.randint(5, 25)
            
            self.cosmic_observatories.append({
                "x": x,
                "y": y,
                "active": True,
                "power_level": random.randint(50, 100)
            })
            
    # ⏰ INSANE TIME TEMPLES!
    def generate_time_temples(self):
        """Generate INSANE time temples!"""
        num_temples = random.randint(1, 3)
        
        for _ in range(num_temples):
            x = random.randint(10, self.width - 10)
            y = random.randint(8, 30)
            
            self.time_temples.append({
                "x": x,
                "y": y,
                "active": True,
                "time_power": random.randint(25, 75)
            })
            
    # 👻 INSANE SOUL ALTARS!
    def generate_soul_altars(self):
        """Generate INSANE soul altars!"""
        num_altars = random.randint(2, 4)
        
        for _ in range(num_altars):
            x = random.randint(8, self.width - 8)
            y = random.randint(10, self.height - 10)
            
            self.soul_altars.append({
                "x": x,
                "y": y,
                "active": True,
                "soul_power": random.randint(30, 80)
            })
            
    # 🌟 INSANE STAR GATES!
    def generate_star_gates(self):
        """Generate INSANE star gates!"""
        num_gates = random.randint(1, 2)
        
        for _ in range(num_gates):
            x = random.randint(20, self.width - 20)
            y = random.randint(5, 25)
            
            self.star_gates.append({
                "x": x,
                "y": y,
                "active": True,
                "destination": random.choice(["alpha_centauri", "andromeda", "orion_nebula"])
            })
            
    # 🕳️ INSANE VOID ANCHORS!
    def generate_void_anchors(self):
        """Generate INSANE void anchors!"""
        num_anchors = random.randint(1, 2)
        
        for _ in range(num_anchors):
            x = random.randint(15, self.width - 15)
            y = random.randint(15, self.height - 15)
            
            self.void_anchors.append({
                "x": x,
                "y": y,
                "active": True,
                "void_power": random.randint(40, 90)
            })
            
    # ♾️ INSANE INFINITY FORGES!
    def generate_infinity_forges(self):
        """Generate INSANE infinity forges!"""
        num_forges = random.randint(1, 2)
        
        for _ in range(num_forges):
            x = random.randint(20, self.width - 20)
            y = random.randint(10, self.height - 10)
            
            self.infinity_forges.append({
                "x": x,
                "y": y,
                "active": True,
                "forge_power": random.randint(60, 100)
            })
            
    # 🩸 INSANE BLOOD ALTARS!
    def generate_blood_altars(self):
        """Generate INSANE blood altars!"""
        num_altars = random.randint(2, 4)
        
        for _ in range(num_altars):
            x = random.randint(10, self.width - 10)
            y = random.randint(12, self.height - 12)
            
            self.blood_altars.append({
                "x": x,
                "y": y,
                "active": True,
                "blood_power": random.randint(35, 85)
            })
            
    # 🌪️ INSANE ELEMENTAL SHRINES!
    def generate_elemental_shrines(self):
        """Generate INSANE elemental shrines!"""
        num_shrines = random.randint(3, 6)
        
        for _ in range(num_shrines):
            x = random.randint(8, self.width - 8)
            y = random.randint(8, self.height - 8)
            element = random.choice(["fire", "water", "earth", "air", "lightning", "ice"])
            
            self.elemental_shrines.append({
                "x": x,
                "y": y,
                "element": element,
                "active": True,
                "power": random.randint(25, 75)
            })
            
    # 🌀 INSANE DIMENSIONAL RIFTS!
    def generate_dimensional_rifts(self):
        """Generate INSANE dimensional rifts!"""
        num_rifts = random.randint(1, 3)
        
        for _ in range(num_rifts):
            x = random.randint(15, self.width - 15)
            y = random.randint(10, self.height - 10)
            
            self.dimensional_rifts.append({
                "x": x,
                "y": y,
                "active": True,
                "stability": random.randint(30, 90)
            })
            
    # 🐉 INSANE DRAGON LAIRS!
    def generate_dragon_lairs(self):
        """Generate INSANE dragon lairs!"""
        num_lairs = random.randint(2, 4)
        
        for _ in range(num_lairs):
            x = random.randint(20, self.width - 20)
            y = random.randint(15, self.height - 15)
            
            self.dragon_lairs.append({
                "x": x,
                "y": y,
                "dragon_type": random.choice(["fire", "ice", "lightning", "shadow", "cosmic"]),
                "active": True,
                "power": random.randint(70, 100)
            })
            
    # ₿ INSANE BITCOIN EXCHANGES!
    def generate_bitcoin_exchanges(self):
        """Generate INSANE bitcoin exchanges!"""
        num_exchanges = random.randint(1, 3)
        
        for _ in range(num_exchanges):
            x = random.randint(15, self.width - 15)
            y = random.randint(8, 25)
            
            self.bitcoin_exchanges.append({
                "x": x,
                "y": y,
                "active": True,
                "bitcoin_rate": random.uniform(50000, 100000),
                "trading_volume": random.randint(100, 1000)
            })
            
    # 🌈 INSANE RAINBOW VALLEYS!
    def generate_rainbow_valleys(self):
        """Generate INSANE rainbow valleys!"""
        num_valleys = random.randint(2, 4)
        
        for _ in range(num_valleys):
            start_x = random.randint(5, self.width - 20)
            end_x = random.randint(start_x + 10, self.width - 5)
            y = random.randint(10, 30)
            
            self.rainbow_valleys.append({
                "start_x": start_x,
                "end_x": end_x,
                "y": y,
                "rainbow_intensity": random.randint(50, 100)
            })
            
    # ⏰ INSANE TIME DISTORTED AREAS!
    def generate_time_distorted_areas(self):
        """Generate INSANE time distorted areas!"""
        num_areas = random.randint(2, 4)
        
        for _ in range(num_areas):
            x = random.randint(10, self.width - 10)
            y = random.randint(10, self.height - 10)
            radius = random.randint(8, 15)
            
            self.time_distorted_areas.append({
                "x": x,
                "y": y,
                "radius": radius,
                "time_speed": random.uniform(0.1, 5.0),
                "active": True
            })
            
    # ⚛️ INSANE QUANTUM FIELDS!
    def generate_quantum_fields(self):
        """Generate INSANE quantum fields!"""
        num_fields = random.randint(1, 3)
        
        for _ in range(num_fields):
            x = random.randint(15, self.width - 15)
            y = random.randint(12, self.height - 12)
            radius = random.randint(10, 20)
            
            self.quantum_fields.append({
                "x": x,
                "y": y,
                "radius": radius,
                "quantum_energy": random.randint(40, 90),
                "active": True
            })
            
    # 🌌 INSANE COSMIC REALMS!
    def generate_cosmic_realms(self):
        """Generate INSANE cosmic realms!"""
        num_realms = random.randint(1, 2)
        
        for _ in range(num_realms):
            x = random.randint(20, self.width - 20)
            y = random.randint(8, self.height - 8)
            radius = random.randint(15, 25)
            
            self.cosmic_realms.append({
                "x": x,
                "y": y,
                "radius": radius,
                "cosmic_power": random.randint(60, 100),
                "active": True
            })
            
    def update_volcanoes(self):
        """Update active volcanoes"""
        for volcano in self.volcanoes:
            if volcano["active"]:
                volcano["eruption_timer"] -= 1
                
                if volcano["eruption_timer"] <= 0:
                    self.erupt_volcano(volcano)
                    volcano["eruption_timer"] = random.randint(400, 800)
                    
    def erupt_volcano(self, volcano):
        """Handle volcano eruption"""
        center_x = volcano["x"]
        center_y = volcano["y"]
        crater_size = volcano["crater_size"]
        
        # Create lava flow
        for _ in range(30):
            flow_x = center_x + random.randint(-15, 15)
            flow_y = center_y + random.randint(-8, 20)
            
            if (0 <= flow_x < self.width and 0 <= flow_y < self.height):
                current_x, current_y = center_x, center_y
                
                while current_y < flow_y and current_y < self.height - 1:
                    current_y += 1
                    if random.random() < 0.8:
                        current_x += random.choice([-1, 0, 1])
                        
                    if 0 <= current_x < self.width:
                        self.blocks[current_x][current_y] = TerrainType.LAVA
                        
        # Create ash cloud
        for _ in range(15):
            ash_x = center_x + random.randint(-20, 20)
            ash_y = center_y - random.randint(8, 30)
            
            if 0 <= ash_x < self.width and ash_y >= 0:
                self.blocks[ash_x][ash_y] = 20  # Ash block

print("🚀 ABSOLUTELY INSANE WORLD GENERATION loaded! - The most EPIC world generation EVER! 🌍💎⛏️🌋")
