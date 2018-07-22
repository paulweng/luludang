profitRatio = 0.001
feeRatio = 0.006

usdt = 450

totalProfit = 0
totalFee = 0

while usdt > 100:
    profit = usdt * profitRatio
    fee = usdt * feeRatio
    print("本金:{0:.6f}，盈利:{1:.6f}，手续费:{2:.6f}".format(usdt, profit, fee))
    totalFee += fee
    totalProfit += profit
    usdt = usdt + profit - fee

print("累计手续费", totalFee)