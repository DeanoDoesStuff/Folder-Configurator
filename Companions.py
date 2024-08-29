#Companions

companion_dict_data = {
    "01=CLASSIC": { # SERIES
        ("1=FRONT", "1=W.I.Y.KIT", "1=MILD STEEL", "1=STANDARD"): { #SUB SERIES
            "1=FRAME MOUNT OPTIONS": {
                "type-variable": ["C=CUSTOM"],
                "selections": [
                    {"selection_1": "1=INCLUDED", "selection_2": "0=NONE"}
                ]
            },
            "2=CENTER OPTIONS": { # COMPANION
                "type-variable": ["1=STANDARD", "2=MOD", "3=34", "C=CUSTOM"],
                "selections": [
                    {"selection_1": "1=STANDARD", "selection_2": "0=NONE"},
                    {"selection_1": "1=STANDARD", "selection_2": "1=LOGO RELOCATED"},
                    {"selection_1": "1=STANDARD", "selection_2": "2=CUSTOM TEXT"},
                    {"selection_1": "1=STANDARD", "selection_2": "4=MOUNTAIN"},
                    {"selection_1": "1=STANDARD", "selection_2": "5=FISH"},
                    {"selection_1": "1=STANDARD", "selection_2": "6=MILITARY"},
                    {"selection_1": "1=STANDARD", "selection_2": "7=U.S. FLAG"},
                    {"selection_1": "1=STANDARD", "selection_2": "8=CIRCLES"},
                    {"selection_1": "1=STANDARD", "selection_2": "9=ANTLERS"},
                    {"selection_1": "1=STANDARD", "selection_2": "A=HORNS"},
                    {"selection_1": "1=STANDARD", "selection_2": "B=STARS"},
                    {"selection_1": "2=20 IN LIGHT BAR", "selection_2": "0=NONE"},
                    {"selection_1": "2=20 IN LIGHT BAR", "selection_2": "1=LOGO RELOCATED"},
                    {"selection_1": "3=30 IN LIGHT BAR", "selection_2": "0=NONE"},
                    {"selection_1": "3=30 IN LIGHT BAR", "selection_2": "1=LOGO RELOCATED"}
                ]
            },
            "8=W2 OPTIONS": { # COMPANION
                "type-variable": ["C=CUSTOM"],
                "selections": [
                    {"selection_1": "1=INCLUDED", "selection_2": "NONE"}
                ]
            },
            "4=MID PROTECTION OPTIONS": { # COMPANION
                "type-variable": ["1=UNIVERSAL"],
                "selections": [
                    {"selection_1": "1=STANDARD", "selection_2": "0=NONE"}
                ]
            },
            "5=FULL PROTECTION OPTIONS": { # COMPANION
                "type-variable": ["C=CUSTOM"],
                "selections": [
                    {"selection_1": "2=1.5IN STANDARD FULL GRILLE", "selection_2": "0=NONE"},
                    {"selection_1": "2=1.5IN STANDARD FULL GRILLE", "selection_2": "W=W2"},
                    {"selection_1": "2=2IN STANDARD FULL GRILLE", "selection_2": "0=NONE"},
                    {"selection_1": "2=2IN STANDARD FULL GRILLE", "selection_2": "W=W2"}
                ]
            },
            "6=CLEVIS MOUNTS OPTIONS": { # COMPANION
                "type-variable": ["1=UNIVERSAL", "0=NONE"],
                "selections": [
                    {"selection_1": "1=INCLUDED", "selection_2": "0=NONE"}
                ]
            }
        },

        ("1=FRONT", "1=W.I.Y.KIT", "1=MILD STEEL", "2=OFFROAD"): { # SUB SERIES
            "1=FRAME MOUNT OPTIONS": {
                "type-variable": ["C=CUSTOM"],
                "selections": [
                    {"selection_1": "1=INCLUDED", "selection_2": "0=NONE"}
                ]
            },
            "2=CENTER OPTIONS": { # COMPANION
                "type-variable": ["1=STANDARD", "2=MOD", "3=34", "C=CUSTOM"],
                "selections": [
                    {"selection_1": "1=STANDARD", "selection_2": "0=NONE"},
                    {"selection_1": "1=STANDARD", "selection_2": "1=LOGO RELOCATED"},
                    {"selection_1": "2=20 IN LIGHT BAR", "selection_2": "0=NONE"},
                    {"selection_1": "3=30 IN LIGHT BAR", "selection_2": "0=NONE"}
                ]
            },
            "6=CLEVIS MOUNTS OPTIONS": { # COMPANION
                "type-variable": ["1=UNIVERSAL", "0=NONE"],
                "selections": [
                    {"selection_1": "1=INCLUDED", "selection_2": "0=NONE"}
                ]
            }
        },
        ("1=FRONT", "2=PREFABRICATED", "1=MILD STEEL", "1=STANDARD"): {
            "1=FRAME MOUNT OPTIONS": {
                "type-variable": ["C=CUSTOM"],
                "selections": [
                    {"selection_1": "1=INCLUDED", "selection_2": "0=NONE"}
                ]
            },
            "2=CENTER OPTIONS": {
                "type-variable": ["C=CUSTOM"],
                "selections": [
                    {"selection_1": "1=INCLUDED", "selection_2": "0=NONE"}
                ]
            }
        },
        ("2=REAR", "1=W.I.Y.KIT", "1=MILD STEEL", "1=STANDARD"): {
            "1=FRAME MOUNT OPTIONS": {
                "type-variable": ["C=CUSTOM"],
                "selections": [
                    {"selection_1": "1=INCLUDED", "selection_2": "0=NONE"}
                ]
            }
        }
    }
}


uni_part_groups = {
    "011111-2": [ # CLASSIC->FRONT->W.I.Y.KIT->MILD STEEL->STANDARD->CENTER OPTIONS
        ["1=STANDARD", "0=NONE"],
        ["1=STANDARD", "1=LOGO RELOCATED"],
        ["1=STANDARD", "2=CUSTOM TEXT"],
        ["1=STANDARD", "4=MOUNTAIN"],
        ["1=STANDARD", "5=FISH"],
        ["1=STANDARD", "6=MILITARY"],
        ["1=STANDARD", "7=U.S. FLAG"],
        ["1=STANDARD", "8=CIRCLES"],
        ["1=STANDARD", "9=ANTLERS"],
        ["1=STANDARD", "A=HORNS"],
        ["1=STANDARD", "B=STARS"],
        ["2=20 IN LIGHT BAR", "0=NONE"],
        ["2=20 IN LIGHT BAR", "1=LOGO RELOCATED"],
        ["3=30 IN LIGHT BAR", "0=NONE"],
        ["3=30 IN LIGHT BAR", "1=LOGO RELOCATED"]
    ],
    "011111-4": [ # CLASSIC->FRONT->W.I.Y.KIT->MILD STEEL->MID PROTECTION OPTIONS
        ["2=1.5 IN BULL BAR", "0=NONE"],
        ["3=2 IN BULL BAR", "0=NONE"],
        ["4=2.5 IN BULL BAR", "0=NONE"],
        ["5=SQUARE FORCE", "0=NONE"],
        ["6=TUBULAR SPORT", "0=NONE"],
        ["7=1.5 IN PRERUNNER", "0=NONE"],
        ["8=2 IN PRERUNNER", "0=NONE"],
        ["9=2.5 IN PRERUNNER", "0=NONE"]
    ],
    "011111-6": [ # CLASSIC->FRONT->W.I.Y.KIT->MILD STEEL->STANDARD->CLEVIS MOUNTS
        ["1=INCLUDED"]
    ],
    "011112-2": [ # CLASSIC->FRONT->W.I.Y.KIT->MILD STEEL->OFFROAD->CENTER OPTIONS
        ["1=STANDARD", "0=NONE"],
        ["1=STANDARD", "1=LOGO RELOCATED"],
        ["1=STANDARD", "2=CUSTOM TEXT"],
        ["1=STANDARD", "4=MOUNTAIN"],
        ["1=STANDARD", "5=FISH"],
        ["1=STANDARD", "6=MILITARY"],
        ["1=STANDARD", "7=U.S. FLAG"],
        ["1=STANDARD", "8=CIRCLES"],
        ["1=STANDARD", "9=ANTLERS"],
        ["1=STANDARD", "A=HORNS"],
        ["1=STANDARD", "B=STARS"],
        ["2=20 IN LIGHT BAR", "0=NONE"],
        ["2=20 IN LIGHT BAR", "1=LOGO RELOCATED"],
        ["3=30 IN LIGHT BAR", "0=NONE"],
        ["3=30 IN LIGHT BAR", "1=LOGO RELOCATED"]
    ],
    "011112-6": [ # CLASSIC->FRONT->W.I.Y.KIT->MILD STEEL->OFFROAD->CLEVIS MOUNTS
    ["1=INCLUDED"]
    ],
}
