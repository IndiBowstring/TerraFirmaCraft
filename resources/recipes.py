#  Work under Copyright. Licensed under the EUPL.
#  See the project README.md and LICENSE.txt for more information.

from mcresources import ResourceManager, utils
from mcresources.recipe_context import RecipeContext

from constants import *


# Crafting recipes
def generate(rm: ResourceManager):
    def stone_cutting(name, item: str, result: str, count: int = 1) -> RecipeContext:
        return rm.recipe(('stonecutting', name), 'minecraft:stonecutting', {
            'ingredient': utils.ingredient(item),
            'result': result,
            'count': count
        })

    def damage_shapeless(name_parts: utils.ResourceIdentifier, ingredients: utils.Json, result: utils.Json, group: str = None, conditions: utils.Json = None) -> RecipeContext:
        res = utils.resource_location(rm.domain, name_parts)
        rm.write((*rm.resource_dir, 'data', res.domain, 'recipes', res.path), {
            'type': 'tfc:damage_inputs_crafting',
            'recipe': {
                'type': 'minecraft:crafting_shapeless',
                'group': group,
                'ingredients': utils.item_stack_list(ingredients),
                'result': utils.item_stack(result),
                'conditions': utils.recipe_condition(conditions)
            }
        })
        return RecipeContext(rm, res)

    # Rock Things
    for rock in ROCKS.keys():

        cobble = 'tfc:rock/cobble/%s' % rock
        raw = 'tfc:rock/raw/%s' % rock
        loose = 'tfc:rock/loose/%s' % rock
        hardened = 'tfc:rock/hardened/%s' % rock
        bricks = 'tfc:rock/bricks/%s' % rock
        smooth = 'tfc:rock/smooth/%s' % rock
        cracked_bricks = 'tfc:rock/cracked_bricks/%s' % rock
        chiseled = 'tfc:rock/chiseled/%s' % rock

        brick = 'tfc:brick/%s' % rock

        # Cobble <-> Loose Rocks
        rm.crafting_shapeless('crafting/rock/%s_cobble_to_loose_rocks' % rock, cobble, (4, loose)).with_advancement(cobble)
        rm.crafting_shaped('crafting/rock/%s_loose_rocks_to_cobble' % rock, ['XX', 'XX'], loose, cobble).with_advancement(loose)

        # Stairs, Slabs and Walls
        for block_type in CUTTABLE_ROCKS:
            block = 'tfc:rock/%s/%s' % (block_type, rock)

            rm.crafting_shaped('crafting/rock/%s_%s_slab' % (rock, block_type), ['XXX'], block, (6, block + '_slab')).with_advancement(block)
            rm.crafting_shaped('crafting/rock/%s_%s_stairs' % (rock, block_type), ['X  ', 'XX ', 'XXX'], block, (6, block + '_stairs')).with_advancement(block)
            rm.crafting_shaped('crafting/rock/%s_%s_wall' % (rock, block_type), ['XXX', 'XXX'], block, (6, block + '_wall')).with_advancement(block)

            # Vanilla allows stone cutting from any -> any, we only allow stairs/slabs/walls as other variants require mortar / chisel
            stone_cutting('rock/%s_%s_slab' % (rock, block_type), block, block + '_slab', 2).with_advancement(block)
            stone_cutting('rock/%s_%s_stairs' % (rock, block_type), block, block + '_stairs', 1).with_advancement(block)
            stone_cutting('rock/%s_%s_wall' % (rock, block_type), block, block + '_wall', 1).with_advancement(block)

        # Other variants
        damage_shapeless('crafting/rock/%s_smooth' % rock, (raw, 'tag!tfc:chisels'), smooth).with_advancement(raw)
        damage_shapeless('crafting/rock/%s_brick' % rock, (loose, 'tag!tfc:chisels'), brick).with_advancement(loose)
        damage_shapeless('crafting/rock/%s_chiseled' % rock, (smooth, 'tag!tfc:chisels'), chiseled).with_advancement(smooth)

        rm.crafting_shaped('crafting/rock/%s_hardened' % rock, ['XMX', 'MXM', 'XMX'], {'X': raw, 'M': 'tag!tfc:mortar'}, (2, hardened)).with_advancement(raw)
        rm.crafting_shaped('crafting/rock/%s_bricks' % rock, ['XMX', 'MXM', 'XMX'], {'X': brick, 'M': 'tag!tfc:mortar'}, (4, bricks)).with_advancement(brick)

        damage_shapeless('crafting/rock/%s_cracked' % rock, (bricks, 'tag!tfc:hammers'), cracked_bricks).with_advancement(bricks)

    # Wood things
    for wood in WOODS:

        logs = 'tfc:wood/log/%s' % wood
        stripped_logs = 'tfc:wood/stripped_log/%s' % wood
        lumber = 'tfc:wood/lumber/%s' % wood
        stripped_woods = 'tfc:wood/stripped_wood/%s' % wood
        woods = 'tfc:wood/wood/%s' % wood

        planks = 'tfc:wood/planks/%s' % wood
        slabs = 'tfc:wood/planks/%s_slab' % wood
        stairs = 'tfc:wood/planks/%s_stairs' % wood
        fences = 'tfc:wood/planks/%s_fence' % wood
        logfences = 'tfc:wood/planks/%s_log_fence' % wood
        gates = 'tfc:wood/planks/%s_fence_gate' % wood
        trapdoors = 'tfc:wood/planks/%s_trapdoor' % wood
        doors = 'tfc:wood/planks/%s_door' % wood
        buttons = 'tfc:wood/planks/%s_button' % wood
        pressureplates = 'tfc:wood/planks/%s_pressure_plate' % wood
        toolracks = 'tfc:wood/planks/%s_tool_rack' % wood
        bookshelves = 'tfc:wood/planks/%s_bookshelf' % wood

        # Planks <-> Lumber
        damage_shapeless('crafting/wood/%s_lumber_logs' % wood, (logs, 'tag!tfc:saws'), (8, lumber))
        damage_shapeless('crafting/wood/%s_planks_to_lumber_planks' % wood, (planks, 'tag!tfc:saws'), (4, lumber))

        # Wood
        rm.crafting_shaped('crafting/wood/%s_wood' % wood, ['XX', 'XX'], logs, (3, woods))
        rm.crafting_shaped('crafting/wood/%s_stripped_wood' % wood, ['XX', 'XX'], stripped_logs, (3, stripped_woods))

        # Plank recipes
        rm.crafting_shaped('crafting/wood/%s_planks' % wood, ['XX', 'XX'], lumber, planks)
        rm.crafting_shaped('crafting/wood/%s_slabs' % wood, ['XXX'], planks, (6, slabs))
        rm.crafting_shaped('crafting/wood/%s_stairs' % wood, ['X  ', 'XX ', 'XXX'], planks, (8, stairs))
        rm.crafting_shaped('crafting/wood/%s_fence' % wood, ['XYX', 'XYX'], {'X': planks, 'Y': lumber}, (8, fences))
        rm.crafting_shaped('crafting/wood/%s_log_fence' % wood, ['XYX', 'XYX'], {'X': logs, 'Y': lumber}, (8, logfences))
        rm.crafting_shaped('crafting/wood/%s_fence_gate' % wood, ['XYX', 'XYX'], {'X': lumber, 'Y': planks}, (2, gates))
        rm.crafting_shaped('crafting/wood/%s_trapdoor' % wood, ['XXX', 'XXX'], lumber, (3, trapdoors))
        rm.crafting_shaped('crafting/wood/%s_door' % wood, ['XX', 'XX', 'XX'], lumber, (2, doors))
        rm.crafting_shaped('crafting/wood/%s_button' % wood, ['X'], planks, buttons)
        rm.crafting_shaped('crafting/wood/%s_pressure_plate' % wood, ['XX'], lumber, pressureplates)
        rm.crafting_shaped('crafting/wood/%s_tool_rack' % wood, ['XXX', '   ', 'XXX'], lumber, toolracks)
        rm.crafting_shaped('crafting/wood/%s_bookshelf' % wood, ['XXX', 'YYY', 'XXX'], {'X': planks, 'Y': 'minecraft:book'}, bookshelves)




