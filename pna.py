import pyvisa
import time

class PNA_Controller():
    def __init__(self,addr="algoquetengoquemirar") -> None:
        rm = pyvisa.ResourceManager()
        self.__visa_resource = rm.open_resource(addr)
        self.__visa_resource.timeout = 20000
        pna_id = self.__visa_resource.query("*IDN?")
        print(pna_id)
        self.__visa_resource.write("FORM:DATA REAL,64")
        self.__pna_test = False #debug purposes
        if "E8362B" in pna_id:
            self.__pna_test = True

    def __del__(self):
        self.__visa_resource.close()

    def setup_multifreq(self,frequencies,fi_bw):
        self.__visa_resource.write("SENS:SWE:TIME:AUTO 1")
        self.__visa_resource.write("SENS:SWE:TRIG:POIN OFF")
        self.__visa_resource.write("SENS:SWE:POIN {}".format(len(frequencies)))
        self.__visa_resource.write("SENS:SWE:MODE HOLD")
        self.__visa_resource.write("TRIG:SOUR MAN")
        self.__visa_resource.write("TRIG:SCOP ALL")
        self.__visa_resource.write("SENS:BWID {}Hz".format(fi_bw))
        self.__visa_resource.write("SENS:SEGM:DEL:ALL")
        frequencies.sort(reverse=True)
        #Since we are pushing frequencies to table, last frequency has to be first
        for f in frequencies:
            self.__visa_resource.write("SENS:SEGM:ADD")
            self.__visa_resource.write("SENS:SEGM:FREQ:CENT {}GHZ".format(f))
            self.__visa_resource.write("SENS:SEGM:FREQ:SPAN 0")
            self.__visa_resource.write("SENS:SEGM:SWE:POIN 1")
            self.__visa_resource.write("SENS:SEGM ON")

        self.__visa_resource.write("SENS:SWE:TYPE SEGM")
        time.sleep(0.1)



    def setup_cut(self,frecuencies,npuntos):
        #self.__visa_resource.write('SYST:FPRESET')
        #self.__visa_resource.write("DISP:WIND1:STATE ON")
        #self.__visa_resource.write("CALC:PAR:DEF 'S_21', ar1, 1") #Diferente
        #self.__visa_resource.write("DISP:WIND1:TRAC1:FEED 'S_21'")
        self.__visa_resource.write("SENS:SWE:TIME:AUTO 1")
        self.__visa_resource.write("SENS:SWE:TRIG:MODE ON")
        self.__visa_resource.write("SENS:SWE:MODE HOLD")
        self.__visa_resource.write("TRIG:SOUR MAN")
        self.__visa_resource.write("TRIG:SCOP ALL")

        self.__visa_resource.write("SENS:FREQ:CENT {} GHz".format(frecuencies[0]))
        self.__visa_resource.write("SENS:FREQ:SPAN 0")
        self.__visa_resource.write("SENS:SWE:POIN {}".format(npuntos))
        self.__visa_resource.write("FORM:DATA REAL,64")
        #Mulrifreq
        """self.__visa_resource.write("SENS:SWE:TYPE SEGM")
        self.__visa_resource.write("SENS:SEGM:DEL:ALL")
        for f in frecuencies:
            self.__visa_resource.write("SENS:SEGM:ADD")
            self.__visa_resource.write("SENS:SEGM:FREQ:CENT {}GHZ".format(f))
            self.__visa_resource.write("SENS:SEGM:FREQ:SPAN 0")
            self.__visa_resource.write("SENS:SEGM ON")
            self.__visa_resource.write("SENS:SEGM:SWE:POIN 1")
        
         """
    #PNA del esférico
    def setup_cut_pna_x(self,frecuency,npuntos,fi_bw=100):
        #self.__visa_resource.write('SYST:FPRESET')
        #self.__visa_resource.write("DISP:WIND1:STATE ON")
        #self.__visa_resource.write("CALC:PAR:DEF 'S_21', ar1, 1") #Diferente
        #self.__visa_resource.write("DISP:WIND1:TRAC1:FEED 'S_21'")
        self.__visa_resource.write("TRIG:SEQ:SOUR MAN")
        self.__visa_resource.write("TRIG:SCOP CURR")
        self.__visa_resource.write("SENS:SWE:TRIG:MODE POINT")

        self.__visa_resource.write("SENS:SWE:GRO:COUN 1")
        self.__visa_resource.write("SENS:FREQ:SPAN 0")
        self.__visa_resource.write("SENS:BWID {}Hz".format(fi_bw))

        self.__visa_resource.write("SENS:SWE:POIN {}".format(npuntos))

        self.__visa_resource.write("SENS:FREQ:CENT {} GHz".format(frecuency))
        #self.__visa_resource.write("FORM:DATA REAL,64")

    #PNA del esférico multifrecuencia
    def setup_multifreq_by_points(self,frequencies,npuntos):
        self.__visa_resource.write("TRIG:SEQ:SOUR MAN")
        self.__visa_resource.write("TRIG:SCOP CURR")

        self.__visa_resource.write("SENS:SWE:GRO:COUN 1")
        self.__visa_resource.write("SENS:SWE:POIN {}".format(npuntos))

        self.__visa_resource.write("SENS:FREQ:START {} GHz".format(frequencies[0]))
        self.__visa_resource.write("SENS:FREQ:STOP {} GHz".format(frequencies[1]))

        time.sleep(0.1)

    #Como en prozenca
    def setup_multifreq_segment(self,frequencies):
        self.__visa_resource.write("SENS:SWE:TRIG:POIN OFF")
        self.__visa_resource.write("SENS:SWE:POIN {}".format(len(frequencies)))
        #self.__visa_resource.write("SENS:FOM 1")
        self.__visa_resource.write("SENS:SWE:MODE HOLD")
        self.__visa_resource.write("TRIG:SOUR MAN")
        self.__visa_resource.write("TRIG:SCOP ALL")
        self.__visa_resource.write("SENS:SEGM:DEL:ALL")
        for f in frequencies:
            self.__visa_resource.write("SENS:SEGM:ADD")
            self.__visa_resource.write("SENS:SEGM:FREQ:CENT {}GHZ".format(f))
            self.__visa_resource.write("SENS:SEGM:FREQ:SPAN 0")
            self.__visa_resource.write("SENS:SEGM:SWE:POIN 1")
            self.__visa_resource.write("SENS:SEGM ON")

        self.__visa_resource.write("SENS:SWE:TYPE SEGM")
        time.sleep(0.1)

    def multiplier(self,fact_mult,subarm,offset):
        self.__visa_resource.write('SYST:FPRESET')
        self.__visa_resource.write("SYST:CONF:EDEV:STAT 'PSG', ON")
        self.__visa_resource.write("DISP:WIND1:STATE ON")
        self.__visa_resource.write("CALC:PAR:EXT 'S_21','B/A,PSG'")
        self.__visa_resource.write("DISP:WIND1:TRAC1:FEED 'S_21'")
        self.__visa_resource.write("SENS:FOM:DISP:SEL 'Primary'")

        self.__visa_resource.write("SENS:FOM:RANG4:COUP ON")
        self.__visa_resource.write("SENS:FREQ:CENT {}GHZ".format(10))
        self.__visa_resource.write("SENS:FREQ:SPAN 180")
        self.__visa_resource.write("SENS:FOM:RANG4:FREQ:DIV {}".format(fact_mult))
        self.__visa_resource.write("SENS:FOM:RANG3:FREQ:DIV {}".format(subarm))
        self.__visa_resource.write("SENS:FOM:RANG3:FREQ:OFFS {} MHZ".format(offset))
        self.__visa_resource.write("SENS:FOM 1")
    
    def multiplier_by_frequency(self,frequency):
        if frequency in range(5,23):
            self.multiplier(1,1,0)
            print("Rango 5 20")
            return
        if frequency in range(23,42):
            self.multiplier(2,8,-6.654930)
            print("Rango 20-40")
            return
        elif frequency in range(42,60):
            self.multiplier(4,10,-6.8450706)
            print("Rango 40-60")
            return
        elif frequency in range(60,75):
            self.multiplier(6,8,-6.6549)
            print(print("Rango 60-75"))
            return
        elif frequency in range(75,130):
            self.multiplier(6,18,-7.18309877777778)
            print("Rango 75-130")
            return
        


    def enable_fifo(self):
        self.__visa_resource.write("SYST:FIFO ON")
        self.__visa_resource.write("SYST:FIFO:DATA:CLEAR")
        self.__visa_resource.write("FORM:DATA REAL,64")

    def read_fifo_len(self):
        return self.__visa_resource.query("SYST:FIFO:DATA:COUNT?")

        
    def read_fifo(self,points):
        return self.__visa_resource.query_binary_values("SYST:FIFO:DATA? {}".format(points),is_big_endian=True,datatype="d")
        
    def trigger(self):
        res = self.__visa_resource.query("INIT:IMM;*OPC?")
    
    def get_data(self):
        #Retrieve data into matrix
        return self.__visa_resource.query_binary_values("CALC:DATA? SDATA",is_big_endian=True,datatype="d")
        

if __name__ == "__main__":
    pna = PNA_Controller("GPIB0::16::INSTR")
    npuntos_fifo = int(pna.read_fifo_len())
    measure = pna.read_fifo(npuntos_fifo)
    with open("multi_pna","w") as f:
        for i in range(0,len(measure),2):
            f.write("{:.10f}\n".format(complex(measure[i],measure[i+1])))
    exit()
    pna.multiplier(6,18,-7.18309877777778)
    n_puntos = 5;
    #pna.setup_cut_pna_x(82,n_puntos)
    pna.setup_multifreq2([75,80],6)
    pna.enable_fifo()
    #pna.setup_multifreq([75,80,90,100,110])
    time.sleep(1)
    for i in range(0,n_puntos):
        pna.trigger()
        print("Trigger")
        time.sleep(2)
    print(pna.read_fifo_len())