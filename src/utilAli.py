import pg8000.native as pg
import pandas as pd
import logging
from boto3 import client
from os import environ
from src.extractor import rows_to_dict

counterpartyCascade = { 'address': 'legal_address_id' }

paymentCascade = { 'counterparty': 'counterparty_id',
                  'currency': 'currency_id',
                  'payment_type': 'payment_type_id',
                  'transaction': 'transaction_id' }

purchase_orderCascade = { 'address': 'agreed_delivery_location_id',
                         'counterparty': 'counterparty_id',
                         'currency': 'currency_id',
                         'staff': 'staff_id' }

sales_orderCascade = { 'address': 'agreed_delivery_location_id',
                      'counterparty': 'counterparty_id',
                      'currency': 'currency_id',
                      'design': 'design_id',
                      'staff': 'staff_id' }

staffCascade = { 'department': 'department_id' }

transactionCascade = { 'purchase_order': 'purchase_order_id',
                      'sales_order': 'sales_order_id' }

tableCascades = {'address': {},
                  'counterparty': counterpartyCascade,
                  'currency': {},
                  'department': {},
                  'design': {},
                  'payment': paymentCascade,
                  'payment_type': {},
                  'purchase_order': purchase_orderCascade,
                  'sales_order': sales_orderCascade,
                  'staff': staffCascade,
                  'transaction': transactionCascade}

tableList = [ 'address',
              'counterparty',
              'currency',
              'department',
              'design',
              'payment',
              'payment_type',
              'purchase_order',
              'sales_order',
              'staff',
              'transaction' ]


def getTimestamps(ts, tabs):
    results = {}
    for table in tabs:
        results[table] = ts
    return results

def makeEmptySets(tabs):
    results = {}
    for table in tabs:
        results[table] = set()
    return results

def moreToDo(sets, tabs):
    for table in tabs:
        idsStillToFetch = sets[table]
        if len(idsStillToFetch) > 0:
            return True
    return False

def copyInto(setsFrom, setsTo, tabs):
    for table in tabs:
        setFrom = setsFrom[table]
        setTo = setsTo[table]
        for id in setFrom:
            setTo.add(id)

def removeFrom(whatToRemove, whatToRemoveFrom, tabs):
    for table in tabs:
        deletions = whatToRemove[table]
        targets = whatToRemoveFrom[table]
        for id in deletions:
            if id in targets:
                targets.remove(id)

def initialFetch(con, tabs, timestamps):
    results = makeEmptySets(tabs)

    for table in tabs:
        resultIds = results[table]

        id = f'{table}_id'

        whereClause = ''
        if timestamps is not None:
            timestamp = timestamps[table]
            whereClause = f'where last_updated >= {pg.literal(timestamp)}'

        stmt = f'select {pg.identifier(id)} from {pg.identifier(table)} {whereClause};'
        rows = con.run(stmt)
        for row in rows:
            resultId = row[0]
            resultIds.add(resultId)

    return results

def bracketExpr(idName, ids):
    if len(ids) < 1:
        return 'where false'

    bracketed = ''
    comma = ''
    for id in ids:
        bracketed = f'{bracketed}{comma}{pg.literal(id)}'
        comma = ','

    return f'where {pg.identifier(idName)} in ({bracketed})'

def fetchCompleteRecords(con, tabs, idsToLoadForFirstTime, idsToDuplicateLoad):
    results = {}

    for table in tabs:
        idName = f'{table}_id'
        whereOrig = bracketExpr(idName, idsToLoadForFirstTime[table])
        whereDup = bracketExpr(idName, idsToDuplicateLoad[table])

        stmt1 = f'select *, false as aa257_duplicate from {pg.identifier(table)} {whereOrig}'
        stmt2 = f'select *, true as aa257_duplicate from {pg.identifier(table)} {whereDup}'

        stmtU = f'{stmt1} union {stmt2}'


        stmt = f'with my_cte as ({stmtU}) select * from my_cte order by aa257_duplicate, {pg.identifier(idName)};'

        rows = con.run(stmt)
        data = rows_to_dict(rows, con.columns)
        results[table] = data

    return results

def depQuery(con, table, idsFromTable, foreignKeyAlias):
    results = []

    primaryKey = f'{table}_id'
    whereClause = bracketExpr(primaryKey, idsFromTable)

    stmt = f'select {pg.identifier(foreignKeyAlias)} from {pg.identifier(table)} {whereClause} and {pg.identifier(foreignKeyAlias)} is not null;'

    rows = con.run(stmt)
    for row in rows:
        results.append(row[0])

    return results

def fetchDependencies(con, tabs, cascades, fetchedIds):
    results = makeEmptySets(tabs)
    for table in tabs:
        idsFromTable = fetchedIds[table]
        if len(idsFromTable) == 0:
            continue
        foreignTables = cascades[table]
        for foreignTable in foreignTables:
            foreignKeyAlias = foreignTables[foreignTable]
            result = depQuery(con, table, idsFromTable, foreignKeyAlias)
            results[foreignTable].update(result)
    return results

def extract_ids_from_unifications(U):
    results = {}

    for table in U:
        idName = f'{table}_id'

        records = U[table]
        duplicate_ids = set()
        ids = set()
        for record in records:
            idValue = record[idName]
            dup = record['aa257_duplicate']
            if dup:
                duplicate_ids.add(idValue)
            else:
                ids.add(idValue)

        result = { 'ids': ids, 'duplicate_ids': duplicate_ids }       
        results[table] = result

    return results


def unifications(con, tabs, timestamps, cascades):

    origIds = initialFetch(con, tabs, timestamps)

    allFetchedIds = makeEmptySets(tabs)
    copyInto(origIds, allFetchedIds, tabs)

    idsFetchedLastTime = makeEmptySets(tabs)
    copyInto(origIds, idsFetchedLastTime, tabs)

    idsToFetchNext = fetchDependencies(con, tabs, cascades, idsFetchedLastTime)

    removeFrom(allFetchedIds, idsToFetchNext, tabs)

    depIds = makeEmptySets(tabs)

    while moreToDo(idsToFetchNext, tabs):
        copyInto(idsToFetchNext, depIds, tabs)
        copyInto(idsToFetchNext, allFetchedIds, tabs)

        idsFetchedLastTime = idsToFetchNext
        idsToFetchNext = fetchDependencies(con, tabs, cascades, idsFetchedLastTime)
        removeFrom(allFetchedIds, idsToFetchNext, tabs)

    return fetchCompleteRecords(con, tabs, origIds, depIds)