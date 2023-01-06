from cycler import cycler
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.image as mpimg
import matplotlib.colors 
import os
import warnings

pallets = {
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

extended_pallets = {
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

        'figure.figsize': (8, 4.5),
        'font.size': font_size,

        'grid.color': '#CCCCCC',
        'grid.linestyle': (0, (1, 4)),

        'legend.loc': 'upper center',
        'legend.frameon': False,  # Remove legend border
        'legend.handlelength': 0.75,  # Shorten size of legend key
        'legend.borderaxespad': -1,  # Place legend outside the figure

        'ytick.left': False,
        'ytick.labelsize': 0.833*font_size,
        'xtick.labelsize': 0.833*font_size,
    }
    # Apply all styles
    for key, value in style_dict.items():
        mpl.rcParams[key] = value


def add_title(title=None, subtitle=None, tag=None, source=None, notes=None,
              title_pad=0, source_pad=0, text_pad=0):
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

    if subtitle:
        plt.figtext(0.05, title_0, subtitle, size=font_size)
        # Increment next titles vertical offset if text was added
        top_offset += font_size * text_pad

    if title:
        plt.figtext(0.05, title_0+top_offset, title,
                    size=1.2*font_size, color='#003A79', weight='bold')
        # Increment next titles vertical offset if text was added
        top_offset += font_size * text_pad * 1.2

    if tag:
        plt.figtext(0.05, title_0+top_offset, tag,
                    # Increment next titles vertical offset if text was added
                    size=0.8*font_size, color='#003A79', weight='light')

    if source:
        plt.figtext(0.05, source_0,
                    r"$\bf{Source:}$ " + source, size=0.8*font_size, color="#666666")
        # Increment the notes vertical offset if text was added
        bottom_offset += font_size * text_pad * 0.8

    if notes:
        plt.figtext(0.05, source_0 - bottom_offset,
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

    name (str): Name of the color map from either the color pallet or 
        extended color pallet.

    reverse (bool): If the color map should be reversed
    '''
    # Valid color pallets from ggbrookings pallet 
    gg_pallets = ['diverging', 'sequential1', 'sequential2', 'political1', 
            'political2', 'contrasting1', 'contrasting2']

    # All valid color maps
    valid_pallets = gg_pallets + list(extended_pallets.keys())
    # If name is invalid throw an error
    if name not in valid_pallets:
        raise Exception('No such pallet "' + name + '"  Try one of the following: ' + str(valid_pallets))

    # Get the colors from the correct dictionary
    if name in gg_pallets:
        colors = pallets[name]
    else:
        colors = extended_pallets[name]

    # Reverse colors if needed
    if reverse:
        colors = colors[::-1]

    # Return a color map over the list of colors
    return matplotlib.colors.LinearSegmentedColormap.from_list("", colors)


def set_pallet(name, ax=None, reverse=False):
    '''
    Sets the a color pallet cycler for the current axis

    name (str): Name of the Brookings color pallet

    ax: Optional matplotlib axis object to specify which axis to apply 
        the color pallet to

    reverse (bool): If the color pallet should be reversed
    '''

    # Check if there's a key for the user pallet name
    try:
        pallet = pallets[name]

    # Throw error with all pallet names if there's no key value pair
    except KeyError:
        raise Exception(
            '"' + str(name)+'" is not a valid color pallet. Try one of the following: ' + str(list(pallets.keys())))

    # pos_neg color pallets are not good for RG color blindness
    if 'pos_neg' in name:
        warnings.warn(
            "This pallet is not high contrast for people color blindness (specifically protanopia and deuteranopia), please avoid using")
    
    # Reverse the pallet if specified
    if reverse:
            pallet = pallet[::-1]

    # Get current axis if not specified
    if not ax:
        ax = plt.gca()

    # Create a cycler for the selected color pallet
    pallet_cycler = cycler(color=pallet)
    # Set the cycler as base for the current/given axis
    ax.set_prop_cycle(pallet_cycler)
