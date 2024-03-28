class CsvLogWriter:
    def __init__(self, filepath, delimiter = "\t"):
        self.header = ""
        self.delimiter = delimiter
        self.filenameFullPath = filepath
        self.rows = []
        self.written_header = False
    
    def addColToHeader(self, col):
        if self.header == "":
            self.header = col
        else:
            self.header = self.header + self.delimiter + col
            
    def addHeaderAsList(self, values: list[str]):
        self.header = self.delimiter.join(values)
            
    def add(self, values: list[str]):
        rowStr = ""
        lastIdx = len(values) - 1
        for idx, value in enumerate(values):
            if idx == lastIdx: rowStr += value
            else: rowStr += value + self.delimiter
        self.rows.append(rowStr)
    
    def writeToLogFile(self):
        f = open(self.filenameFullPath, "w")
        f.write(self.header + "\n")
        for row in self.rows:
            f.write(row + "\n")
        self.rows = []
        f.close()

    def __str__(self):
        delim = self.delimiter
        if self.delimiter == "\t":
            delim = "tab"
        elif self.delimiter == "\n":
            delim = "newline"
        elif self.delimiter ==  " ":
            delim = "space"
        return f"[CsvLogWriter] object\n- header: {delim},\n- filepath: {self.filenameFullPath}\n"
    
    def writeToLogFileAsList(self, values: list[str]):
        self.add(values)
        f = open(self.filenameFullPath, "a")
        for row in self.rows:
            f.write(row + "\n")
        self.rows = []
        f.close()
        
    def writeHeaderToLogFileAsList(self, values: list[str]):
        if self.written_header: return
        self.header = ""
        self.addHeaderAsList(values)
        f = open(self.filenameFullPath, "w")
        f.write(self.header + "\n")
        f.close()
        self.written_header = True
        