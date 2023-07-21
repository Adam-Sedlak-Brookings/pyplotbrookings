def add_title(title=None, subtitle=None, tag=None, v_pad=0, h_pad=0, text_pad=0, tag_length=0):
    '''
    Adds titles to the current figure.

    title (str): The title of the plot. Title should be short

    subtitle (str): The subtitle of the plot. Subtitle can be longer and
         add description to the figure 

    tag (str): The figure name/number plotted above the titles

    v_pad (float): Vertical padding, a number specifying additional amount of 
        spacing to add between the top of the figure and the first title.

    h_pad (float): Horizontal padding, the amount of additional space to offset 
        the title text in the x direction.

    text_pad (float): Number specifying additional amount of spacing to add
        between lines of text.
    '''
    # Get the font size
    font_size = mpl.rcParams['font.size']
    # Set starting y coords
    x = get_coords('left') + h_pad/100
    y = get_coords('top') + v_pad/100
    # Font size to pad
    text_pad = (0.47 + text_pad/100) * font_size
    
    # Add some blank space padding
    plt.figtext(x, y, ' ', size=text_pad+8*text_pad)   

    if subtitle:
        y = get_coords('top')
        plt.figtext(x, y, subtitle, size=0.833*font_size, wrap=True)
        # Increment next titles vertical offset if text was added
        y = get_coords('top')
        plt.figtext(x, y, ' ', size=1.5*text_pad)
        
    if title:    
        y = get_coords('top')
        plt.figtext(x, y, title,
                    size=font_size, weight='bold', wrap=True)
        y = get_coords('top')
        plt.figtext(x, y, ' ', size=2*font_size)

    if tag:
        y = get_coords('top')
        # Estimating the number of box tokens needed based on figure length
        l = int(plt.gcf().get_size_inches()[0] * 10) + 2 + tag_length
        # Adding figure tag
        plt.figtext(x, y, tag.upper() + '   ' + '─'*l,
                    size=0.75*font_size, weight='light', color='#666666')
