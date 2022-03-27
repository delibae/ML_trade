class backtest:
  def __init__(self,start,end,lin,lout,sin,sout,x_a,x_b,data, model_wts):
    self.end = end
    self.start = start
    self.lin = lin
    self.lout = lout
    self.sin = sin
    self.sout = sout
    self.data = data
    self.x_a = x_a
    self.model_wts = model_wts
    self.data = data
    close = self.data['close'].values
    close = close[start:end+1,:]
    self.close = close
  
  def start(self):
    model = MultiArchitecture()
    model.load_state_dict(torch.load(self.model_wts))
    s , l = 0,0
    i = self.start
    lb = []
    lopen = 0
    lclose = 0
    ls = []
    sb = []
    sopen = 0
    sclose = 0
    ss = []
    if i < self.end:
      xa = x_a[i,:]
      xb = x_b[i,:]
      target = model(xa,xb)
      price = self.close[i]
      if target > self.lin and l == 0 and s == 0:
        lb.append(price)
        l += 1
        lopen += 1
      if target < self.lout and l == 1 and s == 0:
        ls.append(price)
        l += -1
        lclose += 1
      if target < self.sin and l == 0 and s == 0:
        sb.append(price)
        s += 1
        sopen += 1
      if target > self.sout and l == 0 and s ==1 :
        ss.append(price)
        s += -1
        sclose += 1
      i += 1
    if lopen != lclose:
      lb = lb[0:-1]
    if sopen != sclose:
      sb = sb[0:-1]
    return lb , ls, sb , ss, lopen, sopen
  
  def lplot(self):
    lperform = sum(ls) - sum(lb) - lopen*35
    sperform = sum(sb) - sum(ss) - sopen*35
    return lperform, sperform
  def hplot(self):
    lper = []
    sper = []
    lgraph = [0]
    ldraw = [0]
    sgraph = [0]
    sdraw = [0]
    for i in range(len(lb)):
      val = ls[i] - lb[i] - 35
      lper.append(val)
    for i in range(len(sb)):
      val = sb[i] - ss[i] - 35
      sper.append(val)
    for phase in ['long','short']:
      if pahse == 'long':
        for i in range(len(lper)):
          gap = lper[i]
          lgraph.append(gap + lgraph[-1])
          if gap < 0:
            ldraw.append(gap)
      if phae == 'short':
        for i in range(len(sper)):
          gap = sper[i]
          sgraph.append(gap + sgraph[-1])
          if gap < 0:
            sdraw.append(gap)
      sdrawdown_df = pd.DataFrame(sdrawdown)
      lgraph_df = pd.DataFrame(lgraph)
      sgraph_df = pd.DataFrame(sgraph)
      ldraw_df = pd.DataFrame(ldraw)
      sdraw_df = pd.DataFrame(sdraw)
      plt.plot(lgraph_df)
      plt.show()
      plt.plot(sgraph_df)
      plt.show()
      plt.plot(ldraw_df)
      plt.show()
      plt.plot(sdraw_df)
      plt.show()

