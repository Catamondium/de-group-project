import pytest
import pg8000.native as pg
from decimal import *
from src.utilAli import *
from os import environ


from copy import deepcopy

from datetime import datetime

testTs = {
        'address': '2022-11-03 14:20:49.962000',
        'counterparty': '2022-11-03 14:20:51.563000',
        'currency': '2022-11-03 14:20:49.962000',
        'department': '2022-11-03 14:20:49.962000',
        'design': '2024-02-07 13:05:09.537000',
        'payment': '2024-01-30 15:08:09.733000',
        'payment_type': '2022-11-03 14:20:49.962000',
        'purchase_order': '2024-01-30 15:08:09.733000',
        'sales_order': '2024-01-31 17:51:09.858000',
        'staff': '2022-11-03 14:20:51.563000',
        'transaction': '2024-01-31 17:51:09.858000'
        }


addressDict1 = { 'address_id': 1,
                   'address_line_1': '6826 Herzog Via',
                   'address_line_2': None,
                   'district': 'Avon',
                   'city': 'New Patienceburgh',
                   'postal_code': '28441',
                   'country': 'Turkey',
                   'phone': '1803 637401',
                   'created_at': datetime.fromisoformat('2022-11-03 14:20:49.962'),
                   'last_updated': datetime.fromisoformat('2022-11-03 14:20:49.962')
                   }
    
counterpartyDict6 = { 'counterparty_id': 6,
                         'counterparty_legal_name' : 'Mraz LLC',
                         'legal_address_id': 23,
                         'commercial_contact': 'Florence Casper',
                         'delivery_contact': 'Eva Upton',
                         'created_at': datetime.fromisoformat('2022-11-03 14:20:51.563'),
                         'last_updated': datetime.fromisoformat('2022-11-03 14:20:51.563') }

currencyDict3 = { 'currency_id': 3,
                     'currency_code': 'EUR',
                     'created_at': datetime.fromisoformat('2022-11-03 14:20:49.962'),
                     'last_updated': datetime.fromisoformat('2022-11-03 14:20:49.962')}
    
departmentDict6 = { 'department_id': 6,
                      'department_name': 'Facilities',
                      'location': 'Manchester',
                      'manager': 'Shelley Levene',
                      'created_at': datetime.fromisoformat('2022-11-03 14:20:49.962'),
                      'last_updated': datetime.fromisoformat('2022-11-03 14:20:49.962') }

designDict1 = { 'design_id': 1,
                   'created_at': datetime.fromisoformat('2022-11-03 14:20:49.962'),
                   'design_name': 'Wooden',
                   'file_location': '/lib',
                   'file_name': 'wooden-20201128-jdvi.json',
                   'last_updated': datetime.fromisoformat('2022-11-03 14:20:49.962') }

paymentDict60 = { 'payment_id': 60,
                    'created_at': datetime.fromisoformat('2022-11-21 08:50:10.292'),
                    'last_updated': datetime.fromisoformat('2022-11-24 07:55:11.996'),
                    'transaction_id': 60,
                    'counterparty_id': 14,
                    'payment_amount': Decimal('20766.9'),
                    'currency_id': 3,
                    'payment_type_id': 3,
                    'paid': True,
                    'payment_date': '2022-11-24',
                    'company_ac_number': 84646166,
                    'counterparty_ac_number': 33121480 }

payment_typeDict3 = { 'payment_type_id': 3,
                          'payment_type_name': 'PURCHASE_PAYMENT',
                          'created_at': datetime.fromisoformat('2022-11-03 14:20:49.962'),
                          'last_updated': datetime.fromisoformat('2022-11-03 14:20:49.962') }

purchase_orderDict35 = { 'purchase_order_id': 35,
                           'created_at': datetime.fromisoformat('2022-11-21 08:50:10.292'),
                           'last_updated': datetime.fromisoformat('2022-11-21 08:50:10.292'),
                           'staff_id': 13,
                           'counterparty_id': 14,
                           'item_code': 'MASCUUC',
                           'item_quantity': 682,
                           'item_unit_price': Decimal('30.45'),
                           'currency_id': 3,
                           'agreed_delivery_date': '2022-11-21',
                           'agreed_payment_date': '2022-11-24',
                           'agreed_delivery_location_id': 23 }

sales_orderDict152 = { 'sales_order_id': 152,
                        'created_at': datetime.fromisoformat('2022-12-21 16:08:10.029'),
                        'last_updated': datetime.fromisoformat('2022-12-21 16:08:10.029'),
                        'design_id': 37,
                        'staff_id': 12,
                        'counterparty_id': 10,
                        'units_sold': 97564,
                        'unit_price': Decimal('2.92'),
                        'currency_id': 3,
                        'agreed_delivery_date': '2022-12-26',
                        'agreed_payment_date': '2022-12-22',
                        'agreed_delivery_location_id': 30 }

staffDict3 = { 'staff_id': 3,
                  'first_name': 'Jeanette',
                  'last_name': 'Erdman',
                  'department_id': 6,
                  'email_address': 'jeanette.erdman@terrifictotes.com',
                  'created_at': datetime.fromisoformat('2022-11-03 14:20:51.563'),
                  'last_updated': datetime.fromisoformat('2022-11-03 14:20:51.563') }
    
transactionDict60 = { 'transaction_id': 60,
                        'transaction_type': 'PURCHASE',
                        'sales_order_id': None,
                        'purchase_order_id': 35,
                        'created_at': datetime.fromisoformat('2022-11-21 08:50:10.292'),
                        'last_updated': datetime.fromisoformat('2022-11-21 08:50:10.292') }

def test_top():
    assert(True)

def test_getTimestamps():
    timestamp = '2024-02-14 22:36:10.887968'

    tables0 = []
    tables1 = ['address']
    tables2 = ['address', 'currency']

    expected0 = {}
    expected1 = { 'address': '2024-02-14 22:36:10.887968' }
    expected2 = { 'address': '2024-02-14 22:36:10.887968', 'currency': '2024-02-14 22:36:10.887968' }

    result0 = getTimestamps(timestamp, tables0)
    result1 = getTimestamps(timestamp, tables1)
    result2 = getTimestamps(timestamp, tables2)

    assert expected0 == result0 and expected1 == result1 and expected2 == result2

def test_makeEmptySets():
    tables0 = []
    tables1 = ['address']
    tables2 = ['address', 'currency']

    expected0 = {}
    expected1 = { 'address': set() }
    expected2 = { 'address': set(), 'currency': set() }

    result0 = makeEmptySets(tables0)
    result1 = makeEmptySets(tables1)
    result2 = makeEmptySets(tables2)

    assert expected0 == result0 and expected1 == result1 and expected2 == result2

def test_moreToDo():
    setWithData = set()
    setWithData.add(1)

    tables0 = []
    tables1 = ['address']
    tables2 = ['address', 'currency']

    sets0 = {}
    sets1 = {'address': set()}
    sets2 = {'address': set(), 'currency': setWithData}

    expected0 = False
    expected1 = False
    expected2 = True

    result0 = moreToDo(sets0, tables0)
    result1 = moreToDo(sets1, tables1)
    result2 = moreToDo(sets2, tables2)

    assert expected0 == result0 and expected1 == result1 and expected2 == result2

def test_copyInto():
    tabs = ['address', 'currency', 'design', 'staff']

    fromA = set()
    toA = set()
    fromA.add(1)
    fromA.add(2)

    fromC = set()
    toC = set()
    fromC.add(3)
    toC.add(4)

    fromD = set()
    toD = set()
    toD.add(6)
    fromD.add(6)

    fromS = set()
    toS = set()
    toS.add(7)

    newA = set()
    newA.add(1)
    newA.add(2)

    newC = set()
    newC.add(3)
    newC.add(4)

    newD = set()
    newD.add(6)

    newS = set()
    newS.add(7)

    fromAll = { 'address': fromA, 'currency': fromC, 'design': fromD, 'staff': fromS }
    toAll = { 'address': toA, 'currency': toC, 'design': toD, 'staff': toS }

    expected = { 'address': newA, 'currency': newC, 'design': newD, 'staff': newS }

    copyInto(fromAll, toAll, tabs)
    assert expected == toAll

def test_removeFrom():
    tabs = ['address', 'currency', 'design', 'staff']

    killA = set()
    targetA = set()
    targetA.add(1)
    targetA.add(2)

    killC = set()
    targetC = set()
    killC.add(3)
    targetC.add(4)

    killD = set()
    targetD = set()
    targetD.add(6)
    targetD.add(7)
    killD.add(5)
    killD.add(6)
    killD.add(7)
    killD.add(8)

    killS = set()
    targetS = set()
    killS.add(8)
    targetS.add(7)
    targetS.add(8)
    targetS.add(9)

    newA = set()
    newA.add(1)
    newA.add(2)

    newC = set()
    newC.add(4)

    newD = set()

    newS = set()
    newS.add(7)
    newS.add(9)

    killAll = { 'address': killA, 'currency': killC, 'design': killD, 'staff': killS }
    targetAll = { 'address': targetA, 'currency': targetC, 'design': targetD, 'staff': targetS }

    expected = { 'address': newA, 'currency': newC, 'design': newD, 'staff': newS }

    removeFrom(killAll, targetAll, tabs)
    assert targetAll == expected

def test_bracketExpr():
    pk = 'address_id'

    set0 = set()

    set1 = set()
    set1.add(1)

    set2 = set()
    set2.add(1)
    set2.add(2)

    expected0 = 'where false'
    expected1 = 'where address_id in (1)'
    expected2 = 'where address_id in (1,2)'

    result0 = bracketExpr(pk, set0)
    result1 = bracketExpr(pk, set1)
    result2 = bracketExpr(pk, set2)

    assert expected0 == result0 and expected1 == result1 and expected2 == result2

def test_extract_ids_from_unifications():
    x = 'aa257_duplicate'
    addressF = deepcopy(addressDict1)
    addressT = deepcopy(addressDict1)
    addressF[x] = False
    addressT[x] = True
    addressFT = [addressF, addressT]

    testU = { 'address': addressFT }

    result = extract_ids_from_unifications(testU)
    expected = { 'address': { 'ids': set([1]), 'duplicate_ids': set([1]) }}
    assert result == expected

def test_depQuery():
    con=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    idsFromTable = set()
    idsFromTable.add(2)

    result1 = depQuery(con, 'staff', idsFromTable, 'department_id')
    expected1 = [6]

    result0 = depQuery(con, 'staff', set(), 'department_id')
    expected0 = []

    assert result0 == expected0 and result1 == expected1

def test_fetchCompleteRecords():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    ids1 = set()
    ids1.add(-1)
    ids1.add(1)

    ids3 = set()
    ids3.add(-1)
    ids3.add(3)

    ids6 = set()
    ids6.add(-1)
    ids6.add(6)

    ids60 = set()
    ids60.add(-1)
    ids60.add(60)

    ids35 = set()
    ids35.add(-1)
    ids35.add(35)

    ids152 = set()
    ids152.add(-1)
    ids152.add(152)

    idsAll = { 'address': ids1,
              'design': ids1,
              'currency': ids3,
              'payment_type': ids3,
              'staff': ids3,
              'counterparty': ids6,
              'department': ids6,
              'payment': ids60,
              'transaction': ids60,
              'purchase_order': ids35,
              'sales_order': ids152 }
    
    results = fetchCompleteRecords(conn, tableList, idsAll, idsAll)

    x = 'aa257_duplicate'

    addressF = deepcopy(addressDict1)
    addressT = deepcopy(addressDict1)
    addressF[x] = False
    addressT[x] = True
    addressFT = [addressF, addressT]

    counterpartyF = deepcopy(counterpartyDict6)
    counterpartyT = deepcopy(counterpartyDict6)
    counterpartyF[x] = False
    counterpartyT[x] = True
    counterpartyFT = [counterpartyF, counterpartyT]

    currencyF = deepcopy(currencyDict3)
    currencyT = deepcopy(currencyDict3)
    currencyF[x] = False
    currencyT[x] = True
    currencyFT = [currencyF, currencyT]

    departmentF = deepcopy(departmentDict6)
    departmentT = deepcopy(departmentDict6)
    departmentF[x] = False
    departmentT[x] = True
    departmentFT = [departmentF, departmentT]

    designF = deepcopy(designDict1)
    designT = deepcopy(designDict1)
    designF[x] = False
    designT[x] = True
    designFT = [designF, designT]

    paymentF = deepcopy(paymentDict60)
    paymentT = deepcopy(paymentDict60)
    paymentF[x] = False
    paymentT[x] = True
    paymentFT = [paymentF, paymentT]

    payment_typeF = deepcopy(payment_typeDict3)
    payment_typeT = deepcopy(payment_typeDict3)
    payment_typeF[x] = False
    payment_typeT[x] = True
    payment_typeFT = [payment_typeF, payment_typeT]

    purchase_orderF = deepcopy(purchase_orderDict35)
    purchase_orderT = deepcopy(purchase_orderDict35)
    purchase_orderF[x] = False
    purchase_orderT[x] = True
    purchase_orderFT = [purchase_orderF, purchase_orderT]

    sales_orderF = deepcopy(sales_orderDict152)
    sales_orderT = deepcopy(sales_orderDict152)
    sales_orderF[x] = False
    sales_orderT[x] = True
    sales_orderFT = [sales_orderF, sales_orderT]

    staffF = deepcopy(staffDict3)
    staffT = deepcopy(staffDict3)
    staffF[x] = False
    staffT[x] = True
    staffFT = [staffF, staffT]

    transactionF = deepcopy(transactionDict60)
    transactionT = deepcopy(transactionDict60)
    transactionF[x] = False
    transactionT[x] = True
    transactionFT = [transactionF, transactionT]

    expected = { 'address': addressFT,
              'counterparty': counterpartyFT,
              'currency': currencyFT,
              'department': departmentFT,
              'design': designFT,
              'payment': paymentFT,
              'payment_type': payment_typeFT,
              'purchase_order': purchase_orderFT,
              'sales_order': sales_orderFT,
              'staff': staffFT,
              'transaction': transactionFT}

    good = True

    for table in tableList:
        x = expected[table]
        r = results[table]

        if x == r:
            continue

        good = False

    assert good

def test_fetchDependencies_address():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    fetchedIds = makeEmptySets(tableList)
    fetchedIds['address'].add(1)
    expected = makeEmptySets(tableList)
    result = fetchDependencies(conn, tableList, tableCascades, fetchedIds)
    assert expected == result


def test_fetchDependencies_counterparty():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    fetchedIds = makeEmptySets(tableList)
    fetchedIds['counterparty'].add(6)
    expected = makeEmptySets(tableList)
    expected['address'].add(23)
    result = fetchDependencies(conn, tableList, tableCascades, fetchedIds)
    assert expected == result


def test_fetchDependencies_currency():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    fetchedIds = makeEmptySets(tableList)
    fetchedIds['currency'].add(3)
    expected = makeEmptySets(tableList)
    result = fetchDependencies(conn, tableList, tableCascades, fetchedIds)
    assert expected == result


def test_fetchDependencies_department():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    fetchedIds = makeEmptySets(tableList)
    fetchedIds['department'].add(6)
    expected = makeEmptySets(tableList)
    result = fetchDependencies(conn, tableList, tableCascades, fetchedIds)
    assert expected == result


def test_fetchDependencies_design():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    fetchedIds = makeEmptySets(tableList)
    fetchedIds['design'].add(1)
    expected = makeEmptySets(tableList)
    result = fetchDependencies(conn, tableList, tableCascades, fetchedIds)
    assert expected == result


def test_fetchDependencies_payment():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    fetchedIds = makeEmptySets(tableList)
    fetchedIds['payment'].add(60)
    expected = makeEmptySets(tableList)
    expected['counterparty'].add(14)
    expected['currency'].add(3)
    expected['payment_type'].add(3)
    expected['transaction'].add(60)
    result = fetchDependencies(conn, tableList, tableCascades, fetchedIds)
    assert expected == result

def test_fetchDependencies_payment_type():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    fetchedIds = makeEmptySets(tableList)
    fetchedIds['payment_type'].add(3)
    expected = makeEmptySets(tableList)
    result = fetchDependencies(conn, tableList, tableCascades, fetchedIds)
    assert expected == result


def test_fetchDependencies_purchase_order():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    fetchedIds = makeEmptySets(tableList)
    fetchedIds['purchase_order'].add(35)
    expected = makeEmptySets(tableList)
    expected['address'].add(23)
    expected['counterparty'].add(14)
    expected['currency'].add(3)
    expected['staff'].add(13)
    result = fetchDependencies(conn, tableList, tableCascades, fetchedIds)
    assert expected == result

def test_fetchDependencies_sales_order():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    fetchedIds = makeEmptySets(tableList)
    fetchedIds['sales_order'].add(152)
    expected = makeEmptySets(tableList)
    expected['address'].add(30)
    expected['counterparty'].add(10)
    expected['design'].add(37)
    expected['currency'].add(3)
    expected['staff'].add(12)
    result = fetchDependencies(conn, tableList, tableCascades, fetchedIds)
    assert expected == result


def test_fetchDependencies_staff():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    fetchedIds = makeEmptySets(tableList)
    fetchedIds['staff'].add(3)
    expected = makeEmptySets(tableList)
    expected['department'].add(6)
    result = fetchDependencies(conn, tableList, tableCascades, fetchedIds)
    assert expected == result


def test_fetchDependencies_transaction():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    fetchedIds = makeEmptySets(tableList)
    fetchedIds['transaction'].add(60)
    fetchedIds['transaction'].add(302)
    expected = makeEmptySets(tableList)
    expected['purchase_order'].add(35)
    expected['sales_order'].add(152)
    result = fetchDependencies(conn, tableList, tableCascades, fetchedIds)
    assert expected == result


def test_initialFetch():
    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    testIds = {
        'address': [1,3,5,7,10,13,20,23,30],
        'counterparty': [6,9,10,12,13,14],
        'currency': [3],
        'department': [4,5,6],
        'design': [313],
        'payment': [9316],
        'payment_type': [3,4],
        'purchase_order': [2792],
        'sales_order': [6562],
        'staff': [2,3,11,12,13,16],
        'transaction': [9363]
        }
    
    expecteds = {}
    for key in tableList:
        expected = set()
        idList = testIds[key]
        for id in idList:
            expected.add(id)
        expecteds[key] = expected

    results = initialFetch(conn, tableList, testTs)

    assert results == expecteds

def test_unifications():

    addressO = set([1,3,5,7,10,13,20,23,30])
    addressD = set()
    counterpartyO = set([6,9,10,12,13,14])
    counterpartyD = set()
    currencyO = set([3])
    currencyD = set()
    departmentO = set([4,5,6])
    departmentD = set()
    designO = set([313])
    designD = set([243])
    paymentO = set([9316])
    paymentD = set()
    payment_typeO = set([3,4])
    payment_typeD = set()
    purchase_orderO = set([2792])
    purchase_orderD = set()
    sales_orderO = set([6562])
    sales_orderD = set()
    staffO = set([2,3,11,12,13,16])
    staffD = set()
    transactionO = set([9363])
    transactionD = set([9316])

    expected = {
        'address': { 'ids': addressO, 'duplicate_ids': addressD },
        'counterparty': { 'ids': counterpartyO, 'duplicate_ids': counterpartyD },
        'currency': { 'ids': currencyO, 'duplicate_ids': currencyD },
        'department': { 'ids': departmentO, 'duplicate_ids': departmentD },
        'design': { 'ids': designO, 'duplicate_ids': designD },
        'payment': { 'ids': paymentO, 'duplicate_ids': paymentD },
        'payment_type': { 'ids': payment_typeO, 'duplicate_ids': payment_typeD },
        'purchase_order': { 'ids': purchase_orderO, 'duplicate_ids': purchase_orderD },
        'sales_order': { 'ids': sales_orderO, 'duplicate_ids': sales_orderD },
        'staff': { 'ids': staffO, 'duplicate_ids': staffD },
        'transaction': { 'ids': transactionO, 'duplicate_ids': transactionD },
        }

    conn=pg.Connection(user=environ.get('PGUSER'),
                  database=environ.get('PGDATABASE'),
                  host=environ.get('PGHOST'),
                  password=environ.get('PGPASSWORD'),
                  port=environ.get('PGPORT'))

    U = unifications(conn, tableList, testTs, tableCascades)
    results = extract_ids_from_unifications(U)

    assert results == expected

test_unifications()
