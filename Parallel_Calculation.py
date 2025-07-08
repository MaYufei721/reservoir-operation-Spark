# coding=utf-8
import numpy as np
import time
from itertools import product
from pyspark import SparkConf, SparkContext
import xlwt


class Cal:
    def __init__(self, Res_Name, VtoZ, ZtoV, qtoZd, Zdtoq, HtoK, KtoH, Qu, dt, dz, fh, Ny, Np, prc, ZU, ZL, ZI, ZE, Zf):

        self.Res_Name = Res_Name

        self.VtoZ = VtoZ
        self.ZtoV = ZtoV
        self.qtoZd = qtoZd
        self.Zdtoq = Zdtoq
        self.HtoK = HtoK
        self.KtoH = KtoH

        self.Qu = Qu
        self.dt = dt
        self.dz = dz
        self.fh = fh
        self.Ny = Ny
        self.Np = Np
        self.prc = prc
        self.Pf = 10
        self.ZU = ZU
        self.ZL = ZL
        self.ZI = ZI
        self.ZE = ZE
        self.Zf = Zf

    def Start_cal(self, cpu_num, Res, Res_num, ):
        conf = SparkConf().setMaster("local[" + str(cpu_num) + "]").setAppName("spark0428")
        sc = SparkContext(conf=conf)

        self.VtoZ = sc.broadcast(self.VtoZ)
        self.ZtoV = sc.broadcast(self.ZtoV)
        self.qtoZd = sc.broadcast(self.qtoZd)
        self.Zdtoq = sc.broadcast(self.Zdtoq)
        self.HtoK = sc.broadcast(self.HtoK)
        self.KtoH = sc.broadcast(self.KtoH)

        self.Qu = sc.broadcast(self.Qu)
        self.dt = sc.broadcast(self.dt)
        self.dz = sc.broadcast(self.dz)
        self.fh = sc.broadcast(self.fh)
        self.Ny = sc.broadcast(self.Ny)
        self.Np = sc.broadcast(self.Np)
        self.prc = sc.broadcast(self.prc)
        self.Pf = sc.broadcast(self.Pf)

        T = len(self.dt.value)
        self.Qo = np.zeros((Res_num, T))
        self.Q = np.zeros((Res_num, T))
        self.Qr = np.zeros((Res_num, T))
        self.Qs = np.zeros((Res_num, T))
        self.Z_cal = np.zeros((Res_num, T + 1))

        def Group_IDP(R, delta_temp):
            Zbest = [[] for i in range(T + 1)]
            ZU_temp = np.zeros((Res_num, T + 1))
            ZL_temp = np.zeros((Res_num, T + 1))
            Z_Index = [[] for i in range(T + 1)]
            Z_WG = [[] for i in range(Res_num)]

            for i in R:
                for t in range(T):
                    if t == 0:
                        ZU_temp[i][t] = ZL_temp[i][t] = self.ZI[i]
                        ZL_temp[i][t + 1] = max(self.ZL[i][t], self.Z_cal[i][t + 1] - 1 * delta_temp)
                        ZU_temp[i][t + 1] = min(self.ZU[i][t], self.Z_cal[i][t + 1] + 1 * delta_temp)
                    elif (t >= 1 and t < 11):
                        ZL_temp[i][t + 1] = max(self.ZL[i][t], self.Z_cal[i][t + 1] - 1 * delta_temp)
                        ZU_temp[i][t + 1] = min(self.ZU[i][t], self.Z_cal[i][t + 1] + 1 * delta_temp)
                    else:
                        ZU_temp[i][t + 1] = ZL_temp[i][t + 1] = self.ZE[i]

            for i in range(Res_num):
                if i in R:
                    for t in range(T + 1):
                        Z_WG[i].append([j for j in np.linspace(ZL_temp[i][t], ZU_temp[i][t], 3)])
                else:
                    for t in range(T + 1):
                        Z_WG[i].append([self.Z_cal[i][t]])

            Z_Index[0].append(self.ZI)
            for t in range(T):
                Z_WG_temp = []
                for i in range(Res_num):
                    Z_WG_temp.append(Z_WG[i][t + 1])
                # Z_Index[t + 1] = list(product(*Z_WG_temp))
                Z_WG_pro = list(product(*Z_WG_temp))
                for i in Z_WG_pro:
                    Z_Index[t + 1].append(list(i))

            Z_Index = sc.broadcast(Z_Index)

            List = [i for i in range(T + 1)]
            for i in range(T + 1):
                List[i] = sc.parallelize(Z_Index.value[i])

            V = sc.broadcast(List[0].map(lambda x: [x, 0]).collect())

            for t in range(1, T + 1):
                List[t] = List[t].map(
                    lambda x: [x, power_benefit(V.value, x, t - 1)]).cache()
                V = sc.broadcast(List[t].map(lambda x: [x[0], x[1][0]]).collect())

            Zbest[T] = self.ZE
            B_best = List[T].first()[1][0]
            for t in range(T - 1, 0, -1):
                temp = Zbest[t + 1]
                Zbest[t] = List[t + 1].filter(lambda x: x[0] == temp).first()[1][1]
                List[t + 1].unpersist()
            Zbest[0] = self.ZI

            return Zbest, B_best

        def power_benefit(Z1_B, Z2, t):
            Benefit_max = -100000
            Z_best = Z1_B[0][0]
            for m in Z1_B:
                Z1 = m[0]
                Benefit_current = m[1]
                for i in range(Res_num):
                    if i == 0:
                        self.Q[i][t] = self.Qu.value[i][t]
                    else:
                        self.Q[i][t] = self.Qu.value[i][t] + self.Qo[i - 1][t]

                    output = power_output(Z1[i], Z2[i], i, t)
                    Benefit = self.prc.value[i] * self.dt.value[t] * output[0] / 36
                    self.Qo[i][t] = output[1] + output[2]
                    Benefit_current += Benefit
                if Benefit_current > Benefit_max:
                    Benefit_max = Benefit_current
                    Z_best = Z1
            temp_A = [Benefit_max, Z_best]

            return temp_A

        def power_output(Z1, Z2, i, t):
            S1 = self.ZtoV.value[i](Z1)
            S2 = self.ZtoV.value[i](Z2)
            Qout = (S1 - S2) / self.dt.value[t] + self.Q[i][t]
            if Qout < 0:
                return -10000, 0, 0
            else:
                Svg = (S1 + S2) / 2
                Zup = self.VtoZ.value[i](Svg)
                Zdown = self.qtoZd.value[i](Qout)
                Hm = Zup - Zdown
                Km = self.HtoK.value[i](Hm)
                Nt = 0.36 * Qout / Km
                if (Nt > 0 and Nt < self.Np.value[i]):
                    N = Nt - self.Pf.value * (Nt - self.Np.value[i]) ** 2
                    # N = self.Pf.value * Nt
                    qr = Qout
                    qs = 0
                    return N, qr, qs
                elif (Nt > self.Ny.value[i] * self.fh.value[i][t]):
                    N = self.Ny.value[i] * self.fh.value[i][t]
                    qr = N * Km / 0.36
                    qs = Qout - qr
                    return N, qr, qs
                else:
                    N = Nt
                    qr = N * Km / 0.36
                    qs = Qout - qr
                    return N, qr, qs

        def Result_save(Z):
            xl = np.zeros((Res_num, T + 1))
            sw = np.zeros((Res_num, T + 1))
            rkll = np.zeros((Res_num, T))
            ckll = np.zeros((Res_num, T))
            fdll = np.zeros((Res_num, T))
            qsll = np.zeros((Res_num, T))

            cl = np.zeros((Res_num, T))
            fdl = np.zeros((Res_num, T))
            fdxy = np.zeros((Res_num, T))
            nfdl = np.zeros((Res_num))
            nfdxy = np.zeros((Res_num))
            nzfdl = 0
            nzfdxy = 0
            yueshu = np.zeros((Res_num, T))

            for i in range(Res_num):
                for t in range(T):

                    sw[i][t] = Z[i][t]
                    xl[i][t] = self.ZtoV.value[i](sw[i][t])
                    if t == T - 1:
                        sw[i][t + 1] = Z[i][t + 1]
                        xl[i][t + 1] = self.ZtoV.value[i](sw[i][t + 1])

                    if i == 0:
                        rkll[i][t] = self.Qu.value[i][t]
                    else:
                        rkll[i][t] = self.Qu.value[i][t] + ckll[i - 1][t]

                    V1 = xl[i][t]
                    V2 = self.ZtoV.value[i](Z[i][t + 1])
                    ckll[i][t] = (V1 - V2) / self.dt.value[t] + rkll[i][t]
                    if ckll[i][t] < 0:
                        yueshu[i][t] += 1
                        ckll[i][t] = 0

                    Svg = (V1 + V2) / 2
                    Zup = self.VtoZ.value[i](Svg)
                    Zdown = self.qtoZd.value[i](ckll[i][t])
                    Hm = Zup - Zdown
                    Km = self.HtoK.value[i](Hm)
                    Nt = 0.36 * ckll[i][t] / Km
                    if (Nt > 0 and Nt < self.Np.value[i]):
                        cl[i][t] = Nt
                        fdll[i][t] = ckll[i][t]
                        qsll[i][t] = 0
                    elif (Nt > self.Ny.value[i] * self.fh.value[i][t]):
                        cl[i][t] = self.Ny.value[i] * self.fh.value[i][t]
                        fdll[i][t] = cl[i][t] * Km / 0.36
                        qsll[i][t] = ckll[i][t] - fdll[i][t]
                    else:
                        cl[i][t] = Nt
                        fdll[i][t] = cl[i][t] * Km / 0.36
                        qsll[i][t] = ckll[i][t] - fdll[i][t]
                    fdl[i][t] = self.dt.value[t] * cl[i][t] / 36
                    fdxy[i][t] = self.prc.value[i] * fdl[i][t]
            for i in range(Res_num):
                for t in range(T):
                    nfdl[i] += fdl[i][t]
                    nfdxy[i] += fdxy[i][t]
                nzfdl += nfdl[i]
                nzfdxy += nfdxy[i]

            return sw, ckll, cl, fdl


        for i in range(Res_num):
            for t in range(T + 1):
                if t == 0:
                    self.Z_cal[i][t] = self.ZI[i]
                elif t == T:
                    self.Z_cal[i][t] = self.ZE[i]
                else:
                    self.Z_cal[i][t] = self.Zf[i][t - 1]

        self.delta = [1, 0.5, 0.1] #, 0.05

        yb = -10000
        time_start = time.time()
        for i in range(4):
            x = Group_IDP(Res, self.delta[i])
            z = x[0]
            y = x[1]

            if y > yb:
                yb = y
                for t in range(T + 1):
                    for i in Res:
                        self.Z_cal[i][t] = z[t][i]

        time_end = time.time()
        Time = time_end - time_start

        RforR = Result_save(self.Z_cal)

        sc.stop()

        return Time, RforR
