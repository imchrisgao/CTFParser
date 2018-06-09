class Frame: #This is the object the Parser makes
    def __init__(self):
        self.__dict = {}
    
    def addtoframe(self, tuplist): 
        tok = None
        val = None
        for i in range(len(tuplist)): #i is index of list
            tok, val = tuplist[i] #take apart tuple

            self.__dict[tok] = val
    #-------------------------------------
    #make Frame iterable
    def __iter__(self):
        return iter(self.__dict) #now I can make an iterator for a frame
    #-------------------------------------
    #random methods to see inside frame
    def toks(self):
        return list(self.__dict.keys()) 

    def values(self):
        return self.__dict.values()

    def items(self):
        return self.__dict.items() #returns list of tok,val tuples

class FParser: #Parses a line, returns a frame
    def __init__(self):
        self.__framelist = [] #list of frames
    #------------------------------------------------------
    #method to execute parse
    def executeparse(self, oneline):
        if len(oneline) == 0: return
        filestring = oneline.strip() #returns trailing characters
        bars = self.__findallchar(filestring, '|') #returns index of bars
        stringwobars = self.__makeexprfrmbars(bars, filestring) #returns list of strings without bars
        tokvallist = self.__maketokvaltup(stringwobars) #returns list of (tok,val) tuples
        #--------------------------------
        f = Frame()
        f.addtoframe(tokvallist) #makes frame out of tok,val list
        self.__framelist.append(f)
    #------------------------------------------------------
    #methods used in exectueparse()
    #these should all be private
    def __findallchargen(self, somestring, char):
        i = 0
        while True:
            try:
                i = somestring.index(char, i) #will either find char to right or will release ValueError
                yield i #yielding retains i; next time generator is called, i will be same value
                i+=1 #move to next index
            except ValueError:
                return #exit while loop

    def __findallchar(self, somestring, char): #calls generator that does actual finding
        return list(self.__findallchargen(somestring, char)) #needs to explicitly be typecasted to list

    def __makeexprfrmbars(self, bars, somestring): #bars is a list of the indexes of bars
        listofstrings = []
        listofstrings.append(somestring[0:bars[0]]) #first string

        for i in range(len(bars)-1): #middle strings #ends right before last string so no out of bounds
            listofstrings.append(somestring[bars[i]+1:bars[i+1]]) 

        listofstrings.append(somestring[bars[len(bars)-1]+1:]) #last string
        return listofstrings
    
    def __maketokvaltup(self, stringslist):
        temptuplist = []
        for i in range(len(stringslist)):
            shortstr = stringslist[i] #saves the string from list
            ind = shortstr.find('=') #finds '=' in stri
            if ind is not -1: 
                tok = shortstr[:ind] #separates tok from shortstr
                val = shortstr[ind+1:] #separates val from shortstr
                temptup = (tok,val)
                temptuplist.append(temptup)
        return temptuplist 
    #------------------------------------------------------
    #method to see list of frames
    def frames(self):
        return self.__framelist

def Main(): #executes Parser 
    p = FParser()
    with open('bcr.txt', 'r') as f: #opens 'bcr.txt' in 'read' mode
        while True: 
            line = f.readline()
            if len(line) == 0: break #this is how to exit while loop
            p.executeparse(line)

    for frame in p.frames():
        for item in frame.items():
            k, v = item
            print(k, v)

#-------------------------------------------------------
if __name__ == '__main__':
    Main()
