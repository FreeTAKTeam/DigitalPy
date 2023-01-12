from fpdf import FPDF

class PDF(FPDF):
    """
    PDF extends FPDF/FPDI.
    """

    def __init__(self, orientation='P', unit='mm', format='A4'):
        FPDF.__init__(self, orientation, unit, format)
        self.pageStarted = False
        self.pageEnded = False

    def header(self):
        FPDF.header(self)
        self.use_template(self.tpl)

    def startPage(self):
        """
        Call this method when rendering a new page
        """
        self.pageStarted = True
        self.pageEnded = False

    def endPage(self):
        """
        Call this method when rendering a page finished
        """
        self.pageEnded = True
        self.pageStarted = False

    def isPageStarted(self):
        """
        Determine if a new page started
        @return Boolean
        """
        return self.pageStarted

    def isPageEnded(self):
        """
        Determine if a page finished
        @return Boolean
        """
        return self.pageEnded

    def moveDown(self, units):
        """
        Move the render position down by given units
        @param units The number of units to move
        """
        self.set_y(units+self.get_y())

    def moveRight(self, units):
        """
        Move the render position right by given units
        @param units The number of units to move
        """
        self.set_x(units+self.get_x())

    def numberOfLines(self, width, text):
        """
        Computes the number of lines a MultiCell of width w will take
        instead of NbLines it correctly handles linebreaks
        @param width The width
        @param text The text
        """
        nbLines = 0
        lines = text.split('\n')
        for line in lines:
            nbLines += self.nb_lines(width, line)
        return nbLines

    def check_page_break(self, h):
        """
        If the height h would cause an overflow, add a new page immediately
        @param h The height
        @return Boolean whether a new page was inserted or not
        """
        if self.get_y()+h > self.page_break_trigger:
            self.add_page(self.cur_orientation)
            return True
        return False

    def nb_lines(self, w, text):
        """
        Computes the number of lines a MultiCell of width w will take
        @param w The width
        @param text The text
        """
        cw = self.current_font['cw']
        if w == 0:
            w = self.w - self.r_margin - self.x
        wmax = (w - 2*self.c_margin)*1000/self.font_size
        s = text.replace("\r", '')
        nb = len(s)
        if nb > 0 and s[nb-1] == "\n":
            nb -= 1
        sep = -1
        i = 0
        j = 0
        l = 0
        nl = 1
        while i < nb:
            c = s[i]
            if c == "\n":
                i += 1
                sep = -1
                j = i
                l = 0
                nl += 1
                continue
            if c == ' ':
                sep = i
            l += cw[c]
            if l > wmax:
                if sep == -1:
                    if i == j:
                        i += 1
                else:
                    i = sep + 1
                sep = -1
                j = i
                l = 0
                nl += 1
            else:
                i += 1
        return nl