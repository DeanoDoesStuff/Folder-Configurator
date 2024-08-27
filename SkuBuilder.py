# SkuBuilder.py
class SkuBuilder:
    def process_depth(self, item, depth):
        # Initialize SKU components
        sku_components = ["", "", "", "", "", "", "", ""]  # Make ID, Model ID, Year ID, Series ID, Location ID
        
        # Traverse up the tree to get the full path
        while item:
            item_text = item.text(0)
            if '=' in item_text:
                id_part, name_part = item_text.split('=')
                if depth == 8:
                    sku_components[7] = id_part # Package ID
                elif depth == 7:
                    sku_components[6] = id_part # Material ID
                elif depth == 6:
                    sku_components[5] = id_part # Fabrication ID
                elif depth == 5:
                    sku_components[4] = id_part # Location ID
                elif depth == 4:
                    sku_components[3] = id_part # Series ID
                elif depth == 3:
                    sku_components[2] = id_part  # Year ID
                elif depth == 2:
                    sku_components[1] = id_part  # Model ID
                elif depth == 1:
                    sku_components[0] = id_part  # Make ID
            depth -= 1
            item = item.parent()
        
        return sku_components
    
    # TODO will need to create a system for generating skus for Series and beyond.
    def build_sku(self, sku_componenets):
        return ''.join(sku_componenets)
    
    def process_kit_sku(clicked_button):
        current_sku = ""
        clicked_button_id = clicked_button.text()

        if "=" in clicked_button_id: # Checks for special character found in clicked_button_id string
            id_part = clicked_button_id.split("=") # Split string at found special character
            current_sku = id_part # Assign the returned variable to the formatted string id_part
        return current_sku # Return id data extracted from the button

    # Handle processing of product SKU -- MMY and KIT SKU combined

    def process_product_sku(clicked_button):
        # Initilize the variables used in this function
        current_sku = ""
        full_id = []

        clicked_button_id = clicked_button.text()
        # Format sub series string to remove -> the process the string normally
        if "->" in clicked_button_id: # Checks instances of special characters in button string
            # Removes special characters and assigns to formatted string
            format_id = clicked_button_id.split("->") 
            # Create a for loop to iterate through format ID list and extract all data before = character
            for entry in format_id:
                if "=" in entry: # Checks for special character at each entry in format_id list
                    id_part = entry.split("=")  # Split the strings at the special character
                    full_id.append(id_part[0]) # Extracts the first value from every pair found in id_part
            current_sku = "".join(full_id)
                
        return current_sku
        


    def format_sku(self, sku_label):
        
        sku_str = sku_label.text()
        if ":" in sku_str:
            sku_tuple = sku_str.split(":")
            print("SKU Split: ", sku_tuple)
            sku_str = sku_tuple[1]
            print("SKU String: ", sku_str)
        return sku_str
        sku_len = len(sku_str)
        print("SKU Len: ", sku_len)

        
