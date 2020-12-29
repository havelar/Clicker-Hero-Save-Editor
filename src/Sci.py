import re, math

class Sci:
    split = 'e'
    sci_format = r'([+-]*\d+\.\d+)e([+-]*\d+)'
    __num = 0.0
    __exp = 0
    
    def __init__(self, sci, int_size=1, float_size=3):
        if isinstance(sci, int) or isinstance(sci, float):
            if sci == math.inf: # If incoming Int or Float is too large
                raise ValueError("Float number sent is too large, received 'inf'.")
            else:
                sci_format = '{' + ":.{0}e".format(float_size) + '}' # Construct the format string with float_len
                sci = sci_format.format(sci) # Set as string to be processed below
                
        if re.search(self.sci_format, sci): # 1.0e100
            groups = re.search(self.sci_format, sci).groups()
            self.__num = float(groups[0])
            self.__exp = int(groups[1])
            self.__fixBase(int_size, float_size)
        else:
            raise ValueError('Sci number should be in scientific notation: "1.00e100"')
            
    #############################################################################################################
    ############################################# Operations ####################################################
    #############################################################################################################
    
    def __truediv__(self, other):
        '''
            self / other
        '''
        if type(other) in (str, int, float):
            sci_other = Sci(other)
        elif isinstance(other, Sci):
            sci_other = other

        exp = self.__exp - sci_other.exp
        num = self.__num / sci_other.num
        return Sci(str(num)+'e'+str(exp))

    def __rtruediv__(self, other):
        '''
            other / self
        '''
        if type(other) in (str, int, float):
            sci_other = Sci(other)
        elif isinstance(other, Sci):
            sci_other = other
            
        exp = sci_other.exp - self.__exp
        num = sci_other.num / self.__num
        return Sci(str(-1*num)+'e'+str(exp))
    
    def __floordiv__(self, other):
        '''
            self // other
        '''
        return self.__truediv__(other)
    def __rfloordiv__(self, other):
        '''
            other // self
        '''
        return self.__rtruediv__(other)
    
    def __mul__(self, other):
        '''
            self * other
        '''
        if type(other) in (str, int, float):
            sci_other = Sci(other)
        elif isinstance(other, Sci):
            sci_other = other

        exp = self.__exp + sci_other.exp
        num = self.__num * sci_other.num
        return Sci(str(num)+'e'+str(exp))
    
    def __rmul__(self, other):
        '''
            other * self
        '''
        if type(other) in (str, int, float):
            sci_other = Sci(other)
        elif isinstance(other, Sci):
            sci_other = other

        exp = self.__exp + sci_other.exp
        num = self.__num * sci_other.num
        return Sci(str(num)+'e'+str(exp))
    
    
    def __add__(self, other):
        '''
            self + other
        '''
        if type(other) in [str, int, float]:
            sci_other = Sci(other)
        elif isinstance(other, Sci):
            sci_other = other
            
        smll = self if self.exp <= sci_other.exp else sci_other
        bigr = self if self.exp > sci_other.exp else sci_other
        
        diff = bigr.exp - smll.exp
        
        exp = smll.exp + diff
        num = smll.num / 10**diff
        num = num + bigr.num
        
        return Sci(str(num) + 'e' + str(exp))
            
    def __radd__(self, other):
        '''
            other + self
        '''
        if type(other) in [str, int, float]:
            sci_other = Sci(other)
        elif isinstance(other, Sci):
            sci_other = other
            
        smll = self if self.exp <= sci_other.exp else sci_other
        bigr = self if self.exp > sci_other.exp else sci_other
        
        diff = bigr.exp - smll.exp
        
        exp = smll.exp + diff
        num = smll.num / 10**diff
        num = num + bigr.num
        
        return Sci(str(num) + 'e' + str(exp))
    
    def __sub__(self, other):
        '''
            self - other
        '''
        if type(other) in [str, int, float]:
            sci_other = Sci(other)
        elif isinstance(other, Sci):
            sci_other = other
            
        smll = self if self.exp <= sci_other.exp else sci_other
        bigr = self if self.exp > sci_other.exp else sci_other
    
        diff = bigr.exp - smll.exp
                
        exp = smll.exp + diff
        num = smll.num / 10**diff
        if smll.exp < 0:
            num = bigr.num - num
        else:
            num = num - bigr.num
        return Sci(str(num) + 'e' + str(exp))
    
    def __rsub__(self, other):
        '''
            other - self
        '''
        if type(other) in [str, int, float]:
            sci_other = Sci(other)
        elif isinstance(other, Sci):
            sci_other = other
            
        smll = self if self.exp <= sci_other.exp else sci_other
        bigr = self if self.exp > sci_other.exp else sci_other
    
        diff = bigr.exp - smll.exp
                
        exp = smll.exp + diff
        num = smll.num / 10**diff
        if smll.exp < 0:
            num = bigr.num - num
        else:
            num = num - bigr.num
        return Sci(str(num) + 'e' + str(exp))
    
    #################################################################################################
    #################################################################################################
    #################################################################################################
    
    def __str__(self):
        return str(self.__num) + 'e' + str(self.__exp)
    def __repr__(self):
        return str(self.__num) + 'e' + str(self.__exp)

    @property
    def num(self):
        return self.__num
    @num.setter
    def num(self, val):
        self.__num = float(val)
        
    @property
    def exp(self):
        return self.__exp
    @exp.setter
    def exp(self, val):
        self.__exp = int(val)
    
    def __fixBase(self, int_size =1, float_size=3):
        '''
            Fix exponential base
        '''
        int_len = len(str(int(abs(self.__num))))

        # Fix Integer part of self.__num
        if int_len > int_size:
            self.__num = self.__num / (10**(int_len-int_size))
        elif int_len < int_size:
            self.__num = self.__num * (10**(int_size-int_len))
        self.__exp = self.__exp - (int_size-int_len) # Fix EXP part
        
        # Fix Float part of self.__num
        self.__num = round(self.__num, float_size)
        float_len = len(str(abs(self.__num)).split('.')[1])
        if float_size and float_len > float_size:
            self.__num = round(self.__num, float_size)