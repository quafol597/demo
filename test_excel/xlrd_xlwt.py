import xlrd
import xlwt


def test_xlrd(filename):
    workbook = xlrd.open_workbook(filename=filename, ragged_rows=True)
    sheet = workbook.sheet_by_index(0)

    # for row in sheet.get_rows():
    #     print(list(map(lambda cell:cell.value, row)))
    for row in sheet._cell_values[1:10]:
        print(type(row), row, sep=': ')



if __name__ == '__main__':
    test_xlrd(filename=r'C:\Users\xiaoan\Desktop\work_file\wechat_file\test_xlrd.xlsx')
