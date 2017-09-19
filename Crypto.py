import os, sys, random,math
from readSVM import readSVM


def Precision(dim_list1, lab2):
   c = 0
   for i in range(len(lab2)):
      c = c + dim_list1.count(lab2[i])
   prec = float(c) / len(dim_list1)
   count = c
   length = len(dim_list1)
   return prec, count, length


def extract_id(start_point, end_point,bin,m):
   lab1=[]
   x=len(bin)
   for a in range(x):
      if m[a]>=start_point and m[a+1]<=end_point:
         lab1.append(bin[a])
      elif m[a]<=start_point and m[a+1]>=start_point:
         lab1.append(bin[a])
      elif m[a]<=end_point and m[a+1]>=end_point:
         lab1.append(bin[a])
   return lab1

def crypto(input_data, transformed_data, dim, enc_file, bin_width, start, end):
   target, records = readSVM(input_data)
   # dim starts from 0
   vec_i = [rec[dim] for rec in records]
   max_i = max(vec_i)
   min_i = min(vec_i)
   p=0
   n=0
   t=0
   nbins = int (1.0/bin_width)
   bin_size = float(max_i-min_i)/nbins
   marks = [min_i+bin_size * i for i in range(nbins)]
   marks.append(max_i)
   binIDs = random.sample(xrange(10000000), nbins)
   f= open(enc_file, "w+")
   for i in range(nbins):
      print >>f, marks[i], marks[i+1], binIDs[i]
   lab = extract_id(start, end,binIDs, marks)
   dim_list =[]
   for i in range(len(records)):
         binid = int(math.floor ((records[i][dim]-min_i)/bin_size))
         if binid == nbins: # upper bound
            binid -=1
         records[i][dim] = binIDs[binid]

         dim_list.append(binIDs[binid])
   p,n,t = Precision(dim_list,lab)
   o = open(transformed_data,"w+")
   for i in range(len(records)):
            if target[i]<0:
               val= str(target[i])+" "
            else:
               val = "+"+str(target[i])+" "
            for j in range(len(records[i])):
               val =val+str(j+1)+":"+str(records[i][j])+" "
            print >>o,val
   print "Precision: " + str(p)
   print "Records in given range: "+str(n)

if __name__ == '__main__':
      i_dataset = sys.argv[1]
      t_dataset = sys.argv[2]
      encodefile = sys.argv[3]
      dimension_col = int(sys.argv[4])
      start_point = float(sys.argv[5])
      end_point = float(sys.argv[6])
      binwidth = float(sys.argv[7])
crypto(i_dataset,t_dataset,dimension_col,encodefile,binwidth,start_point,end_point)
