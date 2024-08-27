#Companions

companion_dict_data = {
    "01=CLASSIC": {
        ("1=FRONT", "1=W.I.Y.KIT", "1=MILD STEEL", "1=STANDARD"): {
            "1=FRAME MOUNT OPTIONS": {
                "type-variable": ["C=CUSTOM"],
                "selections": [
                    {"selection_1": "1=INCLUDED", "selection_2": "0=NONE"}
                ]
            },
            "2=CENTER OPTIONS": {
                "type-variable": ["1=STANDARD", "2=MOD", "3=34", "C=CUSTOM"],
                "selections": [
                    {"selection_1": "1=STANDARD", "selection_2": "0=NONE"},
                    {"selection_1": "1=STANDARD", "selection_2": "1=LOGO RELOCATED"},
                    {"selection_1": "1=STANDARD", "selection_2": "2=CUSTOM TEXT"},
                    # Add other selection combinations here
                ]
            },
            "8=W2 OPTIONS": {
                "type-variable": ["C=CUSTOM"],
                "selections": [
                    {"selection_1": "N/A", "selection_2": "N/A"}
                ]
            },
            "4=MID PROTECTION OPTIONS": {
                "type-variable": ["1=UNIVERSAL"],
                "selections": [
                    {"selection_1": "1=STANDARD", "selection_2": "0=NONE"}
                ]
            },
            "5=FULL PROTECTION OPTIONS": {
                "type-variable": ["C=CUSTOM"],
                "selections": [
                    {"selection_1": "2=1.5IN STANDARD FULL GRILLE", "selection_2": "0=NONE"},
                    {"selection_1": "2=1.5IN STANDARD FULL GRILLE", "selection_2": "W=W2"},
                    {"selection_1": "2=2IN STANDARD FULL GRILLE", "selection_2": "0=NONE"},
                    {"selection_1": "2=2IN STANDARD FULL GRILLE", "selection_2": "W=W2"}
                ]
            },
            "6=CLEVIS MOUNTS OPTIONS": {
                "type-variable": ["1=UNIVERSAL", "0=NONE"],
                "selections": [
                    {"selection_1": "1=INCLUDED", "selection_2": "0=NONE"}
                ]
            }
        },
        ("1=FRONT", "1=W.I.Y.KIT", "1=MILD STEEL", "2=OFFROAD"): {
            "1=FRAME MOUNT OPTIONS": {
                "type-variable": ["C=CUSTOM"],
                "selections": [
                    {"selection_1": "1=INCLUDED", "selection_2": "0=NONE"}
                ]
            },
            "2=CENTER OPTIONS": {
                "type-variable": ["1=STANDARD", "2=MOD", "3=34", "C=CUSTOM"],
                "selections": [
                    {"selection_1": "1=STANDARD", "selection_2": "0=NONE"},
                    {"selection_1": "1=STANDARD", "selection_2": "1=LOGO RELOCATED"},
                    {"selection_1": "2=20 IN LIGHT BAR", "selection_2": "0=NONE"},
                    {"selection_1": "3=30 IN LIGHT BAR", "selection_2": "0=NONE"}
                ]
            }
        }
    }
}


uni_part_groups = {
    "011111-2": [
        {"1=STANDARD", "0=NONE"},
        {"1=STANDARD", "1=LOGO RELOCATED"},
        {"1=STANDARD", "2=CUSTOM TEXT"},
        {"1=STANDARD", "4=MOUNTAIN"},
        {"1=STANDARD", "5=FISH"},
        {"1=STANDARD", "6=MILITARY"},
        {"1=STANDARD", "7=U.S. FLAG"},
        {"1=STANDARD", "8=CIRCLES"},
        {"1=STANDARD", "9=ANTLERS"},
        {"1=STANDARD", "A=HORNS"},
        {"1=STANDARD", "B=STARS"},
        {"2=20 IN LIGHT BAR", "0=NONE"},
        {"2=20 IN LIGHT BAR", "1=LOGO RELOCATED"},
        {"3=30 IN LIGHT BAR", "0=NONE"},
        {"3=30 IN LIGHT BAR", "1=LOGO RELOCATED"}
    ],
    "011111-4": [
        {"2=1.5 IN BULL BAR", "0=NONE"},
        {"3=2 IN BULL BAR", "0=NONE"},
        {"4=2.5 IN BULL BAR", "0=NONE"},
        {"5=SQUARE FORCE", "0=NONE"},
        {"6=TUBULAR SPORT", "0=NONE"},
        {"7=1.5 IN PRERUNNER", "0=NONE"},
        {"8=2 IN PRERUNNER", "0=NONE"},
        {"9=2.5 IN PRERUNNER", "0=NONE"}
    ],
    "011111-6": [
        {"1=INCLUDED"}
    ]
}

