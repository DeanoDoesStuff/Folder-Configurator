class SkuBuilder:
    def process_depth(self, item_text, depth):
        # Handle Make depth
        if depth == 1:
            if '=' in item_text:
                id_part, make_part = item_text.split('=', 1)
                return id_part.strip(), make_part.strip()
            return "", item_text.strip()  # Handle case without '='
        elif depth == 2:
            # Handle Model depth
            if '=' in item_text:
                id_part, model_part = item_text.split('=', 1)
                return id_part.strip(), model_part.strip()
            return "", item_text.strip() # Handle case without '='
        elif depth == 3:
            # Handle Year depth
            if '=' in item_text:
                id_part, model_part = item_text.split('=', 1)
                return id_part.strip(), model_part.strip()
            return "", item_text.strip() # Handle case without '='
        return "", ""
