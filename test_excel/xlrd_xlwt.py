import xlrd
import xlwt


def test_xlrd(filename):
    """读取Excel"""
    workbook = xlrd.open_workbook(filename=filename)
    sheet = workbook.sheet_by_index(0)

    # for row in sheet.get_rows():
    #     print(list(map(lambda cell:cell.value, row)))
    for row in sheet._cell_values[1:10]:
        print(type(row), row, sep=': ')


def test_xlwt(filename):
    """写入Excel"""
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('test')
    for a in range(10):
        for b in range(10):
            sheet.write(a, b, 'hahaha')

    workbook.save(filename)


if __name__ == '__main__':
    test_xlrd(filename=r'C:\Users\xiaoan\Desktop\work_file\wechat_file\test_xlrd.xlsx')
    test_xlwt(filename='test.xls')




