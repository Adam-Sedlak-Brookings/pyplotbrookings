from cycler import cycler
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.image as mpimg
import matplotlib.colors 
from matplotlib import font_manager
import numpy as np
import os
import warnings


palettes = {
    'brand1': ('#FF9E1B', '#8AC6FF', '#003A79'),
    'brand2': ('#D0D3D4', '#FF9E1B', '#003A79'),
    'analogous1': ('#8AC6FF', '#003A79'),
    'analogous2': ('#3EB2C6', '#003A79'),
    'contrasting1': ('#FF9E1B', '#003A79'),
    'contrasting2': ('#F5CC00', '#003A79'),
    'semantic1': ('#F75C57', '#59C6DA'),
    'semantic2': ('#E0BB00', '#A00D11', '#1C8090'),
    'semantic3': ('#FFDD00', '#F75C57', '#59C6DA'),
    'pos_neg1': ('#CD1A1C', '#5CA632'),
    'pos_neg2': ('#CD1A1C', '#F5CC00', '#5CA632'),
    'political1': ('#ED3A35', '#1479BB'),
    'political2': ('#F98B83', '#5AADF6'),
    'political3': ('#E0BB00', '#ED3A35', '#1479BB'),
    'political4': ('#FFE926', '#F98B83', '#5AADF6'),
    'categorical': ('#9e0d12ff', '#de60a1ff', '#f5cc05ff',
                    '#fd9d1fff', '#00649fff', '#2599adff'),
    'sequential1': ('#bcdefbff', '#87c4feff', '#56adf6ff',
                    '#2e97eaff', '#1c8ad6ff', '#0f78baff', '#00649fff'),
    'sequential2': ('#fce829ff', '#b1dc44ff', '#6dc960ff',
                    '#2bb275ff', '#009a80ff', '#008080ff', '#0d636fff'),
    'diverging': ('#e02928ff', '#f07867ff', '#f6b5a9ff',
                  '#efefefff', '#b1c5deff', '#739fceff', '#0f78baff'),
    'misc': ('#F5CC00', '#3EB2C6', '#003A79')
}

extended_palettes = {
    'brand blue': ('#022A4E', '#003A70', '#1A4E80', '#326295', '#517EAD', '#7098C3', '#8DADD0', '#A8BDD5', '#DDE5ED'),
    'vivid blue': ('#023147', '#004B6E', '#00649F', '#1479BB', '#1E8AD6', '#3398EA', '#5AADF6', '#8AC6FF', '#BFDFFC'),
    'teal': ('#032B30', '#09484F', '#116470', '#1C8090', '#2A9AAD', '#3EB2C6', '#59C6DA', '#7CD9EA', '#A6E9F5'),
    'green': ('#1A3404', '#294D0A', '#33660F', '#45821B', '#5CA632', '#7DBF52', '#9CD674', '#BDED9D', '#DEF5CC'),
    'yellow': ('#594C09', '#877414', '#C7A70A', '#E0BB00', '#F5CC00', '#FFDD00', '#FFE926', '#FFF170', '#FFF9C2'),
    'orange': ('#663205', '#994B08', '#B85B0A', '#F26D00', '#FF851A', '#FF9E1B', '#FFB24D', '#FEC87F', '#FBD9A5'),
    'red': ('#660507', '#A00D11', '#CD1A1C', '#E22827', '#ED3A35', '#F75C57', '#F98B83', '#FCB0AA', '#FDD7D4'),
    'magenta': ('#510831', '#8D1655', '#A82168', '#BF317B', '#D2468E', '#E160A2', '#EC81B7', '#F5A8CF', '#FAD4E7'),
    'purple': ('#3E2C72', '#533C91', '#6A50AD', '#7C60BF', '#8E72D0', '#9C82D9', '#B59DEA', '#D0BEF5', '#E9E0FC')
}


def set_theme(font_size=14, line_width=1.4, web=False):
    '''
    Sets matplotlib default style parameters to be consistent with
    the Brookings style. 

    font_size (float): A number specifying the base font size of all 
        default plots

    line_width (float): A number specifying the default thickness of all
        lines in plots

    web (bool): If the plot is for a website figure (the background color for 
        the website is an off white requiring a different color)
    '''
    # Reset matplotlib style parameters to the defaults
    mpl.rcdefaults()
    # Setting the background color
    background_color = '#FAFAFA' if web else '#FFFFFF'

    # Dictionary of style features to set
    style_dict = {
        'axes.axisbelow': True,  # Place gride lines behind the plot
        'axes.facecolor': background_color,

        'axes.grid': True,
        'axes.grid.axis': 'y',
        'axes.labelsize': 0.833*font_size,
        'axes.labelweight': 'bold',
        'axes.linewidth': line_width,
        'axes.spines.left': False,
        'axes.spines.right': False,
        'axes.spines.top': False,
        # Set default cycler
        'axes.prop_cycle': mpl.cycler(color=palettes['brand1']),
        'image.cmap': get_cmap('brand blue'),

        'figure.figsize': (8, 4.5),
        'font.size': font_size,

        'grid.color': '#CCCCCC',
        'grid.linestyle': (0, (1, 4)),

        'legend.loc': 'upper center',
        'legend.frameon': False,  # Remove legend border
        'legend.handlelength': 0.75,  # Shorten size of legend key
        'legend.borderaxespad': -1,  # Place legend outside the figure

        'patch.linewidth': 0,

        'ytick.left': False,
        'ytick.labelsize': 0.833*font_size,
        'xtick.labelsize': 0.833*font_size,
    }
    # Apply all styles
    for key, value in style_dict.items():
        mpl.rcParams[key] = value


def add_title(title=None, subtitle=None, tag=None, source=None, notes=None,
              title_pad=0, source_pad=0, text_pad=0, x_offset=None, src_note_gap=0):
    '''
    Adds titles and foot notes to the current figure.

    title (str): The title of the plot. Title should be short

    subtitle (str): The subtitle of the plot. Subtitle can be longer and
         add description to the figure 

    tag (str): The figure name/number plotted above the titles

    source (str): String citing any data sources used to create the figure.
        Text is added to the bottom of the figure.

    notes (str): Any notes authors may wish to include at the bottom 
        of the figure.

    title_pad (float): Number specifying additional amount of spacing to add
        between the top of the figure and first title

    source_pad (float): Number specifying additional amount of spacing to add
        between the bottom of the figure and the source text or notes

    text_pad (float): Number specifying additional amount of spacing to add
        between lines of text. May be necessary if a different figure size is used.

    x_offset (float): The amount of additional space to offset the title and notes text
        in the x direction (useful if y labels are long) 

    src_note_gap (float): The additional amount of white space between the source 
        text and the notes text.
    '''
    # Get the font size
    font_size = mpl.rcParams['font.size']

    # y value origin for titles
    title_0 = 0.95 + title_pad/100
    # x value origin for source and note text
    source_0 = -font_size*0.006 - source_pad/100
    # Padding to use between titles
    text_pad = 0.0038 + text_pad/10000

    # Initialize offsets for spacing figure titles apart
    top_offset, bottom_offset = 0, 0

    # If there is no specified x_offset parse the figures y axis
    # labels for the longest string and shift text as needed
    if x_offset is None:
        y_labels = plt.gca().get_yticklabels()
        x_offset = -max([len(s.get_text()) for s in y_labels]) / 140

    if subtitle:
        plt.figtext(0.05+x_offset, title_0, subtitle, size=font_size)
        # Parse subtitle for the number of lines
        n_lines = len(subtitle.split('\n'))
        # Increment next titles vertical offset if text was added
        top_offset += font_size * n_lines * text_pad

    if title:
        plt.figtext(0.05+x_offset, title_0+top_offset, title,
                    size=1.2*font_size, color='#003A79', weight='bold')
        # Increment next titles vertical offset if text was added
        top_offset += font_size * text_pad * 1.2

    if tag:
        plt.figtext(0.05+x_offset, title_0+top_offset, tag,
                    # Increment next titles vertical offset if text was added
                    size=0.8*font_size, color='#003A79', weight='light')

    if source:
        plt.figtext(0.05+x_offset, source_0,
                    r"$\bf{Source:}$ " + source, size=0.8*font_size, color="#666666")
        # Increment the notes vertical offset if text was added
        bottom_offset += font_size * text_pad * 0.8 + src_note_gap

    if notes:
        plt.figtext(0.05+x_offset, source_0 - bottom_offset,
                    r"$\bf{Notes:}$ " + notes, size=0.8*font_size, color="#666666")


def add_logo(logo_path, offsets=(0, 0), scale=0.25):
    '''
    Adds a logo to the bottom right of a figure

    logo_path (str): Path to a local file path or an abbreviation for one
         of the package supported logos (see documentation below for more 
         details on supported logos)

    offsets (tuple): Tuple with the X, Y offsets for a figure (in fraction 
        of the figure size)

    scale (float): Scale factor to set the logo size

    Complete list of supported logos abbreviations:
        bc: Brown Center
        bi: Bass Initiative on Innovation and Placemaking
        brookings: Brookings Institution
        cc: China Center
        ccf: Center on Children and Families
        ceaps: Center for East Asia Policy Studies
        cepm: Center for Effective Policy Management 
        chp: Center for Health Policy
        cmep: Center for Middle Eastern Policy
        crm: Center on Regulation and Markets
        csd: Center for Sustainable Development
        cti: Center for Technology Innovation
        cue: Center for Universal Education
        cuse: Center on United States and Europe
        es: Economic Studies 
        fp: Foreign Policy
        global: Global Studies 
        gs: Governance Studies
        hc: Hutchins Center
        metro: Metropolitan Policy Studies
        thp: The Hamilton Project
    '''
    dx, dy = offsets
    font_size = mpl.rcParams['font.size']
    # Map of logo position names to coordinates
    logo_loc = [0.65+dx, -0.12+dy-font_size*0.006, scale, 0.2]

    # List of supported logos
    supported_logos = ["bc", "bi", "brookings", "cc", "ccf", "ceaps", "cepm", "chp", "cmep", "crm", "csd",
                       "cti", "cue", "cuse", "es", "fp", "global", "gs", "hc", "metro", "thp"]

    # Updating string to directory path if using a supported logo
    if logo_path in supported_logos:
        cwd = os.getcwd()
        path = os.path.join(cwd, 'logos')
        logo_path = os.path.join(path, logo_path + '.png')

    try:
        # Read the image
        logo = mpimg.imread(logo_path)

    except FileNotFoundError:
        # Throw error listing valid logo names
        raise Exception('No such file or directory: "' + str(logo_path)
                        + '" Check your path or try one of the following: ' + str(supported_logos))

    # Get current figure
    fig = plt.gcf()
    # Add an axis for the logo plot
    ax = fig.add_axes(logo_loc, zorder=1)

    # Add logo to new axis and turn off axis labeling
    ax.imshow(logo)
    ax.axis('off')


def get_cmap(name, reverse=False):
    '''
    Given a color map name returns a Brookings theme color maps.

    name (str): Name of the color map from either the color palette or 
        extended color palette.

    reverse (bool): If the color map should be reversed
    '''
    # Valid color palettes from ggbrookings palette 
    gg_palettes = ['diverging', 'sequential1', 'sequential2', 'political1', 
            'political2', 'contrasting1', 'contrasting2']

    # All valid color maps
    valid_palettes = gg_palettes + list(extended_palettes.keys())
    # If name is invalid throw an error
    if name not in valid_palettes:
        raise Exception('No such palette "' + name + '"  Try one of the following: ' + str(valid_palettes))

    # Get the colors from the correct dictionary
    if name in gg_palettes:
        colors = palettes[name]
    else:
        colors = extended_palettes[name]

    # Reverse colors if needed
    if reverse:
        colors = colors[::-1]

    # Return a color map over the list of colors
    return matplotlib.colors.LinearSegmentedColormap.from_list("", colors)


def set_palette(name, ax=None, reverse=False):
    '''
    Sets the a color palette cycler for the current axis

    name (str): Name of the Brookings color palette

    ax: Optional matplotlib axis object to specify which axis to apply 
        the color palette to

    reverse (bool): If the color palette should be reversed
    '''

    # Check if there's a key for the user palette name
    try:
        palette = palettes[name]

    # Throw error with all palette names if there's no key value pair
    except KeyError:
        raise Exception(
            '"' + str(name)+'" is not a valid color palette. Try one of the following: ' + str(list(palettes.keys())))

    # pos_neg color palettes are not good for RG color blindness
    if name in ['pos_neg1', 'pos_neg2']:
        warnings.warn("This palette is accessible but NOT contrasting for people with color red-green blindness.")
    
    # Reverse the palette if specified
    if reverse:
            palette = palette[::-1]

    # Get current axis if not specified
    if not ax:
        ax = plt.gca()

    # Create a cycler for the selected color palette
    palette_cycler = cycler(color=palette)
    # Set the cycler as base for the current/given axis
    ax.set_prop_cycle(palette_cycler)


def text_color(hexcolor):
    '''
    Returns recommended color of text (either black or white) 
    to use with the given hexcolor as a background color. Color
    selection is adherent to W3C guidelines. 
    
    hexcolor (str): String of a hexidecimal color
    
    @Source: Mark Ransom (https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color)
    '''
    # Convert hexcolor code to RGB
    rgb_color = list(int(hexcolor[i:i+2], 16) for i in (1, 3, 5))
    
    # Adjusting RGB values
    rgb_new = []
    for c in rgb_color:
        c = c / 255.0
        if c <= 0.04045:
            c = c/12.92 
        else:
            c = ((c+0.055)/1.055) ** 2.4
        rgb_new.append(c)
    # Getting color luminosity
    L = 0.2126 * rgb_new[0] + 0.7152 * rgb_new[1] + 0.0722 * rgb_new[2]
    
    # Return black or white depending on color luminosity
    return '#000000' if L > 0.179 else '#FFFFFF'


def view_palette(name):
    '''
    Given a color palette (base or extended) creates a preview of the palette
    '''

    # All valid color maps
    valid_palettes = list(palettes.keys()) + list(extended_palettes.keys())
    
    # If name is invalid throw an error
    if name not in valid_palettes:
        raise Exception('No such palette "' + name + '"  Try one of the following: ' + str(valid_palettes))
    
    # Otherwise get the correct color
    if name in palettes.keys():
        palette = palettes[name]
        
    elif name in extended_palettes.keys():
        palette = extended_palettes[name]
    
    # Cast color to an array
    palette = np.array(palette)
    
    # Number of columns in the final figure 
    cols = int(np.ceil(len(palette)/2))
    
    # Reshape the data into a 2D image
    data = np.arange(2*cols).reshape(2, cols)
    
    # Append white "squares" to the end of the color map 
    palette_extended = np.append(palette, np.repeat('#FFFFFF', len(palette) % 2))
    
    # Create a color map
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", palette_extended)
    # Plot the image
    plt.imshow(data, cmap=cmap)
    
    # Counter for the order of the colors
    k = 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            
            
            # If the palette is white breakout of labeling the colors
            if k >= len(palette):
                break

            # Get the correct text color
            color = text_color(palette[k])

            # Plot text on top of the palette color with the correct color
            # showing the hexcode and palette order number
            plt.text(j, i, str(k + 1) + '\n' + palette[k].upper(),
                           ha="center", va="center", color=color)
            # Increase the counter
            k += 1
    
    plt.axis('off')
    plt.show()


def import_roboto():
    '''
    Import the Roboto font and add it as the default font family
    '''
    cwd = os.getcwd()
    font_files = font_manager.findSystemFonts(fontpaths=cwd, fontext="ttf")

    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)
        
    mpl.rcParams['font.family'] = 'Roboto'


def figure(size):
    '''
    Create a figure using one of the standard Brookings sizes
    '''
    sizes = {'small': (3.25, 2), 'medium':(6.5, 4), 'large':(9, 6.5)}

    # If name is invalid throw an error
    if size not in sizes.keys():
        raise Exception("Size must be one of 'small', 'medium', or 'large'")

    return plt.figure(figsize=sizes[size])


def save(filename, dpi):
    '''
    Save a plot using standard Brookings DPI values
    '''
    dpi_dict = {"retina": 320, "print": 300, "screen": 72}

    # If name is invalid throw an error
    if dpi not in dpi_dict.keys():
        raise Exception("DPI must be one of 'retina', 'print', or 'screen'")
    
    plt.savefig(filename, dpi=dpi_dict[dpi])
