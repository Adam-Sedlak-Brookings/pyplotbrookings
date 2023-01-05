import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.image as mpimg
from cycler import cycler
import os
import warnings

pallets = {
    'brand1':('#FF9E1B', '#8AC6FF', '#003A79'),
    'brand2':('#D0D3D4', '#FF9E1B', '#003A79'),
    'analogous1':('#8AC6FF', '#003A79'),
    'analogous2':('#3EB2C6', '#003A79'),
    'contrasting1':('#FF9E1B', '#003A79'),
    'contrasting2':('#F5CC00', '#003A79'),
    'semantic1':('#F75C57', '#59C6DA'),
    'semantic2':('#E0BB00', '#A00D11', '#1C8090'),
    'semantic3':('#FFDD00', '#F75C57', '#59C6DA'),
    'pos_neg1':('#CD1A1C', '#5CA632'),
    'pos_neg2':('#CD1A1C', '#F5CC00', '#5CA632'),
    'political1':('#ED3A35', '#1479BB'),
    'political2':('#F98B83', '#5AADF6'),
    'political3':('#E0BB00', '#ED3A35', '#1479BB'),
    'political4':('#FFE926', '#F98B83', '#5AADF6'),
    'categorical':('#9e0d12ff', '#de60a1ff', '#f5cc05ff', '#fd9d1fff', '#00649fff', '#2599adff'),
    'sequential1':('#bcdefbff', '#87c4feff', '#56adf6ff', '#2e97eaff', '#1c8ad6ff', '#0f78baff', '#00649fff'),
    'sequential2':('#fce829ff', '#b1dc44ff', '#6dc960ff', '#2bb275ff', '#009a80ff', '#008080ff', '#0d636fff'),
    'diverging':('#e02928ff', '#f07867ff', '#f6b5a9ff', '#efefefff', '#b1c5deff',' #739fceff', '#0f78baff'),
    'misc':('#F5CC00', '#3EB2C6', '#003A79')
}

#TODO: Add extended pallets
#extended_pallets = {}
    

def set_theme(base_size=14, line_width=1.4, web=False):
    '''
    
    
    '''
    #Reset matplot style parameters to the defauls
    mpl.rcdefaults()
    # Setting the background color
    background_color = '#FAFAFA' if web else '#FFFFFF'
    
    # Dictonary of style features to set
    style_dict = {
        'axes.axisbelow': True, # Place gride lines behind the plot
        'axes.facecolor': background_color,
        
        'axes.grid': True,
        'axes.grid.axis': 'y',
        'axes.labelsize': 0.833*base_size,
        'axes.labelweight': 'bold',
        'axes.linewidth': line_width,
        'axes.spines.left': False,
        'axes.spines.right': False,
        'axes.spines.top': False,
        
        'figure.figsize': (8, 4.5),
        'font.size': base_size, 
        
        'grid.color': '#CCCCCC',
        'grid.linestyle': (0, (1, 4)),
        
        'legend.loc': 'upper center',
        'legend.frameon': False, # Remove legend border
        'legend.handlelength': 0.75, # Shorten size of legend key
        'legend.borderaxespad': -1, # Place legend outside the figure
        
        'ytick.left': False,
        'ytick.labelsize': 0.833*base_size,
        'xtick.labelsize': 0.833*base_size,
    }
    # Apply all styles
    for key, value in style_dict.items():
        mpl.rcParams[key] = value


def add_title(title=None, subtitle=None, tag=None, source=None, notes=None, title_pad=0, source_pad=0, text_pad=0):
    '''
    
    
    '''
    # Get current figure and calculate its size
    fig = plt.gcf()
    plot_size = fig.get_size_inches()
    text_pad = 0.0038 + text_pad/1000
    
    # Get the font size
    base_size = mpl.rcParams['font.size']
    # Initialize offsets for spacing figure titles appart
    top_offset, bottom_offset = 0, 0
    
    if subtitle:
        plt.figtext(0.05, 0.95+title_pad, subtitle, size=base_size)
        # Increment next titles vertical offset if text was added
        top_offset += base_size * text_pad
        
    if title:
        plt.figtext(0.05, 0.95+title_pad+top_offset, title, size=1.2*base_size, color='#003A79', weight='bold')
        top_offset += base_size * text_pad * 1.2
        
    if tag:
        plt.figtext(0.05, 0.95+title_pad+top_offset, tag, size=0.8*base_size, color='#003A79', weight='light')
        
    if source:
        plt.figtext(0.05, source_pad-base_size*0.006, r"$\bf{Source:}$ " +source, size=0.8*base_size, color="#666666")
        bottom_offset += base_size * text_pad * 0.8
        
    if notes:
        plt.figtext(0.05, source_pad-base_size*0.006 - bottom_offset, r"$\bf{Notes:}$ " +notes, size=0.8*base_size, color="#666666")
        
    
def add_logo(logo_path, logo_position='bottom right', offsets=(0,0,0,0), scale=0.2):
    '''
    
    '''
    # Map of logo position names to coordinates
    logo_locs = {'bottom right': [0.65,-0.12-base_size*0.006,0.25,0.2]}
    
    # List of supported logos
    supported_logos = ["brookings", "es", "gs", "fp", "metro", "global", "bi", "bc", 
                           "cc", "ccf", "ceaps", "cepm", "chp", "cmep", "csd", "cti", "crm", 
                           "cue", "cuse", "doha", "hc", "thp"]
    
    # Updating string to directory path if using a supported logo
    if logo_path in supported_logos:
        cwd = os.getcwd()
        path = os.path.join(cwd, 'logos')
        logo_path = os.path.join(path, logo_path +'.png')
     
    try:
        # Read the image
        logo = mpimg.imread(logo_path)
        
    except FileNotFoundError:
        # Throw error listing valid logo names
        raise Exception('No such file or directory: "' + str(name)
                        + '" Check your path or try one of the following: ' + str(supported_logos))
    
    # Get font size for scaling 
    base_size = mpl.rcParams['font.size']
    # Get current figure and calculate its size
    fig = plt.gcf()
    plot_size = fig.get_size_inches()*fig.dpi
    
    # Add an axis for the logo plot
    try:
        ax = fig.add_axes(logo_locs[logo_position], zorder=1) 
    
    except KeyError:
        raise Exception('"' + str(name)+'" is not a valid logo position. Try one of the following: ' + str(list(logo_locs.keys())))
        
    # Add plot and turn off axis labeling
    ax.imshow(logo)
    ax.axis('off')

    
def get_cmap():
    '''
    
    '''
    pass


def set_pallet(name, ax=None):
    '''
    
    '''
    
    # Check if there's a key for the user pallet name
    try:
        pallet = pallets[name]
        
    # Throw error with all pallet names if there's no key value pair
    except KeyError:
        raise Exception('"' + str(name)+'" is not a valid color pallet. Try one of the following: ' + str(list(pallets.keys())))
    
    if not ax:
        ax = plt.gca()
        
    if 'pos_neg' in name:
        warnings.warn("This pallet is not high contrast for people colorblindness (specifically protanopia and deuteranopia) please avoid using")
    
    # Create a cycler for the selected color pallet
    pallet_cycler = cycler(color=pallet)
    # Set the cycler as base for the current/given axis
    ax.set_prop_cycle(pallet_cycler)
