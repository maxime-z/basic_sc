def annual_salary(ms): #monthly salary

    last_saturday = 2.0 * ms / 21.75
    annual_bonus = ms * 12 * 0.3
    allowance = 500

    print('<基本工资>:        %.2f' % ms)
    print('<每月加班补助>      %.2f' % last_saturday)
    print('<每月绩效奖金基数>: %.2f' % (ms*0.15))
    print('<每月薪资>:        %.2f' % (ms+last_saturday+allowance+ms*0.15))
    print('<年薪总额>:        %.2f' % (12*(ms+last_saturday+allowance) + annual_bonus))
    return 'done'

print(annual_salary(13000))