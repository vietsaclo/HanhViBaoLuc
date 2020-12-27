from datetime import datetime, timedelta
from Modules import PublicModules as libs
    
isCheck, res = libs.fun_dayMinus(dayFrom= '2020_12_22_0_8_0', dayTo= '2020_12_20_0_0_0')

print(isCheck)
print(res)