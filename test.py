
import arcpy

# baza = arcpy.GetParameterAsText(1)
# print(baza)

# arcpy.env.workspace = "./zaliczenie"

# with open('./zaliczenie/hydro_test.csv', 'r') as dane_hydro:

#     fc = arcpy.CreateFeatureclass_management("./zaliczenie/warstwy", "test.shp", "POINT")


#     columns = dane_hydro.readline()
#     columns = columns.split(';')
#     print(columns)

#     arcpy.AddField_management(fc, "KOD", "LONG", field_is_required=True)
#     arcpy.AddField_management(fc, "NAZWA", "TEXT", field_is_required=True)
#     arcpy.AddField_management(fc, "CIEK", "TEXT", field_is_required=True)
#     arcpy.AddField_management(fc, "ROK", "SHORT", field_is_required=True)
#     arcpy.AddField_management(fc, "MIES_H", "SHORT", field_is_required=True)
#     arcpy.AddField_management(fc, "DZIEN", "SHORT", field_is_required=True)

#     arcpy.AddField_management(fc, "STAN_WODY", "FLOAT", field_is_nullable = True, field_is_required=False)
#     arcpy.AddField_management(fc, "PRZEPLYW", "FLOAT", field_is_nullable = True, field_is_required=False)
#     arcpy.AddField_management(fc, "TEMP_WODY", "FLOAT", field_is_nullable = True, field_is_required=False)
#     arcpy.AddField_management(fc, "MIES_K", "SHORT", field_is_required=True)

#     cur = arcpy.InsertCursor(fc)

#     line = dane_hydro.readline()

#     while line:
    
#         line = line.split(';')
#         print(line)

#         row = cur.newRow()

#         row.KOD = line[0]
#         row.NAZWA = line[1]
#         row.CIEK = line[2]
#         row.ROK = line[3]
#         row.MIES_H = line[4]
#         row.DZIEN = line[5]
#         row.STAN_WODY = None if line[6] == '' else line[6]
#         row.PRZEPLYW = None if line[7] == '' else line[7]
#         row.TEMP_WODY = None if line[8] == '' else line[8]
#         row.MIES_K = line[9].strip()

#         cur.insertRow(row)

#         line = dane_hydro.readline()




in_table ="d:/geoinformatyka/SEMESTRV/programowanie_gis/zaliczenie/hydtest.csv"

with open(in_table, 'r') as plik:
    columns = plik.readline()

    line = plik.readline().split(';')
    print(type(line[3]))
    print('{}'.format(line[3]))