import sqlalchemy
from sqlalchemy import (MetaData, Table, Column, Integer, String, Date, Float, select, literal, and_, exists)

from sqlalchemy import create_engine

#TODO - iau din odoo produsul si sa il pun in EDA
#practic iau numele si codul si caut asa
#daca ii gasesc codul si in EDA il notific si il adaug
#daca nu il gassec , ii pun codul default pentru echipa si il adaug
engineEDA = create_engine('firebird+fdb://sysdba:masterkey@192.168.2.163:3050/D:\Contabilitate\DataBase\helpan.FDB')
class ProdusEDA:
    def __init__(self,bxcod):
      #  _logger.info(str(bxcod))
        BXPARTTable = Table("BXPART", metadataEDA, autoload=True, autoload_with=engineEDA)
        if(bxcod!=False):
            BXCOD = bxcod
        else:
            BXCOD=""
        select_stmt = BXPARTTable.select().where(BXPARTTable.c.bxcod == BXCOD).order_by(BXPARTTable.c.bxcod.desc()).limit(1)
       # _logger.info(select_stmt)
        rezultat = engineEDA.execute(select_stmt).fetchone()
        if(rezultat!=None):
            self.EDA_BXID = rezultat[0]
            self.EDA_BXCOD = rezultat[1]
            self.EDA_BXNUME = rezultat[2]
            self.EDA_BXUM_ID = rezultat[3]
            self.EDA_GRUPA_ID = rezultat[4]
            self.EDA_BXCOTATVAIMPLICIT_ID=rezultat[5]
            self.EDA_BXCONTIMP_ID_V=rezultat[8]
       #     _logger.info("Next step")
        else:
            self.EDA_BXID=46
            self.EDA_BXCOD=BXCOD
            self.EDA_BXNUME='Marfa'
            self.EDA_BXUM_ID=1
            self.EDA_BXCOTATVAIMPLICIT_ID=4
            self.EDA_BXCOTATVAIMPLICIT_ID=142

            #daca are cod in Odoo il adaugam in SWAN
            # daca nu il adaugam ca marfa - ATENTIE - in functie de echipa ?
            #ideal ar fi sa ii pun pe pagina de echipa produs standard
            #45- avans - AVANS
            #46 - marfa - MARF
            #107 - transport - TRANSP
            #107,45179,46
        #    _logger.info("Eroare 11: Nu gasesc codul")
