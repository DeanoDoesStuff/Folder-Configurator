class SkuBuilder:
    def process_depth(self, item, depth):
        # Initialize SKU components
        sku_components = ["", "", ""]  # Make ID, Model ID, Year ID
        
        # Traverse up the tree to get the full path
        while item:
            item_text = item.text(0)
            if '=' in item_text:
                id_part, name_part = item_text.split('=')
                if depth == 3:
                    sku_components[2] = id_part  # Year ID
                elif depth == 2:
                    sku_components[1] = id_part  # Model ID
                elif depth == 1:
                    sku_components[0] = id_part  # Make ID
            depth -= 1
            item = item.parent()
        
        return sku_components
    
    # TODO will need to create a system for generating skus for Series and beyond.
    
