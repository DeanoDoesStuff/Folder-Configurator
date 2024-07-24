class SkuBuilder:
    def __init__(self):
        self.sku_parts = ['XX']

    def add_part(self, part, depth):
        part_number = part.split('=')[0]
        """
        if depth < len(self.parts):
            self.parts[depth] = part_number"""
    
    def get_sku(self):
        return ''.join(self.parts)
    
    def reset(self):
        self.parts = ['XX'] # Reset parts back to default
    
