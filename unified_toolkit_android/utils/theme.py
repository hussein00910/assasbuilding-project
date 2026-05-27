"""
Color theme and style helpers for the app.
Dark hacker aesthetic with neon accent colors.
"""

# Background colors
BG_DARK    = (0.05, 0.05, 0.08, 1)   # Main background
BG_CARD    = (0.08, 0.08, 0.12, 1)   # Card/panel bg
BG_INPUT   = (0.1, 0.1, 0.15, 1)     # TextInput bg

# Accent colors per category
CAT_COLORS = {
    'recon':       (0.0,  0.8,  1.0,  1),   # Cyan
    'scanning':    (1.0,  0.5,  0.0,  1),   # Orange
    'exploitation':(1.0,  0.15, 0.15, 1),   # Red
    'passwords':   (0.8,  0.0,  1.0,  1),   # Purple
    'web':         (0.0,  1.0,  0.5,  1),   # Green
    'phishing':    (1.0,  0.8,  0.0,  1),   # Yellow
    'wireless':    (0.2,  0.6,  1.0,  1),   # Blue
    'network':     (0.0,  1.0,  1.0,  1),   # Teal
    'forensics':   (0.6,  0.9,  0.0,  1),   # Lime
}

# Text colors
TEXT_PRIMARY   = (0.95, 0.95, 0.95, 1)
TEXT_SECONDARY = (0.6,  0.6,  0.7,  1)
TEXT_SUCCESS   = (0.0,  1.0,  0.5,  1)
TEXT_ERROR     = (1.0,  0.3,  0.3,  1)
TEXT_WARNING   = (1.0,  0.8,  0.0,  1)

# Button sizes
BTN_HEIGHT  = '56dp'
BTN_RADIUS  = [12, 12, 12, 12]

FONT_TITLE  = '22sp'
FONT_BODY   = '15sp'
FONT_SMALL  = '13sp'
FONT_MONO   = '13sp'  # for output


def category_color(cat_name: str):
    """Return RGBA tuple for a category name (lowercase key)."""
    return CAT_COLORS.get(cat_name.lower(), (0.5, 0.5, 0.5, 1))
