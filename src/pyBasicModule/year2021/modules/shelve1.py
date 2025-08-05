import shelve

# More like Dictionary
# Shelve key must be only str
# operations are same
# uses pickling behind the scene.
# not that safe to use
# not ordered

def shelve_demo():
    with shelve.open('modules/io/shelve') as fund:
        fund['AF'] = "TDF and CIT"
        fund['AFIS'] = "Insurance fund"
        fund['CIAM'] = "canadian and European fund"
    print(fund)

def shelve_demo_2():
    fund = shelve.open('modules/io/shelve-2', writeback=True)
    fund['AF'] = "TDF and CIT"
    fund['AFIS'] = "Insurance fund"
    fund['CIAM'] = "canadian and European fund"
    fund['AUS'].append('Fund launch in 2024')
    for k,v in fund.items(): print(k, v, fund[k], sep='::')
    for k in fund: print(k, fund[k], sep='::::')
    fund.close()


