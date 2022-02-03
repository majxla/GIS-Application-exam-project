import arcpy
import os

def hydroData():
    pass

def meteoData():
    pass


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""

        # tu się robi ogólnie tę paczkę toolbox w sensie ta skrzynka z narzędziami co się wyświetla
        self.label = "HydroMeteoData Toolbox"
        self.alias = "HydroMeteoData"

        # List of tool classes associated with this toolbox
        # tu się dodaje narzędzie do skrzynki, my mamy tylko jedno narzędzie, ale można kilka zdefiniować
        self.tools = [HydroMeteoData]


class HydroMeteoData(object):
    # to jest narzędzie w skrzynce

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""

        # tu opis narzędzia
        self.label = "HydroMeteoData"
        self.description = "Generate archival hydrological and meteorological data for Poland from 2010-2020."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # tu definicja pól w narzędziu czyli do wyboru dane hydro/meteo, przedział dat i miejsce do zapisania warstw

        yearList = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

        dane = arcpy.Parameter(
            displayName = "Output Data Class",
            name = "in_value",
            datatype = "String",
            parameterType = "Required",
            direction = "Input"
        )

        dane.filter.type = "ValueList"
        dane.filter.list = ["Dane hydrologiczne", 'Dane meteorologiczne']

        data1 = arcpy.Parameter(
            displayName = "From year",
            name = "year1",
            datatype = "GPLong",
            parameterType = "Required",
            direction = "Input"
        )

        data1.filter.type = "ValueList"
        data1.filter.list = yearList



        data2 = arcpy.Parameter(
            displayName = "To year",
            name = "year2",
            datatype = "GPLong",
            parameterType = "Required",
            direction = "Input"
        )

        data2.filter.type = "ValueList"
        data2.filter.list = yearList

        save = arcpy.Parameter(
            displayName = "Output Features",
            name = "out_features",
            datatype = "GPFeatureLayer",
            parameterType = "Required",
            direction = "Output"
        )

        # save.parameterDependencies = [dane.name]
        # save.schema.clone = True

        params = [dane, data1, data2, save]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""

        # tu że ma działać jak się kliknie że ma działać, nie rozumiem po co ta funkcja się wygenerowała XD
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # tutaj robię tak, że jezeli bedzie wybrany rok OD którego mają być dane to żeby nie dało się wybrać wcześniejszego roku DO którego mają być dane
        # np. jeżeli ROK OD będzie 2013 to żeby nie można było wybrać ROK DO 2011, bo by wyszło od 2013 do 2011 czyli data wsteczna
        if parameters[1].value:
            year1 = parameters[1].value
            yearList = [year for year in range(year1, 2021)]
            parameters[2].filter.list = yearList
        

        # tu analogicznie, jeżeli będzie wybrany rok DO którego mają być dane to żeby nie dało się wybrać roku późniejszego OD którego mają być dane
        if parameters[2].value:
            year2 = parameters[2].value
            yearList2 = [year for year in range(2010, year2+1)]
            parameters[1].filter.list = yearList2

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        # tu jeszcze nie odkryłam po co to
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # tu co ma się dziać jak się naciśnie OK

        # arcpy.env.workspace = "d:/geoinformatyka/SEMESTRV/programowanie_gis/zaliczenie"
        # arcpy.AddMessage(arcpy.env.workspace)

        # tutaj pobieram ścieżkę podaną przez użytkownika i dzielę żeby wydzielić folder, do którego zapisać warstwę i nazwę nowej warstwy
        out = parameters[3].valueAsText.split('\\')
        out_folder = parameters[3].valueAsText.split(out[-1])[0]
        out_name = out[-1] #test.shp

        out_name0 = out_name.split('.') # ['test', 'shp']

        first_year = parameters[1].valueAsText
        last_year = parameters[2].valueAsText

        years = [year for year in range(int(first_year), int(last_year)+1)]
        arcpy.AddMessage(years)

        if parameters[0].valueAsText == "Dane hydrologiczne":
            for year in years:
                out_name = out_name0[0] + str(year) + "." + out_name0[1]

                fc = arcpy.CreateFeatureclass_management(out_folder, out_name, "POINT")

                arcpy.AddField_management(fc, "KOD", "LONG", field_is_required=True)
                arcpy.AddField_management(fc, "NAZWA", "TEXT", field_is_required=True)
                arcpy.AddField_management(fc, "CIEK", "TEXT", field_is_required=True)
                arcpy.AddField_management(fc, "ROK", "SHORT", field_is_required=True)
                arcpy.AddField_management(fc, "MIES_H", "SHORT", field_is_required=True)
                arcpy.AddField_management(fc, "DZIEN", "SHORT", field_is_required=True)

                arcpy.AddField_management(fc, "STAN_WODY", "FLOAT", field_is_nullable = True, field_is_required=False)
                arcpy.AddField_management(fc, "PRZEPLYW", "FLOAT", field_is_nullable = True, field_is_required=False)
                arcpy.AddField_management(fc, "TEMP_WODY", "FLOAT", field_is_nullable = True, field_is_required=False)
                arcpy.AddField_management(fc, "MIES_K", "SHORT", field_is_required=True)
                arcpy.AddField_management(fc, "x", "FLOAT", field_is_required=True)
                arcpy.AddField_management(fc, "y", "FLOAT", field_is_required=True)

                with open("d:/geoinformatyka/SEMESTRV/programowanie_gis/zaliczenie/hydtest.csv", 'r') as plik:
                    columns = plik.readline().split(";")
                    line = plik.readline()
                
                    cur = arcpy.InsertCursor(fc)

                    while line:
                        line = line.split(';')
                        if int(line[3]) == year:

                            row = cur.newRow()

                            row.KOD = line[0]
                            row.NAZWA = line[1]
                            row.CIEK = line[2]
                            row.ROK = line[3]
                            row.MIES_H = line[4]
                            row.DZIEN = line[5]
                            row.STAN_WODY = None if line[6] == '' else line[6]
                            row.PRZEPLYW = None if line[7] == '' else line[7]
                            row.TEMP_WODY = None if line[8] == '' else line[8]
                            row.MIES_K = line[9].strip()
                            row.x = line[10].strip()
                            row.y = line[11].strip()

                            cur.insertRow(row)

                        line = plik.readline()

                dbf = out_name.split('.')[0] + ".dbf"
                xyname = out_name.split('.')[0]
                arcpy.MakeXYEventLayer_management(out_folder + dbf, "x" , "y", xyname)
                arcpy.SaveToLayerFile_management(xyname, out_folder + xyname)

                mxd = arcpy.mapping.MapDocument("CURRENT") # pobiera aktualny projekt z arcmapy
                df = arcpy.mapping.ListDataFrames(mxd)[0] # pobiera ramki danych z arcmapy
                add1 = arcpy.mapping.Layer(out_folder + xyname + ".lyr") # wybiera warstwę do dodania po ścieżce
                arcpy.mapping.AddLayer(df, add1) # dodaje warstwę do ramki czyli do ToC
                arcpy.RefreshTOC() # odświeża tabelę z zawartością 
                arcpy.RefreshActiveView() # odświeża widok
        
        if parameters[0].valueAsText == "Dane meteorologiczne":
            arcpy.AddMessage("METEOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")

        return
