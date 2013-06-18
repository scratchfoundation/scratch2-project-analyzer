

def _real_extract_blocks_from_stack(stack):
    for block in stack:
        if isinstance(block, list):
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
