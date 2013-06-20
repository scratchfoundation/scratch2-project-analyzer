def __tupleit(l):
    return tuple(map(__tupleit, l)) if isinstance(l, (list, tuple)) else l

def _real_extract_blocks_from_stack(stack):
    for block in stack:
        if isinstance(block, list) and block:
            if isinstance(block[0], str): # Got a primitive
                yield block
                for item in _real_extract_blocks_from_stack(block[1:]):
                    yield item
            else: # Inside a sequence
                for item in _real_extract_blocks_from_stack(block):
                    yield item


def extract_blocks_from_script(script):
    '''
    Returns a flattened list of blocks used in the stack.
    Includes all arguments passed to the block.
    '''
    blocks = []
    blocknames = []
    blocks = list(_real_extract_blocks_from_stack(script[2]))
    return blocks

def compare_projects(project1, project2):
    '''
    Compares two project objects (or they can be revisions).
    Comparison is done between scripts and assets.

    Returns: List of changes to sprites and assets.
    '''

    blocks = [[],[]]
    assets = [[],[]]

    i = 0
    for p in [project1, project2]:
        for sprite in p.sprites:
            try:
                for script in sprite.scripts:
                    blocks[i].extend(extract_blocks_from_script(script))
            except AttributeError:
                pass
            sounds = [x.md5 for x in sprite.sounds]
            images = [x.baseLayerMD5 for x in sprite.costumes]
            assets[i] = sounds + images
        i += 1

    block_diff = set(__tupleit(blocks[0])) ^ set(__tupleit(blocks[1]))
    asset_diff = set(assets[0]) ^ set(assets[1])

    return {'block_diff' : block_diff, 'asset_diff' : asset_diff}



